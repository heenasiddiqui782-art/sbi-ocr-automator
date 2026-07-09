import streamlit as st
import pytesseract
from PIL import Image
import re
import pandas as pd



# Set up the web page layout
st.set_page_config(page_title="Customer Form OCR Automator", layout="centered")

st.title("🏦 Customer Form OCR Automator")
st.write("SBI Intern Project: Automated extraction tool to eliminate manual data entry.")

# 1. File Upload functionality
uploaded_file = st.file_uploader("Upload Scanned Form (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Document", use_column_width=True)
    
    # 2. Run OCR Processing
    with st.spinner("Processing document text via AI OCR..."):
        raw_text = pytesseract.image_to_string(image, config='--psm 6')
        
    # Allow the user to see what the AI detected
    with st.expander("View Raw Extracted Text"):
        st.text(raw_text)
        
    # 3. Extract Specific Data fields using Regular Expressions (Regex)
    st.subheader("Structured Data Output")
    
    name_match = re.search(r'(?i)(?:Name|Customer Name)\s*[:\-]?\s*([A-Za-z\s]+)', raw_text)
    acc_match = re.search(r'(?i)(?:Account|A/C)\s*(?:No|Number)?\s*[:\-]?\s*(\d{9,18})', raw_text)
    ifsc_match = re.search(r'(?i)IFSC\s*[:\-]?\s*([A-Z]{4}0[A-Z0-9]{6})', raw_text)
    
    # Build a table structure of the extracted data
    extracted_data = {
        "Field Name": ["Customer Name", "Account Number", "IFSC Code"],
        "Extracted Value": [
            name_match.group(1).strip() if name_match else "Review Required",
            acc_match.group(1).strip() if acc_match else "Review Required",
            ifsc_match.group(1).strip() if ifsc_match else "Review Required"
        ]
    }
    
    # 4. Display as a clean user interface table
    df = pd.DataFrame(extracted_data)
    st.table(df)
    
    # 5. Export Feature to save hours of typing
    csv = df.to_csv(index=False)
    st.download_button(
        label="Export Data to Excel/CSV",
        data=csv,
        file_name="sbi_extracted_data.csv",
        mime="text/csv"
    )
