"""
File: asteroids.py
Original Author: Br. Burton
Designed to be completed by others
This program implements the asteroids game.
"""
from abc import ABC, abstractmethod
import math
import random
import arcade

# These are Global constants to use throughout the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 30

INITIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 15

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 5

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 2

class Start_Screen(arcade.View):
    """
    Class for the main menu or starting screen
    """  
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)
        
    def on_draw(self):
        """
        This will show the title and instructions for the game
        """
        # clear the screen to begin drawing
        arcade.start_render()
        
        # displays title of game on top of screen
        arcade.draw_text("Asteroid Shooting Game", SCREEN_WIDTH/2, SCREEN_HEIGHT-80,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
        
        #Text for instructions
        arcade.draw_text("Instructions: Shoot all the asteroids on the screen with the SPACEBAR.", SCREEN_WIDTH/2, SCREEN_HEIGHT-110,
                         arcade.color.BLACK, font_size=15, anchor_x="center")
        #Text for game modes
        arcade.draw_text("Press 'e' for easy mode", SCREEN_WIDTH/2, SCREEN_HEIGHT-250,
                         arcade.color.RED, font_size=20, anchor_x="center")
        arcade.draw_text("Press 'n' for normal mode", SCREEN_WIDTH/2, SCREEN_HEIGHT-300,
                         arcade.color.RED, font_size=20, anchor_x="center")
        arcade.draw_text("Press 'h' for hard mode", SCREEN_WIDTH/2, SCREEN_HEIGHT-350,
                         arcade.color.RED, font_size=20, anchor_x="center")
        
    def on_key_press(self, key: int, modifiers: int):
        """
        The player can either choose easy mode, normal mode, and hard mode
        depending on which keyboard key they press.
        """      
        if key == arcade.key.E:
            game = Easy()
            self.window.show_view(game)
        elif key == arcade.key.N:
            game = Normal()
            self.window.show_view(game)
        elif key == arcade.key.H:
            game = Hard()
            self.window.show_view(game)

class Point:
    """
    Class responsible for x and y coordinates for positions of objects
    """
    def __init__(self):
        self.x = random.uniform(0, SCREEN_WIDTH)
        self.y = random.uniform(0, SCREEN_HEIGHT)
        
class Velocity:
    """
    Class responsible for velocity of moving objects
    """
    def __init__(self):
        self.dx = 0.0
        self.dy = 0.0

class FlyingObjects(ABC):
    """
    This is the parent class for these flying objects:
    Ship
    Bullets
    Asteroid
    """
    def __init__(self, img, radius):
        self.center = Point()
        self.velocity = Velocity()
        self.alive = True
        self.radius = radius
        self.alpha = 255
        self.image = img
        self.texture = arcade.load_texture(self.image)
        self.width = self.texture.width
        self.height = self.texture.height
        self.direction = 1
        self.angle = 0.0
        self.speed = 0.0
        
    def advance(self):
        """
        Function responsible to move objects forward and move.
        """
        #when objects are advancing, self.wrap() is called to
        #check if the advancing objects are off the screen's boundaries
        #to wrap correctly
        self.wrap()
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy

    def is_alive(self):
        """
        Returns condition of flying object (whether if it's alive or not).
        """
        return self.alive
    
    @abstractmethod
    def draw(self):
        """
        Draws all images for each flying object
        Draw should be an abstract method in base classes and overridden 
        """
        pass
    
    def wrap(self):
        """
        If an object goes off the right edge of the screen,
        it should appear on the left edge.
        """
        if self.center.x > SCREEN_WIDTH:
            self.center.x -= SCREEN_WIDTH
        elif self.center.x < 0:
            self.center.x += SCREEN_WIDTH
        elif self.center.y > SCREEN_HEIGHT:
            self.center.y -= SCREEN_HEIGHT
        elif self.center.y < 0:
            self.center.y += SCREEN_HEIGHT
    
class Asteroid(FlyingObjects, ABC):
    """
    Parent class for different types of asteroids
    """
    def __init__(self, img, radius):
        """
        Calls parent class and asks for img and radius to be passed as parameters
        """
        super().__init__(img, radius)
    
    @abstractmethod
    def advance(self):
        """
        Needs to be overridden by subclasses
        and each differs by amount of degrees for rotation
        """
        pass
        
class Large_Asteroids(Asteroid):
    """
    Class for large asteroids
    """
    def __init__(self):
        """
        Calls parent class and passes the image path and radius to parameters
        """
        super().__init__("asteroid_file/meteorGrey_big1.png", BIG_ROCK_RADIUS)
        #Moves at 1.5 pixels per frame, at a random initial direction.
        self.speed = BIG_ROCK_SPEED
        self.velocity.dx = math.cos(math.radians(self.direction)) * self.speed
        self.velocity.dy = math.sin(math.radians(self.direction)) * self.speed
        
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width, self.height, self.texture, self.angle, self.alpha)
        
    def advance(self):
        """
        Rotates at 1 degree per frame.
        """
        self.angle += BIG_ROCK_SPIN
        self.wrap()
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
        
    def split(self, asteroids):
        """
        If a large asteroid gets hit, it breaks apart and becomes two medium asteroids and one small one.
        """
        #calls Medium_Asteroids() object to spawn medium asteroid
        medium1 = Medium_Asteroids()
        #will have same coordinates as large rock
        medium1.center.x = self.center.x
        medium1.center.y = self.center.y
        #The first medium asteroid has the same velocity as the original
        #large one plus 2 pixel/frame in the up direction.
        medium1.velocity.dy = self.velocity.dy + 2
        
        medium2 = Medium_Asteroids()
        medium2.center.x = self.center.x
        medium2.center.y = self.center.y
        #The second medium asteroid has the same velocity as the original
        #large one plus 2 pixel/frame in the down direction.
        medium2.velocity.dy = self.velocity.dy - 2
        
        small = Small_Asteroids()
        small.center.x = self.center.x
        small.center.y = self.center.y
        #The small asteroid has the original velocity plus 5 pixels/frame to the right.
        small.velocity.dx = self.velocity.dx + 5
        
        #asteroids = self.asteroids list
        asteroids.append(medium1)
        asteroids.append(medium2)
        asteroids.append(small)
        self.alive = False
        
