import pygame
import time
from game.cars import *
from game.utils import scale_image, blit_text_center

class GameInfo:
    LEVELS = 10

    def __init__(self, level=1):
        self.level = level
        self.started = False
        self.level_start_time = 0
        self.inputs = [0, 0] #[vertical, horizontal]

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
        

class ImagesInfos:
    def __init__(self, font, height, TRACK_BORDER_MASK, FINISH_MASK, FINISH_POSITION ):
        self.font = font
        self.height = height
        self.TRACK_BORDER_MASK = TRACK_BORDER_MASK
        self.FINISH_MASK = FINISH_MASK
        self.FINISH_POSITION = FINISH_POSITION

    def draw(self, win, images, player_car, computer_car, game_info):
        for img, pos in images:
            win.blit(img, pos)

        level_text = self.font.render(
            f"Level {game_info.level}", 1, (255, 255, 255))
        win.blit(level_text, (10, self.height - level_text.get_height() - 70))

        time_text = self.font.render(
            f"Time: {game_info.get_level_time()}s", 1, (255, 255, 255))
        win.blit(time_text, (10, self.height - time_text.get_height() - 40))

        vel_text = self.font.render(
            f"Vel: {round(player_car.vel, 1)}px/s", 1, (255, 255, 255))
        win.blit(vel_text, (10, self.height - vel_text.get_height() - 10))

        player_car.draw(win)
        computer_car.draw(win)
        pygame.display.update()


def move_player(player_car, game_info):
    
    moved = False

    if game_info.inputs[1] < 0:
        player_car.rotate(left=True)
    if game_info.inputs[1] > 0:
        player_car.rotate(right=True)
    if game_info.inputs[0] > 0:
        moved = True
        player_car.move_forward()
    if game_info.inputs[0] < 0:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()

    player_car.get_rotated_img()


def handle_collision(player_car, computer_car, game_info, imgs_info, WIN):
    
    game_info.get_inputs()
    move_player(player_car, game_info) 
                        
    computer_car.move()

    if player_car.collide(imgs_info.TRACK_BORDER_MASK) != None:
        
        player_car.bounce(game_info.inputs[0], game_info.inputs[1])

    computer_finish_poi_collide = computer_car.collide(
        imgs_info.FINISH_MASK, *imgs_info.FINISH_POSITION)
    if computer_finish_poi_collide != None:
        blit_text_center(WIN, imgs_info.MAIN_FONT, "You lost!")
        pygame.display.update()
        pygame.time.wait(5000)
        game_info.reset()
        player_car.reset()
        computer_car.reset()

    player_finish_poi_collide = player_car.collide(
        imgs_info.FINISH_MASK, *imgs_info.FINISH_POSITION)
    if player_finish_poi_collide != None:
        if player_finish_poi_collide[1] == 0:
            player_car.bounce(game_info.inputs[0], game_info.inputs[1])
        else:
            game_info.next_level()
            player_car.reset()
            computer_car.next_level(game_info.level)

def run_game(trackpath):


    pygame.font.init()

    GRASS = scale_image(pygame.image.load("/home/fernando/git/CorridaRealidadeAumentada/sprites/grass.jpg"), 2.5)
    #TRACK = scale_image(pygame.image.load("/home/fernando/git/CorridaRealidadeAumentada/sprites/track.png"), 0.9)

    TRACK_BORDER = scale_image(pygame.image.load(trackpath), 1.0)
    TRACK = TRACK_BORDER
    TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

    FINISH = pygame.image.load("/home/fernando/git/CorridaRealidadeAumentada/sprites/finish.png")
    FINISH_MASK = pygame.mask.from_surface(FINISH)
    FINISH_POSITION = (130, 250)

    RED_CAR = scale_image(pygame.image.load("/home/fernando/git/CorridaRealidadeAumentada/sprites/cars/red-car.png"), 0.55)
    GREEN_CAR = scale_image(pygame.image.load("/home/fernando/git/CorridaRealidadeAumentada/sprites/cars/green-car.png"), 0.55)
    WHITE_CAR = scale_image(pygame.image.load("/home/fernando/git/CorridaRealidadeAumentada/sprites/cars/white-car.png"), 0.55)

    WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    print(WIDTH, HEIGHT)
    pygame.display.set_caption("Racing Game!")

    MAIN_FONT = pygame.font.SysFont("comicsans", 44)

    FPS = 60
    PATH = [(175, 119), (110, 70), (56, 133), (70, 481), (318, 731), (404, 680), (418, 521), (507, 475), (600, 551), (613, 715), (736, 713),
            (734, 399), (611, 357), (409, 343), (433, 257), (697, 258), (738, 123), (581, 71), (303, 78), (275, 377), (176, 388), (178, 260)]


    run = True
    clock = pygame.time.Clock()
    #images = [(GRASS, (0, 0)), (TRACK, (0, 0)),
              #(FINISH, FINISH_POSITION), (TRACK_BORDER, (0, 0))]
    images = [(GRASS, (0, 0)), (FINISH, FINISH_POSITION), (TRACK_BORDER, (0, 0))]
    player_car = PlayerCar(150, 200, 4, 4, RED_CAR)
    computer_car = ComputerCar(150, 200, 2, 4, GREEN_CAR, PATH)
    game_info = GameInfo()
    imgs_info = ImagesInfos(MAIN_FONT, HEIGHT, TRACK_BORDER_MASK, FINISH_MASK, FINISH_POSITION)

    while run:
        clock.tick(FPS)

        imgs_info.draw(WIN, images, player_car, computer_car, game_info)

        while not game_info.started:
            blit_text_center(
                WIN, MAIN_FONT, f"Press any key to start level {game_info.level}!")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break

                if event.type == pygame.KEYDOWN:
                    game_info.start_level()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            

        handle_collision(player_car, computer_car, game_info, imgs_info, WIN)

        if game_info.game_finished():
            blit_text_center(WIN, MAIN_FONT, "You won the game!")
            pygame.time.wait(5000)
            game_info.reset()
            player_car.reset()
            computer_car.reset()


    pygame.quit()


if __name__ == '__main__':
    run_game('/home/fernando/git/CorridaRealidadeAumentada/sprites/track-border.png')