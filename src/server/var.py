configuration = {}
default_configuration = {
    "ip": "0.0.0.0",
    "port": 8254,
    "debug": False,
    "use_reloader": False,
    "iterations": 200_000,
    "cert_path": "cert.pem",
    "key_path": "key.pem",
    "common_name": "localhost",
    "domains": ["localhost"],
    "ips": ["127.0.0.1"],
    "shared_chat_hello_message": "Hello, world!",
}


cert: bytes
