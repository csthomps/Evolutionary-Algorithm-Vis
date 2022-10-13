from xmlrpc.client import boolean
import pygame as p
import numpy as np
import random


ROWS = 9
COLS = 9

GEN_SIZE = 5000

WIDTH = 810
HEIGHT = 810

WIN = p.display.set_mode((WIDTH,HEIGHT))
p.display.set_caption("Genetic Algorithm Visualization")

def init_grids():
    grid1 = np.zeros((ROWS,COLS),boolean)
    grid2 = np.zeros((ROWS,COLS),boolean)
    return grid1,grid2

def draw_screen(win,grid1,grid2):
    win.fill(p.Color("White"))
    width1 = WIDTH // COLS
    height1 = HEIGHT // ROWS//2
    
    # drawing lines on grid
    for i in range(ROWS*2):
        p.draw.line(win,p.Color("Grey"),(0,i*height1),(WIDTH,i*height1))
        for j in range(COLS):
            p.draw.line(win,p.Color("Grey"),(j*width1,0),(j*width1,WIDTH))
    
    for i in range(ROWS):
        for j in range(COLS):
            if grid1[i][j]:
                p.draw.rect(win,p.Color("Black"),(j*width1,i*height1,width1,height1))
            if grid2[i][j]:
                p.draw.rect(win,p.Color("Black"),(j*width1,i*height1 + HEIGHT//2,width1,height1))
                
            
    p.draw.line(win,p.Color("black"),(0,HEIGHT//2),(WIDTH,HEIGHT//2),width=2)
    
    p.display.update()

def generate():
    grid2 = []
    
    for i in range(GEN_SIZE):
        grid2.append(np.zeros((ROWS,COLS),boolean))
        for row in range(ROWS):
            for col in range(COLS):
                if random.randint(0,1) > 0:
                    grid2[i][row][col] = True
                else:
                    grid2[i][row][col] = False
    return grid2

def compare(grid1,grid2):
    best_score = -ROWS*COLS - 10
    best_grid = None
    second_best_grid = None
    for i in range(len(grid2)):
        score = 0
        for row in range(ROWS):
            for col in range(COLS):
                if grid1[row][col] == grid2[i][row][col]:
                    score += 1
        if score > best_score:
            best_score = score
            second_best_grid = best_grid
            best_grid = grid2[i]
        elif score == best_score:
            second_best_grid = grid2[i]
            

    return best_grid,best_score,second_best_grid

def smart_generate(grid2,grid2_1):
    grid2_new = []
    comparison_grid = np.equal(grid2,grid2_1)
    for i in range(GEN_SIZE):
        grid2_new.append(np.zeros((ROWS,COLS),boolean))
        for row in range(ROWS):
            for col in range(COLS):
                if comparison_grid[row][col]: # if the two best from last generation are the same 
                    if random.randint(0,50) < 45: # 45 in 50 chance to just keep same 
                        grid2_new[i][row][col] = grid2[row][col]
                    else: # 5 in 50 chance to change
                        grid2_new[i][row][col] = not grid2[row][col]
                else:
                    if random.randint(0,1) == 0:
                        grid2_new[i][row][col] = True
                    else: grid2_new[i][row][col] = False
    # for i in range(GEN_SIZE//2):
    #     grid2_new.append(grid2)
    #     for row in range(ROWS):
    #         for col in range(COLS):
    #             if random.randint(0,1) == 0:
    #                 grid2_new[i][row][col] = not grid2[row][col]
    grid2_new.append(grid2)
    return grid2_new

def get_clicked_pos(pos): # get the position of a click
    width1 = WIDTH // COLS
    height1 = HEIGHT // ROWS//2
    
    x,y = pos
    
    row = y // height1
    col = x // width1
    return row,col

grid1,grid2 = init_grids()
grid2_1 = None
running = False
while True:
    for event in p.event.get():
        if event.type == p.QUIT:
            p.quit()
        
        if event.type == p.MOUSEBUTTONDOWN:
            pos = p.mouse.get_pos()
            row,col = get_clicked_pos(pos)
            if row > ROWS-1: # if in the bottom half, do nothing
                pass
            else: # if in the top half, switch color
                grid1[row][col] = not grid1[row][col]
        if event.type == p.KEYDOWN:
            if event.key == p.K_SPACE:
                score = 0
                running = not running
                grid2 = generate()
                grid2,score,grid2_1 = compare(grid1,grid2)
                draw_screen(WIN,grid1,grid2)
                count = 1
                
                while score < ROWS*COLS and running:
                    for event in p.event.get():
                        if event.type == p.KEYDOWN:
                            if event.key == p.K_SPACE:
                                running = not running

                        
                    grid2 = smart_generate(grid2,grid2_1)
                    grid2,score,grid2_1 = compare(grid1,grid2)
                    count += 1
                    draw_screen(WIN,grid1,grid2)
                
                print(count)
                running = False
                    

    draw_screen(WIN,grid1,grid2)
    
