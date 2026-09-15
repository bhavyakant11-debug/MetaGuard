import re


def check_compliance(text):
    """
    Check OCR text for important Legal Metrology declarations.
    This is a prototype screening tool.
    """

    text_lower = text.lower()

    violations = []
    detected_fields = {}

    # -------------------------------------------------
    # 1. MANUFACTURER / PACKER / IMPORTER
    # -------------------------------------------------

    manufacturer_keywords = [
        "manufactured by",
        "manufactured",
        "manufacturing",
        "packed by",
        "packer",
        "importer",
        "pepsico india",
        "pepsico"
    ]

    manufacturer_found = any(
        keyword in text_lower
        for keyword in manufacturer_keywords
    )

    detected_fields["manufacturer_packer_importer"] = manufacturer_found

    if not manufacturer_found:
        violations.append(
            "Manufacturer/Packer/Importer declaration not detected. "
            "Manual verification recommended."
        )

    # -------------------------------------------------
    # 2. NET QUANTITY
    # -------------------------------------------------

    net_quantity_patterns = [
        r"\bnet\s*(quantity|qty)\b",
        r"\bnet\s*(wt|weight)\b",
        r"\bnet\s*w\b",
        r"\bnet\s*q\b"
    ]

    net_quantity_found = any(
        re.search(pattern, text_lower)
        for pattern in net_quantity_patterns
    )

    detected_fields["net_quantity"] = net_quantity_found

    if not net_quantity_found:
        violations.append(
            "Net quantity declaration not detected. "
            "Manual verification recommended."
        )

    # -------------------------------------------------
    # 3. MRP
    # -------------------------------------------------

    mrp_patterns = [
        r"\bmrp\b",
        r"\bm\.r\.p\b",
        r"\bmaximum\s+retail\s+price\b",
        r"\bmaximum\s+retail\b",
        r"\bretail\s+sale\s+price\b",
        r"\bsale\s+price\b"
    ]

    mrp_found = any(
        re.search(pattern, text_lower)
        for pattern in mrp_patterns
    )

    detected_fields["mrp"] = mrp_found

    if not mrp_found:
        violations.append(
            "MRP/retail sale price declaration not detected. "
            "Manual verification recommended."
        )

    # -------------------------------------------------
    # 4. DATE INFORMATION
    # -------------------------------------------------

    date_keywords = [
        "packed on",
        "packing date",
        "date of packing",
        "manufactured on",
        "manufactured date",
        "mfd",
        "mfg",
        "best before",
        "use by",
        "date"
    ]

    date_found = any(
        keyword in text_lower
        for keyword in date_keywords
    )

    detected_fields["date_information"] = date_found

    if not date_found:
        violations.append(
            "Packing/manufacturing/date information not detected. "
            "Manual verification recommended."
        )

    # -------------------------------------------------
    # 5. CONSUMER CARE
    # -------------------------------------------------

    consumer_keywords = [
        "consumer care",
        "consumer services",
        "consumer complaint",
        "customer care",
        "call us",
        "email us",
        "consumerfeedback"
    ]

    consumer_found = any(
        keyword in text_lower
        for keyword in consumer_keywords
    )

    detected_fields["consumer_care"] = consumer_found

    if not consumer_found:
        violations.append(
            "Consumer care information not detected. "
            "Manual verification recommended."
        )

    # -------------------------------------------------
    # 6. CALCULATE COMPLIANCE SCORE
    # -------------------------------------------------

    total_checks = len(detected_fields)
    passed_checks = sum(detected_fields.values())

    score = int(
        (passed_checks / total_checks) * 100
    )

    if score == 100:
        status = "Compliant"

    elif score >= 60:
        status = "Partially Compliant"

    else:
        status = "Non-Compliant"

    # -------------------------------------------------
    # 7. RETURN RESULT
    # -------------------------------------------------

    return {
        "compliance_status": status,
        "compliance_score": score,
        "detected_fields": detected_fields,
        "violations": violations
    }