from termcolor import colored

import server.const


print(colored(f"{server.const.APP_FULLNAME}", color="green"))
print(
    colored(
        f"Attention: this server is protected by multi-symmetric encryption, but this is not protected from hacker attacks. Use this in private netorks (as Wi-Fi local network or VPN) with small count of clients.",
        color="yellow",
    )
)
