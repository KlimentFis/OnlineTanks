import pygame
import json


def get_settings():
	with open('settings.json', 'r') as file:
		data = json.load(file)

	tanki_params = data.get("Tanki", {})
	server = tanki_params.get("server")
	return server

class Mine_Field():
    def __init__(self, app):
        # self.mins = [Mins(app, i, j) for i in range(9)  for j in range(9) if randint(0, 10)== 1 and (i, j) != (0, 0)]
        self.mins = []
        self.tank = Tank(app)
        self.enemy_tank = Tank(app)
        self.enemy_tank.elements = [
        (1, 1, (64, 3, 3)), (2, 1, (64, 3, 3)), (3, 1, (64, 3, 3)), (4, 1, (64, 3, 3)), (5, 1, (64, 3, 3)), (6, 1, (64, 3, 3)), (7, 1, (64, 3, 3)), (1, 2, (64, 3, 3)), 
        (2, 2, (64, 3, 3)), (3, 2, (64, 3, 3)), (4, 2, (64, 3, 3)), (5, 2, (64, 3, 3)), (6, 2, (64, 3, 3)), (7, 2, (64, 3, 3)), (1, 6, (64, 3, 3)), (2, 6, (64, 3, 3)), 
        (3, 6, (64, 3, 3)), (4, 6, (64, 3, 3)), (5, 6, (64, 3, 3)), (6, 6, (64, 3, 3)), (7, 6, (64, 3, 3)), (1, 7, (64, 3, 3)), (2, 7, (64, 3, 3)), (3, 7, (64, 3, 3)), 
        (4, 7, (64, 3, 3)), (5, 7, (64, 3, 3)), (6, 7, (64, 3, 3)), (7, 7, (64, 3, 3)), (3, 3, (194, 6, 6)), (3, 4, (194, 6, 6)), (3, 5, (194, 6, 6)), (4, 3, (194, 6, 6)), 
        (4, 4, (194, 6, 6)), (4, 5, (194, 6, 6)), (5, 3, (194, 6, 6)), (5, 4, (194, 6, 6)), (5, 5, (194, 6, 6)), (6, 4, (194, 6, 6)), (7, 4, (194, 6, 6)), (8, 4, (194, 6, 6))]
        self.enemy_tank.x = 36
        self.enemy_tank.y = 36

    def update(self, app):
        # self.enemy_tank.update(app, self.tank)
        if self.tank.health <= 0:
            print("Танк взорван!")
            app.GameOver = True
            
        if len(self.mins) == 0 and self.enemy_tank.health <= 0:
            app.Win = True

        for i in self.tank.bullets:
            for j in self.mins:
                if i.get_cord(app) in j.get_cord(app):
                    self.tank.bullets.remove(i) 
                    self.mins.remove(j)
        
        for i in self.tank.get_cord(app):
            for j in self.mins:
                if i in j.get_cord(app):
                    # print(self.tank.elements)
                    # print(i[0]//app.cell_size - self.tank.x, i[1]//app.cell_size - self.tank.y)
                    # print("BOOM")
                    self.mins.remove(j)
                    self.tank.health -= 1

        for i in self.tank.bullets:
            if i.get_cord(app) in self.enemy_tank.get_cord(app):
                self.enemy_tank.health -= 1
                self.tank.bullets.remove(i)

        for i in self.enemy_tank.bullets:
            if i.get_cord(app) in self.tank.get_cord(app):
                self.tank.health -= 1
                self.enemy_tank.bullets.remove(i)
                    

    def draw(self, app):
        [min.draw(app) for min in self.mins]
        self.tank.draw(app)
        self.enemy_tank.draw(app)


