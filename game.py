## ------------- LIBRARY -------------- ##
import pyxel
from collections import deque
import random
import pandas as pd


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


## ----- Background Stars ------ ##
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


## ----- Spaceship Bullet ----- ##
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


## ----- Alien inside UFO (Enemy) ----- ##
class Alien(Sprite):
    width = 16
    height = 16
    frame = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

        # how fast the alien go
        self.vx = (1.7 * random.random() + Game.level)
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
        # append in random starting position
        # pyxel.width -> the very last frame of the game (right)
        cls.sprites.append(
            cls(pyxel.width, random.randint(0, pyxel.height - cls.height)))

    @classmethod
    def update_all(cls):
        if (cls.frame + 1) % 17 == 0:
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
            
            player_center_x = Player.player.x + Player.width // 2
            player_center_y = Player.player.y + Player.height // 2
            sprite_center_x = sprite.x + cls.width // 2
            sprite_center_y = sprite.y + cls.height // 2

            if (player_center_x - sprite_center_x)**2 + (player_center_y - sprite_center_y)**2 < 10**2:
                Game.state = "End"
                if sprite in cls.sprites:
                    cls.sprites.remove(sprite)
                Explosion.append(sprite.x, sprite.y)

        cls.frame += Game.level


## ----- Exploding Alien / Player ----- ##
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

    @classmethod
    def update_all(cls):
        for sprite in cls.sprites.copy():
            sprite.update()
            if sprite.animation_frame > 2:
                cls.sprites.popleft()
        


