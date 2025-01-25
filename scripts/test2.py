from game.game import *
from preprocessing import preprocess



def prompt_file():
    file_name = 'pictures/pista.jpg'
    return file_name


path = prompt_file()
track = preprocess(path, (640, 100))
run_game(track)