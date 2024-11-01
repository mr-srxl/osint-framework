import phonenumbers
import requests
from bs4 import BeautifulSoup as bs
import re
import folium
from pystyle import Colors, Colorate, Write
import whois
import folium as folium
from IPython import display
from PIL import Image, ExifTags
from ipyleaflet import Map, Marker
import folium
from ipyleaflet import Map, basemaps, basemap_to_tiles
from pystyle import Colors, Colorate


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


def get_info_by_ip():
    try:
        ip = input(Colorate.Horizontal(Colors.red_to_yellow, ("IP : ")))
        response = requests.get(url=f'http://ip-api.com/json/{ip}').json()
        info = {
            'ip': response.get('query'),
            'country': response.get('country'),
            'city': response.get('city'),
            'provider': response.get('isp'),
            'organization': response.get('org'),
            'regionName': response.get('regionName'),
            'postal code': response.get('zip'),
            'lat': response.get('lat'),
            'lon': response.get('lon'),
        }
        for k, v in info.items():
            print(Colorate.Horizontal(Colors.red_to_yellow, f'{k} : {v}'.strip()))
        area = folium.Map(location=[response.get('lat'), response.get('lon')])
        area.save(f'{response.get("query")}_{response.get("city")}.html')

    except requests.exceptions.ConnectionError:
        print(Colorate.Horizontal(Colors.red_to_yellow, '[!] Check your connection!'.strip()))

def get_whois():
    domain= input(Colorate.Horizontal(Colors.red_to_yellow, ("Domin : ")))
    try:
      domain_info = whois.whois(domain)
      info = (f"\n"
              f"  |Information about the site: \n"
              f"  |Domain: {domain_info.domain_name}\n"
              f"  |IP address: {domain_info.name_servers}\n"
              f"  |Registered: {domain_info.creation_date}\n"
              f"  |Expires: {domain_info.expiration_date}  \n"
              f"  |Organization: {domain_info.registrant_organization}\n"
              f"  |Owner: {domain_info.registrant_name}\n"
              f"  |Address: {domain_info.registrant_address}\n"
              f"  |Country: {domain_info.registrant_country}\n"
              f"  |City: {domain_info.registrant_city}\n"
              f"  |State: {domain_info.registrant_state}\n"
              f"  |Postal code: {domain_info.registrant_postal_code}\n"
              f"    ")
      Write.Print(info + "\n", Colors.blue_to_red, interval=0.004)
    except Exception as e:
        print(f"Error: {e}\n")



def point_on_map(lat_coordinate, long_coordinate):

  my_map = folium.Map(location=[lat_coordinate, long_coordinate], zoom_start=10)

  folium.Marker(
    location=[lat_coordinate, long_coordinate],
    popup=f"Latitude: {lat_coordinate}\nLongitude: {long_coordinate}",
    icon=folium.Icon(color="red", icon="location-arrow"),
  ).add_to(my_map)

  my_map.save("loc.html")

  Write.Print("Map created successfully! Open location.html in your web browser.",Colors.red_to_green)


def get_exif(filename):
    exif_data = {}
    image = Image.open(filename)
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = ExifTags.TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for gps_tag in value:
                    sub_decoded = ExifTags.GPSTAGS.get(gps_tag, gps_tag)
                    gps_data[sub_decoded] = value[gps_tag]
                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    for i in exif_data.keys():
        if i == "GPSInfo":
            Write.Print(f"{i}: ",Colors.red_to_green,interval=0.00000000000000000000000000001,end="\n")
            for x in exif_data[i].keys():
                Write.Print(f"\t{x} : {exif_data[i][x]}\n", Colors.red_to_green,interval=0.00000000000000000000000000001)
        else:
            Write.Print(f"{i} : {exif_data[i]}\n",Colors.red_to_green,interval=0.00000000000000000000000000001)
    lat_ref = "S"
    lat_degrees = exif_data["GPSInfo"]["GPSLatitude"][0]
    lat_minutes = exif_data["GPSInfo"]["GPSLatitude"][1]
    lat_seconds = exif_data["GPSInfo"]["GPSLatitude"][2]
    lat_coordinate = - (lat_degrees + (lat_minutes / 60) + (lat_seconds / 3600))

    long_ref = "W"
    long_degrees = exif_data["GPSInfo"]["GPSLongitude"][0]
    long_minutes = exif_data["GPSInfo"]["GPSLongitude"][1]
    long_seconds = exif_data["GPSInfo"]["GPSLongitude"][2]
    long_coordinate = - (long_degrees + (long_minutes / 60) + (long_seconds / 3600))
    point_on_map(lat_coordinate, long_coordinate)

