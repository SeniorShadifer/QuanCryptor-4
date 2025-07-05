import datetime
import base64
import json
import os
from ipaddress import ip_address
from datetime import datetime, timezone, timedelta

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.x509.oid import NameOID
from cryptography.fernet import Fernet
from cryptography import x509


import server.var
from common import os_utils, crypto_utils

iterations: int

password: bytes
salt: bytes
key: bytes

checksum_salt: bytes
checksum_hash: bytes
checksum: str = "{}"

fernet: Fernet


def load_key():
    global password, salt, key, checksum, checksum_salt, checksum_hash, fernet, iterations

    iterations = int(server.var.configuration["iterations"])

    password = os_utils.load_or_generate_bytes(f"./password.txt")

    salt = os_utils.load_or_generate_bytes(f"./salt.txt")

    key = crypto_utils.hash_with_salt(password, salt, iterations)

    fernet = Fernet(base64.b64encode(key), backend=default_backend())

    checksum_salt = os.urandom(16).hex().encode()
    checksum_hash = crypto_utils.hash_with_salt(
            password,
            checksum_salt,
            iterations,
        )
    

    checksum = json.dumps(
        {
            "salt": base64.b64encode(checksum_salt).decode(),
            "hash": base64.b64encode(checksum_hash).decode(),
        }
    )


def load_cert():
    private_key = crypto_utils.generate_keypair()

    subject = issuer = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, "RU"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Moscow"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, ""),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "ShadowHack"),
            x509.NameAttribute(
                NameOID.COMMON_NAME, server.var.configuration["common_name"]
            ),
        ]
    )

    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.now(timezone.utc))
        .not_valid_after(datetime.now(timezone.utc) + timedelta(days=365 * 100))
        .add_extension(
            x509.SubjectAlternativeName(
                [x509.DNSName(domain) for domain in server.var.configuration["domains"]]
                + [
                    x509.IPAddress(ip_address(ip))
                    for ip in server.var.configuration["ips"]
                ]
            ),
            critical=False,
        )
        .sign(private_key, hashes.SHA256())
    )

    with open(
        server.var.configuration["key_path"],
        "wb",
    ) as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    public_bytes = cert.public_bytes(serialization.Encoding.PEM)
    with open(
        server.var.configuration["cert_path"],
        "wb",
    ) as f:
        f.write(public_bytes)

    return public_bytes