class Medium_Asteroids(Asteroid):
    """
    Class for medium asteroids
    """
    def __init__(self):
        super().__init__("asteroid_file/meteorGrey_med1.png", MEDIUM_ROCK_RADIUS)
        
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width, self.height, self.texture, self.angle, self.alpha)
        
    def advance(self):
        """
        Rotates at -2 degrees per frame.
        """
        self.angle += MEDIUM_ROCK_SPIN
        self.wrap()
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
        
    def split(self, asteroids):
        """
        If hit, it breaks apart and becomes two small asteroids.
        """
        small1 = Small_Asteroids()
        #will have same coordinates as medium rock
        small1.center.x = self.center.x
        small1.center.y = self.center.y
        #The small asteroid has the same velocity as the original medium one
        #plus 1.5 pixels/frame up and 1.5 pixels/frame to the right.
        small1.velocity.dx = self.velocity.dx + 1.5
        small1.velocity.dy = self.velocity.dy + 1.5
        
        small2 = Small_Asteroids()
        small2.center.x = self.center.x
        small2.center.y = self.center.y
        #The second, 1.5 pixels/frame down and 1.5 to the left.
        small2.velocity.dx = self.velocity.dx - 1.5
        small2.velocity.dy = self.velocity.dy - 1.5
        
        asteroids.append(small1)
        asteroids.append(small2)
        self.alive = False
        
class Small_Asteroids(Asteroid):
    """
    Class for small asteroids
    """
    def __init__(self):
        super().__init__("asteroid_file/meteorGrey_small1.png", SMALL_ROCK_RADIUS)
        
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width, self.height, self.texture, self.angle, self.alpha)
        
    def advance(self):
        """
        Rotates at 5 degrees per frame.
        """
        self.angle += SMALL_ROCK_SPIN
        self.wrap()
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
        
    def split(self, asteroids):
        """
        If a small asteroid is hit, it is destroyed and removed from the game.
        """
        self.alive = False 
        
