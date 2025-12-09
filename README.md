# 🚀 Autonomous Insurance FNOL Claims Processing Agent

This project implements an Autonomous FNOL (First Notice of Loss) Claims Processing Agent capable of:
- Extracting key fields from FNOL documents (PDF/TXT)
- Detecting missing or inconsistent information
- Classifying claims using business routing rules
- Returning a structured JSON response
It simulates automated insurance claim triaging used in real insurance back-office workflows.

# 📑 Table of Contents

- Features
- Extracted Fields
- Routing Rules
- Installation
- Usage
- Example Output
- Project Structure
- Limitations
- Future Improvements
- Tech Stack
- Author

# ✨ Features

- PDF text extraction using pdfplumber
- Regex field extraction
- Detection of missing mandatory data
- Rule-based routing engine
- JSON formatted output
- Command-line usage
- Lightweight, dependency-minimal design

# 📦 Extracted Fields
## Policy Information
- policy number
- policyholder
- effective dates

## Incident Information
- date
- time
- location
- description

## Parties
- claimant
- third parties
- contact details

## Asset
- asset type
- VIN / asset id
- estimated damage

# 🤖 Routing Rules (Business Logic)

**Rule**	                                            **Route**
Estimated damage < 25,000	                              Fast-track
Missing mandatory fields	                              Manual Review
Contains “fraud”, “staged”, “inconsistent”	            Investigation Flag
Claim type = injury	                                    Specialist Queue

# ⚙ Installation

git clone https://github.com/poojareddy30/fnol-claims-agent.git
cd fnol-claims-agent
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# ▶ Usage

Run against any FNOL PDF/TXT document:
python -m fnol_agent.main "ACORD-Automobile-Loss-Notice.pdf" --pretty

# 📌 Example Output

{
   "extractedFields": {
      "policyNumber": "CONTACT",
      "incidentLocation": "STREET",
      ...
   },
   "missingFields": [
      "effectiveDates",
      "assetId",
      "estimatedDamage"
   ],
   "recommendedRoute": "Manual review",
   "reasoning": "Missing mandatory fields"
}

# 📁 Project Structure

fnol-claims-agent/
├── fnol_agent/
│   ├── extractor.py
│   ├── routing.py
│   └── main.py
│
├── requirements.txt
├── README.md
├── .gitignore
└── ACORD-Automobile-Loss-Notice.pdf

# ⚠ Limitations

- Sample provided ACORD file is a blank template, therefore missing fields are expected.
- Regex accuracy depends on form structure.
- No OCR (scanned PDFs not supported).
- No UI (CLI tool only).

# 🧠 Future Improvements

- LLM-based field extraction
- OCR integration (Tesseract)
- Web service (FastAPI)
- Storage layer (Mongo/Postgres)
- Auto-flagging inconsistent values
- Model-driven fraud detection
- Web dashboard

# 🧰 Tech Stack

- Python
- pdfplumber
- regex

# 👩‍💻 Author
Built by **Thipparthi Pooja**
GitHub: https://github.com/poojareddy30

# ⭐ If you like this project

Please ⭐ star the repo 😊
