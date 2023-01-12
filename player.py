import pyxel
from space import Bullet


class Player:
    width = 16
    height = 16

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.frame = 10
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