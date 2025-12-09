from typing import Dict, List, Tuple


def decide_route(fields: Dict, missing_fields: List[str]) -> Tuple[str, str]:
    """
    Return (recommendedRoute, reasoning) based on business rules.
    """

    # If mandatory fields missing → manual review
    if missing_fields:
        return (
            "Manual review",
            f"Missing fields: {', '.join(missing_fields)}"
        )

    description = (fields.get("incidentDescription") or "").lower()
    claim_type = (fields.get("claimType") or "").lower()
    estimated_damage = fields.get("estimatedDamage")

    # Investigation if fraud-like description
    fraud_words = ["fraud", "inconsistent", "staged"]
    if any(word in description for word in fraud_words):
        return (
            "Investigation Flag",
            "Description contains potential fraud keywords"
        )

    # Specialist queue if injury
    if claim_type == "injury":
        return (
            "Specialist Queue",
            "Claim involves injury"
        )

    # Fast-track if less than 25,000
    try:
        if estimated_damage is not None and float(estimated_damage) < 25000:
            return (
                "Fast-track",
                f"Estimated damage ({estimated_damage}) under 25,000"
            )
    except:
        pass

    # Otherwise manual review
    return (
        "Manual review",
        "Default routing applied"
    )
