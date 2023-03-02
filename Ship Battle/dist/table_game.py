war_map = [
    [-3,-3,-3,-3,-3,-3,-3,-3,-3, -2],
    [-3, 0, 0, 0, 0, 0, 0, 0, 0, -2],
    [-3, 0, 0, 0, 0, 0, 0, 0, 0, -2],
    [-3, 0, 0, 0, 0, 0, 0, 0, 0, -2],
    [-3, 0, 0, 0, 0, 0, 0, 0, 0, -2],
    [-3, 0, 0, 0, 0, 0, 0, 0, 0, -2],
    [-3, 0, 0, 0, 0, 0, 0, 0, 0, -2],
    [-3, 0, 0, 0, 0, 0, 0, 0, 0, -2],
    [-3, 0, 0, 0, 0, 0, 0, 0, 0, -2]]

import pygame
from settings import *
from timer import Timer
from copy import deepcopy

class TableGame:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.reset()
        #image
        self.surf = pygame.Surface((tile_size, tile_size))
        self.ship_surf = pygame.Surface((tile_size -4, tile_size -5))
        self.v_line = pygame.Surface((2, tile_size))
        self.v_line.fill('black')
        self.h_line = pygame.Surface((tile_size, 2))
        self.h_line.fill('black')
        #mouse
        self.mouse_pos = [0, 0]
        self.mouse_timer = Timer(0.3)
        #font
        self.font = pygame.font.Font('font/Pixeltype.ttf', 40)
        self.timer_msg = Timer(0.6)
        self.timer_msg.active()

    def reset(self):
        self.comp_map = [deepcopy(war_map), deepcopy(war_map)]
        self.ply_map = [deepcopy(war_map), deepcopy(war_map)]
        self.id_map = 0
        self.ships = [2, 3, 3, 4, 5]
        self.space = [[0, 0], [10, 0]]
        self.ships_placed = [False, False]
        self.msg_ships_placed = [False, False]
        self.placed_ships_pos = [[], []]
        self.placed_shoots_pos = [[], []]
        self.nice_shoots = [[0], [0]]
        self.horiz_ship = True
        self.win = False
        self.winner = 0
    
    def blit_text(self, text, pos, color):
        txt_surf = self.font.render(text, False, color)
        txt_rect = txt_surf.get_rect(center= pos)
        self.display_surface.blit(txt_surf, txt_rect)

    def blit_shadow_text(self, text, pos, color, backcolor='black'):
        self.blit_text(text, [pos[0] + 1, pos[1] + 1], backcolor)
        self.blit_text(text, [pos[0] - 1, pos[1] - 1], backcolor)
        self.blit_text(text, pos, color)

    def place_ships(self, mouse_pos):
        #posiciona os ships no começo do jogo
        atual_map = self.comp_map[self.id_map]
        space = self.space[self.id_map]
        pos = [mouse_pos[0] - space[0], mouse_pos[1] - space[1]]
        if 0 <= pos[0] <= 8 and 0 <= pos[1] <= 8:
            if atual_map[pos[1]][pos[0]] == 0:
                ship_pos = self.return_ship(pos)
                for pos in ship_pos:
                    if pos[0] < 1 or pos[0] > 8 or pos[1] < 1 or pos[1] > 8 or atual_map[pos[1]][pos[0]] != 0:
                        return
                    
                self.placed_ships_pos[self.id_map].append(ship_pos)
                for pos in ship_pos:
                    atual_map[pos[1]][pos[0]] = 1
                
                self.ships.pop(0)
                if len(self.ships) == 0:
                    self.ships_placed[self.id_map] = True
                    self.ships = [2, 3, 3, 4, 5]
                    self.id_map = 1
                    self.timer_msg.active()
    
    def place_shoot(self, mouse_pos):
        #posiciona os ships no começo do jogo
        atual_map = self.ply_map[self.id_map]
        space = self.space[self.id_map]
        pos = [mouse_pos[0] - space[0], mouse_pos[1] - space[1]]
        if 0 <= pos[0] <= 8 and 0 <= pos[1] <= 8:
            if atual_map[pos[1]][pos[0]] == 0:                
                if self.comp_map[self.id_map][pos[1]][pos[0]] == 1:
                    color = 'red'
                    self.nice_shoots[self.id_map][0] += 1
                    print(self.nice_shoots)
                else:
                    color = 'black'
                self.placed_shoots_pos[self.id_map].append([pos[0], pos[1], color])
                atual_map[pos[1]][pos[0]] = 1
                self.id_map = (self.id_map + 1) % 2
                self.timer_msg.active()

    def return_ship(self,  pos):
        if self.horiz_ship:
            if self.ships[0] == 2:
                ship_pos = [[pos[0]-1, pos[1]], [pos[0], pos[1]]]
            elif self.ships[0] == 3:
                ship_pos = [[pos[0]-1, pos[1]], [pos[0], pos[1]], [pos[0]+1, pos[1]]]
            elif self.ships[0] == 4:
                ship_pos = [[pos[0]-1, pos[1]], [pos[0], pos[1]], [pos[0]+1, pos[1]], [pos[0]+2, pos[1]]]
            elif self.ships[0] == 5:
                ship_pos = [[pos[0]-2, pos[1]],[pos[0]-1, pos[1]], [pos[0], pos[1]], [pos[0]+1, pos[1]], [pos[0]+2, pos[1]]]
        else:
            if self.ships[0] == 2:
                ship_pos = [[pos[0], pos[1]-1], [pos[0], pos[1]]]
            elif self.ships[0] == 3:
                ship_pos = [[pos[0], pos[1]-1], [pos[0], pos[1]], [pos[0], pos[1]+1]]
            elif self.ships[0] == 4:
                ship_pos = [[pos[0], pos[1]-1], [pos[0], pos[1]], [pos[0], pos[1]+1], [pos[0], pos[1]+2]]
            elif self.ships[0] == 5:
                ship_pos = [[pos[0], pos[1]-2],[pos[0], pos[1]-1], [pos[0], pos[1]], [pos[0], pos[1]+1], [pos[0], pos[1]+2]]
        return ship_pos
    
    def check_win(self):
        if self.nice_shoots[0][0] == 17:
            self.win = True
            self.winner = 1
        elif self.nice_shoots[1][0] == 17:
            self.win = True
            self.winner = 0

    def input(self):
        if not self.mouse_timer.run:
            self.mouse_pos = [int(pygame.mouse.get_pos()[0]/tile_size), int(pygame.mouse.get_pos()[1]/tile_size)]
            if pygame.mouse.get_pressed()[0]:
                if self.win:
                    self.reset()
                else:
                    if not self.ships_placed[self.id_map]:
                        self.place_ships(self.mouse_pos)
                    else:
                        self.place_shoot(self.mouse_pos)
                        self.check_win()
                self.mouse_timer.active()
            elif not self.ships_placed[self.id_map] and pygame.mouse.get_pressed()[2]:
                self.horiz_ship = not self.horiz_ship
                self.mouse_timer.active()

    def update(self):
        if self.mouse_timer.run:
            self.mouse_timer.update()
        if self.timer_msg.run:
            self.timer_msg.update()
        self.input()

    def draw_msg(self, text, pos):
        pygame.draw.rect(self.display_surface, 'black', [pos[0] - 100, pos[1] - 20, 200, 40])
        pygame.draw.rect(self.display_surface, 'white', [pos[0] - 100, pos[1] - 20, 200, 40], 3)
        self.blit_shadow_text(text, (pos[0], pos[1]), 'red', backcolor='gray')

    def draw_map(self, space, index):
        for j, col in enumerate(self.comp_map[index]):
            for i, num in enumerate(col):
                x = (i + space) * tile_size
                y = j * tile_size

                if num == -2:
                    self.surf.fill('black')
                elif num == -3:
                    self.surf.fill('red')
                else:
                    self.surf.fill('gray')
                self.display_surface.blit(self.surf, (x, y))
                self.display_surface.blit(self.v_line, (x, y))
                self.display_surface.blit(self.h_line, (x, y))
                self.display_surface.blit(self.v_line, (x + tile_size, y))
                self.display_surface.blit(self.h_line, (x, y + tile_size))

    def draw_place_ship(self, mouse_pos):
        if not self.ships_placed[self.id_map]:
            atual_map = self.comp_map[self.id_map]
            space = self.space[self.id_map]
            pos = [mouse_pos[0] - space[0], mouse_pos[1] - space[1]]
            color = 'purple'
            if 0 <= pos[0] <= 8 and 0 <= pos[1] <= 8:
                if atual_map[pos[1]][pos[0]] == 0:
                    ship_pos = self.return_ship(pos)

                    for pos in ship_pos:
                        if pos[0] < 1 or pos[0] > 8 or pos[1] < 1 or pos[1] > 8 or atual_map[pos[1]][pos[0]] != 0:
                            color = 'black'
                            break

                    self.ship_surf.fill(color)
                    for pos in ship_pos:
                        x = (pos[0] + space[0]) * tile_size
                        y = (pos[1] + space[1]) * tile_size
                        self.display_surface.blit(self.ship_surf, (x + 3, y + 3))

    def draw_placed_ships(self):
        if not self.ships_placed[self.id_map]:
            self.ship_surf.fill('red')
            space = self.space[self.id_map]
            for ships_pos in self.placed_ships_pos[self.id_map]:
                for ship_pos in ships_pos:
                    x = (ship_pos[0] + space[0]) * tile_size
                    y = (ship_pos[1] + space[1]) * tile_size
                    self.display_surface.blit(self.ship_surf, (x + 3, y + 3))

    def draw_ply_map(self, space, index):
        for j, col in enumerate(self.ply_map[index]):
            for i, num in enumerate(col):
                x = (i + space) * tile_size
                y = j * tile_size

                if num == -2:
                    self.surf.fill('black')
                elif num == -3:
                    self.surf.fill('red')
                
                else:
                    self.surf.fill('gray')
                self.display_surface.blit(self.surf, (x, y))
                self.display_surface.blit(self.v_line, (x, y))
                self.display_surface.blit(self.h_line, (x, y))
                self.display_surface.blit(self.v_line, (x + tile_size, y))
                self.display_surface.blit(self.h_line, (x, y + tile_size))

    def draw_place_shoot(self, mouse_pos):
        atual_map = self.ply_map[self.id_map]
        space = self.space[self.id_map]
        pos = [mouse_pos[0] - space[0], mouse_pos[1] - space[1]]
        if 0 <= pos[0] <= 8 and 0 <= pos[1] <= 8:
            if atual_map[pos[1]][pos[0]] == 0:
                color = 'purple'
            else:
                color = 'black'
            x = (pos[0] + space[0]) * tile_size
            y = (pos[1] + space[1]) * tile_size
            self.ship_surf.fill(color)
            self.display_surface.blit(self.ship_surf, (x + 3, y + 3))
                
    def draw_placed_shoots(self, id):
        space = self.space[id]
        for shoot_pos in self.placed_shoots_pos[id]:
            self.ship_surf.fill(shoot_pos[2])
            x = (shoot_pos[0] + space[0]) * tile_size
            y = (shoot_pos[1] + space[1]) * tile_size
            self.display_surface.blit(self.ship_surf, (x + 3, y + 3))

    def draw(self):
        if not self.ships_placed[self.id_map]:
            self.draw_map(0, 0)
            self.draw_map(10, 1)
            self.draw_place_ship(self.mouse_pos)
            self.draw_placed_ships()
        else:
            self.draw_map(0, 0)
            self.draw_map(10, 1)
            self.draw_place_shoot(self.mouse_pos)
            self.draw_placed_shoots(0)
            self.draw_placed_shoots(1)
        
        if self.timer_msg.run:
            if not self.ships_placed[self.id_map]:
                txt = 'Place Ship'
                pos = [tile_size*(5+self.space[self.id_map][0]), tile_size*(5+self.space[self.id_map][1])]
            else:
                txt = 'Shoot Enemy Ship'
                id = 1 if self.id_map == 0 else 0
                pos = [tile_size*(5+self.space[id][0]), tile_size*(5+self.space[id][1])]
            self.draw_msg(txt, pos)

        if self.win:
            txt = 'WIN!'
            pos = [tile_size*(5+self.space[self.id_map][0]), tile_size*(5+self.space[self.id_map][1])]
            self.draw_msg(txt, pos)
