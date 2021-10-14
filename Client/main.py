# echo.py

import shlex
import sys

from boto3 import resource

from CalculationService import CalculationService
from menu import menu

def main() -> int:
    print('Welcome to the web worker calculation tool using AWS services')
    calculation_service = CalculationService()

    if not calculation_service.booted:
        print('Error during initialization')
        return -1

    stop = True
    while stop:
        message = menu()
        if message == 0:
            stop = False
        else:
            message_id = calculation_service.send_message(message)
            response = None
            while response == None:
                response = calculation_service.get_message(message_id)
            print(response)
    return 0


if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit
