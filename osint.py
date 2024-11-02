import datetime
import platform
import re
from os import system, name
import folium
import phonenumbers
import requests
import whois
from PIL import Image, ExifTags
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup as bs
from colorama import Fore
from phonenumbers import geocoder, carrier, timezone
from pystyle import Colors, Colorate
from pystyle import Write, Center
import signal


def signal_handler(sig, frame):
  print("\nGoodbye!")
  exit(0)
signal.signal(signal.SIGINT, signal_handler)


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


def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org').text
        return (response)
    except:
        return "check your internet"


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
                pass

    def extract_emails_from_file(self):

        file_path = input("Enter file path: ")
        try:
            with open(file_path, "r") as file:
                urls = file.read().splitlines()
                for url in urls:
                    self.extract_emails_from_url(url)
        except FileNotFoundError or IsADirectoryError:
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
        Write.Print("Map created successfully! Open"+f'{response.get("query")}_{response.get("city")}.html in your web browser.', Colors.red_to_yellow)

    except requests.exceptions.ConnectionError:
        print(Colorate.Horizontal(Colors.red_to_yellow, '[!] Check your connection!'.strip()))


def get_whois():
    domain = input(Colorate.Horizontal(Colors.red_to_yellow, ("Domin : ")))
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

    my_map.save("location.html")

    Write.Print("Map created successfully! Open location.html in your web browser.", Colors.red_to_green)


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
            Write.Print(f"{i}: ", Colors.red_to_green, interval=0.00000000000000000000000000001, end="\n")
            for x in exif_data[i].keys():
                Write.Print(f"\t{x} : {exif_data[i][x]}\n", Colors.red_to_green,
                            interval=0.00000000000000000000000000001)
        else:
            Write.Print(f"{i} : {exif_data[i]}\n", Colors.red_to_green, interval=0.00000000000000000000000000001)
    if "GPSInfo" in exif_data.keys():
        lat_ref = "S"
        lat_degrees, lat_minutes, lat_seconds = exif_data["GPSInfo"]["GPSLatitude"]
        lat_coordinate = - (lat_degrees + (lat_minutes / 60) + (lat_seconds / 3600))

        long_ref = "W"
        long_degrees, long_minutes, long_seconds = exif_data["GPSInfo"]["GPSLongitude"]
        long_coordinate = - (long_degrees + (long_minutes / 60) + (long_seconds / 3600))
        point_on_map(lat_coordinate, long_coordinate)
    else:
        print("GPS data not found in image.")


def pdf_metadate():
    pdf = Write.Input("Path: ", Colors.green, interval=0)
    try:
     reader = PdfReader(pdf)
     meta = reader.metadata
     print("File MEtadata:")
     for i in meta.keys():
         Write.Print(f"\t{i}: {meta[i]}", Colors.blue_to_purple, interval=0.00000000000000000000000000001, end="\n")
    except IsADirectoryError:
         Write.Print("it\'s not a file",Colors.red)



def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


def press_enter_to_continue():
    input(Fore.YELLOW + "\nPress Enter...")
    clear()


now = datetime.datetime.now()
banner = f"""
        ⣿⣿⣿⣿⣿⣿⡿⠛⣛⣛⣛⣛⣛⣛⣛⣛⣛⣛⡛⠛⠿⠿⢿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⡿⢃⣴⣿⠿⣻⢽⣲⠿⠭⠭⣽⣿⣓⣛⣛⣓⣲⣶⣢⣍⠻⢿⣿⣿
        ⣿⣿⣿⡿⢁⣾⣿⣵⡫⣪⣷⠿⠿⢿⣷⣹⣿⣿⣿⢲⣾⣿⣾⡽⣿⣷⠈⣿⣿
        ⣿⣿⠟⠁⣚⣿⣿⠟⡟⠡⠀⠀⠀⠶⣌⠻⣿⣿⠿⠛⠉⠉⠉⢻⣿⣿⠧⡙⢿  Coded by srxl
        ⡿⢡⢲⠟⣡⡴⢤⣉⣛⠛⣋⣥⣿⣷⣦⣾⣿⣿⡆⢰⣾⣿⠿⠟⣛⡛⢪⣎⠈  Time: {now.strftime("%Y-%m-%d %H:%M:%S")}
        ⣧⢸⣸⠐⣛⡁⢦⣍⡛⠿⢿⣛⣿⡍⢩⠽⠿⣿⣿⡦⠉⠻⣷⣶⠇⢻⣟⠟⢀  Os: {platform.uname()[0]}
        ⣿⣆⠣⢕⣿⣷⡈⠙⠓⠰⣶⣤⣍⠑⠘⠾⠿⠿⣉⣡⡾⠿⠗⡉⡀⠘⣶⢃⣾  Version: {1.0}
        ⣿⣿⣷⡈⢿⣿⣿⣌⠳⢠⣄⣈⠉⠘⠿⠿⠆⠶⠶⠀⠶⠶⠸⠃⠁⠀⣿⢸⣿  MY IP: {get_public_ip()}
        ⣿⣿⣿⣷⡌⢻⣿⣿⣧⣌⠻⢿⢃⣷⣶⣤⢀⣀⣀⢀⣀⠀⡀⠀⠀⢸⣿⢸⣿
        ⣿⣿⣿⣿⣿⣦⡙⠪⣟⠭⣳⢦⣬⣉⣛⠛⠘⠿⠇⠸⠋⠘⣁⣁⣴⣿⣿⢸⣿
        ⣿⣿⣿⣿⣿⣿⣿⣷⣦⣉⠒⠭⣖⣩⡟⠛⣻⣿⣿⣿⣿⣿⣟⣫⣾⢏⣿⠘⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣍⡛⠿⠿⣶⣶⣿⣿⣿⣿⣿⣾⣿⠟⣰⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣤⣭⣍⣉⣛⣋⣭⣥⣾⣿⣿

        [1] PHONE NUMBER INFO 
        [2] EmailExtractor(URL)
        [3] EmailExtractor(MULTI URl)
        [4] WHOIS
        [5] IP
        [6] Extract Metadate(IMAGE)
        [7] Extract Metadate(PDF)
"""


def execute_command(choice):
    if choice == '1':
        phone_number = input("Phone: ")
        info = get_phone_number_info(phone_number)
        Write.Print(info, Colors.red_to_yellow, interval=0.00000000000000000000000000001)
        press_enter_to_continue()
    elif choice == '2':
        url = Write.Input("Enter URL: ", Colors.red_to_yellow,
                          interval=0.00000000000000000000000000001)
        email = EmailExtractor()
        email.extract_emails_from_url(url)
        press_enter_to_continue()
    elif choice == '3':
        email = EmailExtractor()
        email.extract_emails_from_file()
    elif choice == '4':
        get_whois()
        press_enter_to_continue()
    elif choice == '5':
        get_info_by_ip()
        press_enter_to_continue()
    elif choice == '6':
        filename = Write.Input("Enter Path: ", Colors.red_to_yellow,
                               interval=0.00000000000000000000000000001)
        get_exif(filename)
        press_enter_to_continue()
    elif choice == '7':
        pdf_metadate()
        press_enter_to_continue()
    else:
        print("wrong!")
        press_enter_to_continue()


while True:
    try:
     Write.Print(banner, Colors.white, interval=0)
     command = input('\nmr.pwd> ')
     execute_command(command)
    except KeyboardInterrupt:
        print("\nGoodbye!")
        break
