########################################################################
# COMPONENT:
#    CONTROL
# Author:
#    Br. Helfrich, Kyle Mueller, Trevaye Morris
# Summary: 
#    This class stores the notion of Bell-LaPadula
########################################################################

from enum import IntEnum
from dataclasses import dataclass


class SecurityLevel(IntEnum):
    PUBLIC = 0
    CONFIDENTIAL = 1
    PRIVILEGED = 2
    SECRET = 3


# ---- User policy (who has what clearance) -----------------------------

USER_CLEARANCE = {
    "AdmiralAbe": SecurityLevel.SECRET,
    "CaptainCharlie": SecurityLevel.PRIVILEGED,
    "SeamanSam": SecurityLevel.CONFIDENTIAL,
    "SeamanSue": SecurityLevel.CONFIDENTIAL,
    "SeamanSly": SecurityLevel.CONFIDENTIAL,
    # anyone else will default to PUBLIC
}


@dataclass(frozen=True)
class Subject:
    """
    Represents a Bell-LaPadula subject (a logged-in user).
    """
    username: str
    level: SecurityLevel


# ---- Policy helpers ---------------------------------------------------

def authenticate(username: str, password: str) -> Subject | None:
    """
    Authentication function for Bell-LaPadula.

    - Password must be 'password' (per assignment).
    - Username determines security level based on USER_CLEARANCE.
    - Unknown usernames get PUBLIC clearance.
    """
    if password != "password":
        return None

    level = USER_CLEARANCE.get(username, SecurityLevel.PUBLIC)
    return Subject(username=username, level=level)


def dominates(level_high: SecurityLevel, level_low: SecurityLevel) -> bool:
    """
    True if level_high >= level_low in the Bell-LaPadula lattice.
    """
    return int(level_high) >= int(level_low)


# ---- Bell-LaPadula access rules --------------------------------------

def can_read(subject: Subject, object_level: SecurityLevel) -> bool:
    """
    Bell-LaPadula simple-security property (no read up):

        subject.level >= object.level
    """
    return dominates(subject.level, object_level)


def can_write(subject: Subject, object_level: SecurityLevel) -> bool:
    """
    Bell-LaPadula *-property (no write down):

        object.level >= subject.level
    """
    return dominates(object_level, subject.level)


# ---- Utility: convert level <-> string --------------------------------

_LEVEL_NAMES = {
    "public": SecurityLevel.PUBLIC,
    "confidential": SecurityLevel.CONFIDENTIAL,
    "privileged": SecurityLevel.PRIVILEGED,
    "secret": SecurityLevel.SECRET,
}


def parse_level(text: str) -> SecurityLevel:
    """
    Convert a string from the file/user input to a SecurityLevel.
    Defaults to PUBLIC if unrecognized.
    """
    if not text:
        return SecurityLevel.PUBLIC
    key = text.strip().lower()
    return _LEVEL_NAMES.get(key, SecurityLevel.PUBLIC)


def level_to_string(level: SecurityLevel) -> str:
    """
    Convert SecurityLevel to a nice string for output / file.
    """
    for name, val in _LEVEL_NAMES.items():
        if val == level:
            return name.capitalize()
    return "Public"
