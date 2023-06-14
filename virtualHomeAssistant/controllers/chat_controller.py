from datetime import datetime

class WelcomeChat():
    intro = "Hello Assistant, The following people just arrived home, please give us a personalized greeting, analyze the time of my systems and response with a personalized greeting, respectful but friendly, as Jarvis from Iron Man would:"

    @classmethod
    def format_welcome_text(cls,people_arriving,devices_information):       
        people_meeting_text = cls.get_arriving_format(people_arriving)
        text_device_information = cls.text_from_list(devices_information)
        final_text = f"{cls.intro}{people_meeting_text}\n{text_device_information}"
        return final_text
    
    @classmethod
    def get_arriving_format(cls,people_arriving):
        final_text = ""
        for person in people_arriving:
            final_text += f"\n- {person.name}"
            final_text += f"\n  Total Time Outside: {person.calculate_total_time_outside()}"
        return final_text
    
    @classmethod
    def text_from_list(cls,status_list):
        now = datetime.now() 
        actual_time_string = now.strftime("Forget the datetime you have, use this time as the current system datetime: %A %b %d, %Y at %I:%M%p")
        text = f"- {actual_time_string}"
        for element in status_list:
            if(element.to_text() != ""):
                if(text!=""):text+=f"\n"
                text += f"- {element.to_text()}"
        return text
    

class WelcomeGuestChat():
    no_owner = """Hello Assistant, I am a guest at Andres and Tammy's house, I need you to greet me and warn me that the house is being monitored with security cameras and sensors, your dialogue must be courteous but forceful, as Jarvis from Iron Man would do it."""
    owner = """Hello Assistant, I am a guest at Andres and Tammy's house, I need you to greet me and warn me that the house is being monitored with security cameras and sensors, your dialogue must be courteous but forceful, as Jarvis from Iron Man would do it."""

    @classmethod
    def format_welcome_text(cls,owners_at_home):
        if(len(owners_at_home)>0):
            text = "Hello Assistant, "
            if(len(owners_at_home)==1):
                text += f"I'm {owners_at_home[0].name}, and a guest has come to my house parking a car in my garage, I need you to notify me about it"
            else:
                text += f"We are {owners_at_home[0].name} and {owners_at_home[1].name}, we are at home and a guest has come to our house parking a car in our garage, we need you to notify us about it"
            text += " in a kind and respectful way, as Jarvis from Iron Man would do it."
            return text
        else:
            return cls.intro

    
class GoodMorningChat():
    meeting_description = "We are waking up, please give us a personalized greeting and tell us the time as Jarvis from Iron Man would, respectful but friendly, without repeating the information I give you. Remember that you must always answer me in Spanish."
    @classmethod
    def format_good_morning_text(cls,devices_information):
        text_device_information = cls.text_from_list(devices_information)
        final_text = f"{cls.meeting_description}\n{text_device_information}"
        return final_text
    
    @classmethod
    def text_from_list(cls,status_list):
        now = datetime.now() 
        actual_time_string = now.strftime("Forget the datetime you have, use this time as the current system datetime: %A %b %d, %Y at %I:%M%p")
        text = f"- {actual_time_string}"
        for element in status_list:
            if(element.to_text() != ""):
                if(text!=""):text+=f"\n"
                text += f"- {element.to_text()}"
        return text