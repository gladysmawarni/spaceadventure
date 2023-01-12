import pyxel
from player import Player
from space import Star, Bullet


class Game:
    score = 0
    high_score = 0

    def __init__(self):
        pyxel.init(width=160, height=90, title="try")
        pyxel.load(filename="assets/res.pyxres")

        self.setup()
        pyxel.run(self.update, self.draw)

    def setup(self):
        Player.setup(x = 5 , y = 50)

        Star.setup()
        Bullet.setup()
        # Asteroid.setup()
    
    def update(self):
        Star.update_all()
        Bullet.update_all()
        # Asteroid.update_all()

        Player.update()

    def draw(self):
        pyxel.cls(0)

        Star.draw_all()
        Bullet.draw_all()
        # Asteroid.draw_all()

        Player.draw()


if __name__ == '__main__':
    Game()
