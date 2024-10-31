from imdb import Cinemagoer
from dataclasses import dataclass, field
from typing import Dict, Any
from themoviedb import TMDb
from datetime import datetime
from Classes import MovieDetails
import PTN

tmdbApiKey = 'b720b01bca41db49c76f5e6a1e31df35'
tmdb = TMDb(key=tmdbApiKey , language="en-US", region="US")
imdb = Cinemagoer()

class MoviesDetails:
    def __init__(self,movie_name: str = None ,source: str = 'tmdb') -> None:
        self.__dict__.clear()
        info = PTN.parse(movie_name)
        self.movie_name = info['title']
        self.year = info['year'] if 'year' in info else None
        self.source = source
        
        self.movieData = self.get_details_from_imdb() if self.source =='imdb' else self.get_details_from_tmdb() if self.source == 'tmdb' else None
    
    def get_details(self) -> MovieDetails:
        return self.movieData

    def convert_date(self,date_str: str) -> str:
        try:return int(date_str)
        except:return datetime.strptime(date_str.split(' (')[0], "%d %b %Y").strftime("%Y-%m-%d")

    def get_details_from_tmdb(self) -> MovieDetails:
        movies = tmdb.search().movies(query=self.movie_name,year=self.year).results[0]
        if movies:
            movie_id = movies.id 
            movie  = tmdb.movie(movie_id).details(append_to_response="credits,external_ids,images,videos")
    
            return MovieDetails(
                name=movie.title,
                released = movie.release_date,
                languages = ', '.join([language.name for language in movie.spoken_languages]),
                year = str(movie.release_date).split('-')[0],
                genres = ', '.join([genre.name for genre in movie.genres]),
                image = "https://image.tmdb.org/t/p/w600_and_h900_bestv2" + str(movie.poster_path),
                rating = movie.vote_average,
                votes = movie.vote_count,
            )

    def get_details_from_imdb(self) -> MovieDetails:
        movieID = imdb.search_movie(self.movie_name)[0].movieID
        movie: Dict = imdb.get_movie(movieID)
        if movie:
            date = movie["original air date"] if movie.get("original air date") else movie.get("year") if movie.get("year") else "N/A"
    
            return MovieDetails(
                name=movie.get('title'),
                released=self.convert_date(str(date)),
                # released=(str(date)),
                languages=str(' ,'.join(movie.get('languages'))).rstrip() if len(movie.get('languages')) > 1 else movie.get('languages')[0],
                year=movie.get('year'),
                genres=str(', '.join(movie.get('genres'))).rstrip() if len(movie.get('genres')) > 1 else movie.get('genres')[0],
                image=movie.get('full-size cover url'),
                rating=movie.get('rating'),
                votes=movie.get('votes'),
            )
    
