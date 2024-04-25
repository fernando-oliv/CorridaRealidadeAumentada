import pygame
import numpy as np
import matplotlib.pyplot as plt
from pygame.locals import *
from scipy.signal import correlate
from PIL import Image
import tkinter
from game.cars import Player
from game import App
import cv2

    



def process_frame(img2, app):
    img2 = cv2.resize(img2, (800, 600))
    app.img2 = img2
    img3 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    im1 = Image.fromarray(img3)
    im1.save('temp.png')
    app.img = pygame.image.load("temp.png")
    global score
    global highscore
    if score > highscore:
        highscore = score
    lower_color = np.array([80, 25, 30])
    upper_color = np.array([130, 255, 255])
    img_hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img_hsv, lower_color, upper_color)
    '''
    cv2.imshow('mask', mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
    ind_x, ind_y = np.where(mask == 255)
    i = 0
    app.allrect = []
    app.player.collisorlist = []
    app.player.life = 4
    app.player.x = 50
    app.player.y = 200
    lower_color = np.array([138, 30, 20])
    upper_color = np.array([179, 255, 255])
    mask1 = cv2.inRange(img_hsv, lower_color, upper_color)

    lower_color = np.array([0, 30, 20])
    upper_color = np.array([10, 255, 255])
    mask2 = cv2.inRange(img_hsv, lower_color, upper_color)
    mask1 = np.add(mask1, mask2)
    

    spawny, spawnx = np.where(mask1 == 255)
    '''
    if spawnx is not ([] or None) and len(spawnx) > 0:
        theApp.player.x = spawnx[0] + 10
        theApp.player.y = spawny[0]
        #print(theApp.player.x)
        #print(theApp.player.y)
    '''
    for ind in ind_x:
        temp = pygame.Rect(ind_y[i], ind, 1, 1)
        app.allrect.append(temp)
        app.player.collisorlist.append(temp)
        i += 1

    global enemies
    enemies = []
    app.delay = 0
    app.currentWave = 0

def prompt_file():
    """Create a Tk file dialog and cleanup when finished"""
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_name

if __name__ == "__main__" :

    dir = "testeRealresized3.jpg"
    img2 = cv2.imread(dir)

    lower_color = np.array([100, 25, 30])
    upper_color = np.array([120, 255, 255])
    
    img_hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
    img_rgb = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2RGB)


    
    
    
    #retorna uma imagem binaria onde os valores encontrados 
    #estão dentro dos limtes de lower_color e upper_color
    mask = cv2.inRange(img_hsv, lower_color, upper_color)


    img = cv2.imread("../sprites/tutorial.png")
    img = cv2.resize(img, (int(1280 * 3 / 4), int(720 * 3 /4)))
    cv2.imshow('tutorial', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #testando o canny edge detection   
    #edge = cv2.Canny(img2, 230, 240)
 
    
    #outro modo de calcular os pixels, usando o filtro de sobel para detecção de bordas
    #mas é necessário suavizar a imagem para remover o ruído
    #problema : a suavização está perdendo muitos detalhes
    #teste : não utilizar a suavização, GRANDE RISCO

    '''
    img2 = cv2.imread(dir)
    img3 = cv2.GaussianBlur(img2, (3, 3), cv2.BORDER_DEFAULT)
    #img3rgb = cv2.cvtColor(img3, cv2.COLOR_BGR2RGB)

    img3 = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
    grad_x = cv2.Sobel(img3, cv2.CV_16S, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
    grad_y = cv2.Sobel(img3, cv2.CV_16S, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)

    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    
    
    grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    _, grad = cv2.threshold(grad, 50, 255, cv2.THRESH_BINARY)
    
    cv2.imshow('sobel', grad)
    cv2.imshow('color', mask)
    cv2.imshow('canny', edge)

    cv2.waitKey(0) 
    cv2.destroyAllWindows() 
    '''

    #agora reconhecer o spawn point
    lower_color = np.array([138, 30, 20])
    upper_color = np.array([179, 255, 255])
    mask1 = cv2.inRange(img_hsv, lower_color, upper_color)

    lower_color = np.array([0, 30, 20])
    upper_color = np.array([10, 255, 255])
    mask2 = cv2.inRange(img_hsv, lower_color, upper_color)
    mask1 = np.add(mask1, mask2)
    

    spawny, spawnx = np.where(mask1 == 255)

    #grad = cv2.subtract(grad, mask1)
    
    ind_x, ind_y = np.where(mask == 255)


    theApp = App(dir)
    FPS = 60
    teste = True
    clock = pygame.time.Clock()
    #plat1 = pygame.Rect(10, theApp.height*3/4, theApp.weight-20, 40)
    if spawnx is not ([] or None) and len(spawnx) > 0:
        theApp.player.x = spawnx[0] + 10
        theApp.player.y = spawny[0]
        #print(theApp.player.x)
        #print(theApp.player.y)
    i = 0
    for ind in ind_x:
        temp = pygame.Rect(ind_y[i], ind, 1, 1)
        theApp.allrect.append(temp)
        theApp.player.collisorlist.append(temp)
        i += 1


    k = 0
    while(teste):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_c]:
            vcap = cv2.VideoCapture(1)
            ret, curr_frame = vcap.read()
            if ret:
                process_frame(curr_frame, theApp)
            vcap.release()
        elif keys[pygame.K_r]:
            dir = prompt_file()
            if dir != "" and dir != None and type(dir) != tuple:
                print('--------------')
                print(type(dir))
                print('-----------------')
                new_img = cv2.imread(dir)
                process_frame(new_img, theApp)
            
        clock.tick(FPS)
        teste = theApp.on_execute()
