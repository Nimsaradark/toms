from ._data import get_database

db_connected = False
user_db = None

class UserDB:
    def users_db(self):
        global db_connected
        global user_db
        if db_connected:return user_db
        db = get_database()
        db_connected = True
        user_db = db["users"]
        return user_db

    def __init__(self):
        self.user_db = self.users_db()

    def is_served_user(self,user_id: int) -> bool:
        user = self.user_db.find_one({"_id": user_id})
        if not user:
            return False
        return True

    def count_users(self) -> int:
        return self.user_db.count_documents({})

    def get_served_users(self) -> list:
        users = self.user_db.find({"_id": {"$gt": 0}})
        if not users:
            return []
        users_list = []
        for user in users:
            user = user.get("_id")
            users_list.append(user)
        return users_list

    def add_served_user(self,user_id: int):
        is_served = self.is_served_user(user_id)
        if is_served:
            return
        return  self.user_db.insert_one({"_id": user_id})

    def remove_served_user(self,user_id: int):
        is_served = self.is_served_user(user_id)
        if is_served:
            return
        return  self.user_db.delete_one({"_id": user_id})
    
    



def check_user_db(func):
    async def wrapper(update, context):
        user_id = update.effective_user.id
        UserDB().add_served_user(user_id)
        await func(update,context)
    return wrapper