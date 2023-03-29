import pygame
import random

# Размер клетки
CELL_SIZE = 10

# Загрузка спрайтов клеток
FIELD = pygame.image.load("images/map/field/image2.png")
ROAD = pygame.image.load("images/map/road/image2.png")
FOREST = pygame.image.load("images/map/forest/image2.png")
CITY = pygame.image.load("images/map/city/image2.png")

def generate_map_data(a, b, c):
    if a == 0 or b == 0:
        raise ValueError("Размеры карты должны быть больше 0")
    #Создаем пустую карту
    map_data = [[None] * b for _ in range(a)]

    # Располагаем начальные тайлы городов
    for i in range(c):
        x = random.randint(10, a - 10)
        y = random.randint(10, b - 2)
        map_data[x][y] = CITY

    # Дополняем тайлы городов прилегающими тайлами
    for i in range(c):
        while True:
            x = random.randint(1, a - 2)
            y = random.randint(1, b - 2)
            if map_data[x][y] == CITY:
                for j in range(random.randint(8, 16)):
                    dx = random.randint(-1, 1)
                    dy = random.randint(-1, 1)
                    if dx == dy == 0 or x + dx < 1 or x + dx > a - 2 or y + dy < 1 or y + dy > b - 2:
                        continue
                    if map_data[x + dx][y + dy] == 0:
                        map_data[x + dx][y + dy] = CITY
                break

    print(map_data)

    # Соединяем тайлы городов дорогами
    for i in range(c):
        city_tiles = []
        for x in range(a):
            for y in range(b):
                if map_data[x][y] == CITY and (x, y) not in city_tiles:
                    city_tiles.append((x, y))
        while len(city_tiles) > 1:
            tile1 = city_tiles.pop()
            min_distance = a * b
            for tile2 in city_tiles:
                distance = abs(tile1[0] - tile2[0]) + abs(tile1[1] - tile2[1])
                if distance < min_distance:
                    min_distance = distance
                    closest_tile = tile2
            x1, y1 = tile1
            x2, y2 = closest_tile
            dx = x2 - x1
            dy = y2 - y1
            if dx != 0:
                stepx = dx // abs(dx)
            else:
                stepx = 0
            if dy != 0:
                stepy = dy // abs(dy)
            else:
                stepy = 0
            x = x1
            y = y1
            while x != x2 or y != y2:
                map_data[x][y] = ROAD
                x += stepx
                y += stepy
            map_data[x2][y2] = CITY
            if x >= 0 and x < a and y >= 0 and y < b:
                map_data[x][y] = ROAD

    # Заполнение свободного пространства полями и лесами
    for i in range(a):
        for j in range(b):
            if map_data[i][j] == 0:
                if random.random() < 0.67:
                    map_data[i][j] = FIELD
                else:
                    map_data[i][j] = FOREST

    return map_data