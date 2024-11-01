import phonenumbers

from phonenumbers import geocoder,carrier,timezone
def get_phone_number_info(phone_number):
    try:
        number = phonenumbers.parse(phone_number)
        if not phonenumbers.is_valid_number(number):
            return "Invalid phone number"

        validity = "Valid" if phonenumbers.is_valid_number(number) else "Invalid"
        location = geocoder.description_for_number(number, "en")
        operator = carrier.name_for_number(number, "en")
        time_zones = timezone.time_zones_for_number(number)

        message = (
            f"Validity: {validity}\n"
            f"Location: {location}\n"
            f"Operator: {operator}\n"
            f"Time Zones: {time_zones}\n"
        )

        country_code = number.country_code
        national_number = number.national_number
        message += (
            f"Country Code: +{country_code}\n"
            f"National Number: {national_number}"
        )

        return message
    except Exception as e:
        return str(e)