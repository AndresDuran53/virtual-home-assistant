from dto.homeassistant.person import Person

class PeopleManager():
    people_list: list[Person]

    def __init__(self,people_list):
        self.people_list = people_list

    def add_person(self,person: Person):
        self.people_list.append(person)
    
    def get_names(self) -> list[str]:
        return [person.name for person in self.people_list]
    
    def get_people_just_get_home(self) -> list[Person]:
        return [person for person in self.people_list if person.just_get_home()]

    def get_people_already_home(self) -> list[Person]:
        return [person for person in self.people_list if person.is_home() and not person.just_get_home()]

    def get_people_not_home(self) -> list[Person]:
        return [person for person in self.people_list if not person.is_home()]
        
    def arriving_to_text(self):
        if len(self.people_list) == 0:
            return ""
        people_arriving = self.get_people_just_get_home()
        all_names = ','.join(person.name for person in people_arriving)
        final_text = f"People arriving at the house: [{all_names}]"
        return final_text

    def already_home_to_text(self):
        if len(self.people_list) == 0:
            return ""
        people_already_home = self.get_people_already_home()
        all_names = ','.join(person.name for person in people_already_home)
        final_text = f"People already in the house from before: [{all_names}]"
        return final_text

    def not_home_to_text(self):
        if len(self.people_list) == 0:
            return ""
        people_not_home = self.get_people_not_home()
        all_names = ','.join(person.name for person in people_not_home)
        final_text = f"People who are not at home: [{all_names}]"
        return final_text

    def all_to_text(self):
        final_text = f"{self.already_home_to_text()}\n"
        final_text += f"{self.arriving_to_text()}\n"
        final_text += f"{self.not_home_to_text()}\n"
        return final_text