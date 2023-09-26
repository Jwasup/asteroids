import pygame
from math import sin
from math import cos
from math import sqrt
import os
from random import randint
from random import uniform


WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids")
pygame.init()

shipTexture = pygame.image.load('assets/ship.png')
shipTexture = pygame.transform.rotate(shipTexture, 180)
bulletTexture = pygame.image.load('assets/bullet.png')

asteroidTexture = pygame.image.load('assets/asteroid.png')

scoreFont = pygame.font.Font('assets/arcadeclassic.ttf', 30)
gameOverFont = pygame.font.Font('assets/arcadeclassic.ttf', 70)
playAgainFont = pygame.font.Font('assets/arcadeclassic.ttf', 40)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PI = 3.141592653589

FPS = 60

def printBoard(ship1, shipTexture, bullets, asteroids, score):
    

    WIN.fill(BLACK)
    shipRect = pygame.rect.Rect(0, 0, 50, 50)
    shipRect.center = (ship1.xPos, ship1.yPos)
    
    #shipTexture = pygame.transform.rotate(shipTexture, ship1.rotation * 360 / 2 / 3.14159)
    

    rot_image = pygame.transform.rotate(shipTexture, ship1.rotation * 360 / (2 * PI))
    rot_rect = shipRect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    

    WIN.blit(rot_image, shipRect)
    
    #pygame.draw.circle(WIN, WHITE, (ship1.xPos, ship1.yPos), 8)
    
    bulletRect = pygame.rect.Rect(0, 0, 2, 5)
    for shot in bullets:

        rotatedBullet = pygame.transform.rotate(bulletTexture, shot.rotation * 360 / 2 / PI)
        bulletRect.center = (shot.xPos, shot.yPos)
        
        WIN.blit(rotatedBullet, bulletRect)
        
        
    for rock in asteroids:
        blitableAsteroidTexture = asteroidTexture
        blitableAsteroidTexture = pygame.transform.scale(blitableAsteroidTexture, (2 * rock.radius, 2 * rock.radius))
        
        
        rot_image = pygame.transform.rotate(blitableAsteroidTexture, rock.rotation * 360 / 2 / PI)
        rot_rect = pygame.rect.Rect(rock.xPos - rock.radius, rock.yPos - rock.radius, 2 * rock.radius, 2 * rock.radius).copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        
        blitableAsteroidTexture = rot_image
        
        WIN.blit(blitableAsteroidTexture, (rock.xPos - rock.radius, rock.yPos - rock.radius))
        
    if score != 0:
        scoreText = scoreFont.render(f'Score   {100 * score}', True, WHITE)
        scoreTextRect = scoreText.get_rect()
        scoreTextRect.topright = (1195, 5)
        WIN.blit(scoreText, scoreTextRect)

    pygame.display.update()

