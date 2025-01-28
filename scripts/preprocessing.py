import cv2
import numpy as np



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


    src = cv2.GaussianBlur(img_resized, (11, 11), 0) #suavização para elimanar ruídos
    #src = img_resized

    img_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY) #conversão para escala de cinza


    #obtenção do gradiente em X e em Y    
    grad_x = cv2.Sobel(img_gray, cv2.CV_16S, 1, 0, ksize=5, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
    grad_y = cv2.Sobel(img_gray, cv2.CV_16S, 0, 1, ksize=5)

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





    cv2.imwrite('track_border.png', result)
   

    return 'track_border.png'