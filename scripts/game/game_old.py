import pygame
from player import Player
from cv2 import waitKey

class App:
    def __init__(self, dir):
        self._running = True
        self.size = self.width, self.height = 1280, 720
        pygame.init()
        pygame.font.get_init()
        self.TEXT_FONT = pygame.font.Font("../font.otf")
        self.display = pygame.display.set_mode((self.width, self.height))
        self.player = Player()
        '''
        borders = []
        borders.append(pygame.Rect(-1, 0, 1, self.height))
        borders.append(pygame.Rect(0, -1, self.width, 1))
        borders.append(pygame.Rect(self.width+1, 0, 1, self.height))
        borders.append(pygame.Rect(0, self.height+1, self.width+1, 1))
        self.player.collisorlist = borders
        '''
        self.player.collisorlist = []
        self.allrect = []
        self.img = pygame.image.load(dir)
        self.enemies = []
        self.enemiesRects = []
        self.score = 0

    def blit_rotate_center(surface, image, top_left, angle):
        rotated_img = pygame.transform.rotate(image, )
           
  
    def on_event(self, event):
        if event.type == pygame.USEREVENT:
            self.timer = True
        if event.type == pygame.QUIT:
            self._running = False


    def on_load(self):
        #load new level
        pass

    def on_cleanup(self):
        #clears previously loaded levels
        pass

    def on_quit(self):
        self.display.fill((255,255,255))
        game_text = self.TEXT_FONT.render(f'GAME OVER', False, (0, 0, 0))
        score_text = self.TEXT_FONT.render(f'SCORE {self.score}', False, (0, 0, 0))
        end_text = self.TEXT_FONT.render(f'aperte qualquer tecla para sair', False, (0, 0, 0))
        game_text = pygame.transform.scale(game_text, (game_text.get_width() * 3,game_text.get_height() * 3)) 
        score_text = pygame.transform.scale(score_text, (score_text.get_width() * 3,score_text.get_height() * 3)) 
        end_text = pygame.transform.scale(end_text, (end_text.get_width() * 1, end_text.get_height() * 1))
        self.display.blit(game_text, ((self.width / 2) - score_text.get_width()/2 - 5, self.height / 2 - 50))
        self.display.blit(score_text, ((self.width / 2) - score_text.get_width()/2, self.height / 2))
        self.display.blit(end_text, ( (self.width - end_text.get_width())/2 ,  (self.height - 50)))
        
        pygame.display.update()
        self.init = pygame.time.get_ticks()
        
        while True:
            self.diff = pygame.time.get_ticks() - self.init
            if self.diff > 10000:
                return
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    return

        

    def on_win(self):
        pass

    def draw_window(self):
        self.display.blit(self.img, (0,0))
        score_text = self.TEXT_FONT.render(f'SCORE {self.score}', False, (0, 0, 0))
        #wave_text = self.TEXT_FONT.render(f'WAVE {self.currentWave}', False, (0, 0, 0))
        self.display.blit(score_text, (self.width - score_text.get_width() - 20, 15))
        #self.display.blit(highscore_text, (self.width - score_text.get_width() - 20, 35))
        #pygame.draw.rect(self.display, (255, 0, 0), (self.player.x, self.player.y, self.player.width, self.player.height), 3)
        self.display.blit(self.player.sprite, (self.player.x, self.player.y))


        for enemy in self.enemies:
            #pygame.draw.rect(self.display, (255, 0, 0), (enemy.x, enemy.y, self.player.width, self.player.height), 3)
            self.display.blit(enemy.sprite, (enemy.x, enemy.y))
        
        pygame.display.update()

    def on_execute(self):
        
        if( self._running ):
            for event in pygame.event.get():
                self.on_event(event)

            self.player.move()
            for index in range(len(self.enemies)):
                tmp = self.enemies[index].move()
                if tmp != None:
                    self.enemiesRects[index] = tmp
                
            self.player.animationController()
            self.draw_window()
            return True
        else:
            self.on_quit()
            return False