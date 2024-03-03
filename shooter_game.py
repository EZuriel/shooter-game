# IMPORT
from pygame import *
from random import randint 

# CLASSES
# GameSprite class
class GameSprite(sprite.Sprite):
    # Constructor Function
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height)) # Resizing the image
        self.speed = player_speed
        
        self.rect = self.image.get_rect()   # Hitbox
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Player Class
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()  # Gets the state of keys (are they pressed?)
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

# Method to "shoot" (uses the player's position as the bullet's initial position)
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

# Enemy Class
class Enemy(GameSprite):
    def update(self):
        global missed # It lets the class change the value of the 'missed' variable (which is a global variable)
        self.rect.y += self.speed

        # Resets the position of the alien when it reaches the bottom of the screen
        if self.rect.y > win_height:    # IF the alien reaches the bottom of the screen
            self.rect.y = 0
            self.rect.x = randint(80, win_width-80)
            missed += 1  # Add the 'missed' counter by 1

# Bullet Class
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        
        if self.rect.y < 0:  # If the bullet's position is above the screen
            self.kill()  # Deletes the bullet from the group (conserving space)

# Set window
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter Game")
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))
clock = time.Clock()

# # Music
# mixer.init()
# mixer.music.load('space.ogg')
# mixer.music.play()

FPS = 60    # Set FPS
isRunning = True    # state of game (is the game running?)
finished = False    # completion of game (is the game finished/over?)

# Scoring variables
score = 0 # Ships destroyed
missed = 0 # Ships missed

# SPRITE OBJECTS
# Ship (an instance of the Player class)
ship = Player('rocket.png', 5, win_height-100, 80, 100, 10)

# Enemies
enemies = sprite.Group()
for i in range(6):  # Do the lines of code below for six times
    enemy = Enemy('ufo.png', randint(80, win_width-80), -40, 80, 50, randint(1, 5))
    enemies.add(enemy)

# Bullet Group
bullets = sprite.Group()

# Initiate font
font.init()   # Initializes the font
font_1 = font.Font(None, 36)  # Generates a font (None --> "Use pygame's font style", 36 --> Font size)
font_2 = font.Font(None, 80)
# Lose text
lose = font_2.render('YOU LOSE!', True, (180, 0, 0))

# Win text
win = font_2.render('YOU WIN!', True, (255, 255, 255))
# GAME LOOP
while isRunning:

    for e in event.get():  # Event handler
        if e.type == QUIT: # If the player presses the X button in the window
            isRunning = False

        elif e.type == MOUSEBUTTONDOWN:  # If the player presses a button on the keyboard
            ship.fire()

    if not finished:
        window.blit(background, (0,0))
        # Score text
        text = font_1.render("Score: " + str(score), 1, (255, 255, 255))  # Creates a text (hasn't displayed it text)
        window.blit(text, (10, 20))  # Displays the text to the window on the given coordinate
        
        # Missed text
        text = font_1.render("Missed: " + str(missed), 1, (255, 255, 255))  # Creates a text (hasn't displayed it text)
        window.blit(text, (10, 50))  # Displays the text to the window on the given coordinate
        
        ship.update()   # Initializes ship movements
        ship.reset()    # Updates the new location of the ship

        enemies.update()
        enemies.draw(window)
        
        bullets.update()  # Update the bullets' positions
        bullets.draw(window)  # Displays the bullets

        # Detect bullets/monsters collision
        collides = sprite.groupcollide(enemies, bullets, True, True)  # Returns a list of monsters if one of the enemies collides with one of the bullets
        for c in collides:
            score = score + 1  # Adds the score
            enemy = Enemy('ufo.png', randint(80, win_width-80), -40, 80, 50, randint(1, 5)) # Generates new enemy
            enemies.add(enemy) # Adds the new enemy into the 'enemies' group

        # Detect ship/monsters collision
        if sprite.spritecollide(ship, enemies, False):
            finished = True  # Stops the game
            window.blit(lose, (200, 200)) # Displays the text

        if missed == 3:
            finished = True  # Stops the game
            window.blit(background, (0,0))
            # Score text
            text = font_1.render("Score: " + str(score), 1, (255, 255, 255))  # Creates a text (hasn't displayed it text)
            window.blit(text, (10, 20))  # Displays the text to the window on the given coordinate
            
            # Missed text
            text = font_1.render("Missed: " + str(missed), 1, (255, 255, 255))  # Creates a text (hasn't displayed it text)
            window.blit(text, (10, 50))  # Displays the text to the window on the given coordinate
            
            ship.update()   # Initializes ship movements
            ship.reset()    # Updates the new location of the ship

            enemies.update()
            enemies.draw(window)
            
            bullets.update()  # Update the bullets' positions
            bullets.draw(window)  # Displays the bullets
            window.blit(lose, (200, 200))

        if score == 10:
            finished = True
            window.blit(background, (0,0))
            # Score text
            text = font_1.render("Score: " + str(score), 1, (255, 255, 255))  # Creates a text (hasn't displayed it text)
            window.blit(text, (10, 20))  # Displays the text to the window on the given coordinate
            
            # Missed text
            text = font_1.render("Missed: " + str(missed), 1, (255, 255, 255))  # Creates a text (hasn't displayed it text)
            window.blit(text, (10, 50))  # Displays the text to the window on the given coordinate
            
            ship.update()   # Initializes ship movements
            ship.reset()    # Updates the new location of the ship

            enemies.update()
            enemies.draw(window)
            
            bullets.update()  # Update the bullets' positions
            bullets.draw(window)  # Displays the bullets
            window.blit(win, (200, 200))

        display.update()
        clock.tick(FPS)