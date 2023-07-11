""" Name of Program: Pac-Man
    Author: Diya Tomar
    Brief Description of Program: Pac-Man must eat all the pellets in the maze to win (move using arrow keys)
                                  Colliding with a ghost will make Pac-Man lose
                                  Eating the cherry will give extra points
                                  Once Pac-Man wins, he can play the next level (ghost movement is faster)

                                  Extras (Thinking):
                                  1. Music (starting / stopping music)
                                  2. Sound effects
                                  3. Buttons with mouse clicks
                                  4. Changing images in a rect depending on direction and movement (to simulate mouth movement)
                                  5. Displaying and updating high score

                                  NOTE: The game can be navigated using the buttons BUT I've included key presses (ex. 'p' for play) just in case

"""

# ------------------------------------------------------------------ general variables ------------------------------------------------------

# imports
import pygame
import sys
import time

# initializing pygame
pygame.init()

# setting caption and screen size
pygame.display.set_caption("Pac-Man")
screen = pygame.display.set_mode((735, 704))

# get screen width and height
screenWidth = screen.get_width()
screenHeight = screen.get_height()
centreX = screenWidth/2
centreY = screenHeight/2
screenCentre = (centreX, centreY)

# colours
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
YELLOW_2 = (255,255,50)
GREY = (200,200,200)

# setting up fonts
fontTitle = pygame.font.SysFont("comicsansms", 25,italic=True)
fontTitleBold = pygame.font.SysFont("comicsansms",30, bold =True)
fontButton = pygame.font.SysFont("comicsansms", 18,italic=True)

# variables for scoring
score = 0
highScore = 0

# variables to decide game outcome
result = ""
replayType = ""

# create clock and set FPS
clock = pygame.time.Clock()
FPS = 60

# variables for maze position
mazeX = 0       
mazeY = 50

# importing cherry image
gameCherry = pygame.image.load("images/cherry.jpeg")

# ------------------------------------------- intro and instructions variables ----------------------------------------------

# import title images
introTitle = pygame.image.load("images/title.jpeg")
introCharacters = pygame.image.load("images/characters.jpeg")

# variables for buttons
playButtonX = centreX - 130
playButtonY = centreY + 40
playButtonWidth = 260
playButtonHeight = 70
playButtonCentreX = playButtonWidth / 2
playButtonCentreY = playButtonHeight / 2

instructionButtonX = playButtonX
instructionButtonY = playButtonY + 100
instructionButtonWidth = playButtonWidth
instructionButtonHeight = playButtonHeight
instructionButtonCentreX = instructionButtonWidth / 2
instructionButtonCentreY = playButtonHeight / 2

backButtonX = centreX - 130
backButtonY = centreY + 160
backButtonWidth = 260
backButtonHeight = 70
backButtonCentreX = backButtonWidth / 2
backButtonCentreY = backButtonHeight / 2

finalButtonX = centreX - 130
finalButtonY = centreY + 40
finalButtonWidth = 260
finalButtonHeight = 70
finalButtonCentreX = finalButtonWidth / 2
finalButtonCentreY = finalButtonHeight / 2

# rects for buttons
playButtonRect = pygame.Rect(playButtonX,playButtonY,playButtonWidth,playButtonHeight)
instructionButtonRect = pygame.Rect(instructionButtonX,instructionButtonY,instructionButtonWidth,instructionButtonHeight)
backButtonRect = pygame.Rect(backButtonX,backButtonY,backButtonWidth,backButtonHeight)
finalButtonRect = pygame.Rect(finalButtonX,finalButtonY,finalButtonWidth,finalButtonHeight)


# ---------------------------------------- pacman variables ----------------------------------
# import pacman images
pacmanNoMouth = pygame.image.load("images/pacmanClose.png")
pacmanClose = pygame.image.load("images/pacmanClose.png")  
pacmanRight = pygame.image.load("images/pacmanRight.png")
pacmanLeft = pygame.image.load("images/pacmanLeft.png")
pacmanUp = pygame.image.load("images/pacmanUp.png")
pacmanDown = pygame.image.load("images/pacmanDown.png")  

# variables for Pacman
pacmanX = mazeX + 32
pacmanY = mazeY + 548
pacmanWidth = 26
pacmanHeight = 26
pacmanDX = 0
pacmanDY = 0
pacmanSpeed = 3