class Ship(FlyingObjects):
    """
    Class for the ship which user can control with keyboard
    """
    def __init__(self):
        super().__init__("asteroid_file/playerShip1_green.png", SHIP_RADIUS)
        #Ship needs an angle or orientation
        self.angle = 1
        self.center.x = SCREEN_WIDTH/2
        self.center.y = SCREEN_HEIGHT/2
        
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width, self.height, self.texture, self.angle, self.alpha)
        
    def turn_left(self):
        """
        The left arrow rotates the ship 3 degrees to the left.
        """
        self.angle += SHIP_TURN_AMOUNT
    
    def turn_right(self):
        """
        The right arrow rotates the ship 3 degrees to the right.
        """
        self.angle -= SHIP_TURN_AMOUNT
    
    def up_thrust(self):
        """
        The up arrow will increase the velocity in the direction the ship is pointed by 0.25 pixels/frame.
        """
        self.velocity.dx -= math.sin(math.radians(self.angle)) * SHIP_THRUST_AMOUNT
        self.velocity.dy += math.cos(math.radians(self.angle)) * SHIP_THRUST_AMOUNT
        
    def down_thrust(self):
        """
        The down arrow will decrease the velocity in the direction the ship is pointed by 0.25 pixels/frame.
        """
        self.velocity.dx += math.sin(math.radians(self.angle)) * SHIP_THRUST_AMOUNT
        self.velocity.dy -= math.cos(math.radians(self.angle)) * SHIP_THRUST_AMOUNT
        
 
class Heart(FlyingObjects):
    """
    Class for the ship's lives
    """
    def __init__(self):
        super().__init__("asteroid_file/heart.png", None)
        
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width, self.height, self.texture, self.angle, self.alpha)
        
    def split(self, hearts):
        self.alive = False

class Heart_List:
    """
    This class will create 3 lives for the player's ship
    """
    def __init__(self, hearts):
        heart1 = Heart()
        heart1.center.x = SCREEN_WIDTH/1.3
        heart1.center.y = SCREEN_HEIGHT-30
        heart2 = Heart()
        heart2.center.x = SCREEN_WIDTH/1.2
        heart2.center.y = SCREEN_HEIGHT-30
        heart3 = Heart()
        heart3.center.x = SCREEN_WIDTH/1.1
        heart3.center.y = SCREEN_HEIGHT-30
        hearts.append(heart1)
        hearts.append(heart2)
        hearts.append(heart3)
        
class Bullet(FlyingObjects):
    """
    Class for bullets that comes out of ship when user presses space bar
    """
        #Bullet class will take ship's angle and coordinates to determine where to shoot
    def __init__(self, ship_angle, ship_x, ship_y):
        super().__init__("asteroid_file/laserBlue01.png", BULLET_RADIUS)
        #Bullets only live for 60 frames, after which they should "die"
        #and be removed from the game.
        self.lives = BULLET_LIFE
        #Bullets should start with the same velocity of the ship (speed and direction)
        #plus 10 pixels per frame in the direction the ship is pointed. 
        self.speed = BULLET_SPEED
        #rotates bullet image by 90 degrees counter clockwise
        self.angle = ship_angle-90
        self.center.x = ship_x
        self.center.y = ship_y
        
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width, self.height, self.texture, self.angle, self.alpha)
    
    def advance(self):
        """
        Overrides advance() from parent
        """
        super().advance()
        #self.lives decrements as it moves
        self.lives -= 1
        #if there are no more self.lives(equal or greater to 0), bullet is no longer alive
        if self.lives <= 0:
            self.alive = False
    
    def fire(self):
        """
        Bullets are should start with the same velocity of the ship (speed and direction)
        plus 10 pixels per frame in the direction the ship is pointed.
        """
        #+90 is added to angle to make sure bullet's direction is positioned correctly from ship's direction
        self.velocity.dx -= math.sin(math.radians(self.angle+90)) * BULLET_SPEED
        self.velocity.dy += math.cos(math.radians(self.angle+90)) * BULLET_SPEED

class Alien(FlyingObjects):
    """
    Class for enemy alien ship that will shoot asteroids at the player
    """
    def __init__(self):
        super().__init__("asteroid_file/ufo.png", None)
        
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width, self.height, self.texture, self.angle, self.alpha)
        
