from typing import Counter
from pieces import Pieces
from utilities import Utilities
import pygame
from pygame.locals import *
import time
import random

class Chess(object):
    def __init__(self,display,piece,coords,lenght):

        self.pieces = {
            "white_king": 0,
            "white_queen": 1,
            "white_bishop": 2,
            "white_knight": 3,
            "white_rook": 4,
            "white_pawn": 5,
            "black_king": 6,
            "black_queen": 7,
            "black_bishop": 8,
            "black_knight": 9,
            "black_rook": 10,
            "black_pawn": 11
        }
        
        self.display = display # поверхня дисплею
        self.chessPieces = Pieces(piece,columns = 6, rows =2) # об'єкт класу Piece для відображення фігур на екрані
        self.boardLocation = coords # збереження координат квадратів дошки
        self.turn = {'black': 0, 'white': 0} #збереження інформації про кількість ходів
        self.lenght = lenght #сторона квадрату шахматної дошки
        self.moves =[] #можливі рухи
        self.utils = Utilities() # об'єкт класу Utils для доступу до методів 
        self.capuredFigures = [] # фігури котрі покинули поле
        self.winner = "" # переможець
        self.refresh()

    def refresh(self): # метод ініціалізації поля нової гри
        self.moves = [] # очистка можливих рухів

        x= random.randint(0,1) # випадковий вибір черги ходів
        if(x == 1):
            self.turn['black'] = 1
        elif(x==0):
            self.turn['white'] = 1
        
        # двохвимірний словних для збереження місця усіх фігур
        self.pieceLocation = {}
        x=0
        for i in range (97,105): # a-h
            a=8
            b=0
            self.pieceLocation[chr(i)] = {}
            while a > 0:# збереження позиції кожного елементу, формат - [назва,поточна?,координати]
                self.pieceLocation[chr(i)][a] = ["",False,[x,b]]
                a = a -1
                b = b + 1
            x = x+1
        # перезапуск дошки
        
        for i in range (97,105):
            x = 8
            while x > 0:
                if(x==8):
                    if(chr(i)== 'a' or chr(i) == 'h'):
                        self.pieceLocation[chr(i)][x][0] = "black_rook"
                    elif(chr(i)=='b' or chr(i) == 'g'):
                        self.pieceLocation[chr(i)][x][0] = "black_knight"
                    elif(chr(i) == 'c' or chr(i) == 'f'):
                        self.pieceLocation[chr(i)][x][0] = "black_bishop"
                    elif(chr(i) == 'd'):
                        self.pieceLocation[chr(i)][x][0] = "black_queen"
                    elif(chr(i) == 'e'):
                        self.pieceLocation[chr(i)][x][0] = "black_king"
                elif(x == 7):
                    self.pieceLocation[chr(i)][x][0] = "black_pawn"
                elif (x == 2):
                    self.pieceLocation[chr(i)][x][0] = "white_pawn"
                elif(x == 1):
                    if(chr(i) == 'a' or chr(i) == 'h'):
                        self.pieceLocation[chr(i)][x][0]= "white_rook"
                    elif(chr(i) == 'b' or chr(i) == 'g'):
                        self.pieceLocation[chr(i)][x][0]= "white_knight"
                    elif(chr(i) == 'c' or chr(i) == 'f'):
                        self.pieceLocation[chr(i)][x][0] = "white_bishop"
                    elif(chr(i) == 'd'):
                        self.pieceLocation[chr(i)][x][0] = "white_queen"
                    elif(chr(i) == 'e'):
                        self.pieceLocation[chr(i)][x][0]= "white_king"
                x= x-1
    
    # відрисовка фігур на дошці
    def drawPieces(self):
        tGreen = (0,194,39,170)
        

        #створення прозорого поля для вибраних фігур
        surface = pygame.Surface((self.lenght,self.lenght),pygame.SRCALPHA)
        surface.fill(tGreen)
        

        # цикл для зміни кольору 
        for value in self.pieceLocation.values():
            for secondValue in value.values():
                pieceName = secondValue[0] # назва поточної фігури
                pieceCoordX, pieceCoordY = secondValue[2] # координати поточної фігури

                if secondValue[1] and len(secondValue[0]) > 5: #зміна кольору фону при виборі фігури                    
                        self.display.blit(surface,self.boardLocation[pieceCoordX][pieceCoordY])
                        if len(self.moves) > 0:
                            for move in self.moves:
                                xCoord = move[0]
                                yCoord = move[1]
                                if xCoord >= 0 and yCoord >= 0 and xCoord < 8 and yCoord<8:
                                    self.display.blit(surface,self.boardLocation[xCoord][yCoord])
                    
        #цикл для рисування фігур
        for value in self.pieceLocation.values():
            for secondValue in value.values():
                #зчитування імені фігури та координат поточної позиції
                pieceName = secondValue[0]
                pieceCoordX,pieceCoordY = secondValue[2]
                #перевірка наявності фігури в квадраті 
                if(len(secondValue[0]) > 1):
                    self.chessPieces.drawPieces(self.display,pieceName,self.boardLocation[pieceCoordX][pieceCoordY])

    def playTurn(self):
        # робота з текстом
        white = (255,255,255)
        font = pygame.font.SysFont("freesans", 20)

        if self.turn["black"]:
            turnText = font.render("Black turn",True,white)
        elif self.turn["white"]:
            turnText = font.render("White turn", True, white)
        
        self.display.blit(turnText,((self.display.get_width() - turnText.get_width())//2,10))
        #виклик функції руху
        if(self.turn["black"]):
            self.movePiece("black")
        elif(self.turn["white"]):
            self.movePiece("white")

    
    def possibleMoves(self,pieceName,pieceCoord):
        # список для збереження можливих рухів
        positions = []
        # пошук можливих місць для руху 
        if len(pieceName) > 0:
            xCoord, yCoord = pieceCoord
            #рухи для Слона
            if pieceName[6:] == "bishop":
                positions = self.diagonalMoves(positions,pieceName,pieceCoord)
            
            #рухи для Пішки
            elif pieceName[6:] == "pawn":
                # конвертуємо інекс списку в словник перебираючи усі позиції фігури
                columnChar = chr(97 + xCoord)
                rowNumber = 8 - yCoord
                # рухи для чорної пішки

                if pieceName == "black_pawn":
                    if yCoord + 1 < 8: # перевірка чи клітинка не остання
                        #беремо наступний рядок
                        rowNumber = rowNumber - 1
                        frontPiece = self.pieceLocation[columnChar][rowNumber][0]
                        #Пішки не можуть рухатись якщо вони заблоковані іншою пішкою
                        if(frontPiece[6:] != "pawn"):
                            positions.append([xCoord , yCoord + 1])
                            # перший хід кожної пішки може бути на два кроки
                            if yCoord < 2:
                                positions.append([xCoord , yCoord + 2])
                            
                        #діагональ ліворуч
                        if(xCoord - 1 >= 0 and yCoord + 1 < 8):
                            x = xCoord - 1
                            y = yCoord + 1

                            columnChar = chr(97+x)
                            rowNumber = 8 - y
                            capture = self.pieceLocation[columnChar][rowNumber]

                            if(capture[0][:5] == "white"):
                                positions.append([x,y])
                        # діагональ праворуч
                        if (xCoord + 1 < 8 and yCoord + 1 < 8):
                            x = xCoord + 1
                            y = yCoord + 1

                            columnChar = chr(97 + x)
                            rowNumber = 8 -y
                            capture = self.pieceLocation[columnChar][rowNumber]

                            if(capture[0][:5] == "white"):
                                positions.append([x,y])
                
                #рухи для білої пішки
                elif pieceName == "white_pawn":
                    if yCoord - 1 >= 0:
                        rowNumber = rowNumber + 1
                        frontPiece = self.pieceLocation[columnChar][rowNumber][0]

                        if(frontPiece[6:] != "pawn"):
                            positions.append([xCoord,yCoord-1])

                            if yCoord > 5:
                                positions.append([xCoord,yCoord - 2])
                        # діагональ ліворуч
                        if xCoord - 1 >= 0 and yCoord - 1 >= 0:
                            x= xCoord - 1
                            y= yCoord - 1

                            columnChar =chr(97 + x)
                            rowNumber = 8 - y
                            capture = self.pieceLocation[columnChar][rowNumber]

                            if(capture[0][:5] == "black"):
                                positions.append([x,y])
                        # діагональ праворуч
                        if xCoord + 1 < 8 and yCoord - 1 >= 0:
                            x = xCoord + 1
                            y = yCoord - 1

                            columnChar = chr(97 + x)
                            rowNumber = 8 - y
                            capture = self.pieceLocation[columnChar][rowNumber]

                            if(capture[0][:5] == "black"):
                                positions.append([x,y])
            #рухи для ладьї

            elif pieceName[6:] == "rook":
                positions = self.linearMoves(positions,pieceName,pieceCoord)
            
            #рухи для коня

            elif pieceName[6:] == "knight":
                #ліва позиція 
                if (xCoord -2) >= 0:
                    if(yCoord - 1) >=0:
                        positions.append([xCoord-2,yCoord-1])
                    if(yCoord + 1) < 8:
                        positions.append([xCoord -2, yCoord + 1])
                #верхня позиція
                if (yCoord -2) >=0:
                    if(xCoord - 1) >= 0:
                        positions.append([xCoord-1, yCoord-2])
                    if(xCoord + 1) < 8:
                        positions.append([xCoord+1, yCoord-2])
                #права позиція
                if(xCoord + 2) < 8:
                    if(yCoord - 1) >= 0:
                        positions.append([xCoord+2, yCoord-1])
                    if(yCoord + 1) < 8:
                        positions.append([xCoord+2, yCoord+1])
                # нижня позиція 
                if(yCoord + 2) < 8:
                    if(xCoord - 1) >= 0:
                        positions.append([xCoord-1, yCoord+2])
                    if(xCoord + 1) < 8:
                        positions.append([xCoord+1, yCoord+2])
        #рухи для короля
            elif pieceName[6:] == "king":
                if(yCoord -1) >=0:
                    #верхня позиція
                    positions.append([xCoord,yCoord-1])
                if(yCoord + 1) < 8:
                    #нижня позиція
                    positions.append([xCoord,yCoord+1])
                if(xCoord -1)>=0:
                    #ліва позиція
                    positions.append([xCoord-1,yCoord])
                    #лівий верхній кут
                    if(yCoord -1 ) >= 0:
                        positions.append([xCoord -1, yCoord -1])
                    #лівий нижній кут
                    if(yCoord + 1) <8:
                        positions.append([xCoord-1,yCoord+1])
                if(xCoord + 1) < 8:
                    #права позиція
                    positions.append([xCoord+1,yCoord])
                    #верхня права
                    if(yCoord -1) >= 0:
                        positions.append([xCoord+1,yCoord -1 ])
                    #нижня права
                    if(yCoord+1)< 8:
                        positions.append([xCoord+1,yCoord+1])
            #рухи для королеви
            elif pieceName[6:] == "queen":
                positions = self.diagonalMoves(positions,pieceName,pieceCoord)
                positions = self.linearMoves(positions,pieceName,pieceCoord)
            remove = []

            #видалення позицій фігури яких перекрили інші
            for pos in positions:
                x,y = pos
                columnChar = chr(97 + x)
                rowNumber = 8 - y
                removePieceName = self.pieceLocation[columnChar][rowNumber][0]
                if(removePieceName[:5] == pieceName[:5]):
                    remove.append(pos)
            
            #очистка позицій з списку позицій
            for i in remove:
                positions.remove(i)
        
        return positions

        
    #діагональні ходи
    def diagonalMoves(self,position,pieceName,pieceCoord):
        x,y = pieceCoord
        while(True): # діагональ вверх-вліво
            x= x-1
            y= y-1
            if(x<0 or y<0):
                break
            else:
                position.append([x,y])
            
            column = chr(97 + x)
            rowNumber = 8 - y
            piece = self.pieceLocation[column][rowNumber]

            if len(piece[0]) > 0 and pieceName[:5] != piece[:5]: #зупинити якщо заблоковано фігурой
                break
        
        x,y = pieceCoord
        while(True): # діагональ вниз-вправо
            x = x+1
            y = y+1
            if(x >7 or y > 7):
                break
            else:
                position.append([x,y])
            
            column = chr(97 + x)
            rowNumber = 8 - y 
            piece = self.pieceLocation[column][rowNumber]

            if len(piece[0]) > 0 and pieceName[:5] != piece[:5]:
                break

        x,y = pieceCoord
        while(True): # діагональ вниз-вліво
            x = x-1
            y = y+1
            if(x < 0 or y > 7):
                break
            else:
                position.append([x,y])
            
            column = chr(97 + x)
            rowNumber = 8 - y
            piece = self.pieceLocation[column][rowNumber]

            if len(piece[0]) > 0 and pieceName[:5] != piece[:5]:
                break
        
        x,y = pieceCoord
        while(True):#вверх-вправо
            x = x + 1
            y = y - 1
            if(x > 7 or y < 0): 
                break
            else:
                position.append([x,y])
        
            column = chr(97 + x)
            rowNumber = 8 - y
            piece = self.pieceLocation[column][rowNumber]

            if len(piece[0]) > 0 and pieceName[:5] != piece[:5]:
                break

        return position     
    #ходи по прямих
    def linearMoves(self,position,pieceName,pieceCoords):
        x,y = pieceCoords

        while(x > 0):#ліво
            x = x -1
            position.append([x,y])

            column = chr(97 + x)
            rowNumber = 8 - y
            piece = self.pieceLocation[column][rowNumber]

            if len(piece[0]) > 0 and pieceName[:5] != piece[:5]:
                break
        
        x,y = pieceCoords
        while(x < 7):#вправо
            x = x + 1
            position.append([x,y])

            column = chr(97 + x)
            rowNumber = 8 - y
            piece = self.pieceLocation[column][rowNumber]

            if len(piece[0]) > 0 and pieceName[:5] != piece[:5]:
                break
        
        x,y = pieceCoords
        while(y > 0):#вверх
            y = y - 1
            position.append([x,y])

            column = chr(97 + x)
            rowNumber = 8 - y
            piece = self.pieceLocation[column][rowNumber]

            if len(piece[0]) > 0 and pieceName[:5] != piece[:5]:
                break
        
        x,y = pieceCoords
        while(y < 7):#вниз
            y = y + 1
            position.append([x,y])

            column = chr(97 + x)
            rowNumber = 8 - y
            piece = self.pieceLocation[column][rowNumber]

            if len(piece[0]) > 0 and pieceName[:5] != piece[:5]:
                break

        
        return position
        
    def movePiece(self,turn):
        #координати вибраного квадрату
        square = self.getSquare()

        if square:
            pieceName = square[0]
            pieceColor = pieceName[:5]
            column = square[1]
            rowNumber = square[2]

            x,y = self.pieceLocation[column][rowNumber][2]
            #якщо на вибраному квадраті є фігура
            if(len(pieceName) > 0) and (pieceColor == turn):
                #знайти всі можливі кроки 
                self.moves = self.possibleMoves(pieceName,[x,y])
            
            #механізм ходів
            p = self.pieceLocation[column][rowNumber]

            for i in self.moves:
                if i == [x,y]:
                    if (p[0][:5] == turn) or len(p[0]) == 0:
                        self.validateMove([x,y])
                    else:
                        self.capturePiece(turn,[column,rowNumber],[x,y])
            #перевірка ходу 
            if(pieceColor == turn):
                for k in self.pieceLocation.keys():
                    for key in self.pieceLocation[k].keys():
                        self.pieceLocation[k][key][1] = False #зняти мітки вибору фігур з інших
            
                self.pieceLocation[column][rowNumber][1] = True # мітка вибору на вибраній фігурі

    def getSquare(self):
        leftClick = self.utils.leftClick()

        if leftClick:
            mouseEvent = self.utils.mouseCoords()

            for i in range(len(self.boardLocation)):
                for j in range(len(self.boardLocation)):
                    rect = pygame.Rect(self.boardLocation[i][j][0],self.boardLocation[i][j][1],
                        self.lenght,self.lenght)
                    collisions = rect.collidepoint(mouseEvent[0],mouseEvent[1])
                    if collisions:
                        selected = [rect.x, rect.y]
                        #координати квадрата
                        for k in range(len(self.boardLocation)):
                            try:
                                l = None
                                l = self.boardLocation[k].index(selected)
                                if l!= None:
                                    for value in self.pieceLocation.values():
                                        for secondValue in value.values():
                                            if not value[1]:
                                                value[1] = False
                                    column = chr(97 + k)
                                    rowNumber = 8 - l
                                    pieceName = self.pieceLocation[column][rowNumber][0]

                                    return [pieceName,column,rowNumber]
                            except:
                                pass
        else: 
            return None
    
    def capturePiece(self,turn,boardCoord,pieceCoord):
        x,y = pieceCoord

        column, rowNumber = boardCoord
        piece = self.pieceLocation[column][rowNumber]

        if piece[0] == "white_king":
            self.winner ="black"
            print("Чорні виграли")
        elif piece[0] == "black_king":
            self.winner = "white"
            print("Білі виграли")
        
        self.capuredFigures.append(piece) #додання фігури в захвачені
        self.validateMove(pieceCoord) #логування даних
    
    def validateMove(self,destination):# логування даних в консоль
        destinationColumn = chr(97 + destination[0])
        destinationRow = 8 - destination[1]

        for k in self.pieceLocation.keys():
            for key in self.pieceLocation[k].keys():
                boardPiece = self.pieceLocation[k][key]

                if boardPiece[1]:
                    #відмінити вибір фігури
                    self.pieceLocation[k][key][1] = False
                    pieceName = self.pieceLocation[k][key][0]
                    self.pieceLocation[destinationColumn][destinationRow][0] = pieceName
                    srcName = self.pieceLocation[k][key][0]
                    self.pieceLocation[k][key][0] = ""

                    if(self.turn["black"]):
                        self.turn["black"] = 0
                        self.turn["white"] = 1
                    elif(self.turn["white"]):
                        self.turn["black"] = 1
                        self.turn["white"] = 0

                    srcLocation = k + str(key)
                    destinationLocation = destinationColumn + str(destinationRow)
                    print("{} рухається з {} до {}".format(srcName,srcLocation,destinationLocation))


                     
    

