import pygame
import random
import heapq

# Размер клетки
CELL_SIZE = 100

# Загрузка спрайтов клеток
FIELD = pygame.image.load("images/map/field/grass.jpg")
ROAD = pygame.image.load("images/map/road/road.jpg")
FOREST = pygame.image.load("images/map/forest/forest.jpg")
CITY = pygame.image.load("images/map/city/old_city.jpg")

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(map_data, start, goal):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        current = heapq.heappop(frontier)[1]

        if current == goal:
            break

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                next = (current[0] + dx, current[1] + dy)

                if 0 <= next[0] < len(map_data[0]) and 0 <= next[1] < len(map_data):
                    new_cost = cost_so_far[current] + 1
                    if next not in cost_so_far or new_cost < cost_so_far[next]:
                        cost_so_far[next] = new_cost
                        priority = new_cost + heuristic(goal, next)
                        heapq.heappush(frontier, (priority, next))
                        came_from[next] = current

    return came_from, cost_so_far

def connect_cities(map_data, cities):
    for i in range(len(cities)):
        for j in range(i + 1, len(cities)):
            came_from, _ = a_star_search(map_data, cities[i], cities[j])

            current = cities[j]
            while current != cities[i]:
                if map_data[current[1]][current[0]] != CITY:
                    map_data[current[1]][current[0]] = ROAD
                current = came_from[current]

#Генерация карты
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

    # Соединение городов

    connect_cities(map_data, cities)

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