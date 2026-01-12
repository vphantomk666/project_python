#!/usr/bin/env python3
import phonenumbers
from phonenumbers import (
    geocoder,
    carrier,
    NumberParseException,
    PhoneNumberFormat,
    format_number,
    region_code_for_number,
)
import time
import random

<<<<<<< HEAD
# ---- Expanded India mobile prefix map (first 4 digits of mobile numbers) ----
# These correspond to telecom circles (approximate states)
INDIA_PREFIX_MAP = {
    # Maharashtra & Goa
    "9820": "Maharashtra (Mumbai)",
    "9822": "Maharashtra (Pune)",
    "9823": "Maharashtra (Nagpur)",
    "9860": "Maharashtra (Mumbai)",
    "9869": "Maharashtra (Pune)",

    # Karnataka
    "9845": "Karnataka (Bangalore)",
    "9844": "Karnataka (Mysore)",
    "9843": "Karnataka (Mangalore)",

    # Delhi NCR
    "9810": "Delhi NCR",
    "9818": "Delhi NCR",
    "9910": "Delhi NCR",

    # Tamil Nadu
    "9840": "Tamil Nadu (Chennai)",
    "9842": "Tamil Nadu (Coimbatore)",

    # Kerala
    "9847": "Kerala (Trivandrum)",
    "9846": "Kerala (Kochi)",
    "8545": "Kerala (Trivandrum/Kochi region)",  # ✅ Added this

    # West Bengal
    "9830": "West Bengal (Kolkata)",
    "9831": "West Bengal (Siliguri)",

    # Gujarat
    "9824": "Gujarat (Ahmedabad)",
    "9898": "Gujarat (Surat)",

    # Telangana / Andhra Pradesh
    "9849": "Telangana (Hyderabad)",
    "9848": "Andhra Pradesh (Vijayawada)",

    # Rajasthan
    "9829": "Rajasthan (Jaipur)",

    # Uttar Pradesh
    "9839": "Uttar Pradesh (Lucknow)",
    "9889": "Uttar Pradesh (Ghaziabad)",

    # Bihar / Jharkhand
    "9431": "Bihar (Patna)",
    "9334": "Jharkhand (Ranchi)",

    # Madhya Pradesh / Chhattisgarh
    "9826": "Madhya Pradesh (Indore)",
    "9752": "Chhattisgarh (Raipur)",
}

def lookup_india_state(national_number_str):
    """Try to find a telecom circle/state for Indian mobile number."""
    if len(national_number_str) < 4:
        return None
    prefix4 = national_number_str[:4]
    return INDIA_PREFIX_MAP.get(prefix4)
=======
# ---- Optional: small demo prefix map for India (example only) ----
# This is illustrative — real mapping needs a much larger, up-to-date dataset.
# Keys here are the first 4-5 digits of the national number for mobile/landline prefixes.
INDIA_PREFIX_MAP = {
    "9876": "Maharashtra > Pune (approx.)",
    "9845": "Karnataka > Bangalore (approx.)",
    "9910": "Delhi (approx.)",
    "022":  "Maharashtra > Mumbai (landline STD 22)",
    "080":  "Karnataka > Bangalore (landline STD 80)",
    # add more prefixes as needed...
}

def lookup_india_district(national_number_str):
    # try 5, then 4, then 3 digit prefixes
    for l in (5, 4, 3):
        if len(national_number_str) >= l:
            prefix = national_number_str[:l]
            if prefix in INDIA_PREFIX_MAP:
                return INDIA_PREFIX_MAP[prefix]
    return None
>>>>>>> b39c30135c4d4ab0e1cb8f446ec019fbe868c3e6

# ---- Tracer function ----
def start_phone_tracer(target):
    """Parse a phone number and print location + carrier info (best-effort)."""
<<<<<<< HEAD
    print("[+] PhoneTracer v3.0 - OSINT\n")
=======
    print("[+] PhoneTracer v2.1 - OSINT\n")
