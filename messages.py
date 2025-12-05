########################################################################
# COMPONENT:
#    MESSAGES
# Author:
#    Br. Helfrich, Kyle Mueller, <your name here if you made a change>
# Summary: 
#    This class stores the notion of a collection of messages
########################################################################

import control
import message

class Messages:

    ##################################################
    # CONSTRUCTOR
    # filename: file containing stored messages
    # clearance: current user's security level
    ##################################################
    def __init__(self, filename, clearance):
        self._messages = []
        self._clearance = clearance
        self._read_messages(filename)

    ##################################################
    # DISPLAY LIST OF MESSAGES (No Read Up enforced)
    ##################################################
    def display(self):
        for m in self._messages:
            if control.can_read(self._clearance, m.get_security_level()):
                m.display_properties()

    ##################################################
    # SHOW SINGLE MESSAGE (No Read Up enforced)
    ##################################################
    def show(self, id):
        for m in self._messages:
            if m.get_id() == id:
                if control.can_read(self._clearance, m.get_security_level()):
                    m.display_text()
                else:
                    print("\tACCESS DENIED")
                return True
        return False

    ##################################################
    # UPDATE MESSAGE (No Write Down enforced)
    ##################################################
    def update(self, id, text):
        for m in self._messages:
            if m.get_id() == id:
                if control.can_write(self._clearance, m.get_security_level()):
                    m.update_text(text)
                else:
                    print("\tACCESS DENIED")

    ##################################################
    # REMOVE MESSAGE (No Write Down enforced)
    ##################################################
    def remove(self, id):
        for m in self._messages:
            if m.get_id() == id:
                if control.can_write(self._clearance, m.get_security_level()):
                    m.clear()
                else:
                    print("\tACCESS DENIED")

    ##################################################
    # ADD NEW MESSAGE (No Write Down enforced)
    ##################################################
    def add(self, text, author, date, security_level):

        # Convert string → integer enum
        if isinstance(security_level, str):
            security_level = getattr(control.SecurityLevel, security_level.upper(), None)

        if control.can_write(self._clearance, security_level):
            m = message.Message(text, author, date, security_level)
            self._messages.append(m)
        else:
            print("\tACCESS DENIED")

    ##################################################
    # READ EXISTING MESSAGES FROM FILE
    ##################################################
    def _read_messages(self, filename):
        try:
            with open(filename, "r") as f:
                for line in f:
                    level, author, date, text = line.split('|')
                    level = level.strip()
                    self.add(text.rstrip("\r\n"), author, date, level)

        except FileNotFoundError:
            print(f"ERROR! Unable to open file \"{filename}\"")
