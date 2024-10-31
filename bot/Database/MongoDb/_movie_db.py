import re
from Classes import MovieData
from ._data import get_database

db_connected = False
movie_db = None
unique_db = None 

class MovieDB:
    def movies_db(self):
        global db_connected , movie_db
        if db_connected:return movie_db
        db = get_database()
        db_connected = True
        movie_db = db["movies"]
        return movie_db
        
    def uniquedb(self):
        global db_connected ,  unique_db
        if db_connected:return movie_db
        db = get_database()
        db_connected = True
        unique_db = db["unique"]
        return unique_db

    def __init__(self):
        self.__dict__.clear()
        self.movie_db = self.movies_db()
        self.unique_db = self.uniquedb()
        self.keywords = {
            r"spiderman|spider-man": "spider man",
            r"kgf": "k g f",
        }

    def is_in_saved_movies(self,title: str) -> bool:
        saved_movie = self.movie_db.find_one({"title": title})
        if not saved_movie:return False
        return True

    def is_file_in_saved_movies(self,movie_title: str , category: str,get_details: bool = False) -> dict:
        saved_movie = self.movie_db.find_one({"title": movie_title})
        if not saved_movie:return False
        else:
            data = category.split('-')
            quality = data[0]
            category = '-'.join(data[1:])
            try:
                if quality in saved_movie["quality"] and category in saved_movie["quality"][quality]:
                    if get_details:return saved_movie
                    else:return True
                else:return False
            except:
                return False


    def find_file(self,unique_id):
        save = self.unique_db.find_one({"_id": unique_id})
        if not save:return False
        return save
    
    def add_unique_id(self,unique_id: str , movie_id: int ,message_id: str ,quality: str, exten: str):
        save = self.unique_db.find_one({"_id": unique_id})
        if not save:
            return self.unique_db.insert_one({"_id": unique_id , "movie_id" : movie_id ,  "file_id" : message_id , "quality" : quality , "exten" : exten})

    def update_unique_id(self,unique_id: str , movie_id: int ,message_id: str ,quality: str, exten: str):
        save = self.unique_db.find_one({"_id": unique_id})
        if save:
            return self.unique_db.update_one({"_id": unique_id} , {"$set": {"movie_id" : movie_id ,  "file_id" : message_id , "quality" : quality , "exten" : exten}})

    def delete_unique_id(self,unique_id: str):
        return self.unique_db.delete_one({"_id": unique_id})
        
    def count_movies(self) -> int:
        return self.movie_db.count_documents({})

    def add_title_to_db(self,title : str, message_id: int) -> None:
        title = title.lower()
        data = {"_id":message_id, "title": title}
        is_served = self.is_in_saved_movies(title)
        if is_served:return
        return self.movie_db.insert_one(data)

    def add_movie_to_db(self,message_id: str, title: str, quality: str, file_size , unique_id: str) -> None:
        title = title.lower()
        served = self.movie_db.find_one({"title": title})
        
        if 'p1' in quality or 'p2' in quality or 'p3' in quality or 'p4' in quality or 'p5' in quality:
            quality = quality.replace('-p1','').replace('-p2','').replace('-p3','').replace('-p4','').replace('-p5','')
            if 'quality' in served:
                if quality in served["quality"]:
                    exist_quality,exist_file_size = str(served["quality"][quality]).split("-")
                    file_size = round((int(file_size) + int(exist_file_size)),2)
                    message_id = f"{exist_quality},{message_id}"
        
        data = quality.split('-')
        quality = data[0]
        exten = '-'.join(data[1:])
        
        self.add_unique_id(unique_id=unique_id,movie_id=served['_id'],message_id=message_id,quality=quality,exten=exten)
        return self.movie_db.update_one({"title": title}, {"$set": {f"quality.{quality}.{exten}":  f"{message_id}-{file_size}"}})
    

    def search_movies(self,title: str) -> list[MovieData]:

        def proccess_data(data: list) -> list[MovieData]:return [MovieData(id=movie["_id"],title=movie["title"]) for movie in data]
        def level_01_seach(query: str) -> list:return list(self.movie_db.find({"title": {"$regex": ".*" + ".*".join(query.split()) + ".*", "$options": "i"}}))[0:10]
        
        def level_02_seach(query: str) -> list:
            for pattern, replacement in self.keywords.items():
                regex_pattern = re.sub(pattern, replacement, query, flags=re.IGNORECASE) 
            regex_pattern = ".*" + ".*".join(regex_pattern) + ".*"
            return list(self.movie_db.find({"title": {"$regex": regex_pattern, "$options": "i"}}))[0:10]

        title = title.lower()
        movies = level_01_seach(title)
        if movies == [] : movies = level_02_seach(title)
        if movies:
            movies = movies = sorted(movies, key=lambda x: x['title'])
            return proccess_data(movies)


    def get_movie(self,id: int):
        movie = self.movie_db.find_one({"_id": id})
        return movie

    def edit_movie_title(self,id,title):
        save = self.movie_db.find_one({"_id": id})
        if not save:return False
        else:
            edit = self.movie_db.update_one({"_id": id}, {"$set": {"title": title}})
            return edit

    def edit_quality(self,id: int,file_id: int, current_quality:str, new_quality: str):
        save = self.movie_db.find_one({"_id": id})
        if not save:return False
        file_details = save['quality'][current_quality]
        for key , value in file_details.items():
            extention = key
            data = value
            if int(file_id) == int(value.split('-')[0]):
                self.movie_db.update_one({"_id": id},{"$unset": {f"quality.{current_quality}.{extention}": ""}})
                self.movie_db.update_one({"_id": id},{"$set": {f"quality.{new_quality}.{extention}": f"{data}"}})
                self.movie_db.update_one({"_id": id, f"quality.{current_quality}": {}},{"$unset": {f"quality.{current_quality}": ""}})
                self.movie_db.delete_one({"_id": id, "quality": {}})
                return True
        
    def edit_file_exten(self,id: int, quality: str ,current_file:str, new_file: str):
        save = self.movie_db.find_one({"_id": id})
        if not save:return False
        file_details = save['quality'][quality]
        for key , value in file_details.items():
            extention = key
            data = value
            if current_file == extention:
                self.movie_db.update_one({"_id": id},{"$unset": {f"quality.{quality}.{current_file}": ""}})
                self.movie_db.update_one({"_id": id},{"$set": {f"quality.{quality}.{new_file}": f"{data}"}})
                self.movie_db.update_one({"_id": id, f"quality.{quality}": {}},{"$unset": {f"quality.{quality}": ""}})
                self.movie_db.delete_one({"_id": id, "quality": {}})
                return True


    def delete_file(self,file_id: int,Movie_id: int):
        file_id = int(file_id)
        movie_id = int(Movie_id)
        movie = self.movie_db.find_one({"_id": movie_id})
        if movie:
            data = dict(movie["quality"])
            for quality , files in data.items():
                for file , file_id_n_message_id in files.items():
                    db_file = int(file_id_n_message_id.split('-')[0])
                    if file_id == db_file:
                        self.movie_db.update_one({"_id": movie_id},{"$unset": {f"quality.{quality}.{file}": ""}})
                        self.movie_db.update_one({"_id": movie_id, f"quality.{quality}": {}},{"$unset": {f"quality.{quality}": ""}})
                        self.movie_db.delete_one({"_id": movie_id, "quality": {}})
                        return True
