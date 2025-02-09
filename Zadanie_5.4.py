# Zadanie: biblioteka filmów

# A teraz coś z zupełnie innej beczki. Wyobraź sobie, że tworzysz system obsługujący bibliotekę filmów i seriali. Wykorzystaj wiedzę na temat programowania obiektowego i napisz program, który spełnia następujące założenia:

#     Jest w stanie przechowywać informacje na temat filmów, które znajdują się w systemie. Każdy film powinien mieć następujące atrybuty:
#         Tytuł
#         Rok wydania
#         Gatunek
#         Liczba odtworzeń
#     Umożliwia przechowywanie informacji na temat seriali. Każdy serial powinien mieć następujące atrybuty:
#         Tytuł
#         Rok wydania
#         Gatunek
#         Numer odcinka
#         Numer sezonu
#         Liczba odtworzeń
#     Filmy i seriale mają metodę play, która zwiększa liczbę odtworzeń danego tytułu o 1.
#     Po wyświetleniu serialu jako string pokazują się informacje o konkretnym odcinku, np.: “The Simpsons S01E05” (gdzie po S pokazany jest numer sezonu w notacji dwucyfrowej, natomiast po E - numer odcinka, również w zapisie dwucyfrowym).
#     Po wyświetleniu filmu jako string widoczne są tytuł i rok wydania np. “Pulp Fiction (1994)”.
#     Przechowuje filmy i seriale w jednej liście.

# Dodatkowo:

#     Napisz funkcje get_movies oraz get_series, które będą filtrować listę i zwracać odpowiednio tylko filmy oraz tylko seriale. Posortuj listę wynikową alfabetycznie.
#     Napisz funkcję search, która wyszukuje film lub serial po jego tytule.
#     Napisz funkcję generate_views, która losowo wybiera element z biblioteki, a następnie dodaje mu losową (z zakresu od 1 do 100) ilość odtworzeń.
#     Napisz funkcję, która uruchomi generate_views 10 razy.
#     Napisz funkcję top_titles(), która zwróci wybraną ilość najpopularniejszych tytułów z biblioteki. Dla chętnych: dodaj do funkcji parametr content_type, którym wybierzesz czy mają zostać pokazane filmy, czy seriale.

# Niech program po uruchomieniu działa w następujący sposób:

#     Wyświetli na konsoli komunikat Biblioteka filmów.
#     Wypełni bibliotekę treścią.
#     Wygeneruje odtworzenia treści za pomocą funkcji generate_views.
#     Wyświetli na konsoli komunikat Najpopularniejsze filmy i seriale dnia <data>, gdzie <data> to bieżąca data w formacie DD.MM.RRRR.
#     Wyświetli listę top 3 najpopularniejszych tytułów.



import random
from datetime import datetime

class Movie:
    def __init__(self, title, year_of_release, type, number_of_plays=0):
        self.title = title
        self.year_of_release = year_of_release
        self.type = type
        self.number_of_plays = number_of_plays

    def play(self):
        """Zwiększa liczbę odtworzeń o 1"""
        self.number_of_plays += 1

    def __str__(self,):
        return f"{self.title}  ({self.year_of_release})"
    


class Serial(Movie):
    def __init__(self, title, year_of_release, type, number_of_plays=0, episode_number=1, season_number=1):
        super().__init__(title, year_of_release, type, number_of_plays)
        self.episode_number = episode_number
        self.season_number = season_number
    
    def __str__(self):
        return f"{self.title}  S{self.season_number:02d}E{self.episode_number:02d}"
  

def play_by_title(library, title):
    """ wyświetla właśnie odtwarzane fimy/seriale"""
    for item in library:
        if item.title.lower() == title.lower():
            item.play()
            print(f"🎬 Odtwarzanie: {item} - {item.number_of_plays}")
            return
    print("❌ Tytuł nie znaleziony!")

def search(library):
    """Sprawdza czy serial/film jest w bibliotece"""
    check = input("Podaj nazwę filmu lub serialu: ")
    found = False
    for item in library:
        if item.title.lower() == check.lower():
            print(item)
            found = True
        
    if not found:
        print("Nie ma takiego filmu/serialu w bibliotece")



def get_movie_or_serial(library, check):
    name = [item for item in library if type(item) == check]
    return sorted(name, key=lambda name: name.title)




def get_movies(library):
    """Zwraca posortowaną alfabetycznie listę filmów"""
    movie_serial = get_movie_or_serial(library, Movie)  
    return movie_serial


def get_series(library):
    """Zwraca posortowaną alfabetycznie listę seriali"""
    movie_serial = get_movie_or_serial(library, Serial)  
    return movie_serial




