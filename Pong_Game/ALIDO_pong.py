"""
File: pong.py
Original Author: Br. Burton
Designed to be completed by others
This program implements a simplistic version of the
classic Pong arcade game.
"""
import arcade
import random

# These are Global constants to use throughout the game
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300


#VARIABLES FOR BALL CLASS
BALL_RADIUS = 10
BALL_COLOR = arcade.color.BURNT_ORANGE


#VARIABLES FOR PADDLE CLASS
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 50
PADDLE_COLOR = arcade.color.BISTRE
MOVE_AMOUNT = 5

#VARIABLES FOR POINTS WHEN BALL IS HIT WITH PADDLE AND IF BALL PASSES THROUGH RIGHT EDGE OF SCREEN
SCORE_HIT = 1
SCORE_MISS = 5

class Point():
    """
    This class is in charge of setting the x and y coordinates for both the ball and the paddle
    """
    def __init__(self):
        """
        Function to declare main member variables.
        X and Y coordinates are set in random locations right along the left edge of screen
        """
        #random.uniform(1, 10) = random float values for x coordinate to make sure ball spawns on left edge of screen with random values
        #random.unform(1, 330) = 1-330 was chosen to make sure the ball can spawn randomly either below or on top of left edge of the screen
        self.x = random.uniform(1, 10)
        self.y = random.uniform(1, 330)
        
class Velocity():
    """
    This class is in charge of the velocity for the moving ball
    """
    def __init__(self):
        """
        Function for Velocity class and dx and dy member variables with a random range of 1-5
        """
        #random.uniform(1, 5) = random float values from 1-5 which will determine the velocity 
        self.dx = random.uniform(1, 5)
        self.dy = random.uniform(1, 5)
        
class Ball():
    """
    This class is in charge of the pong ball and its attributes.
    """
    def __init__(self):
        """
        Function to assign center of ball with Point() class' attributes and the velocity from Velocity() class
        """
        self.center = Point()
        self.velocity = Velocity()
        
    def draw(self):
        """
        Function to draw a circle using the previously made x and y coordinates, global variable radius, and color
        """
        arcade.draw_circle_filled(self.center.x, self.center.y, BALL_RADIUS, BALL_COLOR)
        return
              
    def advance(self):
        """
        This function is responsible for the ball's movement using the velocity.
        """
        #x and y coordinates move and advance by adding the randomly generated velocity 
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
        return
    
    def bounce_horizontal(self):
        """
        Responsible for making sure ball bounces horizontally but lost if it passes the right edge of screen.
        """
        self.velocity.dx = -self.velocity.dx
        return
    
    def bounce_vertical(self):
        """
        Responsible for making sure ball bounces up and down vertically.
        """
        self.velocity.dy = -self.velocity.dy
        return
    
    def restart(self):
        """
        Once the ball is lost from right edge of screen, this function is called to reset ball's position back to
        the start.
        """
        self.__init__()
        return
    
class Paddle():
    """
    This class is in charge of the paddle and its attributes
    """
    def __init__(self):
        """
        Function to assign coordinates of paddle with Point() class
        Assigns new values for paddle's coordinates to make sure it's placed on the right edge of screen
        """
        self.center = Point()
        #x coordinate is set in these amount of pixels to leave a slight gap between the screen and paddle just like in real pong video games
        self.center.x = SCREEN_WIDTH - 10
        #when game starts, paddle is placed on the middle of screen's right edge
        self.center.y = SCREEN_HEIGHT / 2
        
    def draw(self):
        """
        Function to draw rectangle for the paddle using new coordinates, paddle width, height, and color from global
        variables.
        """
        arcade.draw_rectangle_filled(self.center.x, self.center.y, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_COLOR)
        pass
    
    def move_up(self):
        """
        Responsible for making sure paddle moves by 5 pixels up when user presses up button from keyboard
        Stops right exactly on the top edge of the screen
        """
        #if user moves paddle right on top of screen, they won't be able to move it more upwards by using this if statement
        #SCREEN_HEIGHT - 20 = Exact number of pixels where paddle can stop exactly on top edge but still has its body fully shown
        if self.center.y < SCREEN_HEIGHT - 20:
            self.center.y += MOVE_AMOUNT
    
    def move_down(self):
        """
        Responsible for making sure paddle moves by 5 pixels down when user presses down button from keyboard
        Stops right exactly on the lower edge of the screen
        """
        #if user moves paddle right below on the screen, they won't be able to move it more downwards by using this if statement
        #SCREEN_HEIGHT - 280 = Exact number of pixels where paddle can stop exactly on bottom edge but still has its body fully shown
        if self.center.y > SCREEN_HEIGHT - 280:
            self.center.y -= MOVE_AMOUNT