class Mins():
    def __init__(self, x, y):
        self.x = x * 8
        self.y = y  * 8
        self.elements = [
        (3, 2, (21, 63, 87)), (4, 2, (21, 63, 87)), (5, 2, (21, 63, 87)), (2, 3, (21, 63, 87)), (3, 3, (21, 63, 87)), (5, 3, (21, 63, 87)), (6, 3, (21, 63, 87)), 
        (2, 4, (21, 63, 87)), (6, 4, (21, 63, 87)), (2, 5, (21, 63, 87)), (3, 5, (21, 63, 87)), (5, 5, (21, 63, 87)), (6, 5, (21, 63, 87)), (3, 6, (21, 63, 87)), 
        (4, 6, (21, 63, 87)), (5, 6, (21, 63, 87)),(3, 4, (25, 82, 115)), (4, 4, (25, 82, 115)), (5, 4, (25, 82, 115)), (4, 3, (25, 82, 115)), (4, 5, (25, 82, 115))]

    def draw(self, app):
        [pygame.draw.rect(app.display, color, ((x+ self.x) * app.cell_size, (y+self.y) * app.cell_size, app.cell_size, app.cell_size)) for x, y, color in self.elements]

    def get_cord(self, app):
        return [((x+ self.x) * app.cell_size, (y+self.y) * app.cell_size) for x, y, _ in self.elements]


