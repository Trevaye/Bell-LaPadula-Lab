########################################################################
# COMPONENT:
#    CONTROL
# Author:
#    Br. Helfrich, Kyle Mueller, <your name here if you made a change>
# Summary: 
#    This class stores the notion of Bell-LaPadula
########################################################################

# ---------------------------------------------------------
# SECURITY LEVEL ENUM
# ---------------------------------------------------------
class SecurityLevel:
    PUBLIC = 0
    CONFIDENTIAL = 1
    PRIVILEGED = 2
    SECRET = 3


# ---------------------------------------------------------
# USER SECURITY CLEARANCE POLICY
# ---------------------------------------------------------
USER_CLEARANCE = {
    "AdmiralAbe": SecurityLevel.SECRET,
    "CaptainCharlie": SecurityLevel.PRIVILEGED,
    "SeamanSam": SecurityLevel.CONFIDENTIAL,
    "SeamanSue": SecurityLevel.CONFIDENTIAL,
    "SeamanSly": SecurityLevel.CONFIDENTIAL
}

# Unknown users default to PUBLIC level
DEFAULT_CLEARANCE = SecurityLevel.PUBLIC


# ---------------------------------------------------------
# AUTHENTICATE USER (return their clearance)
# ---------------------------------------------------------
def authenticate(username):
    """
    Return the SecurityLevel for the given user.
    Unknown users get PUBLIC clearance.
    """
    return USER_CLEARANCE.get(username, DEFAULT_CLEARANCE)


# ---------------------------------------------------------
# BELL–LAPADULA SIMPLE SECURITY RULE (NO READ UP)
# subject_level >= object_level
# ---------------------------------------------------------
def can_read(user_level, object_level):
    """
    No Read Up:
    A user may READ an object only if their clearance
    is >= the object’s security level.
    """
    return user_level >= object_level


# ---------------------------------------------------------
# BELL–LAPADULA *-PROPERTY (NO WRITE DOWN)
# subject_level <= object_level
# ---------------------------------------------------------
def can_write(user_level, object_level):
    """
    No Write Down:
    A user may WRITE to an object only if their clearance
    is <= the object’s security level.
    """
    return user_level <= object_level