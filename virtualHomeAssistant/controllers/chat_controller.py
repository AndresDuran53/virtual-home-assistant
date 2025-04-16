from datetime import datetime

class BaseChat:

    @staticmethod
    def format_message(prompt: str, internal_information: str, important_information) -> str:
        """
        Formats a message to be sent to the assistant, dividing it into three distinct sections:

        Args:
            prompt (str): Instructions for the assistant to follow.
            internal_information (str): Contextual information for internal use only.
            important_information (str): Information to be shared directly with the user.

        Returns:
            str: A formatted message combining the three sections in a structured way.
        """

        sections = [f"[Automatic system notification]\n--- Instructions ---\n{prompt}\n"]

        if internal_information:
            sections.append(f"--- Internal Information (for assistant's context only) ---\n{internal_information}\n")
        
        if important_information:
            sections.append(f"--- Important Information (to share with the user) ---\n{important_information}\n")

        return "\n".join(sections).strip()

    @staticmethod
    def format_names(names: list[str]) -> str:
        """
        Formats a list of names into a readable string.

        Args:
            names (list[str]): List of names.

        Returns:
            str: Formatted names.
        """
        if len(names) == 1:
            return names[0]
        return ', '.join(names[:-1]) + ' and ' + names[-1]

class GoodMorningChat(BaseChat):
    MEETING_DESCRIPTION = (
        "Please generate a personalized greeting for Andrés and Tammy in Spanish. "
        "They are just waking up. Analyze the system time and greet accordingly. Include any relevant events or tasks for the day. "
        "Keep the response friendly and natural by acting as our smart and clever butler, as Jarvis from Iron Man would. Don't hold back from making smart and clever comments with the information provided below, "
        "but be quick and concise when doing so."
    )

    @classmethod
    def format_good_morning_text(cls, internal_information: str,  text_device_information: str) -> str:
        """
        Formats a good morning message with device information.

        Args:
            text_device_information (str): Information about the device.

        Returns:
            str: The formatted good morning message.
        """
        return cls.format_message(cls.MEETING_DESCRIPTION, internal_information, text_device_information)

class WelcomeChat(BaseChat):
    MEETING_DESCRIPTION = (
        "Please analyze the time of the systems and respond with a personalized greeting, as Jarvis from Iron Man would. "
        "Please read the calendar and remind them of events if necessary. Include the names of the people arriving and any relevant device information."
    )

    @classmethod
    def format_welcome_text(cls, people_arriving_names: list[str], text_device_information: str) -> str:
        """
        Formats a welcome message for people arriving.

        Args:
            people_arriving_names (list[str]): Names of people arriving.
            text_device_information (str): Information about the device.

        Returns:
            str: The formatted welcome message.
        """
        people_names = cls.format_names(people_arriving_names)
        internal_information = f"Arriving People you should greet: {people_names}"
        return cls.format_message(cls.MEETING_DESCRIPTION, internal_information, text_device_information)

class WelcomeGuestChat(BaseChat):
    INTRO = "[Automatic system notification] A guest has entered the house. Let them know that you have already notified me and that everything is being recorded."

    @classmethod
    def format_welcome_text(cls, owners_at_home: list[str]) -> str:
        if not owners_at_home:
            return cls.INTRO
        owners_text = cls.format_owners(owners_at_home)
        return (
            f"Hello Assistant, {owners_text}, and a guest has come to our house parking a car in our garage. "
            "We need you to notify us about it in a kind and respectful way, as Jarvis from Iron Man would do it, "
            "but be concise and short in your answer."
        )

    @staticmethod
    def format_owners(owners: list[str]) -> str:
        if len(owners) == 1:
            return f"I'm {owners[0]}"
        return f"We are {owners[0]} and {owners[1]}"

class FeedCatsReminder(BaseChat):
    MESSAGE_DEFAULT = "[Automatic system notification] Now it's time to feed the cats. Respond with a short custom reminder for Tammy that it's time to feed the cats."

    @classmethod
    def message(cls) -> str:
        """
        Generates a reminder message to feed the cats.

        Returns:
            str: The formatted reminder message.
        """
        now = datetime.now()
        actual_time_string = now.strftime("Current system time: %A %b %d, %Y at %I:%M%p")
        return f"{actual_time_string}\n{cls.MESSAGE_DEFAULT}"


class MaidAnnouncements(BaseChat):
    INTRO = (
        "[Automatic system notification] Heydi has arrived to help us with the cleaning. She helps with certain household tasks. "
        "You must reply with a greeting to her first. Be very careful and respectful in the way you speak to her. Tell her the following information:"
    )

    @classmethod
    def format_information(cls, maid_information: str) -> str:
        """
        Formats a message with information for the maid.

        Args:
            maid_information (str): Information to provide to the maid.

        Returns:
            str: The formatted message.
        """
        return f"{cls.INTRO}\n{maid_information}"
