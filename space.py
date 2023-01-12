import pyxel
from collections import deque
import random
# from game import Game


# parent of all object here
class Sprite:
    def __init__(self):
        pass

    @classmethod
    def setup(cls):
        # deque -> double ended que
        # like a list but quicker append and pop operations from both ends of the container
        cls.sprites = deque()

    @classmethod
    def update_all(cls):
        for sprite in cls.sprites:
            sprite.update()

    @classmethod
    def draw_all(cls):
        for sprite in cls.sprites:
            sprite.draw()


class Star(Sprite):
    frame = 0
    count = 0
    width = 8
    height = 8

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

        # so the star change shape at different frame 
        self.frame = random.randint(10,25)
        # initializing frame to put the star
        self.animation_frame = 0
    
    def update(self):
        # to make the frame move backwards
        self.x -= 2
        # // 9 -> the speed of the star animation
        # % 3 -> the amount of star animation (3 shapes)
        self.animation_frame = self.frame // 9 % 3
        # move to the next frame
        self.frame += 1

    def draw(self):
        pyxel.blt(x=self.x, y=self.y, img=0,
                  u=0, v=Star.height*self.animation_frame, w=Star.width, h=Star.height, colkey=1)
    
    @classmethod
    def append(cls):
        # cls is like self but for classmethod

        # for even entry in our deque
        if cls.count % 2 == 0:
            # appending a location for stars in random range
            # from top to half
            cls.sprites.append(
                cls(x=pyxel.width, y=random.randint(0, (pyxel.height - cls.height) // 2)))
        # for odd entry
        else:
            # from half to bottom
            cls.sprites.append(
                cls(x=pyxel.width, y=random.randint((pyxel.height - cls.height) // 2, pyxel.height - cls.height)))
        cls.count += 1

    @classmethod
    def update_all(cls):
        # after every 3 frame we append
        if cls.frame % 3 == 0:
            cls.append()
        # for every location we append to deque, update it -> add a star
        for sprite in cls.sprites.copy():
            sprite.update()
            # if it's inside the screen range, we pop the star (put it in screen)
            if sprite.x < -cls.width:
                cls.sprites.popleft()

        cls.frame += 1


class Bullet(Sprite):
    width = 8
    height = 8

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        self.animation_frame = 0
    
    def update(self):
        # how fast the bullet goes
        self.x += 4
        # how many animation frame
        self.animation_frame = self.frame % 1
        # to change the frame one at a time
        self.frame += 1
    
    def draw(self):
        pyxel.blt(x = self.x, y = self.y, img = 0, u = 8,
                    v = Bullet.height*self.animation_frame, w = Bullet.width, h = Bullet.height, colkey= 0)

    @classmethod
    def append(cls,x, y):
        # how many bullets can appear in the screen 
        if len(cls.sprites) < 5:
            cls.sprites.append(cls(x,y))
    
    @classmethod
    def update_all(cls):
        for sprite in cls.sprites.copy():
            sprite.update()
            if sprite.x > pyxel.width:
                cls.sprites.popleft()


# class Asteroid(Sprite):
#     width = 16
#     height = 16
#     frame = 0

#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#         self.vx = (1.5 * random.random() + 0.8) * \
#                 (1 + (pyxel.frame_count - Game.start_frame_count) / 600)
#         self.frame = 0
    
#     def update(self):
#         self.x -= self.vx
#         self.frame += 1
    
#     def draw(self):
#         pyxel.blt(x = int(self.x), y = self.y, img = 2,
#                   u = 0, v = 0, w = Asteroid.width, h = Asteroid.height, colkey=1)
    
#     @classmethod
#     def append(cls):
#         cls.sprites.append(cls(pyxel.width, random.randint(0, pyxel.height - cls.height)))

#     @classmethod
#     def update_all(cls):
#         if cls.frame % max(30 - )


