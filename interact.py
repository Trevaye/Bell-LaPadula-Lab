########################################################################
# COMPONENT:
#    INTERACT
# Author:
#    Br. Helfrich, Kyle Mueller, <your name here if you made a change>
# Summary: 
#    This class allows one user to interact with the system
########################################################################

import messages, control

###############################################################
# USER
###############################################################
class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password


# User/password list
userlist = [
    ["AdmiralAbe",     "password"],
    ["CaptainCharlie", "password"],
    ["SeamanSam",      "password"],
    ["SeamanSue",      "password"],
    ["SeamanSly",      "password"]
]

# Convert to User objects
users = [User(*u) for u in userlist]

ID_INVALID = -1


###############################################################
# INTERACT CLASS
###############################################################
class Interact:

    ##################################################
    # CONSTRUCTOR
    ##################################################
    def __init__(self, username, password, p_messages):
        if not self._authenticate(username, password):
            print("Authentication failed!")
            exit()

        self._username = username
        self._p_messages = p_messages

        # Security clearance from Bell–LaPadula policy
        self._clearance_level = control.authenticate(username)

    ##################################################
    # DISPLAY ALL MESSAGES
    ##################################################
    def display(self):
        print("Messages:")
        self._p_messages.display()
        print()

    ##################################################
    # SHOW A MESSAGE
    ##################################################
    def show(self):
        id_ = self._prompt_for_id("display")
        if not self._p_messages.show(id_):
            print(f"ERROR! Message ID '{id_}' does not exist\n")
        print()

    ##################################################
    # ADD MESSAGE (No Write Down)
    ##################################################
    def add(self):
        text = self._prompt_for_line("message")
        date = self._prompt_for_line("date")
        level = input("Security level (Public, Confidential, Privileged, Secret): ").strip()

        # Validate level name exists in enum
        if not hasattr(control.SecurityLevel, level.upper()):
            print("\tERROR: Invalid security level.\n")
            return

        sec_level = getattr(control.SecurityLevel, level.upper())

        # Bell–LaPadula: NO WRITE DOWN
        if control.can_write(self._clearance_level, sec_level):
            self._p_messages.add(text, self._username, date, level)
            print("\tMessage successfully added.\n")
        else:
            print("\tACCESS DENIED: Cannot write down.\n")

    ##################################################
    # UPDATE MESSAGE (No Write Down)
    ##################################################
    def update(self):
        id_ = self._prompt_for_id("update")

        # First check if message exists
        msg_exists = self._p_messages.show(id_)
        if not msg_exists:
            print(f"ERROR! Message ID '{id_}' does not exist\n")
            return

        # Get the message security level
        for m in self._p_messages._messages:
            if m.get_id() == id_:
                msg_level = m.get_security_level()

                # Bell–LaPadula write rule
                if not control.can_write(self._clearance_level, msg_level):
                    print("\tACCESS DENIED: Cannot write down.\n")
                    return

        new_text = self._prompt_for_line("updated message")
        self._p_messages.update(id_, new_text)
        print()

    ##################################################
    # REMOVE MESSAGE (No Write Down)
    ##################################################
    def remove(self):
        id_ = self._prompt_for_id("delete")

        # Find message
        for m in self._p_messages._messages:
            if m.get_id() == id_:
                msg_level = m.get_security_level()

                # Write check
                if not control.can_write(self._clearance_level, msg_level):
                    print("\tACCESS DENIED: Cannot write down.\n")
                    return

        self._p_messages.remove(id_)
        print()

    ##################################################
    # INPUT HELPERS
    ##################################################
    def _prompt_for_line(self, verb):
        return input(f"Please provide a {verb}: ")

    def _prompt_for_id(self, verb):
        return int(input(f"Select the message ID to {verb}: "))

    ##################################################
    # AUTHENTICATE USER
    ##################################################
    def _authenticate(self, username, password):
        for u in users:
            if u.name == username and u.password == password:
                return True
        return False


###############################################################
# DISPLAY USERS
###############################################################
def display_users():
    for u in users:
        print(f"\t{u.name}")