TAG_WEIGHTS = {
    "duplicate_in_other_departments": 0.9,       # Same project name used across multiple ministries
    "multi_unit_duplicate": 0.7,                 # Same project name appears under multiple units in the same ministry
    "over_aggregated_in_region": 0.85,           # A project name appears too frequently in certain units (over-concentration)
    "creative_ambiguous_terminology": 0.3,       # Vague terms like "soft power", "นวัตกรรม", etc.
    "suspicious_procurement": 0.6,               # Keywords like จ้างเหมาบริการ, ครุภัณฑ์, เช่า
    "too_common_term": 0.2                       # Project names that occur very frequently
}
