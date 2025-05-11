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
        "Keep the response friendly and natural by acting as a smart and clever assistant, similar to Jarvis from Iron Man. Be concise and efficient."
    )

    @classmethod
    def format_good_morning_text(cls, internal_information: str,  text_device_information: str) -> str:
        """
        Formats a good morning message with device information.

        Args:
            internal_information (str): Contextual information for internal use only.
            text_device_information (str): Information about the device.

        Returns:
            str: The formatted good morning message.
        """
        return cls.format_message(cls.MEETING_DESCRIPTION, internal_information, text_device_information)

class WelcomeChat(BaseChat):
    MEETING_DESCRIPTION = (
        "Someone has just arrived at home. Please generate a friendly and concise spoken greeting in Spanish for the arriving person or people."
        "Please analyze the time of the system and respond with a personalized greeting"
        "Please read the calendar and remind them of events if necessary. Include the names of the people arriving and any relevant device information."
    )

    @classmethod
    def format_welcome_text(cls, people_arriving_names: list[str], internal_information: str, important_information: str) -> str:
        """
        Formats a welcome message for people arriving.

        Args:
            people_arriving_names (list[str]): Names of people arriving.
            internal_information (str): Contextual information for internal use only.
            important_information (str): Important information about the device.

        Returns:
            str: The formatted welcome message.
        """
        people_names = cls.format_names(people_arriving_names)
        internal_information_complete = f"- The following person or people have just entered the house and should be greeted: {people_names}"
        internal_information_complete += f"{internal_information}"
        return cls.format_message(cls.MEETING_DESCRIPTION, internal_information_complete, important_information)

class WelcomeGuestChat(BaseChat):
    MEETING_DESCRIPTION = (
        "A guest has entered the house. Let them know that you have already notify the owners and that everything is being recorded. "
        "If the owners are at home, include their names in the response. Be concise and respectful, as Jarvis from Iron Man would."
    )

    @classmethod
    def format_welcome_text(cls, owners_at_home: list[str]) -> str:
        """
        Formats a welcome message for a guest entering the house.

        Args:
            owners_at_home (list[str]): Names of owners currently at home.

        Returns:
            str: The formatted welcome message.
        """
        if not owners_at_home:
            internal_information = "No owners are currently at home."
        else:
            owners_text = cls.format_names(owners_at_home)
            internal_information = f"The following owners are currently at home: {owners_text}."
        return cls.format_message(cls.MEETING_DESCRIPTION, internal_information, "")

class FeedCatsReminder(BaseChat):
    MEETING_DESCRIPTION = (
        "It's time to feed the cats. Generate a short custom reminder for Tammy to feed the cats."
    )

    @classmethod
    def message(cls) -> str:
        """
        Generates a reminder message to feed the cats.

        Returns:
            str: The formatted reminder message.
        """
        now = datetime.now()
        actual_time_string = now.strftime("Current system time: %A %b %d, %Y at %I:%M%p")
        internal_information = f"The current system time is {actual_time_string}."
        return cls.format_message(cls.MEETING_DESCRIPTION, internal_information, "")

class MaidAnnouncements(BaseChat):
    MEETING_DESCRIPTION = (
        "Heydi has arrived to help with the cleaning. She helps with certain household tasks. Greet her respectfully and provide her with the necessary information."
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
        internal_information = "Heydi has arrived to assist with household tasks."
        return cls.format_message(cls.MEETING_DESCRIPTION, internal_information, maid_information)
