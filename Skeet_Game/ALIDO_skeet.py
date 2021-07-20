"""
File: skeet.py
Original Author: Br. Burton
Designed to be completed by others
This program implements an awesome version of skeet.
"""
import arcade
import math
import random

from abc import ABC, abstractmethod

# These are Global constants to use throughout the game
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500

RIFLE_WIDTH = 100
RIFLE_HEIGHT = 20
RIFLE_COLOR = arcade.color.DARK_RED

BULLET_RADIUS = 3
BULLET_COLOR = arcade.color.BLACK_OLIVE
BULLET_SPEED = 10

TARGET_RADIUS = 20
TARGET_COLOR = arcade.color.CARROT_ORANGE

#Changing radius to SIDE since target isn't a circle
TARGET_SAFE_COLOR = arcade.color.AIR_FORCE_BLUE
#TARGET_SAFE_RADIUS = 15
TARGET_SAFE_SIDE = 15

class Point():
    """
    Class for creating x and y coordinates
    Point class (likely just an x and y).
    """
    def __init__(self):
        """
        The initial position of the target is anywhere along the top half of the left side the screen.
        """
        self.x = 0
        self.y = random.uniform(SCREEN_HEIGHT/2, SCREEN_HEIGHT)
    
class Velocity():
    """
    Class responsible for the velocity of moving objects
    Velocity class (likely just a dx and dy).
    """
    def __init__(self):
        """
        The vertical component of the velocity should be between -2 and +5 pixels/frame.
        The horizontal component of the velocity should be between 1 and 5 pixels/frame.
        """
        self.dx = random.uniform(1, 5)
        self.dy = random.uniform(-2, 5)
    
class FlyingObject():
    """
    Base class for the flying objects
    """
    def __init__(self):
        #self.center = Point
        self.center = Point()
        #self.velocity = Velocity
        self.velocity = Velocity()
        #self.alive is responsible for to determine if flying object (either bullet or target) is still alive or not
        #self.alive = Boolean
        self.alive = True
        #self.radius = float
        self.radius = 0.0 
    
    def advance(self):
        """
        Responsible for objects' movement
        """
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
        return
    
    def is_off_screen(self, screen_width, screen_height):
        """
        There is no limit to the number of targets & bullets that can be on the screen at a time,
        but they should be removed from the game when they leave the screen.
        """
        if self.center.x > SCREEN_WIDTH or self.center.y > SCREEN_HEIGHT:
            self.alive = False
        return
    
class Target(FlyingObject, ABC):
    """
    Target class will implement abstract methods
    
    advance() and is_off_screen() are already inherited from FlyingObject base class.
    """
    def __init__(self):
        super().__init__()
        #super().__init__() called to overwrite float value 0.0 from base class
        self.radius = float(TARGET_RADIUS)
        
    """
    Functions draw() and hit() are both abstract methods that all the target subclasses need to override
    """
    @abstractmethod
    def draw(self):
        pass
    
    @abstractmethod
    def hit(self):
        pass
    
class Standard(Target):
    """
    Inherits from Target class
    
    Standard target as first type of target created which is destroyed with one hit.        
    """    
    def draw(self):
        """
        Rendered as a circle with a 20px diameter.
        """
        arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, TARGET_COLOR)
        return
    
    def hit(self):
        """
        1 point is awarded for hitting it.
        """
        return 1
    
class Safe(Target):
    """
    Inherits from Target class
    
    Safe target as second type of target which should not be hit.
    """
    
    def draw(self):
        """
        Rendered as a square.
        """
        arcade.draw_rectangle_filled(self.center.x, self.center.y, TARGET_SAFE_SIDE, TARGET_SAFE_SIDE, TARGET_SAFE_COLOR)
        
    def hit(self):
        """
        A penalty of 10 points is incurred if this target is hit.
        """
        return -10
    
