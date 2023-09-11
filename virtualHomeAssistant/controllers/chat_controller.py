from datetime import datetime

class WelcomeChat():
    intro = "please analyze the time of my systems and response with a personalized greeting, as Jarvis from Iron Man would but be concise and short on your answer. You can give them advice, but don't forget to notify about the upcoming events:"

    @classmethod
    def format_welcome_text(cls,people_arriving,devices_information):       
        people_meeting_text = cls.get_arriving_format(people_arriving)
        text_device_information = cls.text_from_list(devices_information)
        intro_with_names = cls.people_intro(people_arriving)
        final_text = f"{intro_with_names}{people_meeting_text}\n{text_device_information}"
        return final_text
    
    @classmethod
    def people_intro(cls,people_arriving):
        names = [person.name for person in people_arriving]
        if len(names) == 1:
            return f"Hello Assistant, {names[0]} just arrived home, "+cls.intro
        else:
            all_names = ', '.join(names[:-1]) + ' and ' + names[-1]
            return f"Hello Assistant, {all_names} just arrived home, "+cls.intro
    
    @classmethod
    def get_arriving_format(cls,people_arriving):
        final_text = "\nPeople you should greet:"
        for person in people_arriving:
            final_text += f"\n- {person.name}"
        return final_text
    
    @classmethod
    def text_from_list(cls,status_list):
        now = datetime.now() 
        actual_time_string = now.strftime("Current system time: %A %b %d, %Y at %I:%M%p")
        text = f"\n- {actual_time_string}"
        for element in status_list:
            if(element.to_text() != ""):
                text+=f"\n"
                text += f"- {element.to_text()}"
        return text
    

class WelcomeGuestChat():
    @classmethod
    def format_welcome_text(cls,owners_at_home):
        if(len(owners_at_home)>0):
            text = "Hello Assistant, "
            if(len(owners_at_home)==1):
                text += f"I'm {owners_at_home[0].name}, and a guest has come to my house parking a car in my garage, I need you to notify me about it"
            else:
                text += f"We are {owners_at_home[0].name} and {owners_at_home[1].name}, we are at home and a guest has come to our house parking a car in our garage, we need you to notify us about it"
            text += " in a kind and respectful way, as Jarvis from Iron Man would do it but be concise and short on your answer."
            return text
        else:
            return cls.intro

    
class GoodMorningChat():
    meeting_description = "We are waking up, please give us a personalized greeting and tell us the time as Jarvis from Iron Man would but be concise and short on your answer, without repeating the information I give you. Remember that you must always answer me in Spanish."
    @classmethod
    def format_good_morning_text(cls,devices_information):
        text_device_information = cls.text_from_list(devices_information)
        final_text = f"{cls.meeting_description}\n{text_device_information}"
        return final_text
    
    @classmethod
    def text_from_list(cls,status_list):
        now = datetime.now() 
        actual_time_string = now.strftime("Current system time: %A %b %d, %Y at %I:%M%p")
        text = f"- {actual_time_string}"
        for element in status_list:
            if(element.to_text() != ""):
                if(text!=""):text+=f"\n"
                text += f"- {element.to_text()}"
        return text
    
class FeedCatsReminder():
    message_default = "Now it's time to feed the cats, respond with a friendly warning message reminding Tammy that it's time to feed the cats."

    @classmethod
    def message(cls):
        now = datetime.now() 
        actual_time_string = now.strftime("Current system time: %A %b %d, %Y at %I:%M%p")
        final_text = f"- {actual_time_string} \n -{cls.message_default}"
        return final_text
