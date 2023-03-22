import pygame
import random

# Constants
POPULATION_SIZE = 100
MUTATION_RATE = 0.1
TARGET_RECT = pygame.Rect(300, 200, 200, 200)
SCREEN_SIZE = (800, 600)
RECT_SIZE = (15, 15)
BG_COLOR = (0,0,0)
RECT_COLOR = (255, 255, 255)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)

def random_color():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

# Define the Rectangle class
class Rectangle:
    def __init__(self, rect=None):
        if rect:
            self.rect = rect
        else:
            self.rect = pygame.Rect(random.randint(0, SCREEN_SIZE[0]), 
                                    random.randint(0, SCREEN_SIZE[1]), 
                                    RECT_SIZE[0], RECT_SIZE[1])
        self.fitness = None
        
    def draw(self):
        pygame.draw.rect(screen, random_color(), self.rect)
        
    def calculate_fitness(self):
        distance = pygame.math.Vector2(TARGET_RECT.center) - pygame.math.Vector2(self.rect.center)
        self.fitness = 1 / (distance.length() + 1)
        
    def mutate(self):
        if random.random() < MUTATION_RATE:
            self.rect.x += random.randint(-1, 1)
            self.rect.y += random.randint(-1, 1)

# Define the Population class
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
            
# Main loop
population = Population()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
            
                screen.fill(BG_COLOR)

                population.draw()
                population.calculate_fitnesses()
                population.reproduce()

                pygame.draw.rect(screen, RECT_COLOR, TARGET_RECT, 3)

                pygame.display.update()