class Strong(Target):
    """
    Inherits from Target class
    
    Strong target as third type of target created which is destroyed with three hits.           
    """
    
    def __init__(self):
        """
        The strong target should move more slowly than the others as defined below.
        The vertical component of the velocity should be between 1 and 3 pixels/frame.
        The horizontal component of the velocity should be between -2 and 3 pixels/frame.
        """
        super().__init__()
        self.velocity.dx = random.uniform(-2, 3)
        self.velocity.dy = random.uniform(1, 3)
        """
        self.lives represents number of hits required for target to disappear
        """
        self.lives = 3
        
    def draw(self):
        """
        Rendered as a circle with a number inside of it.
        """
        arcade.draw_circle_outline(self.center.x, self.center.y, self.radius, TARGET_COLOR)
        text_x = self.center.x - (self.radius / 2)
        text_y = self.center.y - (self.radius / 2)
        arcade.draw_text(repr(self.lives), text_x, text_y, TARGET_COLOR, font_size=20)
    
    def hit(self):
        """
        It takes 3 hits to destroy this target.
        1 point is awarded for each of the first two hits.
        5 points are awarded for the third hit that destroys the target.
        """
        if self.lives >= 2:
            self.lives -= 1 #decrement number of lives by number of hits
            self.alive = True #target stays alive if self.lives is not 1
            return 1
        else:
            self.lives -= 1
            self.alive = False #destroys target completely
            return 5
               
    
class Bullet(FlyingObject):
    """
    Subclass of FlyingObject which is responsible for creating bullets to shoot targets on screen.
    
    There is no limit to the number of bullets.

    Clicking the mouse fires a new bullet.

    New bullets should be aimed in the direction of the rifle.

    Bullets should be removed if they leave the borders of the screen.
    
    advance() and is_off_screen class are inherited from base class FlyingObject()
    """
    def __init__(self):
        """
        Starts bullets at the corner of screen (inside the rifle)
        """
        #super().__init__() is needed and called to overwrite values for member variables set in FlyingObject() class
        super().__init__()
        self.center.x = 0
        self.center.y = 0
        self.radius = float(BULLET_RADIUS)
        
    def draw(self):
        """
        Rendered as a filled-in circle.
        """
        arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, BULLET_COLOR)
        return
        
    def fire(self, angle:float):
        """
        Bullets travel at 10 pixels/frame at that angle at which they are fired.
        """
        self.velocity.dx = math.cos(math.radians(angle)) * BULLET_SPEED
        self.velocity.dy = math.sin(math.radians(angle)) * BULLET_SPEED
        return
    
class Rifle:
    """
    The rifle is a rectangle that tracks the mouse.
    """
    def __init__(self):
        self.center = Point()
        self.center.x = 0
        self.center.y = 0
        self.angle = 45

    def draw(self):
        arcade.draw_rectangle_filled(self.center.x, self.center.y, RIFLE_WIDTH, RIFLE_HEIGHT, RIFLE_COLOR, self.angle)
        return
    
