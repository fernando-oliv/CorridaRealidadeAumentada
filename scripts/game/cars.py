import pygame
from game.utils import *
import math

class AbstractCar:
    def __init__(self, max_vel, rotation_vel, img):
        self.img = img
        self.max_vel = max_vel
        self.vel = 0
        self.laps = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1
        self.rotated_image = self.img
        self.flag_finish_line = False
        self.future_rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def get_rotated_img(self):
        self.rotated_image, self.future_rect = rotate_center(self.img, (self.x, self.y), self.angle)

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.rotated_image)
        offset = (int(self.future_rect.x - x), int(self.future_rect.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0
        self.laps = 0
        self.flag_finish_line = False
    

class PlayerCar(AbstractCar):
    START_POS = (180, 200)

    def __init__(self, x, y, max_vel, rotation_vel, img):
        self.START_POS = (x, y)
        super().__init__(max_vel, rotation_vel, img)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self, vertical , horizontal):
        if self.vel != 0:
            self.vel = -self.vel
    
        if horizontal != 0:
            if horizontal > 0:
                self.angle +=  self.rotation_vel
            else:
                self.angle -= self.rotation_vel
        self.move()


class ComputerCar(AbstractCar):
    START_POS = (150, 200)

    def __init__(self, x, y, max_vel, rotation_vel, img, path=[]):
        self.START_POS = (x, y)
        super().__init__(max_vel, rotation_vel, img)
        self.path = path
        self.current_point = 0
        self.vel = 1.6 * max_vel

    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255, 0, 0), point, 5)

    def draw(self, win):
        super().draw(win)
        #self.draw_points(win)

    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(x_diff / y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))

    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(
            self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            if self.current_point == len(self.path) - 1:
                self.current_point = 0
            else:
                self.current_point += 1

    def move(self):
        if self.current_point >= len(self.path):
            return

        self.calculate_angle()
        self.update_path_point()
        super().move()
        self.get_rotated_img()

    def next_level(self, level):
        self.reset()
        self.vel = 1.5 * self.max_vel + (level - 1) * 0.2
        self.current_point = 0
