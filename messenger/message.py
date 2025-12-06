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
# One message to be displayed or modified
##################################################

from dataclasses import dataclass
from datetime import datetime
from .control import SecurityLevel, Subject, can_read, can_write, parse_level, level_to_string


@dataclass
class Message:
    msg_id: int
    author: str
    text: str
    timestamp: str
    level: SecurityLevel

    # ------------- Bell-LaPadula checks ------------------------------

    def may_read(self, subject: Subject) -> bool:
        return can_read(subject, self.level)

    def may_write(self, subject: Subject) -> bool:
        return can_write(subject, self.level)

    # ------------- Display & storage ---------------------------------

    def short_header(self) -> str:
        return f"[{self.msg_id:03d}] ({level_to_string(self.level)}) {self.author} @ {self.timestamp}"

    def to_line(self) -> str:
        safe = self.text.replace("\n", "\\n")
        return f"{self.msg_id}|{self.author}|{self.timestamp}|{level_to_string(self.level)}|{safe}"

    # ------------- LOADING (supports both formats) -------------------

    @staticmethod
    def from_line(line: str):
        """
        Supports:
        1) id|author|timestamp|level|text
        2) level|author|timestamp|text
        """
        line = line.strip()
        if not line:
            return None

        parts = line.split("|")

        # ---------- FORMAT A: id|author|timestamp|level|text ----------
        if len(parts) == 5:
            try:
                msg_id = int(parts[0])
            except ValueError:
                return None

            author = parts[1]
            timestamp = parts[2]
            level = parse_level(parts[3])
            text = parts[4].replace("\\n", "\n")

            return Message(msg_id, author, text, timestamp, level)

        # ---------- FORMAT B: level|author|timestamp|text -------------
        elif len(parts) == 4:
            level = parse_level(parts[0])
            author = parts[1]
            timestamp = parts[2]
            text = parts[3].replace("\\n", "\n")

            # ID will be assigned later by Messages.load()
            return Message(-1, author, text, timestamp, level)

        else:
            return None

    @staticmethod
    def now_timestamp() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M")
