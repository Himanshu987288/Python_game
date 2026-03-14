import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 640, 6403
SQ = WIDTH // 8
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Chess Game")

WHITE = (240, 217, 181)
BROWN = (181, 136, 99)
GREEN = (0, 255, 0)
BLACK = (0,0,0)

font = pygame.font.SysFont(None, 48)

board = [
 ["br","bn","bb","bq","bk","bb","bn","br"],
 ["bp"]*8,
 ["--"]*8,
 ["--"]*8,
 ["--"]*8,
 ["--"]*8,
 ["wp"]*8,
 ["wr","wn","wb","wq","wk","wb","wn","wr"]
]

selected = None
valid_moves = []
turn = "w"

def draw_board():
    for r in range(8):
        for c in range(8):
            color = WHITE if (r+c)%2==0 else BROWN
            pygame.draw.rect(WIN,color,(c*SQ,r*SQ,SQ,SQ))

def draw_pieces():
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p!="--":
                text = font.render(p[1].upper(), True, BLACK)
                WIN.blit(text,(c*SQ+20,r*SQ+20))

def draw_highlight():
    for (r,c) in valid_moves:
        pygame.draw.circle(WIN,GREEN,(c*SQ+SQ//2,r*SQ+SQ//2),10)

def pawn_moves(r,c):
    moves=[]
    d = -1 if board[r][c][0]=="w" else 1
    if 0<=r+d<8 and board[r+d][c]=="--":
        moves.append((r+d,c))
    return moves

def rook_moves(r,c):
    moves=[]
    dirs=[(1,0),(-1,0),(0,1),(0,-1)]
    for d in dirs:
        for i in range(1,8):
            rr=r+d[0]*i
            cc=c+d[1]*i
            if 0<=rr<8 and 0<=cc<8:
                if board[rr][cc]=="--":
                    moves.append((rr,cc))
                else:
                    if board[rr][cc][0]!=board[r][c][0]:
                        moves.append((rr,cc))
                    break
    return moves

def knight_moves(r,c):
    m=[(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
    moves=[]
    for dr,dc in m:
        rr,cc=r+dr,c+dc
        if 0<=rr<8 and 0<=cc<8:
            if board[rr][cc]=="--" or board[rr][cc][0]!=board[r][c][0]:
                moves.append((rr,cc))
    return moves

def get_moves(r,c):
    p=board[r][c][1]
    if p=="p": return pawn_moves(r,c)
    if p=="r": return rook_moves(r,c)
    if p=="n": return knight_moves(r,c)
    return []

clock=pygame.time.Clock()

while True:
    clock.tick(60)

    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            pygame.quit()
            sys.exit()

        if e.type==pygame.MOUSEBUTTONDOWN:
            x,y=pygame.mouse.get_pos()
            r,c=y//SQ,x//SQ

            if selected:
                if (r,c) in valid_moves:
                    sr,sc=selected
                    board[r][c]=board[sr][sc]
                    board[sr][sc]="--"
                    turn="b" if turn=="w" else "w"
                selected=None
                valid_moves=[]
            else:
                if board[r][c]!="--" and board[r][c][0]==turn:
                    selected=(r,c)
                    valid_moves=get_moves(r,c)

    draw_board()
    draw_pieces()
    draw_highlight()
    pygame.display.update()
