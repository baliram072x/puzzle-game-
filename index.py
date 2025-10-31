import pygame
import random

pygame.init()

# Updated window size for better layout
screen_width, screen_height = 540, 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sliding Puzzle Professional")

# Colors
WHITE = (245, 245, 245)
BLACK = (20, 20, 20)
DARK_GRAY = (62, 68, 83)
BLUE = (32, 140, 222)
GREEN = (30, 204, 106)
RED = (255, 90, 95)
YELLOW = (255, 206, 86)
SHADOW = (225, 225, 230)

main_font = pygame.font.SysFont("Segoe UI", 44)
tile_font = pygame.font.SysFont("Segoe UI Black", 44)
button_font = pygame.font.SysFont("Segoe UI", 22)  # Slightly smaller for better fit

levels = {'Easy': 3, 'Medium': 4, 'Hard': 5}
current_level = 'Easy'
size = levels[current_level]

def get_solved_board(sz):
    arr = list(range(1, sz*sz))
    arr.append(0)
    return arr

def new_board(sz):
    board = get_solved_board(sz)[:]
    for _ in range(100*sz):
        zero = board.index(0)
        moves = []
        row, col = divmod(zero, sz)
        if row > 0: moves.append(zero - sz)
        if row < sz-1: moves.append(zero + sz)
        if col > 0: moves.append(zero - 1)
        if col < sz-1: moves.append(zero + 1)
        swap = random.choice(moves)
        board[zero], board[swap] = board[swap], board[zero]
    return board

class Button:
    def __init__(self, text, center, size, color, hovercolor, radius=18):
        self.text = text
        self.center = center
        self.size = size
        self.rect = pygame.Rect(0, 0, *size)
        self.rect.center = center
        self.color = color
        self.hovercolor = hovercolor
        self.radius = radius

    def draw(self, surf, mouse):
        col = self.hovercolor if self.rect.collidepoint(mouse) else self.color
        pygame.draw.rect(surf, SHADOW, self.rect.move(2,4), border_radius=self.radius)
        pygame.draw.rect(surf, col, self.rect, border_radius=self.radius)
        label = button_font.render(self.text, True, WHITE if col != YELLOW else BLACK)
        label_rect = label.get_rect(center=self.rect.center)
        surf.blit(label, label_rect)

    def clicked(self, mouse, event):
        return self.rect.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1

def draw_board(board, sz):
    tile_size = 420 // sz
    offset_x = (screen_width - tile_size*sz)//2
    offset_y = 32
    for idx, tile in enumerate(board):
        x = (idx % sz) * tile_size + offset_x
        y = (idx // sz) * tile_size + offset_y
        rect = pygame.Rect(x+6, y+6, tile_size-12, tile_size-12)
        if tile:
            pygame.draw.rect(screen, BLUE, rect, border_radius=18)
            pygame.draw.rect(screen, DARK_GRAY, rect, 3, border_radius=18)
            txt = tile_font.render(str(tile), True, WHITE)
            txtr = txt.get_rect(center=rect.center)
            screen.blit(txt, txtr)
    pygame.draw.rect(screen, DARK_GRAY, (offset_x-2, offset_y-2, tile_size*sz+4, tile_size*sz+4), 4, border_radius=22)

def is_solved(board, sz):
    return board == get_solved_board(sz)

def move_tile(board, sz, idx):
    zero = board.index(0)
    row0, col0 = divmod(zero, sz)
    row, col = divmod(idx, sz)
    if (abs(row0-row) == 1 and col0 == col) or (abs(col0-col) == 1 and row0 == row):
        board[zero], board[idx] = board[idx], board[zero]

def main():
    global current_level, size
    size = levels[current_level]
    board = new_board(size)
    solved_board = get_solved_board(size)
    running = True
    win = False

    # Button layout adjusted for better spacing
    btn_y = 455
    btns = [
        Button("Refresh",  (80,btn_y), (100,40), GREEN, (54,205,130)),
        Button("New",      (190,btn_y), (80,40), BLUE, (77,182,242)),
        Button("Easy",     (280,btn_y), (60,40), YELLOW, (246,231,89)),
        Button("Medium",   (370,btn_y), (80,40), YELLOW, (246,231,89)),
        Button("Hard",     (460,btn_y), (60,40), YELLOW, (246,231,89)),
    ]
    level_btn_indices = [2,3,4]
    level_names = ["Easy", "Medium", "Hard"]

    while running:
        mouse = pygame.mouse.get_pos()
        screen.fill(WHITE)

        draw_board(board, size)

        # Title
        title = main_font.render("Sliding Puzzle",True, DARK_GRAY)
        screen.blit(title, (screen_width//2 - title.get_width()//2, 3))

        # Highlight selected level
        for i, level in enumerate(level_names):
            if current_level == level:
                btns[2+i].color = (255, 191, 0)
                btns[2+i].hovercolor = (252, 220, 110)
            else:
                btns[2+i].color = YELLOW
                btns[2+i].hovercolor = (246,231,89)

        # Draw all buttons
        for btn in btns:
            btn.draw(screen, mouse)
        
        if win:
            over = pygame.Surface((screen_width, 80), pygame.SRCALPHA)
            pygame.draw.rect(over, (34,197,94,198), over.get_rect(), border_radius=15)
            wintext = main_font.render("Congratulations!", True, WHITE)
            winrect = wintext.get_rect(center = (screen_width//2, 45))
            over.blit(wintext, winrect.move(0,8))
            screen.blit(over, (0,screen_height//2 - 48))
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif not win and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x,y = event.pos
                offset_x = (screen_width - (420//size)*size)//2
                offset_y = 32
                tile_size = 420 // size
                if offset_x < x < offset_x+tile_size*size and offset_y < y < offset_y+tile_size*size:
                    col = (x - offset_x)//tile_size
                    row = (y - offset_y)//tile_size
                    idx = row*size + col
                    move_tile(board, size, idx)
                    if is_solved(board, size):
                        win = True

            # Button Functions
            for i, btn in enumerate(btns):
                if btn.clicked(mouse, event):
                    if i == 0: # Refresh
                        board = solved_board[:]
                        win = False
                    elif i == 1: # New
                        board = new_board(size)
                        win = False
                    elif i in level_btn_indices:
                        current_level = level_names[i-2]
                        size = levels[current_level]
                        board = new_board(size)
                        solved_board = get_solved_board(size)
                        win = False

    pygame.quit()

if __name__ == "__main__":
    main()