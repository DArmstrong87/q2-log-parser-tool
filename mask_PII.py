import os
import re
import json
from pathlib import Path

# Local path and directory to your Q2 logs
directory = "./files"

# PII patterns
patterns = {
    "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "ssn": r"\b\d{3}[-]?\d{2}[-]?\d{4}\b",
    "credit_card": r"\b(?:\d[ -]*?){13,19}\b",
    "ip_address": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "address": r"\b\d+\s+[A-Za-z\s,]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Circle|Cir|Way|Place|Pl)\b",
    "np_token": r"NP Token:\s*[^\s]+",  # Matches "NP Token:" followed by any non-whitespace characters
}

# Field name patterns with their corresponding value patterns
field_patterns = {
    "name_fields": [
        r"(?:first_name|middle_name|last_name|full_name|name)[=:]\s*([A-Za-z\s\'-]+)",
        r'(?:first_name|middle_name|last_name|full_name|name)\s*=\s*["\']([A-Za-z\s\'-]+)["\']',
    ],
    "email_fields": [
        r"(?:email|email_address|e_mail)[=:]\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})",
        r'(?:email|email_address|e_mail)\s*=\s*["\']([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})["\']',
    ],
    "phone_fields": [
        r"(?:phone|home_phone|mobile_phone|work_phone|cell_phone|telephone)[=:]\s*((?:\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})",
        r'(?:phone|home_phone|mobile_phone|work_phone|cell_phone|telephone)\s*=\s*["\']((?:\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})["\']',
    ],
    "address_fields": [
        r"(?:address1|address2|street_address|mailing_address)[=:]\s*([A-Za-z0-9\s,.-]+)",
        r'(?:address1|address2|street_address|mailing_address)\s*=\s*["\']([A-Za-z0-9\s,.-]+)["\']',
    ],
    "location_fields": [
        r"(?:city|state|postal_code|zip_code)[=:]\s*([A-Za-z0-9\s-]+)",
        r'(?:city|state|postal_code|zip_code)\s*=\s*["\']([A-Za-z0-9\s-]+)["\']',
    ],
    "username_fields": [
        r"(?:login_name|username|user_name)[=:]\s*([A-Za-z0-9._-]+)",
        r'(?:login_name|username|user_name)\s*=\s*["\']([A-Za-z0-9._-]+)["\']',
    ],
}


def mask_json_data(text):
    """Mask PII in JSON/dictionary data within log lines."""
    # Look for dictionary-like data in the line
    dict_pattern = r"Data:\s*(\{.*\})"
    match = re.search(dict_pattern, text)

    if match:
        try:
            # Extract the dictionary part
            dict_str = match.group(1)
            # Replace Python object references with None
            dict_str = re.sub(r"<[^>]+>", "None", dict_str)
            # Convert Python dict string to valid JSON
            dict_str = dict_str.replace("'", '"')
            dict_str = re.sub(r"None", "null", dict_str)

            # Parse the JSON
            data = json.loads(dict_str)

            # Mask PII fields
            pii_fields = {
                "first_name",
                "last_name",
                "middle_name",
                "email_address",
                "home_phone",
                "mobile_phone",
                "work_phone",
                "address1",
                "address2",
                "city",
                "state",
                "postal_code",
                "ssn",
                "customer_primary_cif",
                "user_primary_cif",
                "login_name",
            }

            for field in pii_fields:
                if field in data and data[field]:
                    if field in ["first_name", "last_name", "middle_name"]:
                        data[field] = "[NAME]"
                    elif field in ["email_address"]:
                        data[field] = "[EMAIL]"
                    elif field in ["home_phone", "mobile_phone", "work_phone"]:
                        data[field] = "[PHONE]"
                    elif field in ["address1", "address2"]:
                        data[field] = "[ADDRESS]"
                    elif field in ["city", "state", "postal_code"]:
                        data[field] = "[LOCATION]"
                    elif field in ["ssn", "customer_primary_cif", "user_primary_cif"]:
                        data[field] = "[SSN]"
                    elif field in ["login_name"]:
                        data[field] = "[USERNAME]"

            # Convert back to string and replace in original text
            masked_dict = json.dumps(data)
            return text.replace(match.group(1), masked_dict)
        except json.JSONDecodeError:
            # If JSON parsing fails, return original text
            return text
    return text


def mask_field_values(text):
    """Mask values associated with specific field names."""
    masked_text = text

    # First handle JSON/dictionary data
    masked_text = mask_json_data(masked_text)

    # Then handle other field patterns
    for field_type, patterns_list in field_patterns.items():
        for pattern in patterns_list:
            if "=" in pattern:
                masked_text = re.sub(
                    pattern,
                    lambda m: f"{m.group(0).split('=')[0]}=[{field_type.upper().split('_')[0]}]",
                    masked_text,
                )
            if ":" in pattern:
                masked_text = re.sub(
                    pattern,
                    lambda m: f"{m.group(0).split(':')[0]}: [{field_type.upper().split('_')[0]}]",
                    masked_text,
                )

    return masked_text


def mask_pii(text):
    """Mask PII in the given text."""
    masked_text = text

    # First mask field values
    masked_text = mask_field_values(masked_text)

    # Then mask standalone PII
    masked_text = re.sub(patterns["email"], "[EMAIL]", masked_text)
    masked_text = re.sub(patterns["ssn"], "[SSN]", masked_text)
    masked_text = re.sub(patterns["credit_card"], "[CREDIT_CARD]", masked_text)
    masked_text = re.sub(patterns["ip_address"], "[IP_ADDRESS]", masked_text)
    masked_text = re.sub(patterns["address"], "[ADDRESS]", masked_text)
    
    # Mask NP Tokens
    masked_text = re.sub(patterns["np_token"], "NP Token: [REDACTED]", masked_text)

    return masked_text


def process_file(input_file, output_file):
    """Process a single file and write masked content to output file."""
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            # Process line by line to preserve all content
            masked_lines = []
            for line in f:
                masked_line = mask_pii(line)
                masked_lines.append(masked_line)

        with open(output_file, "w", encoding="utf-8") as f:
            f.writelines(masked_lines)

        print(f"Successfully processed {input_file}")
    except Exception as e:
        print(f"Error processing {input_file}: {str(e)}")


def main():
    # Create output directory if it doesn't exist
    output_dir = Path(directory) / "masked"
    output_dir.mkdir(exist_ok=True)

    # Process each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".log"):
            input_path = os.path.join(directory, filename)
            output_filename = filename.replace(".log", "_masked.log")
            output_path = os.path.join(output_dir, f"{output_filename}")
            process_file(input_path, output_path)


if __name__ == "__main__":
    main()
