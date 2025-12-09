Autonomous Insurance FNOL Claims Processing Agent

This project implements an Autonomous FNOL (First Notice of Loss) Claims Agent which:

extracts key information from FNOL documents (PDF/TXT),

detects missing mandatory fields,

applies rule-based routing,

returns a structured JSON result.

This project was built as part of an assessment and demonstrates:
PDF parsing, regex extraction, rule-based decision making, and automated JSON formatting.

✨ Features

✔ PDF ingestion using pdfplumber
✔ Regex-based field extraction
✔ Mandatory field validation
✔ Rule-based routing engine
✔ Clean JSON output
✔ CLI usage
✔ Lightweight Python project (no UI or heavy frameworks)

⚙ FNOL Fields Extracted
Policy Information

Policy Number

Policyholder Name

Effective Dates

Incident Information

Date of Loss

Time

Location

Description

Involved Parties

Claimant

Third Parties

Contact Details

Asset Details

Asset Type

VIN / Asset ID

Estimated Damage

🧠 Routing Logic

Routing follows the assessment specification:

Rule	                                                 Route
Estimated damage < 25,000	                             Fast-track
Missing mandatory fields	                             Manual Review
Contains keywords: “fraud”, “staged”, “inconsistent”	 Investigation Flag
Claim type = injury	                                     Specialist Queue

📦 Installation

git clone https://github.com/poojareddy30/fnol-claims-agent.git
cd fnol-claims-agent

python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt

▶ Usage
python -m fnol_agent.main "ACORD-Automobile-Loss-Notice.pdf" --pretty


Example output:

{
  "extractedFields": {...},
  "missingFields": ["effectiveDates","assetId","estimatedDamage"],
  "recommendedRoute": "Manual review",
  "reasoning": "Missing mandatory fields"
}

📂 Project Structure
fnol-claims-agent/
│
├── fnol_agent/
│   ├── extractor.py
│   ├── routing.py
│   └── main.py
│
├── requirements.txt
├── README.md
├── .gitignore
└── ACORD-Automobile-Loss-Notice-12.05.16.pdf   (sample)

🧰 Tech Stack

Python

pdfplumber

regex

CLI

🔍 Notes

The provided ACORD sample is a blank FNOL template, so fields will appear as None or placeholder text.
This is expected and proves the missing field detection + routing logic works correctly.

If you run a filled FNOL document, the JSON output will contain real values and routing may change.

🚀 Improvements (Future Work)

OCR for scanned FNOL forms

FastAPI service wrapper

DB storage (Mongo/Postgres)

LLM extraction (instead of regex)

RPA integration (UiPath / Automation)

👩‍💻 Author

Built by Pooja Reddy (@poojareddy30) as part of a technical project.

⭐ If this project helped you

Consider giving it a ⭐ star on GitHub:
👉 https://github.com/poojareddy30/fnol-claims-agent