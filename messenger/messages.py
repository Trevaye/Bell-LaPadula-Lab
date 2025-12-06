########################################################################
# COMPONENT:
#    MESSAGES
# Author:
#    Br. Helfrich, Kyle Mueller, Trevaye Morris
# Summary: 
#    This class stores the notion of a collection of messages
########################################################################

from __future__ import annotations
import os
from typing import List, Optional

from .control import SecurityLevel, Subject, can_write, level_to_string
from .message import Message


class Messages:
    """
    A collection of Message objects. This is the resource
    Bell-LaPadula is protecting.
    """

    def __init__(self, filename: str = "messages.txt") -> None:
        # Always load from the messenger folder
        package_dir = os.path.dirname(os.path.abspath(__file__))
        self._filename = os.path.join(package_dir, filename)

        self._messages: List[Message] = []
        self.load()

    # ----------------------- File I/O ---------------------------------

    def load(self) -> None:
        """
        Load messages from messages.txt.
        Supports both formats: 5 fields or 4 fields.
        Auto-assigns proper sequential IDs.
        """
        self._messages.clear()

        if not os.path.exists(self._filename):
            print("messages.txt NOT FOUND at:", self._filename)
            return

        print("Loading messages from:", self._filename)

        loaded = []
        with open(self._filename, "r", encoding="utf-8") as f:
            for line in f:
                m = Message.from_line(line)
                if m is not None:
                    loaded.append(m)

        # Assign IDs correctly (sequential, starting at 1)
        next_id = 1
        for m in loaded:
            m.msg_id = next_id
            next_id += 1

        self._messages = loaded

    def save(self) -> None:
        """
        Save messages back to messages.txt
        """
        with open(self._filename, "w", encoding="utf-8") as f:
            for m in self._messages:
                f.write(m.to_line() + "\n")

    # ----------------------- Helpers ----------------------------------

    def _find_by_id(self, msg_id: int) -> Optional[Message]:
        for m in self._messages:
            if m.msg_id == msg_id:
                return m
        return None

    # ----------------------- Read operations --------------------------

    def list_for(self, subject: Subject) -> list[Message]:
        """
        Return messages visible to the subject.
        """
        return [m for m in self._messages if m.may_read(subject)]

    def get_for(self, subject: Subject, msg_id: int) -> Optional[Message]:
        """
        Return one message only if subject can read it.
        """
        m = self._find_by_id(msg_id)
        if m is None or not m.may_read(subject):
            return None
        return m

    # ----------------------- Write operations -------------------------

    def add_message(self, subject: Subject, text: str,
                    level: SecurityLevel | None = None) -> Message | None:
        """
        Create a new message.
        New messages always get the next ID.
        """

        if level is None:
            level = subject.level

        if not can_write(subject, level):
            return None

        new_id = len(self._messages) + 1
        timestamp = Message.now_timestamp()

        new_msg = Message(
            msg_id=new_id,
            author=subject.username,
            text=text,
            timestamp=timestamp,
            level=level
        )

        self._messages.append(new_msg)
        self.save()
        return new_msg

    def update_message(self, subject: Subject, msg_id: int, new_text: str) -> bool:
        """
        Modify an existing message.
        """
        m = self._find_by_id(msg_id)
        if m is None:
            return False

        if not m.may_write(subject):
            return False

        m.text = new_text
        self.save()
        return True

    def clear_messages_at_level(self, subject: Subject,
                                level: SecurityLevel) -> int:
        """
        Clear messages if BLP allows.
        """
        if not can_write(subject, level):
            return 0

        count = 0
        for m in self._messages:
            if m.level == level and m.may_write(subject):
                m.text = ""
                count += 1

        if count:
            self.save()

        return count