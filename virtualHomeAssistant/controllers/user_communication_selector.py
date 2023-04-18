from dto.person import Person

class UserCommunicationSelector:
    
    @staticmethod
    def get_people_arriving_home(people_information) -> list:
        people_arriving_home = Person.get_people_just_get_home(people_information)
        return people_arriving_home
    
    @staticmethod
    def get_people_at_home(people_information) -> list:
        people_at_home = []
        for person in people_information:
            if(person.state.lower()=="home"): people_at_home.append(person)
        return people_at_home