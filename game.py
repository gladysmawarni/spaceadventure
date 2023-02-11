import pyxel
from collections import deque
import random


### ----------------------------------- ###
### ------------- SPRITES ------------- ###
### ----------------------------------- ###

# parent of all sprite object here
class Sprite:
    def __init__(self):
        pass

    @classmethod
    def setup(cls):
        # deque -> double ended que
        # like a list but quicker append and pop operations from both ends of the container
        cls.sprites = deque()

    # @classmethod
    # def update_all(cls):
    #     for sprite in cls.sprites:
    #         sprite.update()

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

        self.frame = 0
        # initializing animation frame to put the star
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
        # Copy the region of size (w, h) from (u, v) of the image bank img (0-2) to (x, y). 
        # If negative value is set for w and/or h, it will reverse horizontally and/or vertically. 
        # If colkey is specified, treated as transparent color.
        pyxel.blt(x=self.x, y=self.y, img=0,
                  u=0, v=Star.height*self.animation_frame, w=Star.width, h=Star.height, colkey=1)
    
    @classmethod
    def append(cls):
        # cls is like self but for classmethod

        # for even entry in our deque
        if cls.count % 2 == 0:
            # appending (to the deque) a location for stars in random range
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


class Alien(Sprite):
    width = 16
    height = 16
    frame = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

        # how fast the alien go
        self.vx = (2 * random.random() + 0.8)
        self.frame = 0
        self.animation_frame = 0
    
    def update(self):
        # go left
        self.x -= self.vx
        # change the animation of the alien
        self.animation_frame = self.frame // 5 % 2
        self.frame += 1
    
    def draw(self):
        # Copy the region of size (w, h) from (u, v) of the image bank img (0-2) to (x, y). 
        # If negative value is set for w and/or h, it will reverse horizontally and/or vertically. 
        # If colkey is specified, treated as transparent color.
        pyxel.blt(x = int(self.x), y = self.y, img = 0,
                  u = 16, v = Alien.height*self.animation_frame, w = Alien.width, h = Alien.height, colkey=0)
    
    @classmethod
    def append(cls):
        # append in random starting position (x)
        cls.sprites.append(
            cls(pyxel.width, random.randint(0, pyxel.height - cls.height)))

    @classmethod
    def update_all(cls):
        if cls.frame % max(30 - (pyxel.frame_count - Game.start_frame_count) // 600, 5) == 0:
            cls.append()
        for sprite in cls.sprites.copy():
            sprite.update()
            if sprite.x < -cls.width:
                cls.sprites.remove(sprite)
                continue
            
            # if bullet touched the alien, remove both
            # add explosion sprite
            for bullet in Bullet.sprites.copy():
                if sprite.x < bullet.x + Bullet.width and bullet.x < sprite.x + cls.width and sprite.y < bullet.y + Bullet.height and bullet.y < sprite.y + cls.height:
                    cls.sprites.remove(sprite)
                    Bullet.sprites.remove(bullet)
                    Explosion.append(sprite.x, sprite.y)
                    break

        cls.frame += 1


class Explosion(Sprite):
    count = 0
    width = 16
    height = 16

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        self.animation_frame = 0

    def update(self):
        # change explosion animation (2 frames)
        self.animation_frame = self.frame // 2
        self.frame += 1

    def draw(self):
        pyxel.blt(x=self.x, y=self.y, img=0,
                u=32, v=Explosion.height*self.animation_frame, w=Explosion.width, h=Explosion.height, colkey=0)

    @classmethod
    def append(cls, x, y):
        cls.sprites.append(cls(x=x, y=y))

    @ classmethod
    def update_all(cls):
        for sprite in cls.sprites.copy():
            sprite.update()
            if sprite.animation_frame > 2:
                cls.sprites.popleft()


class Coin(Sprite):
    width = 8
    height = 8
    frame = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 2.0 * random.random() + 0.8
        self.frame = 0
        self.animation_frame = 0

    def update(self):
        self.x -= self.vx
        self.animation_frame = self.frame // 3 % 4
        self.frame += 1

    def draw(self):
        pyxel.blt(x=int(self.x), y=self.y, img=0,
                  u=48, v=Coin.height*self.animation_frame, w=Coin.width, h=Coin.height, colkey=0)

    @classmethod
    def append(cls):
        cls.sprites.append(
            cls(pyxel.width, random.randint(0, pyxel.height - cls.height)))

    @classmethod
    def update_all(cls):
        if cls.frame % 8 == 0:
            cls.append()
        for sprite in cls.sprites.copy():
            sprite.update()
            if sprite.x < -cls.width:
                cls.sprites.remove(sprite)
                continue

            if sprite.x < Player.player.x + Player.width and Player.player.x < sprite.x + cls.width and sprite.y < Player.player.y + Player.height and Player.player.y < sprite.y + cls.height:
                # if App.game_mode == 1:
                #     App.score += 1
                cls.sprites.remove(sprite)
                continue

            for bullet in Bullet.sprites:
                if sprite.x < bullet.x + Bullet.width and bullet.x < sprite.x + cls.width and sprite.y < bullet.y + Bullet.height and bullet.y < sprite.y + cls.height:
                    cls.sprites.remove(sprite)
                    break

        cls.frame += 1



### ----------------------------------- ###
### ------------- PLAYER -------------- ###
### ----------------------------------- ###

class Player:
    width = 16
    height = 16

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.frame = 0
        self.animation_frame = 0
    
    @classmethod # bound to the class rather than its object
    def update(cls):
        cls.player.animation_frame = cls.player.frame // 3 % 2
        cls.player.frame += 1

        # min and max so it does not go past the screen 
        if pyxel.btn(pyxel.KEY_UP):
            cls.player.y = max(cls.player.y -2, 0)
        
        if pyxel.btn(pyxel.KEY_DOWN):
            cls.player.y = min(cls.player.y + 2, pyxel.height - cls.height)
        
        if pyxel.btn(pyxel.KEY_LEFT):
            cls.player.x = max(cls.player.x -2, 2)
        
        # btnp -> button pressed -> not continuous
        if pyxel.btn(pyxel.KEY_RIGHT):
            cls.player.x = min(cls.player.x + 2, pyxel.width //2)
        
        if pyxel.btnp(pyxel.KEY_SPACE):
            # from where do the bullet appears (x,y)
            # cls.width - 8 -> so it comes from behind the body of the spaceship
            # cls.height //2 -> too low | -8 -> too high | //2 -> perfectly middle
            Bullet.append(cls.player.x + cls.width - 8, 
                            cls.player.y + cls.height // 2 -8 //2)


    @classmethod
    def draw(cls):
        pyxel.blt(x = cls.player.x, y = cls.player.y, img = 1, u = 0, v = cls.height * cls.player.animation_frame,
                    w = cls.width, h = cls.height, colkey=0)
    
    @classmethod
    def setup(cls, x, y):
        cls.player = cls(x,y)


### ----------------------------------- ###
### --------------- GAME -------------- ###
### ----------------------------------- ###

class Game:
    score = 0
    high_score = 0

    def __init__(self):
        pyxel.init(width=160, height=90, title="Space Adventure")
        pyxel.load(filename="assets/res.pyxres")

        self.setup()
        pyxel.run(self.update, self.draw)

    def setup(self):
        # initialize x and y 
        Player.setup(x = 5 , y = 50)

        # initialize deque
        Star.setup()
        Bullet.setup()
        Alien.setup()
        Explosion.setup()
        Coin.setup()
    
    def update(self):
        Game.start_frame_count = pyxel.frame_count
        Star.update_all()
        Bullet.update_all()
        Alien.update_all()
        Explosion.update_all()
        Coin.update_all()

        Player.update()

    def draw(self):
        pyxel.cls(0)

        Star.draw_all()
        Bullet.draw_all()
        Alien.draw_all()
        Explosion.draw_all()
        Coin.draw_all()

        Player.draw()


if __name__ == '__main__':
    Game()
