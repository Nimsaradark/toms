import PTN
import re
class _movie_parser:
    def __parse_file_name(self,file_name:str):
        file_name = re.sub(r'@\w+', '', file_name.lower()).strip() 
        self.file_name = file_name.replace('_',' ')
        self.extention = file_name.split('.')[-1]
        self.movie = PTN.parse(self.file_name)
        self.q = []

    def upper_title(self,text):
        text = text.title()
        roman_pattern = r'\b[i|I|v|V|x|X]+\b'
        text = re.sub(roman_pattern, lambda match: match.group(0).upper(), text)
        return text 

    def extract_details(self,file_name: str ) -> list:
        self.__parse_file_name(file_name) 
        self.q .append(self.movie['resolution'] if 'resolution' in self.movie  else 'HD') 
        if 'quality' in self.movie:self.q.append(str(self.movie ['quality']))
        if 'codec' in self.movie:self.q.append(str(self.movie ['codec']).replace('H','x').replace('.',''))    
        if 'psa' in self.file_name:self.q.append('PSA')
        if 'pahe' in self.file_name:self.q.append('Pahe')
        if 'galaxyrg' in self.file_name:self.q.append('GalaxyRG')     
        if any(keyword in file_name.lower() for keyword in ["dolby", "atmos"]):self.q.append("DolbyAtmos")
        if 'imax' in self.file_name:self.q.append('IMAX')
        if '60fps' in self.file_name:self.q.append('60FPS')
        return self.q
    
    def title(self,file_name: str) -> str:
        self.__dict__.clear()
        self.__parse_file_name(file_name)
        self.movie_name = self.movie['title']
        self.year = self.movie['year'] if 'year' in self.movie else None
        if str(self.year) in self.movie_name:self.movie_name = str(self.movie_name).replace(str(self.year),'').rstrip().lstrip()
        self.title = str(str(self.movie_name) + " " +  (str(self.year) if self.year is not None else '')).capitalize()
        return self.title

    def category_title(self,file_name: str) -> str:
        self.__dict__.clear()
        category_list = self.extract_details(file_name)
        try:category_list.append(f"p{int(self.extention)}")
        except ValueError:pass
        return  '-'.join(category_list).rstrip('-')
    
    def cleared_file_name(self,file_name: str) -> str:
        self.__dict__.clear()
        category_list = self.extract_details(file_name)
        title = str(self.movie['title'])
        if 'year' in self.movie:
            category_list.insert(0,f"{(self.movie['year'])}")
            if str(self.movie['year']) in title:title = title.replace(str(self.movie['year']),'').lstrip().rstrip()
        return str(title.replace(' ','.').capitalize() + '.' + '.'.join(category_list).rstrip('.')) + '.' + self.extention

movie_parser = _movie_parser()


# text = "@CC_LINK Don't.Look.Up.2021.2021.720p.WEBRip.x265.@MLDBase.mkv"
# text = "[CC].Rampant.2018.720p.BluRay.x264-[YTS.AM].mp4"
# text = 'Rim.Of.The.World.2019.720p.WEBRip.x264-dolby-[YTS.AM].mp4.002'
# text = "No.One.Will.Save.You.2023.1080p.WEB-DL.6CH.x265.HEVC-Pahe.mkv"
# print(movie_parser.title(text))
# print(movie_parser.category_title(text))
# print(movie_parser.cleared_file_name(text))
