from datetime import datetime

class WelcomeChat():
    intro = "please analyze the time of my systems and response with a personalized greeting, as Jarvis from Iron Man would, please read the calendar and remind us of events if necessary:"

    @classmethod
    def format_welcome_text(cls, people_arriving_names: list[str], text_device_information: str):       
        people_meeting_text = cls.get_arriving_format(people_arriving_names)
        intro_with_names = cls.people_intro(people_arriving_names)
        final_text = f"{intro_with_names}{people_meeting_text}\n{text_device_information}"
        return final_text
    
    @classmethod
    def people_intro(cls, people_arriving_names: list[str]):
        if len(people_arriving_names) == 1:
            return f"[Automatic system notification] Hello Assistant, {people_arriving_names[0]} just arrived home, "+cls.intro
        else:
            all_names = ', '.join(people_arriving_names[:-1]) + ' and ' + people_arriving_names[-1]
            return f"[Automatic system notification] Hello Assistant, {all_names} just arrived home, "+cls.intro
    
    @classmethod
    def get_arriving_format(cls, people_arriving_names: list[str]):
        final_text = "\nPeople you should greet:"
        for person_name in people_arriving_names:
            final_text += f"\n- {person_name}"
        return final_text
    

class WelcomeGuestChat():
    intro = "[Automatic system notification] A guest has enter the house, let them know that you already notify me and that everything is being recorder."

    @classmethod
    def format_welcome_text(cls, owners_at_home: list[str]):
        if(len(owners_at_home)>0):
            text = "Hello Assistant, "
            if(len(owners_at_home)==1):
                text += f"I'm {owners_at_home[0]}, and a guest has come to my house parking a car in my garage, I need you to notify me about it"
            else:
                text += f"We are {owners_at_home[0]} and {owners_at_home[1]}, we are at home and a guest has come to our house parking a car in our garage, we need you to notify us about it"
            text += " in a kind and respectful way, as Jarvis from Iron Man would do it but be concise and short on your answer."
            return text
        else:
            return cls.intro

    
class GoodMorningChat():
    meeting_description = "[Automatic system notification] Instruction to assistant: Please generate a personalized greeting for Andrés and Tammy in Spanish, they are just waking up, analyzes the system time and greets accordingly. Include the current time, temperature, and any relevant events or tasks on the day. Keep the response friendly and natural by acting as our smart and clever butler, so don't hold back from making smart and sarcastic comments with the information provided below, but be quick and concise when doing them."
    @classmethod
    def format_good_morning_text(cls, text_device_information: str):
        final_text = f"{cls.meeting_description}\n{text_device_information}"
        return final_text

    
class FeedCatsReminder():
    message_default = "[Automatic system notification] Now it's time to feed the cats, respond with a short custom reminder for Tammy that it's time to feed the cats."

    @classmethod
    def message(cls):
        now = datetime.now() 
        actual_time_string = now.strftime("Current system time: %A %b %d, %Y at %I:%M%p")
        final_text = f"- {actual_time_string} \n -{cls.message_default}"
        return final_text