class Start_Screen(arcade.View):
    """
    Starting screen which will explain instructions and each target's point/s
    """  
    def on_show(self):
        """
        Called when arcade.View is used to modify background of window
        """
        arcade.set_background_color(arcade.color.WHITE)
        
    def on_draw(self):
        """
        Function that handles drawing things needed for starting screen
        """
        # clear the screen to begin drawing
        arcade.start_render()
        
        # displays title of game on top of screen
        arcade.draw_text("Skeet Shooting Game", SCREEN_WIDTH/2, SCREEN_HEIGHT-80,
                         arcade.color.BLUE, font_size=30, anchor_x="center")
    
        #Text for instructions
        arcade.draw_text("Instructions: Shoot targets using your mouse/trackpad.", SCREEN_WIDTH/2, SCREEN_HEIGHT-110,
                         arcade.color.AO, font_size=15, anchor_x="center")
        
        #Text for target and points
        #Standard target
        arcade.draw_circle_filled(SCREEN_WIDTH/3.1, SCREEN_HEIGHT-150, TARGET_RADIUS, TARGET_COLOR)
        arcade.draw_text("= 1 point", SCREEN_WIDTH/2.61, SCREEN_HEIGHT-165,
                         arcade.color.BLACK, font_size=20)
        #Safe target
        arcade.draw_rectangle_filled(SCREEN_WIDTH/3.1, SCREEN_HEIGHT-200, TARGET_SAFE_SIDE, TARGET_SAFE_SIDE, TARGET_SAFE_COLOR)
        arcade.draw_text("= -10 points", SCREEN_WIDTH/2.61, SCREEN_HEIGHT-215,
                         arcade.color.BLACK, font_size=20)
        #Strong target
        arcade.draw_circle_outline(SCREEN_WIDTH/3.1, SCREEN_HEIGHT-250, TARGET_RADIUS, TARGET_COLOR)
        text_x = SCREEN_WIDTH/3.1 - (TARGET_RADIUS / 2)
        text_y = SCREEN_HEIGHT-250 - (TARGET_RADIUS / 2)
        arcade.draw_text(repr(3), text_x, text_y, TARGET_COLOR, font_size=20)
        arcade.draw_text("= 1 point (first 2 hits)", SCREEN_WIDTH/2.61, SCREEN_HEIGHT-265,
                         arcade.color.BLACK, font_size=20)
        arcade.draw_text("   5 points (third hit)", SCREEN_WIDTH/2.61, SCREEN_HEIGHT-315,
                         arcade.color.BLACK, font_size=20)
        
        arcade.draw_text("Click mouse to start.", SCREEN_WIDTH/2, SCREEN_HEIGHT-400,
                         arcade.color.GRAY, font_size=20, anchor_x="center")
        
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """
        When player clicks mouse/trackpad, this is called and game will start.
        """
        game = Game()
        self.window.show_view(game)

