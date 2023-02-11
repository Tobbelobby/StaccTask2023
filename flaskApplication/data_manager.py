import json

class DataManager:
    def __init__(self, filename):
        self.filename = filename
    
    def read_data(self):
        with open(self.filename, 'r') as file:
            db = json.load(file)
        return db
    
    def write_data(self, db):
        with open(self.filename, 'w') as file:
            json.dump(db, file)