import pygame
import random
import heapq

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
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                x = city_x + dx
                y = city_y + dy
                if (x, y) not in cities and x >= 0 and x < a and y >= 0 and y < b:
                    map_data[y][x] = CITY

    # Константы
    CITY_CELL = 1
    ROAD_CELL = 2

    # Поиск кратчайшего пути между городами
    def shortest_path(map_data, cities, city1, city2):
        # Создаем матрицу расстояний между городами
        dist = [[float('inf') for _ in range(len(cities))] for _ in range(len(cities))]
        for i, city1 in enumerate(cities):
            for j, city2 in enumerate(cities):
                if i == j:
                    dist[i][j] = 0
                elif dist[j][i] < float('inf'):
                    dist[i][j] = dist[j][i]
                else:
                    dist[i][j] = abs(city1[0] - city2[0]) + abs(city1[1] - city2[1])

        # Выполняем поиск кратчайшего пути с помощью алгоритма Дейкстры
        heap = [(0, i) for i in range(len(cities))]
        heapq.heapify(heap)
        visited = set()
        while heap:
            (d, u) = heapq.heappop(heap)
            if u == city2:
                return d
            if u in visited:
                continue
            visited.add(u)
            for v in range(len(cities)):
                if v != u:
                    alt = d + dist[u][v]
                    if alt < float('inf'):
                        heapq.heappush(heap, (alt, v))

        return None

    # Соединение городов дорогами
    def connect_cities(map_data, cities, max_distance):
        for i in range(len(cities)):
            for j in range(i + 1, len(cities)):
                if shortest_path(map_data, cities, i, j) <= max_distance:
                    # Соединяем города дорогой
                    city1 = cities[i]
                    city2 = cities[j]
                    x1, y1 = city1
                    x2, y2 = city2
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
                        if map_data[y][x] != CITY_CELL:
                            map_data[y][x] = ROAD_CELL
                        x += stepx
                        y += stepy
                    if map_data[y2][x2] != CITY_CELL:
                        map_data[y2][x2] = ROAD_CELL

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