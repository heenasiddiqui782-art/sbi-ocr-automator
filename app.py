import streamlit as st
import pytesseract
from PIL import Image
import re
import pandas as pd
import cv2            
import numpy as np    

# --- NEW PRE-PROCESSING FUNCTION ---
def remove_form_boxes(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    
    # Remove Horizontal Lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
    detect_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(image, [c], -1, (255, 255, 255), 2)
        
    # Remove Vertical Lines
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
    detect_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    cnts = cv2.findContours(detect_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(image, [c], -1, (255, 255, 255), 2)
        
    return image


# Set up the web page layout
st.set_page_config(page_title="Customer Form OCR Automator", layout="centered")

st.title("🏦 Customer Form OCR Automator")
st.write("SBI Intern Project: Automated extraction tool to eliminate manual data entry.")

# 1. File Upload functionality
uploaded_file = st.file_uploader("Upload Scanned Form (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # --- UPDATED: IMAGE PRE-PROCESSING BRIDGE ---
    # Read the uploaded file into an OpenCV format in memory
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)
    
    # Display the uploaded image 
    st.image(cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB), caption="Uploaded Document", use_column_width=True)
    
    with st.spinner("Removing form grid lines..."):
        # Erase the boxes using our new function
        cleaned_image = remove_form_boxes(opencv_image)
        # Convert back to standard RGB format for accurate OCR reading
        final_image_for_ocr = cv2.cvtColor(cleaned_image, cv2.COLOR_BGR2RGB)
    
    # 2. Run OCR Processing
    with st.spinner("Processing document text via AI OCR..."):
        raw_text = pytesseract.image_to_string(final_image_for_ocr)
        
    # Allow the user to see what the AI detected
    with st.expander("View Raw Extracted Text"):
        st.text(raw_text)
        
    # 3. Extract Specific Data fields using Regular Expressions (Regex)
    st.subheader("Structured Data Output")
    
    # Name: Grabs letters/spaces non-greedily, STOPS explicitly when it sees PAN, TIN, Date, or Address
    name_match = re.search(r'(?i)(?:Name|Customer Name|Remitter)[\s\.\:\-\*]*\n*([A-Za-z\s]{5,50}?)(?=\n*PAN|\n*TIN|\n*Current Address|\n*Date|$)', raw_text)
    
    acc_match = re.search(r'(?i)(?:Account|A/C|Acc)\s*(?:No|Number)?[\s\.\:\-\*]*\n*([\d\W_]{9,40})', raw_text)
    ifsc_match = re.search(r'(?i)IFSC.*?([A-Z]{4}0[A-Z0-9]{6})', raw_text)
    
    aadhar_match = re.search(r'(?i)(?:Aadhaar|Aadhar|UID)[\s\.\:\-]*\n*([\d\W_]{12,20})', raw_text)
    
    # PAN: Looks for "PAN", skips up to 150 characters of form instructions, then grabs the 10-digit ID
    pan_match = re.search(r'(?i)PAN[\s\S]{0,150}?(?:\b|\n)([A-Z0-9]{10})\b', raw_text)
    
    mobile_match = re.search(r'(?i)(?:Mobile|Phone|Mob|Mo)\s*(?:No|Number)?[\s\.\:\-]*\n*([\d\W_]{10,20})', raw_text)
    mode_match = re.search(r'(?i)\b(Normal|Mormal|Small|Minor|Saving|Savings|Current(?!\s*Address)|CC|OD)\b', raw_text)

    # 2. Advanced Filtering & Cleaning Logic 
    if name_match:
        clean_name = re.sub(r'[^a-zA-Z\s]', '', name_match.group(1))
        clean_name = re.sub(r'\s+', ' ', clean_name).strip() 
    else:
        clean_name = "Review Required"

    if acc_match:
        clean_acc = re.sub(r'\D', '', acc_match.group(1))
        if not (9 <= len(clean_acc) <= 18): clean_acc = "Review Required"
    else:
        clean_acc = "Review Required"

    clean_ifsc = ifsc_match.group(1).strip() if ifsc_match else "Review Required"
    
    if aadhar_match:
        clean_aadhar = re.sub(r'\D', '', aadhar_match.group(1))
        if len(clean_aadhar) != 12: clean_aadhar = "Review Required"
    else:
        clean_aadhar = "Review Required"

    if pan_match:
        clean_pan = re.sub(r'[^A-Z0-9]', '', pan_match.group(1).upper())
        if len(clean_pan) != 10: clean_pan = "Review Required"
    else:
        clean_pan = "Review Required"

    if mobile_match:
        clean_mobile = re.sub(r'\D', '', mobile_match.group(1))
        if len(clean_mobile) >= 10: 
            clean_mobile = clean_mobile[-10:]
        else: 
            clean_mobile = "Review Required"
    else:
        clean_mobile = "Review Required"

    if mode_match:
        clean_mode = mode_match.group(1).capitalize()
        if clean_mode == "Mormal": clean_mode = "Normal" 
    else:
        clean_mode = "Review Required"

    # 3. Build a table structure of the extracted data
    extracted_data = {
        "Field Name": [
            "Customer Name", 
            "Account Number", 
            "IFSC Code", 
            "Aadhaar Number", 
            "PAN Card", 
            "Mobile Number", 
            "Account Type"
        ],
        "Extracted Value": [
            clean_name,
            clean_acc,
            clean_ifsc,
            clean_aadhar,
            clean_pan,
            clean_mobile,
            clean_mode
        ]
    }
    
    # 4. Display as a clean user interface table
    df = pd.DataFrame(extracted_data)
    st.table(df)
    
    # 5. Export Feature
    csv = df.to_csv(index=False)
    st.download_button(
        label="Export Data to Excel/CSV",
        data=csv,
        file_name="sbi_extracted_data.csv",
        mime="text/csv"
    )
    
