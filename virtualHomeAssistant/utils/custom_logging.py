from datetime import datetime

class CustomLogging:
    _instances = {}
    print_debug = True

    def __new__(cls, file_name):
        instance = cls._instances.get(file_name)
        if instance is None:
            instance = super().__new__(cls)
            cls._instances[file_name] = instance
        return instance

    def __init__(self, file_name):
        self.file_name = file_name

    def __repr__(self):
        return f"<CustomLogging file_name={self.file_name}>"

    def debug(self, message):
        self.log('DEBUG', message)

    def info(self, message):
        self.log('INFO', message)

    def warning(self, message):
        self.log('WARNING', message)

    def error(self, message):
        self.log('ERROR', message)

    def log(self, level: str, message: str):
        """
        Logs a message with a specific level.
        """
        timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        final_message = f'[{timestamp}] {level} - {message}\n'
        if(self.print_debug): print(final_message)
        with open(self.file_name, 'a') as file:
            file.write(final_message)