class Pong(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    It assumes the following classes exist:
        Point
        Velocity
        Ball
        Paddle
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class,
    but should not have to if you don't want to.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)

        self.ball = Ball()
        self.paddle = Paddle()
        self.score = 0

        # These are used to see if the user is
        # holding down the arrow keys
        self.holding_left = False
        self.holding_right = False

        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsiblity of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # draw each object
        self.ball.draw()
        self.paddle.draw()

        self.draw_score()

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

        # Move the ball forward one element in time
        self.ball.advance()

        # Check to see if keys are being held, and then
        # take appropriate action
        self.check_keys()

        # check for ball at important places
        self.check_miss()
        self.check_hit()
        self.check_bounce()

    def check_hit(self):
        """
        Checks to see if the ball has hit the paddle
        and if so, calls its bounce method.
        :return:
        """
        too_close_x = (PADDLE_WIDTH / 2) + BALL_RADIUS
        too_close_y = (PADDLE_HEIGHT / 2) + BALL_RADIUS

        if (abs(self.ball.center.x - self.paddle.center.x) < too_close_x and
                    abs(self.ball.center.y - self.paddle.center.y) < too_close_y and
                    self.ball.velocity.dx > 0):
            # we are too close and moving right, this is a hit!
            self.ball.bounce_horizontal()
            self.score += SCORE_HIT

    def check_miss(self):
        """
        Checks to see if the ball went past the paddle
        and if so, restarts it.
        """
        if self.ball.center.x > SCREEN_WIDTH:
            # We missed!
            self.score -= SCORE_MISS
            self.ball.restart()

    def check_bounce(self):
        """
        Checks to see if the ball has hit the borders
        of the screen and if so, calls its bounce methods.
        """
        if self.ball.center.x < 0 and self.ball.velocity.dx < 0:
            self.ball.bounce_horizontal()

        if self.ball.center.y < 0 and self.ball.velocity.dy < 0:
            self.ball.bounce_vertical()

        if self.ball.center.y > SCREEN_HEIGHT and self.ball.velocity.dy > 0:
            self.ball.bounce_vertical()

    def check_keys(self):
        """
        Checks to see if the user is holding down an
        arrow key, and if so, takes appropriate action.
        """
        if self.holding_left:
            self.paddle.move_down()

        if self.holding_right:
            self.paddle.move_up()

    def on_key_press(self, key, key_modifiers):
        """
        Called when a key is pressed. Sets the state of
        holding an arrow key.
        :param key: The key that was pressed
        :param key_modifiers: Things like shift, ctrl, etc
        """
        if key == arcade.key.LEFT or key == arcade.key.DOWN:
            self.holding_left = True

        if key == arcade.key.RIGHT or key == arcade.key.UP:
            self.holding_right = True

    def on_key_release(self, key, key_modifiers):
        """
        Called when a key is released. Sets the state of
        the arrow key as being not held anymore.
        :param key: The key that was pressed
        :param key_modifiers: Things like shift, ctrl, etc
        """
        if key == arcade.key.LEFT or key == arcade.key.DOWN:
            self.holding_left = False

        if key == arcade.key.RIGHT or key == arcade.key.UP:
            self.holding_right = False

# Creates the game and starts it going
window = Pong(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()