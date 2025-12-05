########################################################################
# COMPONENT:
#    MESSAGE
# Author:
#    Br. Helfrich, Kyle Mueller, <your name here if you made a change>
# Summary: 
#    This class stores the notion of a message
########################################################################

##################################################
# MESSAGE
# One message to be displayed to the user or not
##################################################
class Message:

    # Static variable for the next id
    _id_next = 100

    ##################################################
    # MESSAGE CONSTRUCTOR
    # Creates a message and stores its security level
    ##################################################
    def __init__(self, text, author, date, security_level):
        self._text = text
        self._author = author
        self._date = date
        self._security_level = security_level
        self._id = Message._id_next
        Message._id_next += 1
        self._empty = (text == "")

    ##################################################
    # GET SECURITY LEVEL
    ##################################################
    def get_security_level(self):
        return self._security_level

    ##################################################
    # GET ID
    ##################################################
    def get_id(self):
        return self._id

    ##################################################
    # DISPLAY PROPERTIES (ID, Author, Date)
    ##################################################
    def display_properties(self):
        if self._empty:
            return
        print(f"\t[{self._id}] Message from {self._author} at {self._date}")

    ##################################################
    # DISPLAY TEXT CONTENT
    ##################################################
    def display_text(self):
        if not self._empty:
            print(f"\tMessage: {self._text}")

    ##################################################
    # UPDATE TEXT
    ##################################################
    def update_text(self, new_text):
        self._text = new_text

    ##################################################
    # CLEAR MESSAGE
    ##################################################
    def clear(self):
        self._text = "Empty"
        self._author = ""
        self._date = ""
        self._empty = True