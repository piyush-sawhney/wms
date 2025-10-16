import re
product_code_type_mapping = {
    "PC": "Vehicle Insurance",
    "TW": "Vehicle Insurance",
    "NP": "Health Insurance",
    "UK": "Health Insurance",
    "TU": "Health Insurance",
    "HH": "Householder Insurance"
}

def process_policy_number(policy_number: str) -> str:
    return re.sub(r'\D', '', policy_number)

def process_insurance_type(product_code: str) -> str | None:
    return product_code_type_mapping.get(product_code)
