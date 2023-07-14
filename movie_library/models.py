from dataclasses import dataclass, field
from datetime import datetime
# create a Movie class that can hold all of the information we need it to hold

 
#dataclass automatically makes init functions and repr functions and allows for comparisons
@dataclass
class Movie:
    _id: str
    title: str
    director: str
    year: int
    #create a bunch of fields with default values that are optional and can be updated later
    rating: int = 0
    #create a default value for cast like this
    cast: list[str] = field(default_factory=list)
    series: list[str] = field(default_factory=list)
    last_watched: datetime = None
    tags: list[str] = field(default_factory=list) 
    description: str = None
    video_link: str = None