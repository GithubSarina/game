# -*- coding: utf-8 -*-
"""
Created on Sat May 25 14:38:00 2024

@author: hong
"""

import pygame
import random
import time,sys

# 게임 환경 설정
block_size = 30
screen_width = 10 * block_size
screen_height = 20 * block_size
black = (0, 0, 0)
white = (255, 255, 255)
board = [[0 for x in range(screen_width//block_size)] for y in range(screen_height//block_size)]
#board[17] = [(255,255,255),(255,255,255),(255,255,255),(255,255,255),(255,255,255),(255,255,255),(255,255,255),(255,255,255),(255,255,255),0]
#board[18] = [(255,255,255),(255,255,255),(255,255,255),(255,255,255),(255,255,255),(255,255,255),(255,255,255),(255,255,255),(255,255,255),0]
#board[19] = [(255,255,255),(255,255,255),(255,255,255),(255,255,255),(255,255,255),(255,255,255),(255,255,255),(255,255,255),(255,255,255),0]
textFonts = ['comicsansms', 'arial']
textSize = 48
RED = (255,0,0)
score = 0


# 블록 클래스 정의
class Block:
    def __init__(self):
        self.x = screen_width // block_size // 2 - 1
        self.y = 0
        self.color = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)])
        self.rotation = 0
        self.block = self.get_block(self.color)

    def get_block(self, color):
        if color == (255, 0, 0):  # I 블록
            return [[1, 1, 1, 1]]
        elif color == (0, 255, 0):  # S 블록
            return [[0, 1, 1], [1, 1, 0]]
        elif color == (0, 0, 255):  # L 블록
            return [[1, 1, 1], [1, 0, 0]]
        else:  # O 블록
            return [[1, 1], [1, 1]]

    def rotate(self):
        rotated_block = list(map(list, zip(*self.block[::-1])))
        if not self.check_collision(self.x, self.y, rotated_block):
            self.block = rotated_block
            self.rotation = (self.rotation + 1) % 4

    def move_left(self):
        if not self.check_collision(self.x-1, self.y, self.block):
            self.x -= 1

    def move_right(self):
        if not self.check_collision(self.x+1, self.y, self.block):
            self.x += 1

    def move_down(self):
        if not self.check_collision(self.x, self.y+1, self.block):
            self.y += 1
        else:
            # 블록을 보드에 추가
            for i in range(len(self.block)):
                for j in range(len(self.block[0])):
                    if self.block[i][j]:
                        x = self.x + j
                        y = self.y + i
                        if y >= 0:
                            board[y][x] = self.color
    def jump(self):
        

            # 새로운 블록 생성
            self.__init__()

    def check_collision(self, x, y, block):
        for i in range(len(block)):
            for j in range(len(block[0])):
                if block[i][j]:
                    if x+j >= screen_width//block_size or x+j < 0 or y+i >= screen_height//block_size or y+i < 0:
                        return True
                    elif board[y+i][x+j] != 0:
                        return True
        return False

    def draw(self):
        for i in range(len(self.block)):
            for j in range(len(self.block[0])):
                if self.block[i][j]:
                    pygame.draw.rect(screen, self.color, [block_size*(self.x+j), block_size*(self.y+i), block_size, block_size], 0)
    
  
                

# 게임 초기
# 게임 초기화
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tetris - Score : " + str(score))
clock = pygame.time.Clock()
current_block = Block()

# 게임 루프
while True:
    pygame.display.set_caption("Tetris - Score : " + str(score))
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            #exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_block.move_left()
            elif event.key == pygame.K_RIGHT:
                current_block.move_right()
            elif event.key == pygame.K_DOWN:
                current_block.move_down()
            elif event.key == pygame.K_UP:
                current_block.rotate()
            elif event.key == pygame.K_SPACE:
                current_block.jump()

    # 화면 업데이트
    screen.fill(black)

    # 보드 그리기
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j]:
                pygame.draw.rect(screen, board[i][j], [block_size*j, block_size*i, block_size, block_size], 0)

    # 블록 그리기
    current_block.draw()

    # 블록 이동
    if current_block.y + len(current_block.block) <= screen_height // block_size:
        if not current_block.check_collision(current_block.x, current_block.y+1, current_block.block):
            current_block.move_down()
        else:
            # 블록을 보드에 추가
            for i in range(len(current_block.block)):
                for j in range(len(current_block.block[0])):
                    if current_block.block[i][j]:
                        x = current_block.x + j
                        y = current_block.y + i
                        if y >= 0:
                            board[y][x] = current_block.color


           
            y = 19
            while y > 0:
                total = 0
                for x in range(10):
                    if board[y][x] == 0:
                        total += 1
                if total == 0:
                    for k in range(y, 0, -1):
                        board[k] = board[k-1]
                    board[0] = [0 for i in range(10)]
                    score += 1
                else:
                    y -= 1
                if not ([0,0,0,0,0,0,0,0,0,0] == board[0]):
                    pygame.init()
                    fontGameOver = pygame.font.SysFont(textFonts, textSize)
                    textGameOver = fontGameOver.render("Game Over!", True, RED)
                    rectGameOver = textGameOver.get_rect()
                    rectGameOver.center = (screen_width//2, screen_height//2)
                    screen.fill(black)
                    screen.blit(textGameOver, rectGameOver)
                    pygame.display.update()
                    time.sleep(5)
                    pygame.quit()
                    sys.exit()
                    
            
                    
            # 새로운 블록 생성
            current_block = Block()
    else:
        # 게임 종료
        pygame.quit()
        #exit()

    pygame.display.update()
    clock.tick(5)