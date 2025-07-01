import requests


def address_to_key_path(address: str):
    return f"server_certificates/{address.replace(":", ".")}.pem"


def get(url: str, verify: str | bool = False):
    response = requests.get(url, verify=verify)
    if not response.ok:
        raise Exception(
            f"Failed to fetch {url}: error {response.status_code}: {response.text}"
        )
    return response.text