# rect for Pacman
pacmanRect = pacmanClose.get_rect()
pacmanRect.x = pacmanX
pacmanRect.y = pacmanY

# --------------------------------------------- ghost variables -----------------------------------------

# blue ghost variables, image import, and rect
gameGhost = pygame.image.load("images/blueghost.png")
ghostX = mazeX + 34
ghostY = mazeY + 100
ghostSpeed = 2
ghostDX = ghostSpeed
ghostDY = 0

ghostRect = gameGhost.get_rect()
ghostRect.x = ghostX
ghostRect.y = ghostY

# second blue ghost variables, image import, and rect
gameGhost2 = pygame.image.load("images/blueghost.png")
ghostX2 = mazeX + 660
ghostY2 = mazeY + 480
ghostSpeed2 = 2
ghostDX2 = ghostSpeed2
ghostDY2 = 0

ghostRect2 = gameGhost2.get_rect()
ghostRect2.x = ghostX2
ghostRect2.y = ghostY2

# pink ghost variables, image import, and rect
gameGhost3 = pygame.image.load("images/pinkghost.png")
ghostX3 = mazeX + 130
ghostY3 = mazeY + 72
ghostSpeed3 = 2
ghostDX3 = 0
ghostDY3 = -ghostSpeed3

ghostRect3 = gameGhost3.get_rect()
ghostRect3.x = ghostX3
ghostRect3.y = ghostY3

# second pink ghost variables, image import, and rect
gameGhost4 = pygame.image.load("images/pinkghost.png")
ghostX4 = mazeX + 580
ghostY4 = mazeY + 500
ghostSpeed4 = 2
ghostDX4 = 0
ghostDY4 = -ghostSpeed4

ghostRect4 = gameGhost4.get_rect()
ghostRect4.x = ghostX4
ghostRect4.y = ghostY4

# ------------------------------------------------------ maze setup function ------------------------------------------------

# sets up the maze every time the game is played
def reset():

   # empty array for cherries
   cherries = []

   # maze starting positions
   mapX = 0       
   mapY = 50

   # empty array to store rects for each wall
   walls = []

   # starting position of dots
   dotX = mapX     
   dotY = mapY

   # empty array to store rects for each food pellet
   pellets = []
   
#create the layout of the array
   map = [
   "WWWWWWWWWWWWWWWWWWWWWWW",
   "W..........W..........W",
   "W.WW.WWWWW.W.WWWWW.WW.W",
   "W.....................W",
   "W.WW.W.WWWWWWWWW.W.WW.W",
   "W....W.....W.....W....W",
   "WWWW.WWWWW.W.WWWWW.WWWW",
   "WWWW.W...........W.WWWW",
   "WWWW.W.WW     WW.W.WWWW",
   "W......W...C...W......W",
   "WWWW.W.WWWWWWWWW.W.WWWW",
   "WWWW.W...........W.WWWW",
   "WWWW.WWWWW.W.WWWWW.WWWW",
   "W....W.....W.....W....W",
   "W.WW.W.WWWWWWWWW.W.WW.W",
   "W.....................W",
   "W.WW.WWWWW.W.WWWWW.WW.W",
   "W .........W..........W",
   "WWWWWWWWWWWWWWWWWWWWWWW",
   ]

   # reads the array and creates the appropriate Rects
   for row in map:
      for col in row:
         # creating wall rects   
         if col == "W":
            wallRect = pygame.Rect(mapX,mapY,32,32)
            walls.append(wallRect)
         # creating pellet rects
         if col == ".":
            pelletRect = pygame.Rect(mapX,mapY,32,32)
            pellets.append(pelletRect)
         # creating cherry rects
         if col == "C":
            cherryRect = pygame.Rect(mapX,mapY,32,32)
            cherries.append(cherryRect)
         mapX += 32
      mapY += 32
      mapX = 0

   return walls, pellets, cherries, cherryRect

# ------------------------------------- loop variables --------------------------------------------

# set instructions, game and final loops to false so they won't run
instructions = False
game = False
final = False

# set main and intro loops to True so they will run
intro = True
main = True

# ------------------------------------------ music ------------------------------------

