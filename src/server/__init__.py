import os

from termcolor import colored

import server.var
import server.path
from common import os_utils


print(colored(f"{server.const.APP_FULLNAME}", color="green"))


server.path.absolute_application_path = os.path.dirname(os.path.abspath(__file__))
