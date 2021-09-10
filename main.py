import requests
import os
import logging
import argparse

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
PORKBUN_API_KEY = os.getenv('PORKBUN_API_KEY', '123')
PORKBUN_SECRET_KEY = os.getenv('PORKBUN_SECRET_KEY', '123')
URI_ENDPOINT = 'https://porkbun.com/api/json/v3/dns/'


def get_public_ip():
    """
    Gets the public IP address of the machine.
    """
    try:
        response = requests.get('https://api.ipify.org')
        return response.text
    except Exception as e:
        logging.error(e)
        return None


def get_dns_record(domain):
    """
    Gets the DNS record for a domain.
    """
    url = '{}/retrieve/{}'.format(URI_ENDPOINT, domain)
    payload = {
        'apikey': PORKBUN_API_KEY,
        'secretapikey': PORKBUN_SECRET_KEY
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        return response.json().get('records')
    except Exception as e:
        logging.error(e)
        return response.json()


def get_id_from_records(domain, subdomain):
    """
    Gets the ID of the DNS record from a list of records.
    """
    records = get_dns_record(domain)
    try:
        for record in records:
            if record['name'] == '{}.{}'.format(subdomain, domain):
                return record['id']
    except Exception as e:
        logging.error(e)
        return None


def create_dns_record(domain, subdomain):
    """
    Creates a DNS record for a domain.
    """
    url = '{}/create/{}'.format(URI_ENDPOINT, domain)
    payload = {
        'apikey': PORKBUN_API_KEY,
        'secretapikey': PORKBUN_SECRET_KEY,
        'name': subdomain,
        'type': 'A',
        'content': get_public_ip(),
        'ttl': '300',
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        return response.json()
    except Exception as e:
        logging.error(e)
        return None


def update_dns_record(domain, subdomain):
    """
    Updates the DNS record for a domain.
    """
    id = get_id_from_records(domain, subdomain)
    url = '{}/edit/{}/{}'.format(URI_ENDPOINT, domain, id)
    payload = {
        'apikey': PORKBUN_API_KEY,
        'secretapikey': PORKBUN_SECRET_KEY,
        'name': subdomain,
        'type': 'A',
        'content': get_public_ip(),
        'ttl': '300',
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        return response.json()
    except Exception as e:
        logging.error(e)
        return None


def check_if_dns_record_exists(domain, subdomain):
    """
    Checks if a DNS record exists for a domain.
    """
    records = get_dns_record(domain)
    full_domain = '{}.{}'.format(subdomain, domain)
    for record in records:
        if full_domain not in record['name']:
            logging.info(
                'DNS record does not exist for {}, creating record'.format(full_domain))
            create_dns_record(domain, subdomain)
            return 'Created DNS record'
        if record['name'] == full_domain and record['content'] != get_public_ip():
            logging.info(
                'DNS record exists for {}, updating record'.format(full_domain))
            update_dns_record(domain, subdomain)
            return 'Updated DNS record'
        if record['name'] == full_domain:
            logging.info('Domain exists and is up to date')
            return 'Domain exists and is up to date'
    return


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--domain', help='Domain to check', required=True)
    parser.add_argument('-s', '--subdomain',
                        help='Subdomain to check', required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    check_if_dns_record_exists(args.domain, args.subdomain)


if __name__ == "__main__":
    main()
