from termcolor import colored

import server.const
import server.flask_server


def main():
    print(colored(f"{server.const.APP_FULLNAME}", color="green"))
    server.flask_server.server.run("localhost", 8252)
