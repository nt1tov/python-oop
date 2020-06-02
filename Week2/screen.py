

import pygame
import random
import math



SCREEN_DIM = (800, 600)


class Vec2d:
    def __init__(self, coord):
        self.x = [None, None]
        self.x[0] = coord[0]
        self.x[1] = coord[1]
       # print(self.x)


    def __sub__(self, other):
        '''возвращает разность двух векторов'''
        return Vec2d((self.x[0] - other.x[0],  self.x[1] - other.x[1]))


    def __add__(self, other):
        """возвращает сумму двух векторов"""

        return  Vec2d((self.x[0] + other.x[0],  self.x[1] + other.x[1]))

    def __str__(self):
        return f"{self.x[0], self.x[1]} "

    def __repr__(self):
         return f"{self.x[0], self.x[1]} "

    def __len__(self):
        """возвращает длину вектора"""
        return math.sqrt(self.x[0] * self.x[0] + self.x[1] * self.x[1])

    def __mul__(self, k):
        """возвращает произведение вектора на число"""
        return Vec2d((self.x[0] * k, self.x[1] * k))

    def __rmul__(self, k):
        """возвращает произведение вектора на число"""
        return Vec2d((self.x[0] * k, self.x[1] * k))

    @property
    def int_pair(self):
        return (self.x[0], self.x[1])



class Polyline:
    

    def __init__(self):
        self.points = []
        self.speeds = []
        
    
    def add_point(self, point):
        # print(f"Point {point} added to list")
        
        self.points.append(Vec2d(point))
        # print(f"List: {self.points}")
        self.speeds.append(Vec2d((random.random() * 2, random.random() * 2)))

    def set_points(self):
        """функция перерасчета координат опорных точек"""
        for p in range(len(self.points)):
           
            
            self.points[p] +=  self.speeds[p] #add(points[p], speeds[p])
            speed = self.speeds[p]
            point = self.points[p]
            if point.int_pair[0] > SCREEN_DIM[0] or point.int_pair[0] < 0:
                self.speeds[p] = Vec2d((- speed.int_pair[0], speed.int_pair[1]))
            if point.int_pair[1] > SCREEN_DIM[1] or point.int_pair[1] < 0:
                self.speeds[p] = Vec2d((speed.int_pair[0], -speed.int_pair[1]))

    def draw_points(self, points, style="points", width=3, color=(255, 255, 255)):
       # print(f"Len of points: {len(points)}")
        """функция отрисовки точек на экране"""
        if style == "line":
            for p_n in range(-1, len(points) - 1):
               # print(points)
                point1 = points[p_n]
                point2 = points[p_n+1]
                pygame.draw.line(gameDisplay, color,
                                (int(point1.int_pair[0]), int(point1.int_pair[1])),
                                (int(point2.int_pair[0]), int(point2.int_pair[1])), width)

        elif style == "points":
            for p in points:
                pygame.draw.circle(gameDisplay, color,
                                (int(p.int_pair[0]), int(p.int_pair[1])), width)


class Knot(Polyline):
    def __init__(self):
        super().__init__()
        self.hue = 0
        self.steps = 3
        self.color = pygame.Color(0)

    def SmoothUp(self):
        self.steps +=1

    def SmoothDown(self):
        self.steps -= 1 if self.steps > 1 else 0
    
    def Clear(self):
        self.points = []
        self.speeds
        self.steps = 3
        self.color = pygame.Color(0)




    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return alpha*points[deg] + (1-alpha)*self.get_point(points, alpha, deg-1)
        #return add(mul(points[deg], alpha), mul(get_point(points, alpha, deg - 1), 1 - alpha))

    def get_points(self, base_points):
        alpha = 1 / self.steps
        res = []
        for i in range(self.steps):
            res.append(self.get_point(base_points, i * alpha))
        return res

    
    def get_knot(self):
        p = self.points
        if len(p) < 3:
            return []
        res = []

        for i in range(-2, len(p) - 2):
            ptn = []
            #ptn.append(mul(add(points[i], points[i + 1]), 0.5))
            ptn.append(0.5*(p[i]+p[i+1]))
            ptn.append(p[i+1])
            ptn.append(0.5*(p[i+1]+p[i+2]))
            #ptn.append(mul(add(points[i + 1], points[i + 2]), 0.5))

            res.extend(self.get_points(ptn))
        return res

    def draw_points(self):     
        self.hue = (self.hue + 1) % 360
        self.color.hsla = (self.hue, 100, 50, 100)
        #print(f"List: {len(self.points)}")
        super().draw_points(points=self.points, style="points", width=3, color=(255, 255, 255))
        super().draw_points(points=self.get_knot(), style="line", width=3, color=self.color)



def draw_help(steps):
    """функция отрисовки экрана справки программы"""
    gameDisplay.fill((0, 255, 0))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["****", "****"])
    data.append([str(steps), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 255, 255, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (0, 0, 0)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (0, 0, 0)), (200, 100 + 30 * i))


# =======================================================================================
# Функции, отвечающие за расчет сглаживания ломаной
# =======================================================================================



# =======================================================================================
# Основная программа
# =======================================================================================
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    working = True

    show_help = False
    pause = True

    

    knot = Knot()

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    knot.Clear()
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    print("++ new steps")
                    steps.SmoothUp()
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    print("-- new steps")
                    knot.SmoothDown()

            if event.type == pygame.MOUSEBUTTONDOWN:
                knot.add_point(event.pos)

        gameDisplay.fill((0, 0, 0))

        if not show_help:
            knot.draw_points()
            if not pause:
                knot.set_points()
        else:
            draw_help(knot.steps)

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
