from dataclasses import dataclass
from typing import List

@dataclass
class quality:
    quality : str
    files : list[str]
    size : int

@dataclass
class MovieData:
    id : int
    title : str


@dataclass
class MovieDetails:
    name : str
    released : str
    languages : str
    year :str
    genres : str
    image : str
    rating : str
    votes : str
   