## ------ Moneyyyy (Score) ----- ##
class Coin(Sprite):
    width = 8
    height = 8
    frame = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 1.5 
        self.frame = 0
        self.animation_frame = 0

    def update(self):
        # go left
        self.x -= self.vx
        # change coin animation (4 frames)
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
        # 40 -> not too much coins
        if cls.frame % 40 == 0:
            cls.append()
        for sprite in cls.sprites.copy():
            sprite.update()
            if sprite.x < -cls.width:
                cls.sprites.remove(sprite)
                continue

            if sprite.x < Player.player.x + Player.width and Player.player.x < sprite.x + cls.width and sprite.y < Player.player.y + Player.height and Player.player.y < sprite.y + cls.height:
                if Game.state == "Playing":
                    Game.score += 1
                cls.sprites.remove(sprite)
                continue

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
        
        if pyxel.btn(pyxel.KEY_RIGHT):
            cls.player.x = min(cls.player.x + 2, pyxel.width //2)
        
        # btnp -> button pressed -> not continuous
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
    def __init__(self):
        # size of the screen
        pyxel.init(width=120, height=90, title="Space Adventure")
        pyxel.load(filename="assets/res.pyxres")

        self.setup()
        pyxel.run(self.update, self.draw)


    def setup(self):
        Game.state = 'Start'
        Game.score = 0
        Game.level = 1

        # for saving
        Game.pname = ""
        Game.saveindex = 0
        Game.save_state = 0
        Game.load_state = False

        # load save file
        # ex: {0 : [name, score], 1: [name, score]}
        savefile = pd.read_csv('load.csv')
        Game.save_dict = {k:v for k,v in zip(savefile.index, list(zip(savefile['Name'], savefile['Score'])))}


        # initialize x and y of the spaceship
        Player.setup(x = 5 , y = 50)

        # initialize deque
        Star.setup()
        Bullet.setup()
        Alien.setup()
        Explosion.setup()
        Coin.setup()
    

    def update(self):
        ## START PLAYING - NEW OR LOAD
        # new game
        if pyxel.btnp(pyxel.KEY_SPACE) and Game.state == 'Start':
            Game.state = "Playing"
            Game.start_frame_count = pyxel.frame_count
        # load saved game -> go to the load menu
        if (pyxel.btnp(pyxel.KEY_L)) and (Game.state == 'Start') and (len(Game.save_dict) > 0):
            Game.state = "Load Menu"
        
        # when game is playing -> update all
        if Game.state == "Playing":
            Star.update_all()
            Bullet.update_all()
            Alien.update_all()
            Explosion.update_all()
            Coin.update_all()
            Player.update()
        
        # when game is paused (on menu) -> let stars continue
        if Game.state == "Pause":
            Star.update_all()   

        # when the game is over -> let stars continue and left exploded spaceship there
        if Game.state == "End":
            Star.update_all()
            Explosion.update_all()


    def draw(self):
        pyxel.cls(0)

        # when the app first started - logo + instructions to start
        if Game.state == 'Start':
            # space
            pyxel.blt(x = 25, y =15, img = 0,
                    u = 0, v = 66, w = 67, h = 16, colkey=0)
            
            # adventure
            pyxel.blt(x = 28, y =30, img = 0,
                    u = 0, v = 86, w = 62, h = 8, colkey=0)
            
            # instruction 
            pyxel.text(8, 60, "Press [Space] key to start.", 15)

            # check for load
            if len(Game.save_dict) > 0:
                pyxel.text(17, 70, "Press [L] key to load.", 15)


        # when the game is playing 
        elif Game.state == 'Playing':
            Star.draw_all()
            Bullet.draw_all()
            Alien.draw_all()
            Explosion.draw_all()
            Coin.draw_all()

            Player.draw()
            pyxel.text(1, pyxel.height - 14, f"[M] Menu", 13)
            pyxel.text(1, pyxel.height - 7, f"Score: {Game.score}", 12)

            if pyxel.btnp(pyxel.KEY_M):
                Game.state = 'Pause'
            
            if (Game.score != 0) and (Game.score % 10 == 0):
                Game.level = int((Game.score / 10) + 1)

                pyxel.blt(x = 20, y=30, img=0,
                  u=0, v=96, w=72, h=16, colkey=0)
                
                pyxel.text(40, 50, f"Level {Game.level}", 14)


        # when the game is paused - logo + instruction to save or go back
        elif Game.state == "Pause":
            Star.draw_all()

            # space
            pyxel.blt(x = 25,y =15, img = 0,
                    u = 0, v = 66, w = 67, h = 16, colkey=0)
            
            # adventure
            pyxel.blt(x = 28, y =30, img = 0,
                    u = 0, v = 86, w = 62, h = 8, colkey=0)
            
            # instruction 
            pyxel.text(32, 50, "[S] save game", 11)
            pyxel.text(35, 60, "[M] go back", 11)

            # resume playing
            if pyxel.btnp(pyxel.KEY_M):
                Game.state = "Playing"

            # go to save menu
            if pyxel.btnp(pyxel.KEY_S):
                Game.state = "Save Menu"
        

        ## save menu for new game (not loaded)
        # FIRST screen - select save slot
        elif (Game.state == "Save Menu") and (Game.load_state == False) and (Game.save_state == 0):
            pyxel.text(25, 20, "Select Save Slot", 11)

            line = 30
            order = 1
            # go through the saved data and show it in order
            for i, data in list(zip(Game.save_dict.keys(), Game.save_dict.values())):
                # number [1-5]
                pyxel.text(30, line, "[" + str(order) + "]", 7)
                # name
                pyxel.text(50, line, data[0], 14)
                # score
                pyxel.text(80, line, str(data[1]), 12)
                # index & line space (y axis)
                order += 1
                line += 10

            # if the data is less than 5, we just want to show the number, to indicate the player can create a new save or rewrite the old ones
            if order <= 5:
                pyxel.text(30, line, "[" + str(order) + "]", 7)
                order += 1
                line += 10

            # listen to the user input, to record which save slot they want to save the game
            if pyxel.input_text:
                try:
                    if int(pyxel.input_text[0]) in [1,2,3,4,5]:
                        Game.saveindex = int(pyxel.input_text[0])-1
                        Game.save_state = 2
                except ValueError:
                    pass
        
        # SECOND screen - to insert name
        elif (Game.state == "Save Menu") and (Game.load_state == False) and (Game.save_state == 2):
            # instructions
            pyxel.text(35, 20, "Insert Name", 11)
            pyxel.text(27, 60, "[Enter] to save", 11)

            # listen to the keyboard inputs for player's name (Game.pname)
            if pyxel.input_text:
                if len(Game.pname) <= 10:
                    Game.pname += pyxel.input_text[0]
                else:
                    pass
            pyxel.text(35, 30, Game.pname, 9)

            # ENTER key to save the name and score in the specified index/save slot
            if pyxel.btnp(pyxel.KEY_RETURN) and Game.save_state == 2:
                pyxel.text(45, 50, "Saved!", 10)

                Game.save_dict[Game.saveindex] = [Game.pname, Game.score]

                df = pd.DataFrame(Game.save_dict.values(), columns=['Name', 'Score'])
                df.to_csv('load.csv', index=False)

                Game.save_state = 1
            
            # continue playing after saving
            if Game.save_state == 1:
                Game.state = "Playing"
                Game.save_state = 0
                Game.pname = ""
    

        # load screen - when player choose to load previous saved game
        elif Game.state == "Load Menu":
            pyxel.text(25, 20, "Select Load File", 11)

            line = 30
            order = 1
            # go through the saved data and show it in order
            for i, data in list(zip(Game.save_dict.keys(), Game.save_dict.values())):
                pyxel.text(30, line, "[" + str(order) + "]", 7)
                pyxel.text(50, line, data[0], 14)
                pyxel.text(80, line, str(data[1]), 12)
                order += 1
                line += 10
            
            # it listens to key input with this
            if pyxel.btnp(pyxel.KEY_P):
                print("P")
            
            # listen to keyboard inputs to see which save slot the player wants to load
            if pyxel.input_text:
                try:
                    if int(pyxel.input_text[0]) in list(range(1, order)):
                        Game.saveindex = int(pyxel.input_text[0]) -1
                        Game.pname = Game.save_dict[Game.saveindex][0]
                        Game.score = Game.save_dict[Game.saveindex][1]

                        Game.state = "Playing"
                        Game.start_frame_count = pyxel.frame_count
                        Game.load_state = True
                        
                except ValueError:
                    pass
        

        # save menu for loaded game
        elif (Game.state == "Save Menu") and (Game.load_state == True):
            pyxel.text(45, 50, "Saved!", 10)

            Game.save_dict[Game.saveindex] = [Game.pname, Game.score]

            df = pd.DataFrame(Game.save_dict.values(), columns=['Name', 'Score'])
            df.to_csv('load.csv', index=False)

            Game.save_state = 1
            
            # continue playing
            if Game.save_state == 1:
                Game.state = "Playing"
                Game.save_state = False

        
        # game over screen
        elif Game.state == "End":
            Star.draw_all()
            Explosion.append(Player.player.x, Player.player.y)
            Explosion.draw_all()
            # final score
            pyxel.text(1, pyxel.height - 7, f"Final Score: {Game.score}", 12)
            # game over
            pyxel.blt(x = 28, y =25, img = 1,
                    u = 16, v = 48, w = 79, h = 79, colkey=0)
            
            # to restart the game
            pyxel.text(20, 60, "Press [M] to restart", 9)
            if pyxel.btnp(pyxel.KEY_M):
                Game.state = "Start"


if __name__ == '__main__':
    Game()
