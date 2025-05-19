#!/usr/bin/env python3
import requests
import webbrowser
from urllib.parse import quote_plus
from pyfiglet import Figlet
from colorama import init
from termcolor import colored

# Initialize colorama
init()

# ASCII Banner for tool
def print_main_banner():
    figlet = Figlet(font='slant')
    banner = figlet.renderText("AUTOMATED OSINT Tool")
    print(colored(banner, 'green'))

# ASCII Banner for sections
def print_banner(section_name):
    figlet = Figlet(font='slant')
    banner = figlet.renderText(section_name)
    print(colored(banner, 'cyan'))

# 1. WHOIS Lookup
def whois_lookup():
    print_banner("WHOIS Lookup")
    domain = input("Enter domain: ")
    url = f"https://whois.domaintools.com/{domain}"
    print(f"Opening WHOIS info for: {domain}")
    webbrowser.get('chromium').open(url)

# 2. DNS Lookup
def dns_lookup():
    print_banner("DNS Lookup")
    domain = input("Enter domain: ")
    url = f"https://api.hackertarget.com/dnslookup/?q={domain}"
    try:
        response = requests.get(url)
        print(response.text)
    except Exception as e:
        print(f"DNS Lookup failed: {e}")

# 3. Reverse DNS
def reverse_dns():
    print_banner("Reverse DNS")
    ip = input("Enter IP address: ")
    url = f"https://api.hackertarget.com/reversedns/?q={ip}"
    try:
        response = requests.get(url)
        print(response.text)
    except Exception as e:
        print(f"Reverse DNS failed: {e}")

# 4. GeoIP and Location
def geoip_location():
    print_banner("GeoIP / Location")
    choice = input("1. IP Lookup\n2. Place Search\nChoose option (1/2): ")
    if choice == "1":
        ip = input("Enter IP address: ")
        url = f"https://api.hackertarget.com/geoip/?q={ip}"
        try:
            response = requests.get(url)
            print(response.text)
            if "Latitude" in response.text and "Longitude" in response.text:
                # Try to extract lat/long if included
                lines = response.text.splitlines()
                lat, lon = None, None
                for line in lines:
                    if "Latitude" in line:
                        lat = line.split(":")[1].strip()
                    if "Longitude" in line:
                        lon = line.split(":")[1].strip()
                if lat and lon:
                    maps_url = f"https://www.google.com/maps?q={lat},{lon}"
                    print(f"Opening Google Maps at: {maps_url}")
                    webbrowser.get('chromium').open(maps_url)
            else:
                location = response.text.split("\n")[1].split(":")[1].strip()
                maps_url = f"https://www.google.com/maps/search/{quote_plus(location)}"
                print(f"Opening Google Maps for: {location}")
                webbrowser.get('chromium').open(maps_url)
        except Exception as e:
            print(f"GeoIP failed: {e}")
    elif choice == "2":
        place = input("Enter place name: ")
        query = quote_plus(place)
        maps_url = f"https://www.google.com/maps/search/{query}"
        print(f"Opening map for: {place}")
        webbrowser.get('chromium').open(maps_url)
    else:
        print("Invalid choice.")

# 5. HTTP Header Grabber
def http_headers():
    print_banner("HTTP Headers")
    domain = input("Enter domain: ")
    url = f"https://api.hackertarget.com/httpheaders/?q={domain}"
    try:
        response = requests.get(url)
        print(response.text)
    except Exception as e:
        print(f"Header fetch failed: {e}")

# 6. Subnet Lookup
def subnet_lookup():
    print_banner("Subnet Lookup")
    ip = input("Enter IP address or subnet: ")
    url = f"https://api.hackertarget.com/subnetcalc/?q={ip}"
    try:
        response = requests.get(url)
        print(response.text)
    except Exception as e:
        print(f"Subnet Lookup failed: {e}")

# 7. ASN Lookup
def asn_lookup():
    print_banner("ASN Lookup")
    ip = input("Enter IP or domain: ")
    url = f"https://api.hackertarget.com/aslookup/?q={ip}"
    try:
        response = requests.get(url)
        print(response.text)
    except Exception as e:
        print(f"ASN Lookup failed: {e}")

# 8. Username Search
def search_username():
    print_banner("Username Search")
    username = input("Enter username: ")
    print("[+] Searching username across platforms...")
    platforms = {
        "Facebook": f"https://www.facebook.com/{username}",
        "Instagram": f"https://www.instagram.com/{username}",
        "GitHub": f"https://github.com/{username}",
        "LinkedIn": f"https://www.linkedin.com/search/results/all/?keywords={quote_plus(username)}",
        "Google Scholar": f"https://scholar.google.com/scholar?q={quote_plus(username)}",
        "Scopus": f"https://www.scopus.com/freelookup/form/author.uri?authorName={quote_plus(username)}",
        "ResearchGate": f"https://www.researchgate.net/search?q={quote_plus(username)}"
    }
    for platform, url in platforms.items():
        print(f"[*] {platform}: {url}")
        webbrowser.get('chromium').open(url)

# 9. Exit
def exit_tool():
    print(colored("Exiting Automated OSINT Tool. Stay safe!", 'red'))
    exit()

# Main Menu
def main():
    print_main_banner()
    while True:
        print(colored("""
[1] WHOIS Lookup
[2] DNS Lookup
[3] Reverse DNS
[4] GeoIP / Location
[5] HTTP Header Grabber
[6] Subnet Lookup
[7] ASN Lookup
[8] Username Search
[9] Exit
""", 'yellow'))

        choice = input("Choose an option: ")

        if choice == "1":
            whois_lookup()
        elif choice == "2":
            dns_lookup()
        elif choice == "3":
            reverse_dns()
        elif choice == "4":
            geoip_location()
        elif choice == "5":
            http_headers()
        elif choice == "6":
            subnet_lookup()
        elif choice == "7":
            asn_lookup()
        elif choice == "8":
            search_username()
        elif choice == "9":
            exit_tool()
        else:
            print("Invalid option. Try again.")

# Run
if __name__ == "__main__":
    main()