def repeat_10_times(func):
    """Dekorator wykonujący funkcję 10 razy."""           
    def wrapper(library):
        for _ in range(10):
            func(library)       
    return wrapper

@repeat_10_times
def generate_views(library):
    """Losowo wybiera film lub serial i zwiększa liczbę odtworzeń o losową wartość (1-100)."""
    item = random.choice(library)  # Losowy wybór z biblioteki
    views = random.randint(1, 100)  # Losowa liczba odtworzeń
    item.number_of_plays += views
    # print(f" {item} obejrzano {views} razy. Nowa liczba odtworzeń: {item.number_of_plays}")  

def views(quantity, input_, type_="filmy i seriale"):
    top = sorted(input_, key=lambda s: s.number_of_plays, reverse=True)[:quantity]
    # print(f"\n Top {quantity} Najpopularniejsze {type_}:")
    for m in top:
        print(f"{m} - {m.number_of_plays} odtworzeń")
   

def top_titles(library):
    """Zwraca wybraną ilość najpopularniejszych tytułów z biblioteki"""
    content_type = input("Sprawdzasz najpopularniejsze tytuły. Wpisz 'film', aby zobaczyć najpopularniejsze filmy,'serial', aby zobaczyć najpopularniejsze seriale lub 'film serial' aby zobaczyć najpopularniejsze filmy oraz seriale: ").strip().lower()
    quantity = input("Ile z nich chcesz zobaczyć? ").strip()

    if not quantity.isdigit():  # Sprawdzam czy liczba
        print("❌ Miałeś podać liczbę!")
        return
    
    quantity = int(quantity)  # Konwersja na int
    
    if content_type == "serial":
        type_= "seriale"
        input_ = get_series(library)
        return views(quantity, input_, type_) 

    
    elif content_type == "film":
        type_ ="filmy"
        input_ = get_movies(library)
        return views(quantity, input_, type_)

    elif content_type == "serialfilm" or "filmserial":
        type_ = "filmy i seriale"
        input_ = library
        return views(quantity, input_)
   
    else:
        print("Niepoprawna opcja! Wpisz 'film' lub 'serial'.")


if __name__ == "__main__":


    print("Biblioteka filmów")  #Wyświetli na konsoli komunikat Biblioteka filmów.

 #Wypełni bibliotekę treścią.
    library = [   
    # Filmy
    Movie("Inception", 2010, "Sci-Fi", 150),
    Movie("Interstellar", 2014, "Sci-Fi", 300),
    Movie("The Matrix", 1999, "Sci-Fi", 500),
    Movie("The Dark Knight", 2008, "Action", 450),
    Movie("Pulp Fiction", 1994, "Crime", 400),
    Movie("Forrest Gump", 1994, "Drama", 350),
    Movie("Fight Club", 1999, "Drama", 320),
    Movie("The Shawshank Redemption", 1994, "Drama", 600),
    Movie("Gladiator", 2000, "Historical", 280),
    Movie("Titanic", 1997, "Romance", 700),

    # Seriale
    Serial("Breaking Bad", 2008, "Crime", 200, episode_number=5, season_number=2),
    Serial("Game of Thrones", 2011, "Fantasy", 600, episode_number=9, season_number=4),
    Serial("The Office", 2005, "Comedy", 500, episode_number=3, season_number=1),
    Serial("Friends", 1994, "Comedy", 450, episode_number=2, season_number=5),
    Serial("Stranger Things", 2016, "Sci-Fi", 350, episode_number=7, season_number=3),
    Serial("Sherlock", 2010, "Crime", 300, episode_number=1, season_number=1),
    Serial("The Mandalorian", 2019, "Sci-Fi", 280, episode_number=4, season_number=2),
    Serial("House of Cards", 2013, "Drama", 400, episode_number=10, season_number=3),
    Serial("Rick and Morty", 2013, "Animation", 500, episode_number=8, season_number=4),
    Serial("Black Mirror", 2011, "Sci-Fi", 420, episode_number=3, season_number=5)
    ]




    #Wygeneruje odtworzenia treści za pomocą funkcji generate_views. 
    generate_views(library)

    # Wyświetli na konsoli komunikat Najpopularniejsze filmy i seriale dnia <data>, gdzie <data> to bieżąca data w formacie DD.MM.RRRR.

    print(f"Najpopularniejsze filmy i seriale dnia {datetime.today().strftime("%d.%m.%Y")} ")



    # Wyświetli listę top 3 najpopularniejszych tytułów.
    views(3, library, )

    


    
