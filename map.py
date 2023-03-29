import pygame
import random

# Размер клетки
CELL_SIZE = 10

# Загрузка спрайтов клеток
FIELD = pygame.image.load("images/map/field/image2.png")
ROAD = pygame.image.load("images/map/road/image2.png")
FOREST = pygame.image.load("images/map/forest/image2.png")
CITY = pygame.image.load("images/map/city/image2.png")

def generate_map(a, b, c):
    map_data = [[FIELD for _ in range(a)] for _ in range(b)]

    # Размещение городов
    cities = []
    for _ in range(c):
        city_x = random.randint(0, a - 1)
        city_y = random.randint(0, b - 1)
        while (city_x, city_y) in cities:
            city_x = random.randint(0, a - 1)
            city_y = random.randint(0, b - 1)
        cities.append((city_x, city_y))
        map_data[city_y][city_x] = CITY

    # Размещение дорог
    for i in range(len(cities) - 1):
        current_city = cities[i]
        next_city = cities[i + 1]
        x1, y1 = current_city
        x2, y2 = next_city

        # Горизонтальная дорога
        for x in range(min(x1, x2), max(x1, x2) + 1):
            map_data[y1][x] = ROAD

        # Вертикальная дорога
        for y in range(min(y1, y2), max(y1, y2) + 1):
            map_data[y][x2] = ROAD

    # Размещение лесов
    forest_count = int(a * b * 0.25)  # Заполняем 25% карты лесами
    for _ in range(forest_count):
        forest_x = random.randint(0, a - 1)
        forest_y = random.randint(0, b - 1)
        while map_data[forest_y][forest_x] != FIELD:
            forest_x = random.randint(0, a - 1)
            forest_y = random.randint(0, b - 1)
        map_data[forest_y][forest_x] = FOREST

    return map_data