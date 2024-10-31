from ._data import get_database
from Classes import TVData


db_connected = False
tv_db = None

class TvDB:
    def tvs_db(self):
        global db_connected
        global tv_db
        if db_connected:return tv_db
        db = get_database()
        db_connected = True
        tv_db = db["tv_shows"]
        return tv_db
    
    def __init__(self):
        self.__dict__.clear()
        self.tv_db = self.tvs_db()

    def is_saved_tv_show(self,id: int) -> bool:
        id = int(str(id).replace('-100',''))
        saved = self.tv_db.find_one({"_id" : id})
        print(saved)
        if not saved:return False
        return True

    def count_tv_shows(self) -> int:
        return self.tv_db.count_documents({})

    def add_tv_show(self,chat_id: int,title : str, link: str):
        id = int(str(chat_id).replace('-100',''))
        data = {"_id": id, "title": title , "link": link}
        save = self.is_saved_tv_show(id)
        if save:return
        return tv_db.insert_one(data)

    def remove_tv_show(self,chat_id: int):
        id = int(str(chat_id).replace('-100',''))
        save =  self.is_saved_tv_show(chat_id)

        if save:
            return tv_db.delete_one({"_id": id})

    def search_tv_shows(self,title: str) -> list[TVData]:
        title = title.lower()
        regex_pattern = ".*" + ".*".join(title.split()) + ".*"
        tv_show = list(tv_db.find({"title": {"$regex": regex_pattern, "$options": "i"}}))
        if tv_show != []:
            tv_show =  sorted(tv_show, key=lambda x: x['title'])
            return [TVData(title=tv['title'],id=tv['_id'],link=None) for tv in tv_show]

    def get_tv_show(self,id: int):
        tv_show = tv_db.find_one({"_id": id})
        return TVData(title=tv_show['title'],id=None,link=tv_show['link'])
