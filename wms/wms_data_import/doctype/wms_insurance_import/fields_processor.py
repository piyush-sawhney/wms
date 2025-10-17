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

def process_client_name(name: str) -> str:
    if not name:
        return name
    name = re.sub(r'^(mr|mrs|ms|miss|shri|smt)\.?\s+', '', name, flags=re.IGNORECASE)
    return re.sub(r'\s+', ' ', name).strip().upper()

def process_premium_amount(amount_str: str) -> float:
    return float(amount_str.replace(',', ''))


def process_sum_insured_amount(amount_str: str) -> float:
    return float(amount_str.replace(',', ''))