class Game(arcade.View):
    """
    This class handles all the game callbacks and interaction
    It assumes the following classes exist:
        Rifle
        Target (and it's sub-classes)
        Point
        Velocity
        Bullet
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class, but mostly
    you shouldn't have to. There are a few sections that you
    must add code to.
    """
    def __init__(self):
        super().__init__()
        self.rifle = Rifle()
        self.score = 0

        self.bullets = []

        # TODO: Create a list for your targets (similar to the above bullets)
        self.targets = []
    
    def on_show(self):
        """
        In charge of setting background color to white
        """        
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # draw each object
        self.rifle.draw()

        for bullet in self.bullets:
            bullet.draw()

        # TODO: iterate through your targets and draw them...
        for target in self.targets:
            target.draw()

        self.draw_score()
        #calls pause_text() function to display instructions in pausing the game
        self.pause_text()
        
    def pause_text(self):
        """
        Displays how to pause game
        """
        pause_text = "Press Esc. to pause game"
        start_x = SCREEN_WIDTH/3
        start_y = SCREEN_HEIGHT - 25
        arcade.draw_text(pause_text, start_x=start_x, start_y=start_y, font_size=15, color=arcade.color.NAVY_BLUE)
                
    def draw_score(self):
        """
        Puts the current score on the screen
        """
        score_text = "Score: {}".format(self.score)
        start_x = 10
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.NAVY_BLUE)


    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_collisions()
        self.check_off_screen()

        # decide if we should start a target
        if random.randint(1, 50) == 1:
            self.create_target()

        for bullet in self.bullets:
            bullet.advance()

        # TODO: Iterate through your targets and tell them to advance
        for target in self.targets:
            target.advance()

    def create_target(self):
        """
        Creates a new target of a random type and adds it to the list.
        :return:
        """

        # TODO: Decide what type of target to create and append it to the list
        #creates standard target and appends to list
        standard = Standard()
        strong = Strong()
        safe = Safe()
        
        
        #creates a tuple of the 3 different types of targets
        #tuple takes less memory than a list
        target_tuple = (standard, strong, safe)
        
        #randomly selects which type of target to spawn
        random_target = random.choice(target_tuple)
        
        self.targets.append(random_target)
        
        
    def check_collisions(self):
        """
        Checks to see if bullets have hit targets.
        Updates scores and removes dead items.
        :return:
        """

        # NOTE: This assumes you named your targets list "targets"

        for bullet in self.bullets:
            for target in self.targets:

                # Make sure they are both alive before checking for a collision
                if bullet.alive and target.alive:
                    too_close = bullet.radius + target.radius

                    if (abs(bullet.center.x - target.center.x) < too_close and
                                abs(bullet.center.y - target.center.y) < too_close):
                        # its a hit!
                        bullet.alive = False
                        target.alive = False #to remove target from screen after getting hit with bullet
                        self.score += target.hit()

                        # We will wait to remove the dead objects until after we
                        # finish going through the list

        # Now, check for anything that is dead, and remove it
        self.cleanup_zombies()

    def cleanup_zombies(self):
        """
        Removes any dead bullets or targets from the list.
        :return:
        """
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)

        for target in self.targets:
            if not target.alive:
                self.targets.remove(target)

    def check_off_screen(self):
        """
        Checks to see if bullets or targets have left the screen
        and if so, removes them from their lists.
        :return:
        """
        for bullet in self.bullets:
            if bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.bullets.remove(bullet)

        for target in self.targets:
            if target.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.targets.remove(target)
                
    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # set the rifle angle in degrees
        self.rifle.angle = self._get_angle_degrees(x, y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        # Fire!
        angle = self._get_angle_degrees(x, y)

        bullet = Bullet()
        bullet.fire(angle)

        self.bullets.append(bullet)
        
    def _get_angle_degrees(self, x, y):
        """
        Gets the value of an angle (in degrees) defined
        by the provided x and y.
        Note: This could be a static method, but we haven't
        discussed them yet...
        """
        # get the angle in radians
        angle_radians = math.atan2(y, x)

        # convert to degrees
        angle_degrees = math.degrees(angle_radians)

        return angle_degrees
    
    def on_key_press(self, key, _modifiers):
        """
        If the player clicks Esc. key, they will be taken
        to the pause screen.
        """
        if key == arcade.key.ESCAPE:
            #Pause() class takes parameter game_view and Game() is passed to preserve view's state
            pause = Pause(self)
            #shows pause screen
            self.window.show_view(pause)
            
class Pause(arcade.View):
    """
    This class is responsible for creating a pause feature in the game.
    """
    
    def __init__(self, game_view):
        super().__init__()
        #self.game_view represents the ongoing game for resuming purposes
        self.game_view = game_view

    def on_show(self):
        """
        This will make pause screen's color to light blue
        """
        arcade.set_background_color(arcade.color.ALICE_BLUE)

    def on_draw(self):
        """
        Called to draw things needed for pause screen
        """
        # clear the screen to begin drawing
        arcade.start_render()

        #Text Paused appears on top of screen
        arcade.draw_text("Paused", SCREEN_WIDTH/2, SCREEN_HEIGHT/2+50,
                         arcade.color.BLACK, font_size=50, anchor_x="center")

        # Show instructions for resuming
        #anchor_x = "center" centers text automatically 
        arcade.draw_text("Press Esc. to return",
                         SCREEN_WIDTH/2,
                         SCREEN_HEIGHT/2,
                         arcade.color.BLACK,
                         font_size=15,
                         anchor_x="center")
        
        # Show instructions for restarting
        arcade.draw_text("Press Spacebar to restart game",
                         SCREEN_WIDTH/2,
                         SCREEN_HEIGHT/2-30,
                         arcade.color.BLACK,
                         font_size=15,
                         anchor_x="center")
        
        # Show instructions for going back to start screen
        arcade.draw_text("Press Tab to go back to starting screen",
                         SCREEN_WIDTH/2,
                         SCREEN_HEIGHT/2-60,
                         arcade.color.BLACK,
                         font_size=15,
                         anchor_x="center")

    def on_key_press(self, key, _modifiers):
        """
        If Esc. key is pressed, game is paused
        If space bar is pressed, game is reset
        If tab key is pressed, it goes back to starting screen 
        """
        if key == arcade.key.ESCAPE:   # resume game
            self.window.show_view(self.game_view)
        elif key == arcade.key.SPACE:  # reset game
            game = Game()
            self.window.show_view(game)
        elif key == arcade.key.TAB: #go back to starting screen
            start = Start_Screen()
            self.window.show_view(start)
            
# Creates the game and starts it going
window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT)
#Starting screen is shown first
game = Start_Screen()
window.show_view(game)
arcade.run()

