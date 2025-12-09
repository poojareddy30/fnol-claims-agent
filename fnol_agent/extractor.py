import re
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple, Any
import os
import pdfplumber


# Data structure to store extracted fields
@dataclass
class ExtractedFields:
    policyNumber: Optional[str] = None
    policyholderName: Optional[str] = None
    effectiveDates: Optional[str] = None
    incidentDate: Optional[str] = None
    incidentTime: Optional[str] = None
    incidentLocation: Optional[str] = None
    incidentDescription: Optional[str] = None
    claimantName: Optional[str] = None
    thirdParties: Optional[str] = None
    contactDetails: Optional[str] = None
    assetType: Optional[str] = None
    assetId: Optional[str] = None
    estimatedDamage: Optional[float] = None
    claimType: Optional[str] = None
    attachments: Optional[str] = None
    initialEstimate: Optional[float] = None


MANDATORY_FIELDS = [
    "policyNumber",
    "policyholderName",
    "effectiveDates",
    "incidentDate",
    "incidentTime",
    "incidentLocation",
    "incidentDescription",
    "claimType",
    "assetType",
    "assetId",
    "estimatedDamage",
]


# Read PDF text
def _read_pdf(path: str) -> str:
    text = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text.append(page.extract_text() or "")
    return "\n".join(text)


def _read_file(path: str) -> str:
    if path.lower().endswith(".pdf"):
        return _read_pdf(path)
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def _extract_single(regex_list, text):
    for regex in regex_list:
        m = re.search(regex, text, flags=re.IGNORECASE | re.MULTILINE)
        if m:
            value = m.group(1).strip()
            if value:
                return value
    return None


def _extract_money(regex_list, text):
    raw = _extract_single(regex_list, text)
    if not raw:
        return None
    raw = raw.replace(",", "").replace("$", "")
    m = re.search(r"(\d+(\.\d+)?)", raw)
    if not m:
        return None
    return float(m.group(1))


def extract_fields_from_text(text: str) -> ExtractedFields:
    # Policy number
    policy_number = _extract_single(
        [
            r"POLICY NUMBER\s*[:\-]?\s*([A-Za-z0-9\-\/]+)",
            r"Policy\s*No\.?[:\s]*([A-Za-z0-9\-\/]+)",
        ],
        text,
    )

    # Insured
    policyholder = _extract_single(
        [
            r"NAME OF INSURED.*?\n(.*)",
            r"Insured\s*[:\-]\s*(.*)"
        ],
        text,
    )

    # Effective dates (ACORD doesn't explicitly have, so often missing)
    effective_dates = _extract_single(
        [
            r"Effective Dates?\s*[:\-]\s*(.*)",
            r"POLICY PERIOD.*?\n(.*)",
        ],
        text,
    )

    # Incident date
    incident_date = _extract_single(
        [
            r"DATE OF LOSS.*?\n(.*)",
            r"Date of Loss\s*[:\-]\s*(.*)",
        ],
        text,
    )

    # Incident time
    incident_time = _extract_single(
        [
            r"DATE OF LOSS AND TIME.*?(AM|PM|[0-9:]+\s*[AP]M?)",
            r"Time\s*[:\-]\s*([0-9:]+\s*[AP]M?)",
        ],
        text,
    )

    # Location
    location = _extract_single(
        [
            r"LOCATION OF LOSS.*?\n(.*)",
            r"Loss Location\s*[:\-]\s*(.*)",
            r"Describe Location of Loss.*?\n(.*)",
        ],
        text,
    )

    # Simplified incident description extraction
    incident_desc = _extract_single(
        [
            r"DESCRIPTION OF ACCIDENT[:\s]*(.*)",
            r"Accident Description[:\s]*(.*)",
        ],
        text,
    )

    # Claimant (driver)
    claimant = _extract_single(
        [
            r"DRIVER'S NAME AND ADDRESS.*?\n(.*)",
            r"Claimant\s*[:\-]\s*(.*)",
        ],
        text,
    )

    # VIN – improved capturing
    vin = _extract_single(
        [
            r"V\.?I\.?N\.?\s*[:\-]?\s*([A-HJ-NPR-Z0-9]{6,})",
        ],
        text,
    )

    # Estimate amount – improved
    est_damage = _extract_money(
        [
            r"ESTIMATE AMOUNT[:\s]*([\$\d,\.]+)",
            r"Estimated Damage[:\s]*([\$\d,\.]+)",
            r"Initial Estimate[:\s]*([\$\d,\.]+)",
        ],
        text,
    )

    claim_type = _extract_single(
        [
            r"LINE OF BUSINESS\s*[:\-]?\s*(.*)",
            r"Claim Type\s*[:\-]\s*(.*)",
        ],
        text,
    )

    if not claim_type:
        lc = text.lower()
        if "injury" in lc:
            claim_type = "injury"
        elif "auto" in lc or "vehicle" in lc:
            claim_type = "auto"
        else:
            claim_type = "other"

    return ExtractedFields(
        policyNumber=policy_number,
        policyholderName=policyholder,
        effectiveDates=effective_dates,
        incidentDate=incident_date,
        incidentTime=incident_time,
        incidentLocation=location,
        incidentDescription=incident_desc,
        claimantName=claimant,
        thirdParties=None,
        contactDetails=None,
        assetType="vehicle",
        assetId=vin,
        estimatedDamage=est_damage,
        claimType=claim_type,
        attachments=None,
        initialEstimate=est_damage,
    )


def extract_from_file(path: str) -> Tuple[Dict[str, Any], List[str]]:
    text = _read_file(path)
    fields = extract_fields_from_text(text)
    d = asdict(fields)

    missing = []
    for key in MANDATORY_FIELDS:
        val = d.get(key)
        if val is None or (isinstance(val, str) and not val.strip()):
            missing.append(key)

    return d, missing