class Enemy_Bullets(FlyingObjects):
    """
    Class for enemy's projectiles or asteroids
    """
    def __init__(self, alien_angle, alien_x, alien_y):
        super().__init__("asteroid_file/asteroid.png", BULLET_RADIUS)
        self.speed = BULLET_SPEED
        self.angle = alien_angle
        self.center.x = alien_x
        self.center.y = alien_y
      
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width, self.height, self.texture, self.angle, self.alpha)
    
    def advance(self):
        """
        Overrides advance() from parent class. Enemy asteroids will
        only be "dead" or removed from the list once it is out of
        the screen's boundaries
        """
        super().advance()
        if self.center.x > SCREEN_WIDTH:
            self.alive = False
        elif self.center.y > SCREEN_HEIGHT:
            self.alive = False
        elif self.center.x < 0:
            self.alive = False
        elif self.center.y < 0:
            self.alive = False
            
    def fire(self):
        self.velocity.dx -= math.sin(math.radians(self.angle+270)) * BULLET_SPEED
        self.velocity.dy += math.cos(math.radians(self.angle+270)) * BULLET_SPEED
  
class Easy(arcade.View):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class.
    """

    def __init__(self):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__()

        self.held_keys = set()

        # TODO: declare anything here you need the game class to track
        self.asteroids = []
        self.bullets = []
        self.ships = []

        #5 Large Asteroids to be appended to asteroids list
        for i in range(INITIAL_ROCK_COUNT):
            Large = Large_Asteroids()
            self.asteroids.append(Large)
            
        self.ships.append(Ship())
        
        #Sounds for the game
        #All sound resources are from the arcade library
        self.shoot_sound = arcade.sound.load_sound("asteroid_file/hurt5.wav")
        self.collide_sound = arcade.sound.load_sound("asteroid_file/laser3.wav")
        self.victory_sound = arcade.sound.load_sound("asteroid_file/coin1.wav")
              
    def on_show(self):
        arcade.set_background_color(arcade.color.SMOKY_BLACK)
        
    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # TODO: draw each object
        for asteroid in self.asteroids:
            asteroid.draw()
            
        for bullet in self.bullets:
            bullet.draw()
            
        for ship in self.ships:
            ship.draw()
            
        #Instruction on how to pause the game 
        arcade.draw_text("Press Esc. to pause the game", SCREEN_WIDTH/2, SCREEN_HEIGHT-40,
                         arcade.color.WHITE, font_size=15, anchor_x="center")
                      
    def remove_deadObjects(self):
        """
        Removes dead objects from screen
        """
        for bullet in self.bullets:
            #if bullet is dead, remove it from the list
            if not bullet.alive:
                self.bullets.remove(bullet)
                
        for asteroid in self.asteroids:
            if not asteroid.alive:
                self.asteroids.remove(asteroid)
         
        for ship in self.ships:
            if not ship.alive:
                self.ships.remove(ship)
    
    def check_asteroids(self):
        """
        This will check how many asteroids are left in the screen to show victory screen
        """
        if len(self.asteroids) <= 0:
            victory = Victory(Normal())
            self.victory_sound.play()
            self.window.show_view(victory)
                                      
    def check_collisions(self):
        """
        Checks when flying objects collide
        """
        for bullet in self.bullets:
            for asteroid in self.asteroids:
                #bullet and asteroid both need to be alive for collision detection  
                if bullet.alive and asteroid.alive:
                    #max distance between the two flying objects
                    too_close = asteroid.radius + bullet.radius
                    #if the positions of asteroid and bullet are within close proximity,
                    #check if the proximity is below the max distance and detect collision
                    if abs(asteroid.center.x - bullet.center.x) < too_close and abs(asteroid.center.y - bullet.center.y) < too_close:
                        bullet.alive = False
                        asteroid.split(self.asteroids)
           
        
       #same logic but with asteroids and the ship
        for asteroid in self.asteroids:
                for ship in self.ships:
                    if asteroid.alive and ship.alive:
                        too_close = ship.radius + asteroid.radius
                        if abs(ship.center.x - asteroid.center.x) < too_close and abs(ship.center.y - asteroid.center.y) < too_close:
                            #once ship gets hit by asteroid, it disappears from screen
                            #along with the asteroid that caused the impact
                            #a sound is also played for every collision
                            self.collide_sound.play()
                            ship.alive = False
                            asteroid.alive = False
                            #A new ship is made after every collision
                            self.ships.append(Ship())
        
        #Move to victory screen once all asteroids are destroyed 
        self.check_asteroids()                   
                            
    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()

        # TODO: Tell everything to advance or move forward one step in time
        for asteroid in self.asteroids:
            asteroid.advance()
            
        for bullet in self.bullets:
            bullet.advance()
            
        for ship in self.ships:
            ship.advance()
            
        #calls remove_deadObjects() as objects advance
        self.remove_deadObjects()
        
        # TODO: Check for collisions
        self.check_collisions()
        

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        for ship in self.ships:
            
            if arcade.key.LEFT in self.held_keys:
                ship.turn_left()
                
            if arcade.key.RIGHT in self.held_keys:
                ship.turn_right()
                
            if arcade.key.UP in self.held_keys:
                ship.up_thrust()

            if arcade.key.DOWN in self.held_keys:
                ship.down_thrust()

            # Machine gun mode...
            #if arcade.key.SPACE in self.held_keys:
            #    pass


    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        for ship in self.ships:
            if ship.alive:
                self.held_keys.add(key)
                
                if key == arcade.key.SPACE:
                    # TODO: Fire the bullet here!
                    #Passes ship's angle, x coordinate, and the y coordinate
                    #to the bullet as parameters
                    bullet = Bullet(ship.angle, ship.center.x, ship.center.y)
                    self.bullets.append(bullet)
                    bullet.fire()
                    self.shoot_sound.play()
        
        if key == arcade.key.ESCAPE:
            #Pause() class takes parameter game_view and current game mode is passed to preserve view's state
            pause = Pause(self)
            #shows pause screen
            self.window.show_view(pause)

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)

class Normal(Easy):
    """
    Normal mode class will inherit from Easy() and override certain methods
    to include a "lives" system for the ship
    """
    def __init__(self):
        """
        self.hearts represents the list of lives for the player's ship
        """
        super().__init__()
        self.hearts = []
        Heart_List(self.hearts)
        
    def on_draw(self):
        """
        Draws the hearts for the ship
        """
        super().on_draw()
        for heart in self.hearts:
            heart.draw()
        
    def remove_deadObjects(self):
        super().remove_deadObjects()
        for heart in self.hearts:
            if not heart.alive:
                self.hearts.remove(heart)
                
    def check_asteroids(self):
        """
        Overrides victory screen
        """
        super().check_asteroids()
        if len(self.asteroids) <= 0:
            victory = Victory(Hard())
            self.victory_sound.play()
            self.window.show_view(victory)
                
    def check_collisions(self):
        """
        Overriden to include ship's lives
        """
        for bullet in self.bullets:
            for asteroid in self.asteroids: 
                if bullet.alive and asteroid.alive:
                    too_close = asteroid.radius + bullet.radius
                    if abs(asteroid.center.x - bullet.center.x) < too_close and abs(asteroid.center.y - bullet.center.y) < too_close:
                        bullet.alive = False
                        asteroid.split(self.asteroids)
           
        #A ship only has 3 lives/hearts, and it will show a "game over" screen
        #once all hearts are lost from collisions
        if len(self.hearts) > 0:
            for asteroid in self.asteroids:
                for ship in self.ships:
                    for heart in self.hearts:
                        if asteroid.alive and ship.alive and heart.alive:
                            too_close = ship.radius + asteroid.radius
                            if abs(ship.center.x - asteroid.center.x) < too_close and abs(ship.center.y - asteroid.center.y) < too_close:
                                self.collide_sound.play()
                                ship.alive = False
                                asteroid.alive = False
                                heart.split(self.hearts)
                                self.ships.append(Ship())
        
        self.check_asteroids()
                            
        if len(self.hearts) <= 0:
            game_over = Game_Over(Normal())
            self.window.show_view(game_over)
            
class Hard(Normal):
    """
    This class is the hard mode for the game which includes
    an enemy alien ship shooting asteroids at the player
    """
    def __init__(self):
        """
        Overrides Normal's __init__ method to include
        the enemy, enemy bullet list, and a frame count
        """
        super().__init__()
        self.enemy_bullets = []
        self.frame_count = 0
        self.alien = Alien()
        
    def on_draw(self):
        super().on_draw()
        self.alien.draw()
        for enemy in self.enemy_bullets:
            enemy.draw()
            
    def remove_deadObjects(self):
        super().remove_deadObjects()
        for enemy in self.enemy_bullets:
            if not enemy.alive:
                self.enemy_bullets.remove(enemy)
                
    def check_asteroids(self):
        """
        Overrides victory screen
        """
        super().check_asteroids()
        if len(self.asteroids) <= 0:
            victory = Final_Victory(Easy())
            self.victory_sound.play()
            self.window.show_view(victory)
    
    def check_collisions(self):
        """
        This overrides original check_collisions() method to include logic with the 
        enemy alien's asteroids colliding with the ship
        """
        super().check_collisions()
        for bullet in self.bullets:
            for enemy in self.enemy_bullets:  
                if bullet.alive and enemy.alive:
                    too_close = enemy.radius + bullet.radius
                    if abs(enemy.center.x - bullet.center.x) < too_close and abs(enemy.center.y - bullet.center.y) < too_close:
                        bullet.alive = False
                        enemy.alive = False
                                
        if len(self.hearts) > 0:
            for enemy in self.enemy_bullets:
                for ship in self.ships:
                    for heart in self.hearts:
                        if enemy.alive and ship.alive and heart.alive:
                            too_close = ship.radius + enemy.radius
                            if abs(ship.center.x - enemy.center.x) < too_close and abs(ship.center.y - enemy.center.y) < too_close:
                                self.collide_sound.play()
                                ship.alive = False
                                enemy.alive = False
                                heart.split(self.hearts)
                                self.ships.append(Ship())
        
        self.check_asteroids()                     
        
        if len(self.hearts) <= 0:
            game_over = Game_Over(Hard())
            self.window.show_view(game_over)
    
    def update(self, delta_time):
        """
        update() function is overriden to include enemy shooting projectiles every 60 frames
        """
        super().update(delta_time)
        self.frame_count +=1
        
        for enemy in self.enemy_bullets:
            enemy.advance()
       
        #starting initial positions for the enemy alien
        self.alien.center.x = SCREEN_WIDTH/8
        self.alien.center.y = SCREEN_HEIGHT-80
            
        for ship in self.ships:
            #calculate where the enemy will face
            x_destination = ship.center.x
            y_destination = ship.center.y
                
            x_diff = x_destination - self.alien.center.x
            y_diff = y_destination - self.alien.center.y
            angle = math.atan2(y_diff, x_diff)
            
            #This will make enemy face the current direction of the player
            self.alien.angle = math.degrees(angle)- 270 
            if self.frame_count % 60 == 0:
                #The enemy will fire asteroids after every 60 frames
                enemy_bullet = Enemy_Bullets(math.degrees(angle), self.alien.center.x, self.alien.center.y)
                self.enemy_bullets.append(enemy_bullet)
                enemy_bullet.fire()
                
class Pause(arcade.View):
    """
    This class is responsible for pausing the game
    """
    
    def __init__(self, game_view):
        super().__init__()
        #self.game_view represents the ongoing game for resuming purposes
        self.game_view = game_view

    def on_show(self):
        arcade.set_background_color(arcade.color.ARSENIC)

    def on_draw(self):
        """
        Called to draw things needed for pause screen
        """
        arcade.start_render()

        arcade.draw_text("Paused", SCREEN_WIDTH/2, SCREEN_HEIGHT/2+50,
                         arcade.color.WHITE, font_size=50, anchor_x="center")

        #Instructions displayed for resuming and going back to the main menu
        arcade.draw_text("Press Esc. to return",
                         SCREEN_WIDTH/2,
                         SCREEN_HEIGHT/2,
                         arcade.color.WHITE,
                         font_size=15,
                         anchor_x="center")        
        arcade.draw_text("Press Enter to go back to starting screen",
                         SCREEN_WIDTH/2,
                         SCREEN_HEIGHT/2-30,
                         arcade.color.WHITE,
                         font_size=15,
                         anchor_x="center")

    def on_key_press(self, key, _modifiers):
        """
        If Esc. key is pressed, game is paused
        If Enter key is pressed, it goes back to starting screen 
        """
        if key == arcade.key.ESCAPE:   # resume game
            self.window.show_view(self.game_view)
            
        elif key == arcade.key.ENTER: #go back to starting screen or main menu
            start = Start_Screen()
            self.window.show_view(start)
            
class Game_Over(arcade.View):
    """
    This class is responsible for the Game Over Screen which will appear
    once the player loses all the ship's lives
    """
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        
        arcade.draw_text("Game Over", SCREEN_WIDTH/2, SCREEN_HEIGHT/2+50,
                         arcade.color.WHITE, font_size=50, anchor_x="center")

        #Instructions for restarting game and going back to main menu
        arcade.draw_text("Press r to restart game",
                         SCREEN_WIDTH/2,
                         SCREEN_HEIGHT/2,
                         arcade.color.WHITE,
                         font_size=15,
                         anchor_x="center")
        
        arcade.draw_text("Press Enter to go back to the main menu",
                         SCREEN_WIDTH/2,
                         SCREEN_HEIGHT/2-30,
                         arcade.color.WHITE,
                         font_size=15,
                         anchor_x="center")
        
    def on_key_press(self, key, _modifiers):
        """
        If r key is pressed, it will restart game
        If Enter key is pressed, it will go back
        to main menu
        """
        if key == arcade.key.R:
            self.window.show_view(self.game_view)
        elif key == arcade.key.ENTER:
            main_menu = Start_Screen()
            self.window.show_view(main_menu)
            
class Victory(arcade.View):
    """
    This class is responsible for the victory screen that will appear
    once the player shoots all the asteroids on the screen
    """
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        
        arcade.draw_text("Congratulations! You have won!", SCREEN_WIDTH/2, SCREEN_HEIGHT/2+50,
                         arcade.color.BLACK, font_size=25, anchor_x="center")

        #Instructions for continuing to next level and going back to main menu        
        arcade.draw_text("Press Enter to go back to the main menu",
                         SCREEN_WIDTH/2,
                         SCREEN_HEIGHT/2,
                         arcade.color.BLACK,
                         font_size=15,
                         anchor_x="center")
        arcade.draw_text("Click your mouse if you want to continue to the next game mode",
                         SCREEN_WIDTH/2,
                         SCREEN_HEIGHT/2-30,
                         arcade.color.BLACK,
                         font_size=15,
                         anchor_x="center")
        
    def on_key_press(self, key, _modifiers):
        """
        If Enter key is pressed, it will go back to main menu
        """
        if key == arcade.key.ENTER:
            main_menu = Start_Screen()
            self.window.show_view(main_menu)
            
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """
        When player clicks mouse/trackpad, it will move on to the next game mode.
        """
        game = self.game_view
        self.window.show_view(game)
        
class Final_Victory(Victory):
    """
    This class will show the final victory screen once the
    player completes all game modes or only the hard mode
    """   
    def on_draw(self):
        super().on_draw()
        arcade.start_render()
        #attributes needed for the trophy image
        alpha = 255
        image = "asteroid_file/award.png"
        texture = arcade.load_texture(image)
        width = texture.width
        height = texture.height
        angle = 1
        
        arcade.draw_text("Congratulations! You've completed hard mode!", SCREEN_WIDTH/2, SCREEN_HEIGHT/2+50,
                         arcade.color.BLACK, font_size=25, anchor_x="center")
        
        arcade.draw_texture_rectangle(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, width, height, texture, angle, alpha)

        #Instructions for restarting on easy mode and going back to main menu       
        arcade.draw_text("Press Enter to go back to the main menu",
                         SCREEN_WIDTH/2,
                         SCREEN_HEIGHT/2-100,
                         arcade.color.BLACK,
                         font_size=15,
                         anchor_x="center")
        arcade.draw_text("Press r to restart game on easy mode",
                         SCREEN_WIDTH/2,
                         SCREEN_HEIGHT/2-130,
                         arcade.color.BLACK,
                         font_size=15,
                         anchor_x="center")
        
    def on_key_press(self, key, _modifiers):
        """
        Override on_key_press() method
        If r is pressed, it will go back to easy mode
        and restart game. If Enter key is pressed,
        it will go back to main menu
        """
        if key == arcade.key.ENTER:
            main_menu = Start_Screen()
            self.window.show_view(main_menu)
        if key == arcade.key.R:
            restart = self.game_view
            self.window.show_view(restart)
            
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """
        Overrides previous method
        """
        pass
                  
"""
Credits and authors for the alien, hearts, purple asteroid, and trophy icons:
https://www.flaticon.com/authors/pixel-buddha
https://www.flaticon.com/authors/kiranshastry
https://www.flaticon.com/authors/good-ware
https://www.flaticon.com/authors/freepik
"""

# Creates the game and starts it going
window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT)
start = Start_Screen()
window.show_view(start)
arcade.run()


