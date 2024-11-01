import phonenumbers
import requests
from bs4 import BeautifulSoup as bs
import re


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




class EmailExtractor:
  def __init__(self):
    pass

  def extract_emails_from_url(self, url):
    # Handle http/https
    if 'http' not in url:
      url = 'https://' + url

    try:
      response = requests.get(url)
    except Exception as e:
      print(f"Error fetching URL: {e}")
      return

    if response.status_code == 200:
      text = response.text
      soup = bs(text, 'html.parser').body
      emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', str(soup))
      emails_set = set(emails)
      if emails_set:
        for email in emails_set:
          print(email)
      else:
        print('No emails found.')

  def extract_emails_from_file(self):
    file_path = input("Enter file path: ")
    try:
      with open(file_path, "r") as file:
        urls = file.read().splitlines() # Read lines from the file
        for url in urls:
          self.extract_emails_from_url(url)
    except FileNotFoundError:
      print(f"File not found: {file_path}")




