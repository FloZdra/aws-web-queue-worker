# echo.py

import shlex
import sys

from Client.CalculationService import CalculationService


def main() -> int:
    print('Welcome to the web worker calculation tool using AWS services')

    calculation_service = CalculationService()

    if not calculation_service.booted:
        print('Error during initialization')
        return -1

    message_id = calculation_service.send_message([1, 2, 3])

    response = calculation_service.get_message(message_id)

    return 0


if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit
