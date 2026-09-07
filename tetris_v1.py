import random
import pygame, sys
from pygame import mixer
from datetime import datetime, time
from tkinter import messagebox
from button_ver1 import Buttons
from mysql.connector import connect, Error
 
"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""
 
pygame.font.init()
 
# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30


mixer.init()

exp_sound = mixer.Sound('assets/explode.wav')
exp_sound.set_volume(0.5)
exp_play = True
poch_sound = mixer.Sound('assets/change.wav')
poch_sound.set_volume(0.5)
poch_play = True
game_sound = mixer.Sound('assets/game_over.wav')
game_sound.set_volume(0.5)

pause = False
run = True
BG = pygame.image.load("assets/Background.png")

 
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height
 
 
# SHAPE FORMATS
 
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]
 
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
 
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]
 
O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
 
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
 
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
 
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]
 
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape
  

class Piece(object):
    rows = 20  # y
    columns = 10  # x
 
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # number from 0-3

    
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)
 
def create_grid(locked_positions={}):
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]
 
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid
 
 
def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]
 
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
 
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
 
    return positions
 
 
def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)
 
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
 
    return True
 
 
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    global shapes, shape_colors
 
    return Piece(5, 0, random.choice(shapes))
 
 
def draw_text_middle(text, size, color, surface):
    font = get_font(size)
    label = font.render(text, 1, color)
 
    surface.blit(label, (top_left_x + play_width/2 - (label.get_width() / 2), top_left_y + play_height/2 - label.get_height()/2))
 
 
def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128,128,128), (sx, sy+ i*30), (sx + play_width, sy + i * 30))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (128,128,128), (sx + j * 30, sy), (sx + j * 30, sy + play_height))  # vertical lines
 
 
def clear_rows(grid, locked,play):
    
    global exp_sound
    # need to see if row is clear the shift every other row above down one
 
    inc = 0
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            # add positions to remove from locked
            ind = i
            if play == True:
                exp_sound.play()
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc
 
 
def draw_next_shape(shape, surface):
    
    global top_left_x
    
    
    font = get_font(15)
    label = font.render('Next Shape', 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    
    format = shape.shape[shape.rotation % len(shape.shape)]
 
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*30, sy + i*30, 30, 30), 0)
 
    surface.blit(label, (sx + 10, sy- 30))
 
 
def draw_window(surface,score = 0, time = '0:0:0'):
    surface.fill((0,0,0))
    # Tetris Title
    font = get_font(40)
    label = font.render('TETRIS', 1, (255,255,255))
 
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    font = get_font(15)
    label_s = font.render('Score: ' + str(score), 1, (255,255,255))

    label_t = font.render('Timer: ' + time, 1, (255,255,255))
 
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    surface.blit(label_s, (sx + 10, sy + 180))
    surface.blit(label_t, (sx - 20, sy + 250))
 
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j* 30, top_left_y + i * 30, 30, 30), 0)
 
    # draw grid and border
    draw_grid(surface, 20, 10)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)
    # pygame.display.update()

def pause_page(SCREEN,BG):
    global pause
    global run

    running = True
    while running:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("PAUSE MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 150))

        PLAY_BUTTON = Buttons(image=pygame.image.load("assets/Play Rect.png"), pos=(400, 350), 
                            text_input="RESUME", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Buttons(image=pygame.image.load("assets/Play Rect.png"), pos=(400, 500), 
                            text_input="QUIT GAME", font=get_font(25), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    running = False
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    running = False
                    run = False
                    #pygame.quit()
                    #sys.exit()

        pygame.display.update()

    pause = False
 
def main(play,vol,filename,explay,loseplay,poch_play,playId):
    global grid
    global poch_sound
    global game_sound
    global pause
    global run

    if run == False:
        run = True
 
    locked_positions = {}  # (x,y):(255,0,0)
    grid = create_grid(locked_positions)
 
    change_piece = False
    #run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    clock_time = 0
    changeSpeed = False

    score = 0

    play_time = datetime.now()
    secs = 0
    mins = 0
    hours = 0

    q = 0
    scores = range(30,150,30) # [30, 60, 90, 120]

    fall_speed = 0.37
 
    while run:
        
        icon = pygame.image.load("assets/pause.png")
        icon = pygame.transform.scale(icon, (60, 60))

        PAUSE_BUTTON = Buttons(image=icon, pos=(100,85),text_input='',font=get_font(2),base_color="#d7fcd4", hovering_color="White")

        if score % 30 == 0 and score == scores[q] and q < 5:
            if fall_speed > 0.15:
                fall_speed -= 0.05
                q += 1
           
        
        grid = create_grid(locked_positions)
        if pause == False:
            fall_time += clock.get_rawtime()
            clock_time += clock.get_rawtime()
            clock.tick()
 
        # PIECE FALLING CODE
        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        if clock_time/1000 >= 1:
            secs += 1
            if secs == 60:
                mins += 1
                secs = 0
            if mins == 60:
                hours += 1
                mins = 0
            clock_time = 0
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PAUSE_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    if pause == False:
                        pause = True
                        pause_page(win,BG)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
 
                elif event.key == pygame.K_d:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_w:
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if poch_play == True:
                        poch_sound.play()
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)
 
                if event.key == pygame.K_s:
                    # move shape down
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
 
                if event.key == pygame.K_SPACE:
                   while valid_space(current_piece, grid):
                       current_piece.y += 1
                   current_piece.y -= 1
                   if poch_play == True:
                        poch_sound.play()
                   #print(convert_shape_format(current_piece))  # todo fix
 
        shape_pos = convert_shape_format(current_piece)
 
        # add piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color
 
        # IF PIECE HIT GROUND
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
 
            # call four times to check for multiple clear rows
            score += clear_rows(grid, locked_positions,explay) * 10
 
        timer = ('{}:{}:{}'.format(hours,mins,secs))
        draw_window(win,score,timer)
        draw_next_shape(next_piece, win)

        PAUSE_BUTTON.changeColor(pygame.mouse.get_pos())
        PAUSE_BUTTON.update(win)

        pygame.display.update()
 
        # Check if user lost
        if check_lost(locked_positions):
            run = False
    
    mixer.music.stop()
    draw_text_middle("You Lost", 40, (255,255,255), win)
    if loseplay == True:
        game_sound.play()
        
    dur = time(hour=hours,minute=mins,second=secs)
    try:
        connection = connect(host = 'localhost',user = 'root', password = '', database = 'testing', port = '3306')
        conn = connection.cursor()
        insert_query = f'''INSERT INTO `info`(`score`, `date`, `duration`, `player_id`) 
        VALUES ({score},'{play_time}','{dur}',{playId})
        '''
        conn.execute(insert_query)
        # print('New row added.')
        connection.commit()
    except Error as e:
        messagebox.showerror('',f'Connection not working. {e}')
        print(e)

    score = 0
    pygame.display.update()
    pygame.time.delay(2000)
    
    if play == 1:
        mixer.music.load(filename)
        mixer.music.set_volume(vol)
        mixer.music.play(-1)
    
win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
 
#main_menu()  # start game