class Tank():
    def __init__(self, app):
        self.health = 2
        self.x = 0
        self.y = 0
        self.ways = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.ind = 0
        self.dx = 1
        self.dy = 0 
        self.elements = [
        (1, 1, (110, 54, 1)), (2, 1, (110, 54, 1)), (3, 1, (110, 54, 1)), (4, 1, (110, 54, 1)), (5, 1, (110, 54, 1)), (6, 1, (110, 54, 1)), (7, 1, (110, 54, 1)), 
        (1, 2, (110, 54, 1)), (2, 2, (110, 54, 1)), (3, 2, (110, 54, 1)), (4, 2, (110, 54, 1)), (5, 2, (110, 54, 1)), (6, 2, (110, 54, 1)), (7, 2, (110, 54, 1)),
        (1, 6, (110, 54, 1)), (2, 6, (110, 54, 1)), (3, 6, (110, 54, 1)), (4, 6, (110, 54, 1)), (5, 6, (110, 54, 1)), (6, 6, (110, 54, 1)), (7, 6, (110, 54, 1)),
        (1, 7, (110, 54, 1)), (2, 7, (110, 54, 1)), (3, 7, (110, 54, 1)), (4, 7, (110, 54, 1)), (5, 7, (110, 54, 1)), (6, 7, (110, 54, 1)), (7, 7, (110, 54, 1)),
        (3, 3, (168, 85, 7)), (3, 4, (168, 85, 7)), (3, 5, (168, 85, 7)), (4, 3, (168, 85, 7)), (4, 4, (168, 85, 7)), (4, 5, (168, 85, 7)), (5, 3, (168, 85, 7)), 
        (5, 4, (168, 85, 7)), (5, 5, (168, 85, 7)), (6, 4, (168, 85, 7)), (7, 4, (168, 85, 7)), (8, 4, (168, 85, 7))]
        self.wounded_element = [
        (1, 1, (110, 54, 1)), (2, 1, (110, 54, 1)), (3, 1, (110, 54, 1)), (4, 1, (110, 54, 1)), (5, 1, (110, 54, 1)), (6, 1, (110, 54, 1)), (7, 1, (110, 54, 1)), 
        (1, 2, (110, 54, 1)), (2, 2, (110, 54, 1)), (3, 2, (110, 54, 1)), (4, 2, (110, 54, 1)), (5, 2, (110, 54, 1)), (6, 2, (41, 35, 23)), (7, 2, (41, 35, 23)),
        (1, 6, (110, 54, 1)), (2, 6, (110, 54, 1)), (3, 6, (110, 54, 1)), (4, 6, (110, 54, 1)), (5, 6, (110, 54, 1)), (6, 6, (41, 35, 23)), (7, 6, (41, 35, 23)),
        (1, 7, (110, 54, 1)), (2, 7, (110, 54, 1)), (3, 7, (110, 54, 1)), (4, 7, (110, 54, 1)), (5, 7, (110, 54, 1)), (6, 7, (110, 54, 1)), (7, 7, (110, 54, 1)),
        (3, 3, (168, 85, 7)), (3, 4, (168, 85, 7)), (3, 5, (168, 85, 7)), (4, 3, (168, 85, 7)), (4, 4, (168, 85, 7)), (4, 5, (168, 85, 7)), (5, 3, (41, 35, 23)), 
        (5, 4, (41, 35, 23)), (5, 5, (41, 35, 23)), (6, 4, (41, 35, 23)), (7, 4, (41, 35, 23)), (8, 4, (41, 35, 23))]
        self.die_elements = [
        (0, 0, (110, 54, 1)), (1, 0, (110, 54, 1)), (2, 0, (110, 54, 1)), (3, 0, (110, 54, 1)), (4, 0, (110, 54, 1)), (5, 0, (110, 54, 1)), (6, 0, (110, 54, 1)), 
        (7, 0, (110, 54, 1)), (0, 1, (110, 54, 1)), (1, 1, (110, 54, 1)), (2, 1, (110, 54, 1)), (3, 1, (110, 54, 1)), (4, 1, (110, 54, 1)), (5, 1, (110, 54, 1)), 
        (6, 1, (110, 54, 1)), (7, 1, (110, 54, 1)), (7, 2, (110, 54, 1)), (7, 3, (110, 54, 1)), (7, 4, (110, 54, 1)), (7, 5, (110, 54, 1)), (7, 6, (110, 54, 1)), 
        (7, 7, (110, 54, 1)), (7, 8, (110, 54, 1)), (8, 2, (110, 54, 1)), (8, 3, (110, 54, 1)), (8, 4, (110, 54, 1)), (8, 5, (110, 54, 1)), (8, 6, (110, 54, 1)), 
        (8, 7, (110, 54, 1)), (8, 8, (110, 54, 1)), (0, 0, (168, 85, 7)), (0, 1, (168, 85, 7)), (0, 2, (168, 85, 7)), (1, 0, (168, 85, 7)), (1, 1, (168, 85, 7)), 
        (1, 2, (168, 85, 7)), (2, 0, (168, 85, 7)), (2, 1, (168, 85, 7)), (2, 2, (168, 85, 7)), (4, 4, (168, 85, 7)), (4, 5, (168, 85, 7)), (4, 6, (168, 85, 7))]

        self.bullets = []

    def draw(self, app):
        if self.health <= 0:
            [pygame.draw.rect(app.display, color, ((x+ self.x) * app.cell_size, (y+self.y) * app.cell_size, app.cell_size, app.cell_size)) for x, y, color in self.die_elements]
        elif self.health == 1:
            [pygame.draw.rect(app.display, color, ((x+ self.x) * app.cell_size, (y+self.y) * app.cell_size, app.cell_size, app.cell_size)) for x, y, color in self.wounded_element]
            [bullet.update() for bullet in self.bullets]
            [bullet.draw() for bullet in self.bullets]
        else:
            [pygame.draw.rect(app.display, color, ((x+ self.x) * app.cell_size, (y+self.y) * app.cell_size, app.cell_size, app.cell_size)) for x, y, color in self.elements]
            [bullet.update() for bullet in self.bullets]
            [bullet.draw() for bullet in self.bullets]

    def move(self, app, forward):
        if self.health <= 0:
            return

        if forward == 1:
            self.cord = {
                (1, 0): (8, 4),
                (0, 1): (4, 8),
                (-1, 0): (0, 4),
                (0, -1): (4, 0)
            }
            pos = (self.x + self.cord[self.dx, self.dy][0], self.y + self.cord[self.dx, self.dy][1])
            if 0 < pos[0] + self.dx < app.row and 0 < pos[1] + self.dy < app.col:
                self.x += self.dx
                self.y += self.dy
        else:
            self.cord = {
                (1, 0): (0, 4),
                (0, 1): (4, 0),
                (-1, 0):(8, 4),
                (0, -1): (4, 8)
            }
            pos = (self.x + self.cord[self.dx, self.dy][0], self.y + self.cord[self.dx, self.dy][1])
            if 0 < pos[0] + self.dx < app.row and 0 < pos[1] + self.dy < app.col:
                self.x -= self.dx
                self.y -= self.dy


    def rotate(self, forward):    
        if self.health == 0:
            return
        if forward == 1:
            self.ind += 1
            self.elements = [(8 - j, i, color) for i, j, color in self.elements]
            self.wounded_element = [(8 - j, i, color) for i, j, color in self.wounded_element]
        if forward == -1:
            self.ind -= 1
            self.elements = [(j, 8 - i, color) for i, j, color in self.elements]
            self.wounded_element = [(j, 8 - i, color) for i, j, color in self.wounded_element]

        self.dx, self.dy = self.ways[self.ind % 4]
        
    def shot(self):
        if self.health == 0:
            return
        self.bullets += [Bullet(self.elements[-1][0] + self.x + self.dx, self.elements[-1][1] + self.y + self.dy, self.dx, self.dy)]

    def get_cord(self, app):
        return [((x+ self.x) * app.cell_size, (y+self.y) * app.cell_size) for x, y, _ in self.elements]

