from datetime import datetime,timedelta

class ConversationLog:
    def __init__(self):
        self.entries = []

    def new_message(self,role,content):
        new_entry = ConversationEntry(role, content)
        self.add_entry(new_entry)

    def add_entry(self, entry):
        self.filter_entries()
        self.entries.append(entry)

    def filter_entries(self):
        today = datetime.now().date()
        self.entries = [entry for entry in self.entries if entry.timestamp.date() == today]

    def get_entries_as_dicts(self):
        entry_dicts = []
        for entry in self.entries:
            entry_dict = {"role": entry.role, "content": entry.content}
            entry_dicts.append(entry_dict)
        return entry_dicts


class ConversationEntry:
    timestamp: datetime
    role: str
    content: str
    def __init__(self, role, content):
        self.timestamp = datetime.now()
        self.role = role
        self.content = content


if __name__ == "__main__":
    log = ConversationLog()
    entry = log.new_message("User", "New message for today")
    print(log.get_entries_as_dicts())