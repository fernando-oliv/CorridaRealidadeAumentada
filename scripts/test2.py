from game.game import *
from preprocessing import preprocess
from tkinter import filedialog



def prompt_file():
    file_name = filedialog.askopenfilename(title="selecione a foto")
    return file_name


path = prompt_file()
track = preprocess(path)
run_game(track)