class Enemy(Tank):
    ...

class Bullet():
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = (255, 0, 0)

    def draw(self):
        [pygame.draw.rect(app.display, self.color, (self.x * app.cell_size, self.y * app.cell_size, app.cell_size, app.cell_size))]

    def update(self):
        self.x += self.dx 
        self.y += self.dy

    def get_cord(self, app):
        return (self.x * app.cell_size, self.y * app.cell_size)

class App():
    def __init__(self):
        self.cell_size = 10
        self.col = 81
        self.row = 81
        self.width = self.cell_size * self.row
        self.height = self.cell_size * self.col
        self.display = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.GameOver = False
        self.Win = False
        self.Win_print = [[210, 260], [210, 270], [220, 260], [220, 270], [210, 280], [220, 280], [220, 290], [220, 300], [230, 290], [230, 300], [220, 310], [230, 310], [230, 320], [230, 330], [240, 320], [240, 330], [240, 340], [230, 340], [250, 340], [260, 340], [250, 350], [260, 350], [270, 340], [270, 350], [280, 340], [280, 350], [290, 340], [290, 330], [290, 320], [300, 320], [300, 330], [300, 340], [300, 310], [300, 300], [300, 290], [310, 290], [310, 300], [310, 310], [310, 280], [310, 270], [310, 260], [320, 270], [320, 260], [320, 280], [260, 360], [270, 360], [260, 370], [270, 370], [260, 380], [270, 380], [260, 390], [270, 390], [260, 400], [270, 400], [270, 410], [260, 410], [410, 260], [420, 260], [430, 260], [440, 260], [450, 260], [460, 260], [470, 260], [400, 270], [390, 280], [480, 260], [490, 260], [500, 270], [510, 280], [390, 290], [390, 300], [390, 310], [390, 330], [390, 320], [390, 340], [390, 350], [390, 370], [390, 360], [390, 380], [390, 390], [400, 400], [410, 410], [430, 410], [420, 410], [440, 410], [450, 410], [460, 410], [470, 410], [480, 410], [490, 410], [500, 400], [510, 390], [510, 290], [510, 300], [510, 310], [510, 320], [510, 340], [510, 330], [510, 350], [510, 360], [510, 370], [510, 380], [400, 280], [410, 270], [420, 270], [430, 270], [440, 270], [460, 270], [470, 270], [450, 270], [480, 270], [490, 270], [500, 280], [490, 280], [500, 290], [500, 300], [500, 310], [500, 320], [500, 330], [500, 340], [500, 350], [500, 360], [500, 370], [500, 380], [500, 390], [490, 400], [490, 390], [480, 400], [470, 400], [460, 400], [450, 400], [440, 400], [430, 400], [420, 400], [410, 400], [410, 390], [400, 390], [400, 290], [400, 300], [410, 280], [400, 310], [400, 320], [400, 330], [400, 340], [400, 350], [400, 360], [400, 370], [400, 380], [560, 270], [560, 280], [560, 290], [560, 300], [560, 320], [560, 310], [560, 330], [560, 340], [560, 360], [560, 350], [560, 370], [560, 380], [560, 390], [570, 400], [580, 410], [590, 410], [600, 410], [610, 410], [620, 410], [630, 410], [640, 410], [650, 400], [660, 390], [660, 400], [660, 410], [670, 410], [670, 400], [670, 390], [660, 380], [670, 380], [660, 370], [670, 370], [660, 360], [670, 360], [660, 350], [670, 350], [660, 340], [670, 340], [660, 330], [670, 330], [660, 320], [670, 320], [660, 310], [670, 310], [660, 300], [670, 300], [660, 290], [670, 290], [660, 280], [670, 280], [660, 270], [670, 270], [570, 270], [570, 280], [570, 290], [570, 300], [570, 310], [570, 320], [570, 330], [570, 340], [570, 350], [570, 360], [570, 370], [570, 380], [570, 390], [580, 390], [580, 400], [590, 400], [600, 400], [610, 400], [620, 400], [630, 400], [640, 400], [650, 390], [150, 490], [150, 480], [160, 480], [160, 490], [150, 500], [160, 500], [170, 510], [170, 520], [180, 510], [180, 520], [170, 530], [180, 530], [190, 540], [200, 540], [190, 550], [200, 550], [190, 560], [200, 560], [210, 570], [220, 570], [210, 580], [220, 580], [210, 590], [220, 590], [230, 560], [240, 560], [230, 550], [240, 550], [230, 540], [240, 540], [250, 530], [250, 520], [260, 520], [260, 530], [270, 540], [280, 540], [270, 550], [280, 550], [270, 560], [280, 560], [290, 570], [290, 580], [300, 570], [300, 580], [290, 590], [300, 590], [310, 550], [310, 540], [320, 540], [320, 550], [320, 560], [330, 530], [330, 520], [330, 510], [340, 510], [340, 520], [340, 530], [350, 500], [350, 490], [350, 480], [360, 480], [360, 490], [360, 500], [560, 260], [570, 260], [660, 260], [670, 260], [250, 540], [260, 540], [230, 570], [200, 570], [180, 540], [190, 530], [160, 510], [170, 500], [280, 570], [290, 560], [310, 570], [300, 560], [310, 560], [330, 540], [320, 530], [350, 510], [340, 500], [270, 530], [240, 530], [210, 560], [220, 560], [440, 480], [440, 490], [450, 480], [450, 490], [440, 510], [450, 510], [440, 520], [450, 520], [440, 530], [450, 530], [440, 550], [450, 540], [440, 540], [450, 550], [440, 560], [450, 560], [440, 570], [450, 570], [440, 580], [450, 580], [440, 590], [450, 590], [440, 600], [450, 600], [560, 480], [560, 490], [560, 500], [560, 510], [560, 520], [560, 530], [560, 540], [560, 600], [560, 590], [560, 580], [560, 570], [560, 560], [560, 550], [570, 490], [570, 500], [580, 500], [580, 510], [590, 510], [590, 520], [600, 530], [610, 530], [610, 540], [620, 540], [620, 550], [630, 550], [630, 560], [640, 560], [660, 600], [660, 590], [650, 580], [660, 580], [650, 570], [660, 560], [660, 570], [660, 550], [660, 530], [660, 540], [660, 520], [660, 510], [660, 500], [660, 490], [660, 480], [570, 510], [640, 570], [670, 480], [670, 490], [670, 500], [670, 510], [670, 520], [670, 530], [670, 540], [670, 550], [670, 560], [670, 570], [670, 580], [670, 590], [670, 600], [570, 600], [570, 590], [570, 580], [570, 570], [570, 560], [570, 550], [570, 540], [570, 530], [570, 520], [570, 480], [580, 490], [590, 500], [600, 510], [600, 520], [610, 520], [620, 530], [630, 540], [640, 550], [650, 560]]
        self.game_over_print = [[210, 270], [200, 270], [190, 270], [180, 280], [190, 280], [220, 270], [230, 270], [230, 280], [220, 280], [240, 280], [200, 280], [190, 290], [180, 290], [170, 290], [170, 300], [180, 300], [170, 310], [180, 310], [170, 320], [180, 320], [170, 330], [180, 330], [170, 340], [180, 340], [170, 350], [180, 350], [170, 360], [180, 360], [170, 370], [180, 370], [190, 370], [180, 380], [190, 380], [200, 380], [210, 380], [210, 280], [240, 290], [190, 390], [200, 390], [210, 390], [220, 390], [220, 380], [230, 380], [230, 390], [240, 380], [240, 370], [230, 370], [240, 360], [250, 360], [250, 370], [250, 350], [240, 350], [240, 340], [230, 340], [230, 350], [220, 340], [220, 350], [210, 340], [210, 350], [250, 340], [250, 290], [240, 300], [250, 300], [280, 390], [290, 390], [280, 380], [290, 380], [280, 370], [290, 360], [290, 350], [290, 340], [300, 360], [300, 350], [300, 340], [300, 330], [310, 330], [300, 320], [310, 320], [300, 310], [310, 310], [310, 300], [320, 300], [310, 290], [320, 290], [310, 280], [320, 280], [320, 270], [330, 270], [340, 280], [340, 290], [330, 280], [330, 300], [330, 290], [340, 300], [350, 310], [340, 310], [340, 320], [350, 320], [340, 330], [350, 330], [350, 350], [350, 340], [360, 340], [360, 350], [350, 360], [360, 360], [360, 370], [360, 380], [360, 390], [370, 370], [370, 380], [370, 390], [310, 350], [320, 350], [330, 350], [340, 350], [310, 360], [320, 360], [330, 360], [340, 360], [290, 370], [300, 370], [350, 370], [400, 280], [400, 290], [400, 300], [400, 310], [400, 320], [400, 330], [400, 340], [400, 350], [400, 360], [400, 370], [400, 380], [400, 390], [410, 280], [410, 270], [420, 280], [410, 290], [410, 300], [410, 310], [410, 320], [410, 330], [410, 340], [410, 350], [410, 360], [410, 370], [410, 380], [410, 390], [420, 290], [430, 290], [420, 300], [430, 300], [430, 310], [440, 300], [450, 310], [440, 310], [440, 320], [450, 320], [450, 330], [460, 330], [460, 320], [470, 310], [470, 320], [470, 330], [460, 340], [480, 320], [480, 310], [480, 300], [490, 300], [490, 310], [490, 290], [500, 290], [500, 300], [500, 280], [510, 280], [510, 290], [510, 270], [520, 280], [520, 290], [520, 300], [520, 310], [510, 300], [510, 310], [520, 320], [510, 320], [520, 330], [510, 330], [510, 340], [520, 340], [510, 350], [520, 350], [510, 360], [520, 360], [510, 370], [520, 370], [510, 380], [520, 380], [510, 390], [520, 390], [560, 270], [550, 280], [560, 280], [570, 270], [570, 280], [580, 270], [580, 280], [590, 270], [590, 280], [600, 270], [600, 280], [610, 270], [610, 280], [620, 280], [550, 290], [560, 290], [550, 300], [560, 300], [550, 310], [560, 310], [550, 320], [560, 320], [550, 330], [560, 330], [550, 340], [560, 340], [550, 350], [560, 350], [550, 360], [560, 360], [550, 370], [560, 370], [550, 380], [560, 380], [560, 390], [570, 390], [570, 380], [580, 380], [580, 390], [590, 380], [620, 270], [630, 280], [590, 390], [600, 390], [610, 390], [620, 390], [610, 380], [600, 380], [620, 380], [630, 380], [570, 330], [570, 340], [580, 330], [580, 340], [590, 330], [590, 340], [600, 330], [600, 340], [610, 340], [610, 330], [620, 330], [620, 340], [190, 420], [200, 420], [210, 420], [220, 420], [230, 420], [240, 430], [250, 440], [180, 430], [170, 440], [180, 440], [190, 430], [200, 430], [210, 430], [220, 430], [230, 430], [240, 440], [190, 440], [230, 440], [170, 450], [180, 450], [170, 460], [180, 460], [170, 470], [180, 470], [170, 480], [180, 480], [170, 490], [180, 490], [180, 500], [170, 500], [170, 510], [180, 510], [190, 510], [180, 520], [190, 520], [190, 530], [200, 530], [210, 530], [220, 530], [230, 530], [200, 520], [210, 520], [220, 520], [230, 520], [240, 520], [240, 450], [250, 450], [240, 460], [250, 460], [240, 470], [250, 470], [240, 480], [250, 480], [240, 490], [250, 490], [240, 500], [250, 500], [240, 510], [250, 510], [230, 510], [280, 420], [290, 420], [280, 430], [290, 430], [280, 440], [290, 440], [290, 450], [300, 450], [300, 460], [290, 460], [290, 470], [300, 470], [300, 480], [300, 490], [310, 480], [310, 490], [300, 500], [310, 500], [310, 510], [320, 510], [320, 530], [330, 530], [330, 510], [330, 520], [340, 510], [340, 500], [350, 500], [340, 490], [350, 490], [340, 480], [350, 480], [340, 520], [310, 520], [320, 520], [350, 470], [360, 470], [350, 460], [360, 460], [350, 450], [360, 450], [360, 440], [370, 440], [360, 430], [370, 430], [360, 420], [370, 420], [400, 430], [400, 440], [410, 420], [410, 430], [410, 440], [400, 450], [400, 460], [400, 470], [400, 480], [400, 490], [400, 500], [400, 510], [400, 520], [410, 530], [410, 520], [420, 520], [420, 530], [430, 520], [430, 530], [440, 520], [440, 530], [450, 520], [460, 520], [470, 520], [480, 520], [450, 530], [460, 530], [470, 530], [420, 420], [430, 420], [440, 420], [450, 420], [460, 420], [470, 420], [410, 450], [410, 460], [410, 470], [410, 480], [410, 490], [410, 500], [410, 510], [420, 430], [430, 430], [440, 430], [450, 430], [460, 430], [470, 430], [480, 430], [420, 470], [420, 480], [430, 470], [430, 480], [440, 470], [440, 480], [450, 470], [450, 480], [460, 470], [460, 480], [470, 470], [470, 480], [630, 330], [630, 340], [540, 420], [530, 420], [520, 430], [510, 440], [550, 420], [560, 420], [570, 420], [580, 430], [590, 440], [530, 430], [540, 430], [550, 430], [560, 430], [570, 430], [520, 440], [580, 440], [580, 450], [590, 450], [580, 460], [590, 460], [580, 470], [570, 480], [570, 470], [560, 470], [560, 480], [550, 470], [550, 480], [510, 430], [510, 450], [520, 460], [520, 450], [510, 460], [520, 470], [510, 470], [530, 470], [530, 480], [540, 470], [540, 480], [510, 480], [520, 480], [510, 490], [520, 490], [510, 500], [520, 500], [510, 510], [520, 510], [510, 520], [520, 520], [510, 530], [520, 530], [580, 530], [570, 530], [570, 520], [580, 520], [570, 510], [560, 520], [560, 510], [560, 500], [550, 510], [550, 500], [540, 500], [550, 490], [530, 490], [540, 490], [530, 500]]
        # pygame.mixer.init()
        # pygame.mixer.music.set_volume(30)

    def run(self):
        field = Mine_Field(self)
        pressed = False
        direction = 1
        # while not self.GameOver:
        while True:
            if self.GameOver or self.Win:
                if self.GameOver:
                    pygame.time.wait(1000)
                    self.display.fill(pygame.Color("black"))
                    for i in self.game_over_print:
                        # pygame.draw.rect(self.display, (255, 255, 255), (i[0] + 1, i[1] + 1, self.cell_size - 2, self.cell_size - 2))
                        pygame.draw.rect(self.display, (255, 255, 255), (i[0], i[1], self.cell_size, self.cell_size))
                        pygame.display.update()
                    pygame.time.wait(5000)
                    break
                if self.Win:
                    pygame.time.wait(1000)
                    self.display.fill(pygame.Color("black"))
                    for i in self.Win_print:
                        # pygame.draw.rect(self.display, (255, 255, 255), (i[0] + 1, i[1] + 1, self.cell_size - 2, self.cell_size - 2))
                        pygame.draw.rect(self.display, (255, 255, 255), (i[0], i[1], self.cell_size, self.cell_size))
                        pygame.display.update()
                    pygame.time.wait(5000)
                    break


            self.clock.tick(15)
            self.display.fill(pygame.Color("black"))
            [pygame.draw.rect(self.display, (220, 220, 220), (x * 8 * self.cell_size, y * 8 * self.cell_size, self.cell_size, self.cell_size), 0) for x in range(11) for y in range(11)]
            field.update(self)
            field.draw(self)
            pygame.display.update()
            if pressed:
                field.tank.move(self, direction)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        direction = 1
                        pressed = True
                    if event.key == pygame.K_DOWN:
                        direction = -1
                        pressed = True
                    if event.key == pygame.K_LEFT:
                        field.tank.rotate(-1)
                    if event.key == pygame.K_RIGHT:
                        field.tank.rotate(1)
                    if event.key == pygame.K_SPACE:
                        field.tank.shot()
                            # pygame.mixer.music.unload()
                            # pygame.mixer.music.load("tank-firin.mp3")
                            # pygame.mixer.music.play(loops=0, start=0.0)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        pressed = False
                    if event.key == pygame.K_DOWN:
                        pressed = False

if __name__ == '__main__':
    if get_settings() == "None":
        print("[!!!]Пропишите адресс сервера")
    while True:
        app = App()
        app.run()
        print("Выход")