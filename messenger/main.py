########################################################################
# Program:
#    Lab 12, Bell-LaPadula
# Author:
#    Br. Helfrich, Kyle Mueller, Trevaye Morris
# Summary:
#    This program manages secret messages using Bell–LaPadula.
########################################################################

from .interact import Interact


def main() -> None:
    interact = Interact()
    interact.run()


if __name__ == "__main__":
    main()
