########################################################################
# COMPONENT:
#    INTERACT
# Author:
#    Br. Helfrich, Kyle Mueller, Trevaye Morris
# Summary: 
#    This class allows one user to interact with the system
########################################################################

from __future__ import annotations

from .control import (
    Subject,
    SecurityLevel,
    authenticate,
    level_to_string,
)
from .messages import Messages


class Interact:
    """
    Provides a simple text-based UI for the messaging system.
    """

    def __init__(self) -> None:
        self._subject: Subject | None = None
        self._messages = Messages()

    # -------------------- Top-level control ---------------------------

    def run(self) -> None:
        self._login()
        self._loop()

    # -------------------- Authentication ------------------------------

    def _login(self) -> None:
        """
        Prompt until we get a valid Bell-LaPadula subject.
        """
        print("=== WWII Message System (Bell-LaPadula Protected) ===")
        print("All users share the same password: 'password'")
        print()

        while self._subject is None:
            username = input("User name: ").strip()
            password = input("Password: ").strip()

            subject = authenticate(username, password)
            if subject is None:
                print("Invalid credentials. Try again.\n")
            else:
                self._subject = subject
                print(
                    f"\nWelcome, {subject.username} "
                    f"[{level_to_string(subject.level)} clearance]\n"
                )

    # -------------------- Main menu loop ------------------------------

    def _loop(self) -> None:
        assert self._subject is not None
        subject = self._subject

        while True:
            print("Menu:")
            print("  L - List messages you can read")
            print("  R - Read a specific message")
            print("  P - Post a new message")
            print("  U - Update an existing message")
            print("  C - Clear messages at a level")
            print("  Q - Quit")
            choice = input("> ").strip().upper()

            if choice == "L":
                self._do_list(subject)
            elif choice == "R":
                self._do_read(subject)
            elif choice == "P":
                self._do_post(subject)
            elif choice == "U":
                self._do_update(subject)
            elif choice == "C":
                self._do_clear(subject)
            elif choice == "Q":
                print("Goodbye.")
                break
            else:
                print("Unknown command.\n")

    # -------------------- Commands ------------------------------------

    def _do_list(self, subject: Subject) -> None:
        msgs = self._messages.list_for(subject)
        if not msgs:
            print("No messages visible at your clearance level.\n")
            return

        print("\nMessages you may READ:")
        for m in msgs:
            print("  " + m.short_header())
        print()

    def _do_read(self, subject: Subject) -> None:
        try:
            msg_id = int(input("Message ID to read: "))
        except ValueError:
            print("Invalid ID.\n")
            return

        m = self._messages.get_for(subject, msg_id)
        if m is None:
            print("You are not allowed to read that message (or it does not exist).\n")
            return

        print("\n" + m.short_header())
        print("-" * 60)
        print(m.text if m.text else "<empty message>")
        print()

    def _do_post(self, subject: Subject) -> None:
        print("Enter message text (end with an empty line):")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)

        text = "\n".join(lines)

        # For this lab, we will default the message level to the subject's
        # own clearance, which is always safe w.r.t Bell-LaPadula *-property.
        m = self._messages.add_message(subject, text, level=subject.level)
        if m is None:
            print("You are not allowed to create a message at that level.\n")
            return

        print(f"Message {m.msg_id} created at level {level_to_string(m.level)}.\n")

    def _do_update(self, subject: Subject) -> None:
        try:
            msg_id = int(input("Message ID to update: "))
        except ValueError:
            print("Invalid ID.\n")
            return

        print("Enter new text (end with an empty line):")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)

        text = "\n".join(lines)

        ok = self._messages.update_message(subject, msg_id, text)
        if not ok:
            print(
                "You are not allowed to modify that message "
                "(Bell-LaPadula *-property).\n"
            )
            return

        print("Message updated.\n")

    def _do_clear(self, subject: Subject) -> None:
        print("Clear messages at which level?")
        print("  0 - Public")
        print("  1 - Confidential")
        print("  2 - Privileged")
        print("  3 - Secret")

        try:
            lvl_num = int(input("Level: "))
            level = SecurityLevel(lvl_num)
        except (ValueError, KeyError):
            print("Invalid level.\n")
            return

        count = self._messages.clear_messages_at_level(subject, level)
        if count == 0:
            print(
                "No messages cleared. Either none existed at that level "
                "or you are not allowed to write at that level.\n"
            )
        else:
            print(f"Cleared {count} messages at {level_to_string(level)}.\n")

