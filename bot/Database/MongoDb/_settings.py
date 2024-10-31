from ._data import get_database
from Classes import SettingData

db_connected = False
setting_db = None

class SettingDB:
    def settings_db(self):
        global db_connected
        global setting_db
        if db_connected:return setting_db
        db = get_database()
        db_connected = True
        setting_db = db["temp"]
        return setting_db
        
    def __init__(self):
        self.__dict__.clear()
        self.setting_db = self.settings_db()

    def add_setting(self,setting: str,text: str):
        data = {"text": text, "message_status": setting}
        return self.setting_db.insert_one(data)

    def get_setting(self,setting):
        setting =  self.setting_db.find_one({f"message_status": setting})
        if setting:return SettingData(setting=setting['message_status'],status=setting['text'])

    def edit_setting(self,setting: str,status: str):
        return self.setting_db.update_one({"message_status": setting}, {"$set": {"text": status}})
    

# print(SettingDB().get_setting("test"))