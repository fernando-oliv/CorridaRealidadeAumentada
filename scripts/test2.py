from game.game import *
from preprocessing import preprocess
import cv2
import tkinter.filedialog

def prompt_file():
    """Create a Tk file dialog and cleanup when finished"""
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_name

path = '../pictures/test_track4.jpg'
path = prompt_file()
track, lista = preprocess(path, (640, 100))
run_game(track, lista)