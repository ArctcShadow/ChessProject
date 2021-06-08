import pygame 
from pygame.locals import *
import os
from pieces import Pieces
from chess import Chess
from utilities import Utilities

class Game:
    def __init__(self):
        width = 640
        height = 750
        self.menuActive = False
        self.running = True
        self.resources = "png"

        pygame.display.init()
        pygame.font.init()

        self.display = pygame.display.set_mode([width,height])
        title = "Шахмати"
        pygame.display.set_caption(title)

        iconsrc = os.path.join(self.resources,"icon.png")
        icon = pygame.image.load(iconsrc)
        pygame.display.set_icon(icon)
        pygame.display.flip()

        self.clock = pygame.time.Clock()

    def start(self):
        self.offsetX = 0
        self.offsetY = 50
        self.boardDimensions = (self.offsetX,self.offsetY)

        boardSource = os.path.join(self.resources,"board.png")
        self.boardImg = pygame.image.load(boardSource).convert()

        squareLenght = self.boardImg.get_rect().width // 8
        self.boardLocations = []

        for x in range(0,8):
            self.boardLocations.append([])
            for y in range (0,8):
                self.boardLocations[x].append([self.offsetX+(x*squareLenght), self.offsetY+(y*squareLenght)])

        piecesSrc = os.path.join(self.resources,"pieces.png")
        self.chess = Chess(self.display,piecesSrc,self.boardLocations,squareLenght)

        #головний ігровий цикл
        while self.running:
            self.clock.tick(5)

            for event in pygame.event.get():
                keyPressed = pygame.key.get_pressed()
                if event.type == pygame.QUIT or keyPressed[K_ESCAPE]:
                    self.running = False
                elif keyPressed[K_SPACE]:
                    self.chess.refresh()
            
            winner = self.chess.winner

            if self.menuActive == False:
                self.menu()
            elif len(winner) > 0:
                self.declareWinner(winner)
            else:
                self.game()
            
            pygame.display.flip()
            pygame.event.pump()
        
        pygame.quit()
    
    def menu(self):
        bgColor = (255, 255 , 255)
        self.display.fill(bgColor)
        black = (0,0,0)
        button = pygame.Rect(270,300,100,50)
        pygame.draw.rect(self.display,black,button)

        white =(255, 255 ,255)
        bFont = pygame.font.SysFont("freesans", 50)
        sFont = pygame.font.SysFont("freesans", 20)

        welcomeText = bFont.render("Chess", False,black)
        createdBy = sFont.render("Created by Prokopiuk Oleksandr",True,black)
        buttonLabel = sFont.render("Play",True,white)

        self.display.blit(welcomeText,((self.display.get_width() - welcomeText.get_width()) //2,
        150))
        self.display.blit(createdBy,((self.display.get_width()-createdBy.get_width())//2,
        self.display.get_height() - createdBy.get_height()-100))
        self.display.blit(buttonLabel,((button.x +(button.width - buttonLabel.get_width()) // 2,
        button.y + (button.height - buttonLabel.get_height())//2)))

        keyPressed = pygame.key.get_pressed()
        util = Utilities()

        if util.leftClick():
            mouseCoords = util.mouseCoords()

            if button.collidepoint(mouseCoords[0],mouseCoords[1]):
                pygame.draw.rect(self.display,white,button,3)

                self.menuActive = True
            elif keyPressed[K_RETURN]:
                self.menuActive = True

    def game(self):
        color = (0,0,0)
        self.display.fill(color)
        self.display.blit(self.boardImg,self.boardDimensions)
        self.chess.playTurn()
        self.chess.drawPieces()
    
    def declareWinner(self, winner):
        bgColor = (255,255,255)
        self.display.fill(bgColor)
        black = (0,0,0)
        resetButton = pygame.Rect(250,300,140,50)
        pygame.draw.rect(self.display,black,resetButton)

        white = (255,255,255)
        bFont = pygame.font.SysFont("arial",50)
        sFont = pygame.font.SysFont("arial",20)
        text = winner + " wins!"
        winner_text= bFont.render(text,False,black)

        resetLabel = "Play again"
        resetButtonLabel = sFont.render(resetLabel,True,white)

        self.display.blit(winner_text,
        ((self.display.get_width() - winner_text.get_width()) // 2,
        150))

        self.display.blit(resetButtonLabel,
        ((resetButton.x + (resetButton.width - resetButtonLabel.get_width()) // 2,
        resetButton.y + (resetButton.height - resetButtonLabel.get_height()) // 2)))

        keyPressed =  pygame.key.get_pressed()

        util = Utilities()

        if util.leftClick():
            mouseCoords = util.mouseCoords()

            if resetButton.collidepoint(mouseCoords[0],mouseCoords[1]):
                pygame.draw.rect(self.display,white,resetButton,3)

                self.menuActive = False
            elif keyPressed[K_RETURN]:
                self.menuActive = False
            self.chess.refresh()
            self.chess.winner = ""
