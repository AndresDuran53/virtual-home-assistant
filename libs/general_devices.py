class GeneralDevice():
    def __init__(self,entity_id,name,state=None,ignoring_states=[]):
        self.entity_id = entity_id
        self.name = name
        self.state = state
        self.ignoring_states = ignoring_states

    def set_state(self,state):
        self.state = state

    def needs_to_be_ignore(self):
        if(self.state in self.ignoring_states): return True
        return False

    def to_text(self):
        name = self.name
        if(self.state): state = self.state
        else: state = "Unknow"
        if(self.state == "idle"): state ="non-operational"
        return(f"{name}: {state}")
    
    @classmethod
    def exclude_non_important_from_list(cls,list_general_device):
        result_list = []
        for general_device in list_general_device:
            if(not general_device.needs_to_be_ignore()):
                result_list.append(general_device)
        return result_list