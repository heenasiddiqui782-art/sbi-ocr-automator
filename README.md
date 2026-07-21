# 🏦 Customer Form OCR Automator

> **An AI-powered OCR and regex data-parsing pipeline engineered to eliminate manual data entry bottlenecks in branch banking operations.**

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Tesseract OCR](https://img.shields.io/badge/Tesseract--OCR-412991?style=for-the-badge&logo=google&logoColor=white)](https://github.com/tesseract-ocr/tesseract)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

---

## 📌 Executive Overview

Physical customer forms (KYC updates, account opening, loan applications) remain a major operational bottleneck in traditional banking workflows. Manual typing is slow, error-prone, and inflates customer turnaround time (TAT).

The **Customer Form OCR Automator** was built as a proof-of-concept for **State Bank of India (SBI)** branch operations. It converts unstructured document images into structured, verified tabular data within seconds.

* 🚀 **Speed Boost:** Reduces manual typing time by up to 80% per form.
* 🧠 **Pattern Intelligence:** Utilizes custom Regular Expressions (Regex) to automatically isolate financial identifiers (PAN, Mobile, Account Numbers).
* 🛡️ **Safety-First Architecture:** Implements a "Review Required" fallback mechanism for low-confidence or corrupted text, preserving strict banking compliance standards.

---

## 🎬 Live Demo Video

https://drive.google.com/drive/folders/1quVfSmCMFboRL_nk04OhzGKiHI8DUHFV?usp=sharing

> **Video Walkthrough:** [Click here to watch the 1-minute application walkthrough](https://drive.google.com/drive/folders/1quVfSmCMFboRL_nk04OhzGKiHI8DUHFV?usp=sharing) showing form upload, real-time OCR extraction, regex field mapping, and CSV export.

---

## ⚡ Key Features

<details>
<summary><b>📄 Multi-Format Ingestion</b> (Click to expand)</summary>
Supports high-resolution scanned forms and digital document uploads natively (PNG, JPG, JPEG) with automatic image resizing and contrast adjustments for optimal reading.
</details>

<details>
<summary><b>🎯 Precision Regex Parsing</b> (Click to expand)</summary>
Contextual pattern matching automatically isolates critical banking data:
<ul>
  <li>Customer Name</li>
  <li>11-digit Account Numbers</li>
  <li>10-character PAN Identifiers (e.g., <code>^[A-Z]{5}[0-9]{4}[A-Z]{1}$</code>)</li>
  <li>10-digit Mobile Numbers & IFSC Codes</li>
</ul>
</details>

<details>
<summary><b>⚖️ Human-in-the-Loop Validation</b> (Click to expand)</summary>
Instead of making false guesses that could corrupt a banking database, the system automatically flags ambiguous fields as <code>Review Required</code>, ensuring a bank official maintains final data authority.
</details>

---

## 📸 Interface & Workflow Showcase

### 1. Document Upload & Interface
*Clean, web-based Streamlit UI built for non-technical branch officials.*

<img width="960" height="490" alt="S1" src="https://github.com/user-attachments/assets/0bcf9a22-1556-47e1-9b6a-fb6360febaf1" />


---

### 2. Structured Data Extraction & Regex Mapping
*Raw image text is instantly converted into validated tabular output.*

<img width="960" height="518" alt="S2" src="https://github.com/user-attachments/assets/e8c25e09-db2c-4c0b-b994-440ae096b3a0" />


---

### 3. Safety Flagging & Edge-Case Handling
*Ambiguous characters or comb-boxed fields are safely flagged for human verification.*

<img width="1920" height="1003" alt="S3" src="https://github.com/user-attachments/assets/c9ee68f8-c9e4-4bdd-8152-cd18b240ec92" />


---

## 🛠️ System Architecture

```text
┌─────────────────┐      ┌─────────────────┐      ┌──────────────────┐
│  Uploaded Form  │ ───► │  Tesseract OCR  │ ───► │ Raw Text Stream  │
│  (PNG / JPG)    │      │  Engine         │      │                  │
└─────────────────┘      └─────────────────┘      └────────┬─────────┘
                                                           │
                                                           ▼
┌─────────────────┐      ┌─────────────────┐      ┌──────────────────┐
│ Verified CSV    │ ◄─── │ Streamlit Table │ ◄─── │ Python Regex     │
│ Export          │      │ Dashboard       │      │ Extraction Layer │
└─────────────────┘      └─────────────────┘      └──────────────────┘
