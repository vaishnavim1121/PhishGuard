import re
import socket
import whois
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import dns.resolver
import pandas as pd

def has_ip_address(url):
    pattern = r'(\d{1,3}\.){3}\d{1,3}'
    return -1 if re.search(pattern, url) else 1

def url_length(url):
    length = len(url)
    if length < 54:
        return 1
    elif 54 <= length <= 75:
        return 0
    else:
        return -1

def shortening_service(url):
    shortening_services = r"(bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|qr\.ae|adf\.ly|bitly\.com|cur\.lv|tinyurl\.com|ity\.im|q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net)"
    match = re.search(shortening_services, url)
    print(f"URL: {url}")
    print(f"Pattern: {shortening_services}")
    print(f"Match: {match}")
    return -1 if match else 1

def has_at_symbol(url):
    return -1 if '@' in url else 1

def double_slash_redirecting(url):
    pos = url.find('//', url.find('://') + 3)
    return -1 if pos != -1 else 1

def prefix_suffix(url):
    domain = urlparse(url).netloc
    return -1 if '-' in domain else 1

def has_subdomain(url):
    domain = urlparse(url).netloc
    count = domain.count('.')
    if count == 1:
        return 1
    elif count == 2:
        return 0
    else:
        return -1

def ssl_final_state(url):
    try:
        response = requests.get(url, timeout=5)
        return 1 if response.url.startswith('https') else -1
    except:
        return -1

def domain_registration_length(url):
    try:
        domain = urlparse(url).netloc
        w = whois.whois(domain)
        expiration_date = w.expiration_date
        creation_date = w.creation_date
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if expiration_date and creation_date:
            days = (expiration_date - creation_date).days
            return 1 if days / 365 > 1 else -1
        else:
            return -1
    except:
        return -1

def favicon(url):
    # Placeholder: returning 1 for simplicity
    return 1

def port(url):
    domain = urlparse(url).netloc
    parts = domain.split(':')
    return -1 if len(parts) == 2 else 1

def https_token(url):
    domain = urlparse(url).netloc
    return -1 if 'https' in domain else 1

def request_url(url):
    # Placeholder: returning 1 for simplicity
    return 1

def url_of_anchor(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')
        anchors = soup.find_all('a', href=True)
        if len(anchors) == 0:
            return -1
        suspicious = 0
        total = len(anchors)
        domain = urlparse(url).netloc
        for a in anchors:
            href = a['href']
            href_domain = urlparse(href).netloc
            if href == '' or href == '#' or 'javascript' in href.lower():
                suspicious += 1
            elif href_domain != '' and href_domain != domain:
                suspicious += 1
        ratio = suspicious / total
        if ratio < 0.31:
            return 1
        elif 0.31 <= ratio <= 0.67:
            return 0
        else:
            return -1
    except:
        return -1

def links_in_tags(url):
    # Placeholder: returning 1 for simplicity
    return 1

def sfh(url):
    # Placeholder: returning 1 for simplicity
    return 1

def submitting_to_email(url):
    return -1 if 'mailto:' in url else 1

def abnormal_url(url):
    # Placeholder: returning 1 for simplicity
    return 1

def redirect(url):
    try:
        response = requests.get(url, timeout=5)
        count = len(response.history)
        if count <= 1:
            return 1
        elif 2 <= count <= 4:
            return 0
        else:
            return -1
    except:
        return -1

def on_mouseover(url):
    # Placeholder: returning 1 for simplicity
    return 1

def right_click(url):
    # Placeholder: returning 1 for simplicity
    return 1

def popup_window(url):
    # Placeholder: returning 1 for simplicity
    return 1

def iframe(url):
    # Placeholder: returning 1 for simplicity
    return 1

def age_of_domain(url):
    try:
        domain = urlparse(url).netloc
        w = whois.whois(domain)
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if creation_date:
            days = (pd.Timestamp.now() - pd.Timestamp(creation_date)).days
            return 1 if days >= 180 else -1
        else:
            return -1
    except:
        return -1

def dns_record(url):
    try:
        domain = urlparse(url).netloc
        dns.resolver.resolve(domain, 'A')
        return 1
    except:
        return -1

def web_traffic(url):
    # Placeholder: returning 1 for simplicity
    return 1

def page_rank(url):
    # Placeholder: returning 1 for simplicity
    return 1

def google_index(url):
    try:
        domain = urlparse(url).netloc
        search_url = f"https://www.google.com/search?q=site:{domain}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(search_url, headers=headers, timeout=5)
        if "did not match any documents" in response.text:
            return -1
        else:
            return 1
    except:
        return 0

def links_pointing_to_page(url):
    # Placeholder: returning 1 for simplicity
    return 1

def statistical_report(url):
    # Placeholder: returning 1 for simplicity
    return 1

def extract_features(url):
    features = []
    features.append(has_ip_address(url))
    features.append(url_length(url))
    features.append(shortening_service(url))
    features.append(has_at_symbol(url))
    features.append(double_slash_redirecting(url))
    features.append(prefix_suffix(url))
    features.append(has_subdomain(url))
    features.append(ssl_final_state(url))
    features.append(domain_registration_length(url))
    features.append(favicon(url))
    features.append(port(url))
    features.append(https_token(url))
    features.append(request_url(url))
    features.append(url_of_anchor(url))
    features.append(links_in_tags(url))
    features.append(sfh(url))
    features.append(submitting_to_email(url))
    features.append(abnormal_url(url))
    features.append(redirect(url))
    features.append(on_mouseover(url))
    features.append(right_click(url))
    features.append(popup_window(url))
    features.append(iframe(url))
    features.append(age_of_domain(url))
    features.append(dns_record(url))
    features.append(web_traffic(url))
    features.append(page_rank(url))
    features.append(google_index(url))
    features.append(links_pointing_to_page(url))
    features.append(statistical_report(url))
    return features
