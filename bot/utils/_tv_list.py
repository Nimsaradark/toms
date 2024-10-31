from themoviedb import TMDb
from Classes import TVData
from dataclasses import dataclass
@dataclass
class TVDPoster:
    title : str
    id : int
    poster : str 


def get_tv_series_list(self) -> TVData:
    tmdb = TMDb(key='b720b01bca41db49c76f5e6a1e31df35' , language="en-US", region="US")
    tv = tmdb.search().tv(self).results[0]
    return TVData(id=tv.id ,title=tv.name)

def get_tv_series_poster(tv_name) -> TVData:
    tmdb = TMDb(key='b720b01bca41db49c76f5e6a1e31df35' , language="en-US", region="US")
    tv = tmdb.search().tv(tv_name).results[0]
    return TVDPoster(id=tv.id ,title=tv.name,poster=tv.poster_url())
