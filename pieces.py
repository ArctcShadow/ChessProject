import os
import pygame

class Pieces(pygame.sprite.Sprite): # ініціалізація класу графічних об'єктів
    def __init__(self,file,columns,rows):
        pygame.sprite.Sprite.__init__(self)
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
        self.piece = pygame.image.load(file).convert_alpha() # завантаження рисунку фігур для вирізання
        self.rows = rows
        self.columns = columns
        self.cellCount = columns * rows

        self.rectangle = self.piece.get_rect() #зчитування розмірів фігури
        width = self.cellWidth = self.rectangle.width // self.columns # розрахунок ширини і висоти клітинки фігури
        height = self.cellHeight = self.rectangle.height // self.rows
        # розрахунок розміру клітинки для рисування на вікні користувача методом проходження по списку усіх елементів
        self.cells = list([(i % columns * width, i // columns * height, width, height) for i in range(self.cellCount)])

    def drawPieces(self,surface,pieceName,coords):
        pieceIndex = self.pieces[pieceName]
        surface.blit(self.piece,coords,self.cells[pieceIndex])