def main():
    run = True
    class ship:
        xPos = 600
        yPos = 400
        xVel = 0
        yVel = 0
        netVel = 0
        rotation = PI
        health = 3
    class bullet:
        def __init__(self, xPos, yPos, xVel, yVel, rotation):
            self.xPos = xPos
            self.yPos = yPos
            self.xVel = xVel
            self.yVel = yVel
            self.rotation = rotation
    class asteroid:
        def __init__(self):
            randAngle1 = uniform(0, 2 * PI)
            self.xStart = 1500 * cos(randAngle1)
            self.yStart = 1500 * sin(randAngle1)
            
            randAngle2 = randAngle1
            while abs(randAngle2 - randAngle1) < 1:
                randAngle2 = uniform(0, 2 * PI)
                self.xEnd = 750 * cos(randAngle2) + WIDTH // 2
                self.yEnd = 750 * sin(randAngle2) + HEIGHT // 2
            
            self.xPos = self.xStart
            self.yPos = self.yStart
            
            randAngle = uniform(0, 2 * PI)
            self.rotation = randAngle
            
            randRotationVelocity = uniform(-.03, .03)
            self.rotationVelocity = randRotationVelocity
            
            speed = uniform(3, 4)
            self.xVel = speed * (self.xEnd - self.xStart) / (abs(self.xStart - self.xEnd) + abs(self.yStart - self.yEnd))
            self.yVel = speed * (self.yEnd - self.yStart) / (abs(self.xStart - self.xEnd) + abs(self.yStart - self.yEnd))
            
            self.radius = uniform(10, 45)
        
        def updatePos(self):
            self.xPos += self.xVel
            self.yPos += self.yVel
            self.rotation += self.rotationVelocity
            if sqrt((self.xPos - self.xEnd) ** 2 + (self.yPos - self.yEnd) ** 2) <= 4:
                return False
            return True
    gamePaused = False
    gameOver = False
    score = 0
    ship1 = ship
    Clock = pygame.time.Clock()
    frameCount = 0
    bullets = []
    asteroids = []
    while run:
        Clock.tick(FPS)
        frameCount += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(bullet(ship1.xPos + 20 * (sin(ship1.rotation)), ship1.yPos + 20 * (cos(ship1.rotation)), ship1.xVel + 15 * (sin(ship1.rotation)), ship1.yVel + 15 * (cos(ship1.rotation)), ship1.rotation))
                elif event.key == pygame.K_ESCAPE:
                    gamePaused = True


        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and not keys[pygame.K_s]:
            if ship1.xVel * sin(ship1.rotation) > 0:
                ship1.xVel += (sin(ship1.rotation) * abs(sin(ship1.rotation))) / 6
            else:
                ship1.xVel += (sin(ship1.rotation) * abs(sin(ship1.rotation))) / 5
            if ship1.yVel * cos(ship1.rotation) > 0:
                ship1.yVel += (cos(ship1.rotation) * abs(cos(ship1.rotation))) / 6
            else:
                ship1.yVel += (cos(ship1.rotation) * abs(cos(ship1.rotation))) / 5
                
            ship1.netVel = sqrt(ship1.xVel ** 2 + ship1.yVel ** 2)
            if ship1.netVel > 15:
                ship1.xVel *= (15 / ship1.netVel)
                ship1.yVel *= (15 / ship1.netVel)
        else:
            ship1.xVel *= (19/20)
            ship1.yVel *= (19/20)
            
        if keys[pygame.K_a]:
            ship1.rotation += .06
        if keys[pygame.K_d]:
            ship1.rotation -= .06
        
        ship1.xPos += ship1.xVel
        ship1.yPos += ship1.yVel
                    
        ship1.netVel = sqrt(ship1.xVel ** 2 + ship1.yVel ** 2)
        
        
        if ship1.xPos > WIDTH:
            ship1.xPos -= WIDTH
        if ship1.yPos > HEIGHT:
            ship1.yPos -= HEIGHT
        if ship1.yPos < 0:
            ship1.yPos += HEIGHT
        if ship1.xPos < 0:
            ship1.xPos += WIDTH

                
        if frameCount % (10) == 1:
            asteroids.append(asteroid())
        
        if keys[pygame.K_o]:
            bullets.append(bullet(ship1.xPos + 20 * (sin(ship1.rotation)), ship1.yPos + 20 * (cos(ship1.rotation)), ship1.xVel + 15 * (sin(ship1.rotation)), ship1.yVel + 15 * (cos(ship1.rotation)), ship1.rotation))

        if keys[pygame.K_0]:
            bullets.append(bullet(ship1.xPos + 20 * (sin(ship1.rotation)), ship1.yPos + 20 * (cos(ship1.rotation)), ship1.xVel + 15 * (sin(ship1.rotation)), ship1.yVel + 15 * (cos(ship1.rotation)), ship1.rotation))
            ship1.rotation += .06
        
        for shot in bullets:
            shot.xPos += shot.xVel
            shot.yPos += shot.yVel
            if shot.xPos < -5 or shot.xPos > 1205 or shot.yPos < -5 or shot.yPos > 805:
                bullets.remove(shot)
                del(shot)
                
        for rock in asteroids:
            if rock.updatePos() == False:
                asteroids.remove(rock)
                del(rock)
                
        for rock in asteroids:
            if sqrt((rock.xPos - ship1.xPos) ** 2 + (rock.yPos - ship1.yPos) ** 2) < rock.radius + 8:
                gameOver = True
            for shot in bullets:
                if sqrt((rock.xPos - shot.xPos) ** 2 + (rock.yPos - shot.yPos) ** 2) < rock.radius:
                    if rock.radius <= 20:
                        asteroids.remove(rock)
                        del(rock)
                        bullets.remove(shot)
                        del(shot)
                        score += 1
                        break
                    else:
                        bullets.remove(shot)
                        del(shot)
                        score += 1
                        for i in range(randint(1, 4)):
                            asteroids.append(asteroid())
                            length = len(asteroids)
                            asteroids[length - 1].radius = rock.radius / 2
                            asteroids[length - 1].xPos = rock.xPos + uniform(0, rock.radius)
                            asteroids[length - 1].yPos = rock.yPos + uniform(0, rock.radius)
                            asteroids[length - 1].xVel *= 1.5
                            asteroids[length - 1].yVel *= 1.5
                        asteroids.remove(rock)
                        del(rock)
                        break
        
        if gamePaused:
            pygame.draw.rect(WIN, WHITE, pygame.rect.Rect(565, 363, 25, 74))
            pygame.draw.rect(WIN, WHITE, pygame.rect.Rect(610, 363, 25, 74))
            pygame.display.update()
        
        while gamePaused == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                    gamePaused = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gamePaused = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    if 565 <= mouseX <= 635 and 363 <= mouseY <= 437:
                        gamePaused = False
            
        
        printBoard(ship1, shipTexture, bullets, asteroids, score)
    
        if gameOver == True:            
            for i in range(3):
                
                pygame.time.wait(500)
                
                printBoard(ship1, shipTexture, bullets, asteroids, score)
                
                pygame.time.wait(500)
                
                gameOverText = gameOverFont.render(f'Game   Over', True, WHITE)
                gameOverRect = gameOverText.get_rect()
                gameOverRect.center = (WIDTH // 2, HEIGHT // 2 - 35)
                WIN.blit(gameOverText, gameOverRect)
                
                pygame.display.update()
                
            playAgainText = playAgainFont.render(f'Play  Again', True, WHITE)
            playAgainRect = playAgainText.get_rect()
            playAgainRect.center = (WIDTH // 2, HEIGHT // 2 + 35)
            WIN.blit(playAgainText, playAgainRect)
                
            pygame.display.update()
            
    
        while gameOver == True:
            Clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    gameOver = False
                    run = False
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    if playAgainRect.left <= mouseX <= playAgainRect.right and playAgainRect.top <= mouseY <= playAgainRect.bottom:
                        gameOver = False
                        score = 0
                        del(ship1)
                        for rock in asteroids:
                            del(rock)
                        for shot in bullets:
                            del(bullet)
                        ship1 = ship
                        bullets = []
                        asteroids = []
                        frameCount = 0
                        
            
    
if __name__ == '__main__':
    main()