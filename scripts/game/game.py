import pygame
import time
from game.cars import *
from game.utils import scale_image, blit_text_center

WIDTH, HEIGHT = 0, 0
class GameInfo:
    LEVELS = 1

    def __init__(self, level=1):
        self.level = level
        self.started = False
        self.ajusted = False
        self.level_start_time = 0
        self.inputs = [0, 0] #[vertical, horizontal]
        self.inputs2 = [0, 0] #[vertical, horizontal]
        self.player_vencedor = "Ninguem"

    def next_level(self):
        self.level += 1
        self.started = False

    def reset(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0

    def game_finished(self):
        return self.level > self.LEVELS

    def start_level(self):
        self.started = True
        self.level_start_time = time.time()

    def get_level_time(self):
        if not self.started:
            return 0
        return round(time.time() - self.level_start_time)
    
    def value_keys(self, boolean):
        if boolean:
            return 1
        else:
            return 0
    
    def get_inputs(self):
        keys = pygame.key.get_pressed()
        self.inputs[0] = self.value_keys(keys[pygame.K_w])
        self.inputs[0] += -1 * self.value_keys(keys[pygame.K_s])
        self.inputs[1] = self.value_keys(keys[pygame.K_d])
        self.inputs[1] += -1 * self.value_keys(keys[pygame.K_a])
        self.inputs2[0] = self.value_keys(keys[pygame.K_UP])
        self.inputs2[0] += -1 * self.value_keys(keys[pygame.K_DOWN])
        self.inputs2[1] = self.value_keys(keys[pygame.K_RIGHT])
        self.inputs2[1] += -1 * self.value_keys(keys[pygame.K_LEFT])
        

class ImagesInfos:
    def __init__(self, font, height, TRACK_BORDER_MASK, FINISH_MASK, FINISH_POSITION ):
        self.font = font
        self.height = height
        self.TRACK_BORDER_MASK = TRACK_BORDER_MASK
        self.FINISH_MASK = FINISH_MASK
        self.FINISH_POSITION = FINISH_POSITION
        self.parametros = None
        self.angle = 0

    def set_dest(self, x, y):
        self.dest_x = x
        self.dest_y = y

    def set_angle(self, x):
        self.angle = x

    def draw(self, win, images, player_car, computer_car, game_info, WIDTH, HEIGHT, ajusted):
        win.fill((0,0,0), None, 0)
        tempWin = win.copy()
        currentLap = player_car.laps if player_car.laps > computer_car.laps else computer_car.laps
        currentLap += 1
        if computer_car.laps > player_car.laps:
            lap = computer_car.laps
        for img, pos in images:
            tempWin.blit(img, pos)

        level_text = self.font.render('Lap '+ str(currentLap) + '/3', 1, (255, 0, 0))
        tempWin.blit(level_text, (10, self.height - level_text.get_height() - 70))

        time_text = self.font.render(
            "Time: " + str(game_info.get_level_time()) + "s", 1, (255, 0, 0))
        tempWin.blit(time_text, (10, self.height - time_text.get_height() - 40))

        #vel_text = self.font.render(
        #    f"Vel: {round(player_car.vel, 1)}px/s", 1, (255, 255, 255))
        #win.blit(vel_text, (10, self.height - vel_text.get_height() - 10))

        player_car.draw(tempWin)
        computer_car.draw(tempWin)
        #computer_car.draw_points(win)
        if ajusted:
            win.blit(pygame.transform.rotate(pygame.transform.scale(tempWin, (WIDTH, HEIGHT)), self.angle), (self.dest_x, self.dest_y))
        else:
            win.blit(pygame.transform.scale(tempWin, (WIDTH, HEIGHT)), (0, 0))
        pygame.display.update()


def move_player(player_car, game_info, player1):
    
    moved = False
    if player1:
        input = game_info.inputs
    else:
        input = game_info.inputs2
    
    if input[1] < 0:
        player_car.rotate(left=True)
    if input[1] > 0:
        player_car.rotate(right=True)
    if input[0] > 0:
        moved = True
        player_car.move_forward()
    if input[0] < 0:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()

    player_car.get_rotated_img()



def handle_collision(player_car, computer_car, game_info, imgs_info):
    
    game_info.get_inputs()
    move_player(player_car, game_info, True)
    move_player(computer_car, game_info, False)
                        
    #computer_car.move()


    #computer_finish_poi_collide = computer_car.collide(
#        imgs_info.FINISH_MASK, *imgs_info.FINISH_POSITION)
#    if computer_finish_poi_collide != None:
#        if computer_car.flag_finish_line == False:
#            computer_car.laps += 1
#            computer_car.flag_finish_line = True

#        if computer_car.laps >= 3:
#            blit_text_center(WIN, imgs_info.font, "You lost!")
#            pygame.display.update()
#            pygame.time.wait(5000)
#            game_info.reset()
#            player_car.reset()
#            computer_car.reset()
        
#    else:
#        computer_car.flag_finish_line = False

    if player_car.collide(imgs_info.TRACK_BORDER_MASK) != None:
        player_car.bounce(game_info.inputs[0], game_info.inputs[1])

    player_finish_poi_collide = player_car.collide(
        imgs_info.FINISH_MASK, *imgs_info.FINISH_POSITION)
    if player_finish_poi_collide != None:
        if player_finish_poi_collide[1] == 0 and not player_car.flag_finish_line:
            player_car.bounce(game_info.inputs[0], game_info.inputs[1])
        else:
            if player_car.flag_finish_line == False:
                player_car.laps += 1
                player_car.flag_finish_line = True
            if player_car.laps >= 3:
                game_info.next_level()
                game_info.player_vencedor = "Vermelho"
                player_car.reset()
    else:
        player_car.flag_finish_line = False





    if computer_car.collide(imgs_info.TRACK_BORDER_MASK) != None:
        computer_car.bounce(game_info.inputs2[0], game_info.inputs2[1])

    player_finish_poi_collide = computer_car.collide(
        imgs_info.FINISH_MASK, *imgs_info.FINISH_POSITION)
    if player_finish_poi_collide != None:
        if player_finish_poi_collide[1] == 0 and not computer_car.flag_finish_line:
            computer_car.bounce(game_info.inputs2[0], game_info.inputs2[1])
        else:
            if computer_car.flag_finish_line == False:
                computer_car.laps += 1
                computer_car.flag_finish_line = True
            if computer_car.laps >= 3:
                game_info.next_level()
                game_info.player_vencedor = "Verde"
                computer_car.reset()
                
    else:
        computer_car.flag_finish_line = False


def run_game(trackpath):

    pygame.init()
    pygame.image.load("sprites/grass.jpg")
    pygame.font.init()

    GRASS = scale_image(pygame.image.load("sprites/grass.jpg"), 2.5)
    #TRACK = scale_image(pygame.image.load("/home/fernando/git/CorridaRealidadeAumentada/sprites/track.png"), 0.9)

    TRACK_BORDER = scale_image(pygame.image.load(trackpath), 1.0)
    TRACK = TRACK_BORDER
    TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

    FINISH = pygame.image.load("sprites/finish.png")
    FINISH_MASK = pygame.mask.from_surface(FINISH)
    FINISH_POSITION = (130, 250)

    RED_CAR = scale_image(pygame.image.load("sprites/cars/red-car.png"), 0.55)
    GREEN_CAR = scale_image(pygame.image.load("sprites/cars/green-car.png"), 0.55)
    WHITE_CAR = scale_image(pygame.image.load("sprites/cars/white-car.png"), 0.55)

    WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    print(WIDTH, HEIGHT)
    pygame.display.set_caption("Racing Game!")

    MAIN_FONT = pygame.font.Font("font.otf", 44)

    FPS = 60
    

  
    run = True
    clock = pygame.time.Clock()
    images = [(TRACK, (0, 0)),
              (FINISH, FINISH_POSITION), (TRACK_BORDER, (0, 0))]

    player_car = PlayerCar(150, 200, 100, 4, RED_CAR)
    computer_car = PlayerCar(150, 200, 100, 4, GREEN_CAR)
    imgs_info = ImagesInfos(MAIN_FONT, HEIGHT, TRACK_BORDER_MASK, FINISH_MASK, FINISH_POSITION)
    game_info = GameInfo()

    while(run):
        imgs_info.draw(WIN, images, player_car, computer_car, game_info, WIDTH, HEIGHT, False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                FINISH_POSITION = (x, y)
                images = [ (FINISH, FINISH_POSITION), (TRACK_BORDER, (0, 0))]
                
                imgs_info = ImagesInfos(MAIN_FONT, HEIGHT, TRACK_BORDER_MASK, FINISH_MASK, FINISH_POSITION)
                run = False
    run = True

    player_car = PlayerCar(FINISH_POSITION[0] + 20 , FINISH_POSITION[1] - 50, 4, 4, RED_CAR)
    #computer_car = ComputerCar(FINISH_POSITION[0] + 20 , FINISH_POSITION[1] - 50, 2, 4, GREEN_CAR, tmp)
    computer_car = PlayerCar(FINISH_POSITION[0] + 20 , FINISH_POSITION[1] - 50, 4, 4, GREEN_CAR)
    #computer_car.path = tmp
    computer_car.x, computer_car.y = player_car.x, player_car.y
    f = open("parametros.txt", "r")
    print("escala do arq")
    scale = float(f.readline())
    angle = float(f.readline())
    dest_x = float(f.readline())
    dest_y = float(f.readline())
    f.close()
    #loop principal
    while run:
        clock.tick(FPS)

        imgs_info.draw(WIN, images, player_car, computer_car, game_info, WIDTH, HEIGHT, game_info.ajusted)
        #WIN.blit(pygame.transform.scale(WIN, (WIDTH, HEIGHT)), (0,0))

        #aqui
        i = 1
        while not game_info.ajusted:
            #blit_text_center(
            #    WIN, MAIN_FONT, "Ajuste a tela com as setas !")
            #pygame.display.update()
            keys = pygame.key.get_pressed()
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_p]:
                        WIDTH = scale * WIDTH
                        HEIGHT = scale * HEIGHT
                        game_info.ajusted = True
                        imgs_info.set_dest(dest_x, dest_y)
                
                        images = images [:-1]
                        print("escala = ", scale)
                        print("dest_x = ", dest_x)
                        print("dest_y = ", dest_y)
                        print("angle = ", angle)
                        f = open("parametros.txt", "w")
                        f.writelines(str(scale)+"\n")
                        f.writelines(str(angle)+"\n")
                        f.writelines(str(dest_x)+"\n")
                        f.writelines(str(dest_y)+"\n")
                        f.close()
                        RED_CAR = scale_image(RED_CAR, 0.55 / scale)
                        player_car = PlayerCar(FINISH_POSITION[0] + 20 , FINISH_POSITION[1] - 40, 2.5, 4, RED_CAR)
                        GREEN_CAR = scale_image(GREEN_CAR, 0.55 / scale)
                        computer_car = PlayerCar(FINISH_POSITION[0] + 20 , FINISH_POSITION[1] - 40, 2.5, 4, GREEN_CAR)
                        FINISH_POSITION = (FINISH_POSITION[0], FINISH_POSITION[1])
                        break
                    if keys[pygame.K_w]:
                        scale += 0.01
                    if keys[pygame.K_s]:
                        if scale > 0.1:
                            scale -= 0.01
                    if keys[pygame.K_LEFT]:
                        dest_x -= 10
                    if keys[pygame.K_RIGHT]:
                        dest_x += 10
                    if keys[pygame.K_UP]:
                        dest_y -= 10
                    if keys[pygame.K_DOWN]:
                        dest_y += 10
                    if keys[pygame.K_j]:
                        angle -= 0.5
                    if keys[pygame.K_l]:
                        angle += 0.5
                    #WIN = pygame.transform.scale(WIN, (WIDTH * scale, HEIGHT * scale))
                    imgs_info.set_dest(dest_x, dest_y)
                    imgs_info.set_angle(angle)
                    imgs_info.draw(WIN, images, player_car, computer_car, game_info, int(WIDTH * scale), int(HEIGHT * scale), True)
                    #WIN.blit(pygame.transform.scale(WIN, (WIDTH * scale, HEIGHT * scale)), (dest_x,dest_y))
                    #pygame.display.update()
                 

        while not game_info.started:
            imgs_info.draw(WIN, images, player_car, computer_car, game_info, WIDTH, HEIGHT, game_info.ajusted)
            blit_text_center(
                WIN, MAIN_FONT, "Aperte P para começar !")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                elif event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    keys = keys[pygame.K_p]
                    if keys:
                        imgs_info.draw(WIN, images, player_car, computer_car, game_info, WIDTH, HEIGHT, game_info.ajusted)
                        blit_text_center(WIN, MAIN_FONT, "3")
                        pygame.display.update()
                        time.sleep(1.0)
                        imgs_info.draw(WIN, images, player_car, computer_car, game_info, WIDTH, HEIGHT, game_info.ajusted)
                        blit_text_center(WIN, MAIN_FONT, "2")
                        pygame.display.update()
                        time.sleep(1.0)
                        imgs_info.draw(WIN, images, player_car, computer_car, game_info, WIDTH, HEIGHT, game_info.ajusted)
                        blit_text_center(WIN, MAIN_FONT, "1")
                        pygame.display.update()
                        time.sleep(1.0)
                        imgs_info.draw(WIN, images, player_car, computer_car, game_info, WIDTH, HEIGHT, game_info.ajusted)
                        blit_text_center(WIN, MAIN_FONT, "VAI")
                        pygame.display.update()
                        game_info.start_level()
                        print(WIDTH, HEIGHT)
                    

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
   

        handle_collision(player_car, computer_car, game_info, imgs_info)

        if game_info.game_finished():
            blit_text_center(WIN, MAIN_FONT, game_info.player_vencedor + " ganhou a corrida")
            pygame.display.update()
            time.sleep(2.5)
            game_info.reset()
            player_car.reset()
            computer_car.reset()
            #run = False

    print("acabou aqui")
    pygame.quit()


if __name__ == '__main__':
    run_game('sprites/track-border.png')
