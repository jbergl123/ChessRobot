import pygame as p
import Engine


WIDTH = HEIGHT = 728
DIMENSION = 8
SQSIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ["bp","br", "bn",
              "bb", "bq", "bk",
              "wp", "wr", "wn",
              "wb", "wq", "wk"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("assets/images/imgs-80px/" + piece + ".png"), (SQSIZE,SQSIZE))

#Driver: User input, updating graphics
def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = Engine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag for when a move is made

    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []


    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x,y) of mouse clik
                col = location[0]//SQSIZE
                row = location[1]//SQSIZE
                if sqSelected == (row, col):
                    sqSelected = () #deselect
                    playerClicks = [] #deselect
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2: #on second click move that junt
                    move = Engine.Move(playerClicks[0], playerClicks[1], gs.board)
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            sqSelected = () #reset clicks
                            playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

#Responsible for all graphics in a current game state
def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    colors = [p.Color(255,255,255), p.Color(105,146,62)]

    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row+col) % 2)]
            p.draw.rect(screen, color, p.Rect(col*SQSIZE, row*SQSIZE, SQSIZE, SQSIZE))



def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(col*SQSIZE, row*SQSIZE, SQSIZE,SQSIZE))



main()