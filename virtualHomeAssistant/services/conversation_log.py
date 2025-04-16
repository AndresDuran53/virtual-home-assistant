from datetime import datetime, timedelta

class ConversationEntry:
    timestamp: datetime
    role: str
    content: str
    def __init__(self, role, content):
        self.timestamp = datetime.now()
        self.role = role
        self.content = content

class ConversationLog:
    def __init__(self):
        self.daily_logs = {}

    def new_message(self, role: str, content: str):
        today = datetime.now().strftime("%Y-%m-%d")
        new_entry = ConversationEntry(role, content)
        self.add_entry(today, new_entry)

    def add_entry(self, day: str, entry: ConversationEntry):
        if day not in self.daily_logs:
            self.daily_logs[day] = []
        self.daily_logs[day].append(entry)

    def get_entries_as_dicts(self, day=None):
        if day is None:
            day = datetime.now().strftime("%Y-%m-%d")
        if day not in self.daily_logs:
            return []
        entry_dicts = []
        for entry in self.daily_logs[day]:
            entry_dict = {"role": entry.role, "content": entry.content}
            entry_dicts.append(entry_dict)
        return entry_dicts

if __name__ == "__main__":
    log = ConversationLog()
    log.new_message("User", "New message for today")
    print(log.get_entries_as_dicts())