>>>>>>> b39c30135c4d4ab0e1cb8f446ec019fbe868c3e6
    print(f"[*] Target: {target}")
    print("[*] Initiating trace ...")
    time.sleep(random.uniform(0.3, 0.9))

    try:
        p = phonenumbers.parse(target, None)
    except NumberParseException as e:
        print(f"[!] Number parse error: {e}")
        return

<<<<<<< HEAD
    possible = phonenumbers.is_possible_number(p)
    valid = phonenumbers.is_valid_number(p)

    e164 = format_number(p, PhoneNumberFormat.E164)
    intl = format_number(p, PhoneNumberFormat.INTERNATIONAL)
    nat = format_number(p, PhoneNumberFormat.NATIONAL)
    region = region_code_for_number(p)
=======
    # basic validity checks
    possible = phonenumbers.is_possible_number(p)
    valid = phonenumbers.is_valid_number(p)

    # core formatting and metadata
    e164 = format_number(p, PhoneNumberFormat.E164)
    intl = format_number(p, PhoneNumberFormat.INTERNATIONAL)
    nat = format_number(p, PhoneNumberFormat.NATIONAL)
    region = region_code_for_number(p)  # e.g., 'IN', 'US'
>>>>>>> b39c30135c4d4ab0e1cb8f446ec019fbe868c3e6
    country_code = p.country_code
    national_number_str = str(p.national_number)

    print(f"[+] Possible number: {possible}")
    print(f"[+] Valid number:    {valid}")
    print("Formatted:")
<<<<<<< HEAD
    print(f"  E.164:         {e164}")
    print(f"  International: {intl}")
    print(f"  National:      {nat}")
=======
    print("  E.164:        ", e164)
    print("  International:", intl)
    print("  National:     ", nat)
>>>>>>> b39c30135c4d4ab0e1cb8f446ec019fbe868c3e6
    print(f"[+] Country code:  +{country_code}")
    print(f"[+] Region code:   {region if region else '(unknown)'}")
    print(f"[+] National num:  {national_number_str}")

<<<<<<< HEAD
    loc = geocoder.description_for_number(p, "en")
    print(f"[+] Geocoder location: {loc if loc else '(unknown)'}")

    car = carrier.name_for_number(p, "en")
    print(f"[+] Carrier:           {car if car else '(unknown)'}")

    # ---- Improved India state lookup ----
    if region == "IN":
        state = lookup_india_state(national_number_str)
        if state:
            print(f"[+] Likely state/circle: {state}")
        else:
            print("[+] State/circle: (not found in prefix map)")
    else:
=======
    # geolocation (best-effort human readable)
    loc = geocoder.description_for_number(p, "en")
    print(f"[+] Geocoder location: {loc if loc else '(unknown)'}")

    # carrier (best-effort)
    car = carrier.name_for_number(p, "en")
    print(f"[+] Carrier:           {car if car else '(unknown)'}")

    # Additional country-specific approximate district lookup (example: India)
    if region == "IN":
        approx = lookup_india_district(national_number_str)
        if approx:
            print(f"[+] Approx district/state (from prefix map): {approx}")
        else:
            print("[+] Approx district/state (prefix map): (not found in demo map)")
    else:
        # For other countries you could implement similar prefix->region maps
>>>>>>> b39c30135c4d4ab0e1cb8f446ec019fbe868c3e6
        print("[+] Approx district/state: (country-specific mapping not configured)")

    print("\n[+] Trace complete")

<<<<<<< HEAD

if __name__ == "__main__":
    number = input("Enter phone number with country code (e.g. +918976543210): ").strip()
    if number:
        start_phone_tracer(number)
    else:
        print("[!] No input provided.")
=======
if __name__ == "__main__":
    number = input("Enter phone number with country code (e.g. +14155552671): ").strip()
    start_phone_tracer(number)

>>>>>>> b39c30135c4d4ab0e1cb8f446ec019fbe868c3e6
