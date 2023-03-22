import pygame
import random

#constants
POPULATION_SIZE = 50
MUTATION_RATE = 0.1
TARGET_RECT = pygame.Rect(400, 300, 100, 100)
SCREEN_SIZE = (800,600)
RECT_SIZE = (20,20)
BG_COLOUR = (255,255,255)
RECT_COLOR = (0,0,0)

#initialise pygame
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)

#define the rectangle class
class Rectangle:
    def __init__(self, rect=None):
        if rect:
            self.rect = rect
        else:
            self.rect = pygame.Rect(random.randint(0, (SCREEN_SIZE[0] - RECT_SIZE[0])),
            random.randint(0, SCREEN_SIZE[1] - RECT_SIZE[1]),
            RECT_SIZE[0], RECT_SIZE[1])
        self.fitness = None

    def draw(self):
        pygame.draw.rect(screen, RECT_COLOR, self.rect)

    def calculate_fitness(self):
        distance = pygame.math.Vector2(TARGET_RECT.center) - pygame.math.Vector2(self.rect.center)
        self.fitness = 1 / (distance.length() + 1)
    
    def mutate(self):
        if random.random() < MUTATION_RATE:
            self.rect.x += random.randint(-10, 10)
            self.rect.y += random.randint(-10, 10)

#define the population class
class Population:
    def __init__(self):
        self.rectangles = []
        for i in range(POPULATION_SIZE):
            self.rectangles.append(Rectangle())

    def draw(self):
        for rectangle in self.rectangles:
            rectangle.draw()

    def calculate_fitnesses(self):
        for rectangle in self.rectangles:
            rectangle.calculate_fitness()
        self.rectangles.sort(key=lambda rectangle: rectangle.fitness, reverse=True)
    
    def reproduce(self):
        new_rectangles = []
        for i in range(POPULATION_SIZE):
            parent1 = self.rectangles[random.randint(0, int(POPULATION_SIZE/2))]
            parent2 = self.rectangles[random.randint(0, int(POPULATION_SIZE/2))]
            child_rect = pygame.Rect(parent1.rect.x, parent2.rect.y, RECT_SIZE[0], RECT_SIZE[1])
            child = Rectangle(child_rect)
            child.mutate()
            new_rectangles.append(child)
        self.rectangles = new_rectangles

#main loop
population = Population()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    
    screen.fill(BG_COLOUR)

    population.draw()
    population.calculate_fitnesses()
    population.reproduce()

    pygame.draw.rect(screen, RECT_COLOR, TARGET_RECT, 3)

    pygame.display.update()

