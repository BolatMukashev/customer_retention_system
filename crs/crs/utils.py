import re

def format_phone_number(value):
    digits = re.sub(r"\D", "", str(value))
    if len(digits) == 11 and digits[0] in ("7", "8"):
        return f"+7 {digits[1:4]} {digits[4:7]} {digits[7:9]} {digits[9:11]}"
    return value