# importing sounds and music to use during game
pygame.mixer.music.load("music\introMusic.mp3")
eatingSound = pygame.mixer.Sound("music\eatingSound.wav")
cherrySound = pygame.mixer.Sound("music\cherryEat.mp3")
gameOver = pygame.mixer.Sound("music\gameOverMusic.mp3")
winSound = pygame.mixer.Sound("music\winMusic.mp3")

#----------------------------------------------------- main loop ---------------------------------------

while main:
   for event in pygame.event.get(): # check for any events (i.e key press, mouse click etc.)
      if event.type == pygame.QUIT: # check to see if it was "x" at top right of screen
         main = False         # set the "main" variable to False to exit while loop

    # the introduction loop,  first page users will see
   if intro == True:
      pygame.mixer.music.play(0)

   while intro:
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            main = False
            intro = False
         # what happens when each key is pressed (this is included in case you want to check a certain page using keys) 
         if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
               main = False
               intro = False
            elif event.key == pygame.K_p:
               intro = False
               game = True
               pygame.mixer.music.stop()
            elif event.key == pygame.K_i:
               intro = False
               instructions = True
               pygame.mixer.music.stop()
                    
         # what happens when mouse clicks on a button
         if event.type == pygame.MOUSEBUTTONDOWN:
            if playButtonRect.collidepoint(pygame.mouse.get_pos()):
               intro = False
               game = True
               pygame.mixer.music.stop()
            elif instructionButtonRect.collidepoint(pygame.mouse.get_pos()):
               intro = False
               instructions = True
               pygame.mixer.music.stop()

        
      screen.fill(BLACK)

     # displaying images for intro screen
      screen.blit(introTitle, (0, 0))
      screen.blit(introCharacters, (0, screenHeight - 500))

     # displaying intro buttons
      pygame.draw.rect(screen, GREY, playButtonRect,0)
      pygame.draw.rect(screen, GREY, instructionButtonRect,0)
     
     # text for buttons
      textTitle = fontButton.render("PLAY", False, RED)
      textTitle2 = fontButton.render("INSTRUCTIONS",False, BLUE)
      textRect = textTitle.get_rect()
      textRect2 = textTitle2.get_rect()
      textRect.center = (centreX, 425)
      textRect2.center = (centreX,525)
      screen.blit(textTitle, textRect)
      screen.blit(textTitle2, textRect2)


      #update the screen
      pygame.display.flip()

   # contains all the instructions if the user want to read them
   while instructions:
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            main = False
            instructions = False
         # what happens when each key is pressed 
         if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
               main = False
               instructions = False
            elif event.key == pygame.K_b:
               instructions = False
               intro = True
                    
         # what happens when mouse clicks on a button
         if event.type == pygame.MOUSEBUTTONDOWN:
            if backButtonRect.collidepoint(pygame.mouse.get_pos()):
               instructions = False
               intro = True

      screen.fill(BLACK)

     # displaying button to go back to main screen
      pygame.draw.rect(screen, GREY, backButtonRect,0)

     # button text
      textTitle = fontButton.render("Go back to", False, RED)
      textTitle2 = fontButton.render("main screen",False, RED)
      textRect = textTitle.get_rect()
      textRect2 = textTitle2.get_rect()
      textRect.center = (centreX, 535)
      textRect2.center = (centreX,560)
      screen.blit(textTitle, textRect)
      screen.blit(textTitle2, textRect2)
     
     # instructions text
      textTitle = fontTitle.render("INSTRUCTIONS", False, RED)
      textRect = textTitle.get_rect()
      textRect.center = (centreX, 200)
      screen.blit(textTitle, textRect)
      
      textTitle2 = fontTitle.render("Use the arrow keys to move Pac-man",False, BLUE )
      textRect2 = textTitle2.get_rect()
      textRect2.center = (centreX,250)
      screen.blit(textTitle2, textRect2)

      textTitle3 = fontTitle.render("Eat all of the pellets in the maze to win",False, BLUE )
      textRect3 = textTitle3.get_rect()
      textRect3.center = (centreX,300)
      screen.blit(textTitle3, textRect3)

      textTitle4 = fontTitle.render("Avoid the ghosts. If you collide with a ghost, the game ends",False, BLUE )
      textRect4 = textTitle4.get_rect()
      textRect4.center = (centreX,350)
      screen.blit(textTitle4, textRect4)

      textTitle5 = fontTitle.render("Eat the cherry to get 500 bonus points",False, BLUE )
      textRect5 = textTitle5.get_rect()
      textRect5.center = (centreX,400)
      screen.blit(textTitle5, textRect5)

      #update the screen
      pygame.display.flip()

   #starting the timer
   start = time.perf_counter()
   walls, pellets, cherries, cherryRect = reset()
   # responsible for the main game
   while game:
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            game = False
            main = False
         # what happens when each key is pressed 
         if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
               game = False
            elif event.key == pygame.K_UP:
               pacmanClose = pacmanUp
               pacmanDX = 0
               pacmanDY = -pacmanSpeed
            elif event.key == pygame.K_DOWN:
               pacmanClose = pacmanDown
               pacmanDX = 0
               pacmanDY = pacmanSpeed
            elif event.key == pygame.K_LEFT:
               pacmanClose = pacmanLeft
               pacmanDX = -pacmanSpeed
               pacmanDY = 0
            elif event.key == pygame.K_RIGHT:
               pacmanClose = pacmanRight
               pacmanDX = pacmanSpeed
               pacmanDY = 0
         if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
               pacmanClose = pacmanNoMouth
               pacmanDX = 0
               pacmanDY = 0
            elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
               pacmanClose = pacmanNoMouth
               pacmanDX = 0
               pacmanDY = 0

      screen.fill(BLACK)

      # store current position of pacman
      pacmanOldX = pacmanRect.x
      pacmanOldY = pacmanRect.y
      
      # move the x and y positions of pacman
      pacmanRect.move_ip(pacmanDX,pacmanDY)

      # preventing pacman from passing through maze walls
      for wall in walls:
         if pacmanRect.colliderect(wall):
            pacmanRect.x = pacmanOldX
            pacmanRect.y = pacmanOldY
            
      # pellet disappears during collision with pacman
      for pellet in pellets:
         if pacmanRect.colliderect(pellet):
            pellets.remove(pellet)
            score = score + 1
            eatingSound.play()
            
      # cherry disappears during collision with pacman
      for cherry in cherries:
         if pacmanRect.colliderect(cherry):
            cherries.remove(cherry)
            score = score + 500
            cherrySound.play()

      # draw the pellets
      for pellet in pellets:
          pygame.draw.circle(screen,YELLOW,pellet.center,2)
      # draw the walls    
      for wall in walls:
          pygame.draw.rect(screen,BLUE,wall,0)
      # display cherry to screen
      for cherry in cherries:
         screen.blit(gameCherry, cherryRect)

      # draw pacman circle
      screen.blit(pacmanClose, pacmanRect)

      # x and y movements of ghosts
      ghostRect.move_ip(ghostDX,ghostDY)
      ghostRect2.move_ip(ghostDX2,ghostDY2)
      ghostRect3.move_ip(ghostDX3,ghostDY3)
      ghostRect4.move_ip(ghostDX4,ghostDY4)


      # ghost movements when colliding against walls
      for wall in walls:
         if ghostRect.colliderect(wall):
            if ghostDX > 0:
               ghostDX = -ghostSpeed
               ghostDY = 0
            elif ghostDX < 0:
               ghostDX = ghostSpeed
               ghostDY = 0
               
         if ghostRect2.colliderect(wall):
            if ghostDX2 > 0:
               ghostDX2 = -ghostSpeed2
               ghostDY2 = 0
            elif ghostDX2 < 0:
               ghostDX2 = ghostSpeed2
               ghostDY2 = 0
               
         if ghostRect3.colliderect(wall):
            if ghostDY3 > 0:
               ghostDX3 = 0
               ghostDY3 = -ghostSpeed3
            elif ghostDY3 < 0:
               ghostDX3 = 0
               ghostDY3 = ghostSpeed3

         if ghostRect4.colliderect(wall):
            if ghostDY4 > 0:
               ghostDX4 = 0
               ghostDY4 = -ghostSpeed4
            elif ghostDY4 < 0:
               ghostDX4 = 0
               ghostDY4 = ghostSpeed4

      # displaying ghosts to screen
      screen.blit(gameGhost, ghostRect)
      screen.blit(gameGhost2, ghostRect2)
      screen.blit(gameGhost3, ghostRect3)
      screen.blit(gameGhost4, ghostRect4)
      
      # displaying score text
      textTitle = fontTitle.render("Score: " + str(score), False, YELLOW)
      textRect = textTitle.get_rect()
      textRect.center = (80, 25)
      screen.blit(textTitle, textRect)

      # code for game timer
      elapsedTime = int(time.perf_counter()- start)

      # code to display text for timer
      timerStr = "Time: " + str(elapsedTime) + "s"
      textTitle = fontTitle.render(timerStr, True, YELLOW)
      textTitleRect = textTitle.get_rect(center = (screenWidth - 90, 25))
      screen.blit(textTitle, textTitleRect)

      # game outcomes
      if score == 201 or score == 701:
         game = False
         final = True
         result = "Win!"
         replayType = "Next Level"
         # FPS is increased after every win to make game harder
         FPS = FPS + 15
         winSound.play()
         if score > highScore:
            highScore = score

      if pacmanRect.colliderect(ghostRect) or pacmanRect.colliderect(ghostRect2):
         game = False
         final = True
         result = "Lose"
         replayType = "Play Again"
         gameOver.play()
         if score > highScore:
            highScore = score

      if pacmanRect.colliderect(ghostRect3) or pacmanRect.colliderect(ghostRect4):
         game = False
         final = True
         result = "Lose"
         replayType = "Play Again"
         gameOver.play()
         if score > highScore:
            highScore = score

      # controlling FPS
      clock.tick(FPS)
      
      # update the screen using flip
      pygame.display.flip()
      
   # what happens at the end of the game
   while final:
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            main = False
            final = False
         # what happens when each key is pressed 
         if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
               main = False
               final = False
            elif event.key == pygame.K_b:
               # resets high score to 0 if player goes to next level
               if score == 201 or score == 701:
                  highScore = 0
               pacmanRect.center = (pacmanX + 13, pacmanY + 13)
               score = 0
               pacmanDX = 0
               pacmanDY = 0
               pacmanClose = pacmanNoMouth
               final = False
               intro = True
            elif event.key == pygame.K_p:
               if score == 201 or score == 701:
                  highScore = 0
               pacmanRect.center = (pacmanX + 13, pacmanY + 13)
               pacmanClose = pacmanNoMouth
               score = 0
               pacmanDX = 0
               pacmanDY = 0
               pygame.mixer.music.stop()
               final = False
               game = True

         # what happens when button is pressed
         if event.type == pygame.MOUSEBUTTONDOWN:
            if finalButtonRect.collidepoint(pygame.mouse.get_pos()):
               if score == 201 or score == 701:
                  highScore = 0
               pacmanRect.center = (pacmanX + 13, pacmanY + 13)
               score = 0
               pacmanDX = 0
               pacmanDY = 0
               pacmanClose = pacmanNoMouth
               pygame.mixer.music.stop()
               final = False
               game = True

      screen.fill(BLACK)    

      # text displayed at final screen
      textTitle = fontTitle.render("You " + result, False, RED)
      textRect = textTitle.get_rect()
      textRect.center = (centreX, 200)
      screen.blit(textTitle, textRect)

      timerStr = "Time: " + str(elapsedTime) + "s"
      textTitle2 = fontTitle.render(timerStr, True, YELLOW)
      textRect2 = textTitle2.get_rect(center = (centreX, centreY - 80))
      screen.blit(textTitle2, textRect2)

      textTitle5 = fontTitle.render("High Score: " + str(highScore), False, YELLOW)
      textRect5 = textTitle5.get_rect()
      textRect5.center = (centreX, centreY - 40)
      screen.blit(textTitle5, textRect5)

      textTitle3 = fontTitle.render("Score: " + str(score), False, YELLOW)
      textRect3 = textTitle3.get_rect()
      textRect3.center = (centreX, centreY)
      screen.blit(textTitle3, textRect3)

      # displaying final button
      pygame.draw.rect(screen, GREY, finalButtonRect,0)

      # text for button
      textTitle4 = fontTitle.render(replayType + "", False, BLUE)
      textRect4 = textTitle3.get_rect()
      textRect4.center = (centreX - 13, centreY + 70)
      screen.blit(textTitle4, textRect4)

      # controlling FPS
      clock.tick(FPS)

      #update the screen
      pygame.display.flip()

pygame.quit()
sys.exit()
