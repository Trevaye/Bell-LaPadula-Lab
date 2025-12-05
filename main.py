########################################################################
# Program:
#    Lab 12, Bell-LaPadula
# Author:
#    Br. Helfrich, Kyle Mueller, Trevaye Morris
#    This program is designed to keep track of a number of secret
#    messages. IT will display messages to the appropriate users
#    and withhold messages from those lacking the authority.
########################################################################

from os import path
import interact, messages, control

# Locate messages.txt file
FILE_NAME = path.join(path.dirname(path.abspath(__file__)), "messages.txt")

session_open = True

def close_session():
    global session_open
    session_open = False

def open_session():
    global session_open
    session_open = True

################################################
# DISPLAY OPTIONS
################################################
def display_options():
    print("\td .. Display the list of messages\n" +
          "\ts .. Show one message\n" +
          "\ta .. Add a new message\n" + 
          "\tu .. Update an existing message\n" + 
          "\tr .. Delete an existing message\n" + 
          "\to .. Display this list of options\n" + 
          "\tl .. Log out\n")

####################################################
# SESSION
# One login session
####################################################
def session():
    open_session()

    print("Users:")
    interact.display_users()

    username = input("\nWhat is your username? ")
    password = input("What is your password? ")

    # Determine security clearance before loading messages
    clearance = control.authenticate(username)

    # Load messages with user clearance
    msgs = messages.Messages(FILE_NAME, clearance)

    # Create interaction session
    interact_ = interact.Interact(username, password, msgs)

    print(f"\nWelcome, {username}. Please select an option:\n")
    display_options()

    # Command options
    options = {
        "o": "print('Options:'); display_options();",
        "d": "interact_.display();",
        "s": "interact_.show();",
        "a": "interact_.add();",
        "u": "interact_.update();",
        "r": "interact_.remove();",
        "l": "print(f'Goodbye, {username}{chr(10)}'); close_session();"
    }

    while session_open:
        option = input(f"{username}> ")
        exec(options.get(option, f"print(f\"Unknown option: '{option}'\");"))

####################################################
# MAIN
####################################################
def main():
    done = False
    while not done:
        session()
        done = input("Will another user be logging in? (y/n) ").upper() != "Y"
    return 0


if __name__ == "__main__":
    main()