import pygame
from clases.Hero import Bandit
from map import generate_map_data
from map import FIELD
from map import FOREST
from map import ROAD
from map import CITY
from map import CELL_SIZE

#Размеры окна
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

#оздаем окно
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#Создаем объект класса Bandit
bandit = Bandit("bandit.png")
bandit.set_position(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

#Начальные координаты камеры
camera_x = 0
camera_y = 0

#Скорость движения камеры
camera_speed = 1

#Создание карты
a = 100
b = 20
c = 2
map_data = generate_map_data(a, b, c)

#Определяем количество тайлов по горизонтали и вертикали
tiles_horizontal = WINDOW_WIDTH // CELL_SIZE
tiles_vertical = WINDOW_HEIGHT // CELL_SIZE

#Основной цикл игры
while True:
    #Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
        # Выход из игры при закрытии окна
            pygame.quit()
            exit()

    # Получение состояния клавиш на клавиатуре
    keys = pygame.key.get_pressed()

    # Движение камеры по горизонтали
    if keys[pygame.K_a]:
        camera_x += camera_speed
    elif keys[pygame.K_d]:
        camera_x -= camera_speed

    # Движение камеры по вертикали
    if keys[pygame.K_w]:
        camera_y += camera_speed
    elif keys[pygame.K_s]:
        camera_y -= camera_speed

    # Вычисляем индексы крайних тайлов, попадающих в камеру
    min_x = max(camera_x // CELL_SIZE, 0)
    max_x = min(min_x + tiles_horizontal, b)
    min_y = max(camera_y // CELL_SIZE, 0)
    max_y = min(min_y + tiles_vertical, a)

    # Отображение тайлов на экране
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            if map_data[y][x] == 0:
                screen.blit(FIELD, (x * CELL_SIZE - camera_x, y * CELL_SIZE - camera_y))
            elif map_data[y][x] == 1:
                screen.blit(ROAD, (x * CELL_SIZE - camera_x, y * CELL_SIZE - camera_y))
            elif map_data[y][x] == 2:
                screen.blit(FOREST, (x * CELL_SIZE - camera_x, y * CELL_SIZE - camera_y))
            elif map_data[y][x] == 3:
                screen.blit(CITY, (x * CELL_SIZE - camera_x, y * CELL_SIZE - camera_y))

    # Отображение персонажа на экране
    screen.blit(bandit.image, bandit.rect)

    # Здесь можно рисовать другие объекты

    # Обновление экрана
    pygame.display.flip()