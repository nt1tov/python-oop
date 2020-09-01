import pygame
import collections
import Service
import os
import random

colors = {
    "black": (0, 0, 0, 255),
    "white": (255, 255, 255, 255),
    "red": (255, 0, 0, 255),
    "green": (0, 255, 0, 255),
    "blue": (0, 0, 255, 255),
    "wooden": (153, 92, 0, 255),
}


class ScreenHandle(pygame.Surface):

    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            self.min_x = 0
            self.min_y = 0
            self.successor = args[-1]
            self.next_coord = args[-2]
            args = args[:-2]
        else:
            self.successor = None
            self.next_coord = (0, 0)
        super().__init__(*args, **kwargs)
        self.fill(colors["wooden"])

    def draw(self, canvas):
        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            self.successor.draw(canvas)

    # FIXME connect_engine
    def connect_engine(self, engine):
        self.engine = engine
        if self.successor is not None:
            self.successor.connect_engine(engine)


class GameSurface(ScreenHandle):



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.min_pos = [0, 0]
        self.screen_size = [0, 0]
        self.map_size = [0,0]

    # FIXME save engine and send it to next in chain
    def connect_engine(self, engine):
        self.game_engine = engine
        self.screen_size[0] = self.get_width() // self.game_engine.sprite_size
        self.screen_size[1] = self.get_height() // self.game_engine.sprite_size
        self.map_size[0] = len(self.game_engine.map[0])
        self.map_size[1] = len(self.game_engine.map)
        super().connect_engine(engine)

        

    def draw_hero(self):
        screen_size_x = 640 // self.game_engine.sprite_size
        screen_size_y = 480 // self.game_engine.sprite_size
        pos = self.game_engine.hero.position[:]


        if pos[0] + self.screen_size[0]//2 < self.map_size[0]:
            pos[0] = self.screen_size[0]//2 if pos[0] >= self.screen_size[0]//2 else pos[0]
        else:
            #FIXME
            pos[0] = self.screen_size[0]+1 - (self.map_size[0] - pos[0])


        if pos[1] + self.screen_size[1]//2 < self.map_size[1]:
            pos[1] = self.screen_size[1]//2 if pos[1] >= self.screen_size[1]//2 else pos[1]
        else:
            #FIXME
            pos[1] = self.screen_size[1] - (self.map_size[1] - pos[1]) 

        self.game_engine.hero.draw(self, pos)

  #  @staticmethod
    def calc_min_pos(self):
        obj_pos = self.game_engine.hero.position
        screen_size = self.screen_size
        

        calc = lambda p, s: max(0, p  - s//2)
        pos = self.min_pos[:]
        if obj_pos[0] + screen_size[0]//2 < self.map_size[0]:
            pos[0] =  calc(obj_pos[0], screen_size[0])
        
        if obj_pos[1] + screen_size[1]//2 <= self.map_size[1]:
            pos[1] =  calc(obj_pos[1], screen_size[1])
        
        self.min_pos = pos
        

    #480 x 640
    def draw_map(self):
        if self.game_engine.map:
            for i in range(len(self.game_engine.map[0]) - self.min_pos[0]):
                for j in range(len(self.game_engine.map) - self.min_pos[1]):
                   # print(self.game_engine.sprite_size)
                    self.blit(self.game_engine.map[self.min_pos[1] + j][self.min_pos[0] + i][0], (i * self.game_engine.sprite_size, j * self.game_engine.sprite_size))
        else:
            assert False, "No map"
            self.fill(colors["white"])

    def draw_object(self, sprite, coord):
        size = self.game_engine.sprite_size
        

        self.blit(sprite, ((coord[0] - self.min_pos[0]) * self.game_engine.sprite_size,
                           (coord[1] - self.min_pos[1]) * self.game_engine.sprite_size))

    def draw(self, canvas):
        self.calc_min_pos()


        self.draw_map()
        for obj in self.game_engine.objects:
            self.blit(obj.sprite[0], ((obj.position[0] - self.min_pos[0]) * self.game_engine.sprite_size,
                                      (obj.position[1] - self.min_pos[1]) * self.game_engine.sprite_size))
        self.draw_hero()

        # draw next surface in chain
        super().draw(canvas)
        #self.draw_next_chain(canvas)


   


class ProgressBar(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fill(colors["black"])

    def draw(self, canvas):
        self.fill(colors["black"])
        pygame.draw.rect(self, colors["black"], (50, 30, 200, 30), 2)
        pygame.draw.rect(self, colors["black"], (50, 70, 200, 30), 2)

        pygame.draw.rect(self, colors["red"], (50, 30, 200 * self.engine.hero.hp / self.engine.hero.max_hp, 30))
        pygame.draw.rect(self, colors["green"], (50, 70, 200 * self.engine.hero.exp / (100 * (2**(self.engine.hero.level - 1))), 30))

        font = pygame.font.SysFont("comicsansms", 20)
        self.blit(font.render(f'Hero at {self.engine.hero.position}', True, colors["white"]),
                  (250, 2))

        self.blit(font.render(f'{self.engine.level} floor', True, colors["white"]),
                  (10, 0))

        self.blit(font.render(f'HP', True, colors["white"]),
                  (10, 30))
        self.blit(font.render(f'Exp', True, colors["white"]),
                  (10, 70))

        self.blit(font.render(f'{self.engine.hero.hp}/{self.engine.hero.max_hp}', True, colors["white"]),
                  (60, 30))
        self.blit(font.render(f'{self.engine.hero.exp}/{(100*(2**(self.engine.hero.level-1)))}', True, colors["white"]),
                  (60, 70))

        self.blit(font.render(f'Level', True, colors["white"]),
                  (300, 30))
        self.blit(font.render(f'Gold', True, colors["white"]),
                  (300, 70))

        self.blit(font.render(f'{self.engine.hero.level}', True, colors["white"]),
                  (360, 30))
        self.blit(font.render(f'{self.engine.hero.gold}', True, colors["white"]),
                  (360, 70))

        self.blit(font.render(f'Str', True, colors["white"]),
                  (420, 30))
        self.blit(font.render(f'Luck', True, colors["white"]),
                  (420, 70))

        self.blit(font.render(f'{self.engine.hero.stats["strength"]}', True, colors["white"]),
                  (480, 30))
        self.blit(font.render(f'{self.engine.hero.stats["luck"]}', True, colors["white"]),
                  (480, 70))

        self.blit(font.render(f'SCORE', True, colors["white"]),
                  (550, 30))
        self.blit(font.render(f'{self.engine.score:.4f}', True, colors["white"]),
                  (550, 70))

        # draw next surface in chain
        super().draw(canvas)



class InfoWindow(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.len = 30
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)

    def update(self, value):
        self.data.append(f"> {str(value)}")

    def draw(self, canvas):
        self.fill(colors["black"])
        size = self.get_size()

        font = pygame.font.SysFont("comicsansms", 20)
        for i, text in enumerate(self.data):
            self.blit(font.render(text, True, colors["white"]), (5, 20 + 18 * i))

        # FIXME
        # draw next surface in chain
        super().draw(canvas)


    def connect_engine(self, engine):
        self.engine = engine
        self.engine.subscribe(self)
        super().connect_engine(engine)



class HelpWindow(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.len = 30
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)
        self.data.append([" →", "Move Right"])
        self.data.append([" ←", "Move Left"])
        self.data.append([" ↑ ", "Move Top"])
        self.data.append([" ↓ ", "Move Bottom"])
        self.data.append([" H ", "Show Help"])
        self.data.append(["Num+", "Zoom +"])
        self.data.append(["Num-", "Zoom -"])
        self.data.append([" R ", "Restart Game"])

    def draw(self, canvas):
        print("in draw")
        alpha = 0
        if self.engine.show_help:
            alpha = 128
        self.fill((0, 0, 0, alpha))
        size = self.get_size()
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        if self.engine.show_help:
            pygame.draw.lines(self,  colors["white"], True, [
                              (1, 1), (700, 0), (700, 500), (0, 500)], 5)
            for i, text in enumerate(self.data):
                self.blit(font1.render(text[0], True,  colors["white"]),
                          (50, 50 + 30 * i))
                self.blit(font2.render(text[1], True,  colors["white"]),
                          (150, 50 + 30 * i))
        
        super().draw(canvas)


class HelpWindow2(ScreenHandle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.len = 30
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)
        self.data.append([" →", "Move Right"])
        self.data.append([" ←", "Move Left"])
        self.data.append([" ↑ ", "Move Top"])
        self.data.append([" ↓ ", "Move Bottom"])
        self.data.append([" H ", "Show Help"])
        self.data.append(["Num+", "Zoom +"])
        self.data.append(["Num-", "Zoom -"])
        self.data.append([" R ", "Restart Game"])




    def draw(self, canvas):
        alpha = 0
        
        sprite_size = 100
        #background = [0]
        font1 = pygame.font.SysFont("courier", 70)
        font2 = pygame.font.SysFont("serif", 70)

        background = Service.create_sprite(os.path.join("texture", "background.png"), sprite_size, angle=90)
        #hero_logo = Service.create_sprite(os.path.join("texture", "hero-2.png"), 2*sprite_size, angle=0)
        #hero_logo_1 = Service.create_sprite(os.path.join("texture", "hero-2.png"), 150, angle=0)
        width = self.get_width()
        height = self.get_height()
        if self.engine.show_help:
            alpha = 128
        self.fill((0, 0, 0, alpha))
        if self.engine.show_help:
            for i in range(width // sprite_size):
                for j in range(height // sprite_size):
                    self.blit(background, (i * sprite_size, j * sprite_size))

            pygame.draw.lines(self,  colors["white"] , True, [(0, 0), (width, 0), (width, height), (0, height)], 10)

            # self.blit(hero_logo, (250, 50)) 
            # self.blit(hero_logo_1, (150, 100))


            for i, text in enumerate(self.data):
                self.blit(font1.render(text[0], True,  colors["white"]) ,
                            (150, 100 + 50 * i))
                self.blit(font2.render(text[1], True,  colors["white"]),
                            (300, 100 + 50 * i))
        super().draw(canvas)




class StartWindow(ScreenHandle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.blink_time = 50

        self.main_text = "Stoopid Knight Wars"
        self.start_text = "Press Space to start the game..."

    
    def draw_text(self):

        font1 = pygame.font.SysFont("courier", 70)
        font2 = pygame.font.SysFont("serif", 50)

        self.blit(font1.render(self.main_text, True,  colors["white"]), (150, 500))
        if self.blink_time >= 25:
            self.blink_time -= 1
            self.blit(font2.render(self.start_text, True,  colors["white"]), (200, 550))
        elif self.blink_time == 0:
            self.blink_time = 50
        else:
            self.blink_time -= 1

    def draw(self, canvas):
        alpha = 0
        
        sprite_size = 100

        background = Service.create_sprite(os.path.join("texture", "stone-ground-1.png"), sprite_size, angle=90)
        hero_logo = Service.create_sprite(os.path.join("texture", "hero-2.png"), 2*sprite_size, angle=0)
        gnome_1_logo = Service.create_sprite(os.path.join("texture/ally", "gnome-1.png"), 2*sprite_size, angle=0)
        gnome_2_logo = Service.create_sprite(os.path.join("texture/ally", "gnome-2.png"), 2*sprite_size, angle=0)
        gnome_3_logo = Service.create_sprite(os.path.join("texture/ally", "gnome-3.png"), 2*sprite_size, angle=0)

        knight_logo = Service.create_sprite(os.path.join("texture/enemies", "knight_enemy.png"), 2*sprite_size, angle=0)
        dragon_logo = Service.create_sprite(os.path.join("texture/enemies", "dragon.png"), 2*sprite_size, angle=0)
        naga_logo = Service.create_sprite(os.path.join("texture/enemies", "naga.png"), 2*sprite_size, angle=0)

        chest_logo = Service.create_sprite(os.path.join("texture/objects", "chest.png"), sprite_size, angle=0)

        width = self.get_width()
        height = self.get_height()

        if self.engine.show_start:
            alpha = 128
        self.fill((0, 0, 0, alpha))
        
        if self.engine.show_start:
            for i in range(width // sprite_size):
                for j in range(height // sprite_size):
                    self.blit(background, (i * sprite_size, j * sprite_size))


            pygame.draw.lines(self,  colors["white"] , True, [
                                (0, 0), (width, 0), (width, height), (0, height)], 10)

            self.blit(hero_logo, (height // 2, 50))
            self.blit(gnome_1_logo, (0, 300))
            self.blit(gnome_2_logo, (90, 300))
            self.blit(gnome_3_logo, (170, 300))
            self.blit(chest_logo, (width//2 - sprite_size//2, 250))
            self.blit(knight_logo, (width-200, 300))
            self.blit(dragon_logo, (width-250, 300))
            self.blit(naga_logo, (width-350, 300))

            self.draw_text()

            # for i, text in enumerate(self.data):
            #     self.blit(font1.render(text[0], True,  colors["white"]) ,
            #                 
            #     self.blit(font2.render(text[1], True,  colors["white"]),
            #                 (300, 100 + 30 * i))
        
        super().draw(canvas)
