import cv2
import numpy as np
from skimage.morphology import skeletonize



def preprocess(path, start):
    #path = '../pictures/test_track4.jpg'
    img = cv2.imread(path)

    START_X, START_Y = start

    img_resized = cv2.resize(img, (1280, 720), 
                  interpolation = cv2.INTER_LINEAR)

    #---------------------------------------------------------------
    #img = cv2.imread('../pictures/test_track3_resized.png')
    result = np.ndarray((img_resized.shape[0], img_resized.shape[1], 4), dtype=np.uint8) #criando imagem cinza com transparencia

    result[:,:,0:3] = img_resized[:,:,:] #copiando a imagem para o resultado


    src = cv2.GaussianBlur(img_resized, (5, 5), 0) #suavização para elimanar ruídos

    img_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY) #conversão para escala de cinza


    #obtenção do gradiente em X e em Y    
    grad_x = cv2.Sobel(img_gray, cv2.CV_16S, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
    grad_y = cv2.Sobel(img_gray, cv2.CV_16S, 0, 1, ksize=3)

    #absoluto de cada gradiente
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)

    #cálculo da média dos dois gradientes
    grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)


    #binarização da imagem de acordo com o threshold
    #esse threshold foi escolhido arbitrariamente ao observar os valores do gradiente
    threshold = 70
    grad[grad < threshold] = 0
    grad[grad > 0] = 1



    result[:,:,3] = grad[:,:] #adição do gradiente limiarizado como o canal alpha
    result[:,:,3] *= 255



    #------------------------------------------------
    #utilizando o gradiente para criar um caminho para que o carro-npc possa seguir
    cv2.floodFill(grad, None, (START_X, START_Y), 1) #preenchendo o interior da pista

    kernel = np.asarray([[1, 1, 1], #kernel que será usado para preencher o espaço entre 
                         [1, 1, 1], #as bordas da pista criado pelo filtro de sobel
                         [1, 1, 1]])

    kernel =  cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))

    grad2 = cv2.dilate(grad, kernel, iterations = 3) #usando dilatação para preencher os espaços citados acima
    #grad2 = cv2.erode(grad2, kernel, iterations = 20)

    #cv2.imshow('teste', grad2*255)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    path = skeletonize(grad2) #esqueletonização para obter o caminho que sempre estará ao centro da pista
                             #esse processo gera uma imagem que contém True ou False em vez de valores de pixeis

    pathInt = np.ndarray((path.shape), dtype=np.uint8) #criação da imagem que conterá o caminho

    #substituição dos valores booleanos por valores normais de pixeis
    pathInt[path == False] = 0  
    pathInt[path == True] = 255

    cv2.imwrite('track_border.png', result)
    cv2.imwrite('npc_path_line.png', pathInt)

    #----------------------------------------------------------------

    #img = cv2.imread('npc_path_line_edited.png')

    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    contours, _ = cv2.findContours(image=pathInt, mode=cv2.RETR_EXTERNAL, 
                                           method=cv2.CHAIN_APPROX_NONE)

    #cv2.drawContours(img_resized, contours, -1, (0,255,0), 3)
    #cv2.imshow("teste",img_resized)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    tmp = contours[0]
    for i in range(0,len(contours)):
        if len(contours[i]) > len(tmp):
            tmp = contours[i]
    contours = tmp

    lista = []
    for i in range(len(contours)):
        lista.append([contours[i][0][0], contours[i][0][1]])


    return 'track_border.png', lista