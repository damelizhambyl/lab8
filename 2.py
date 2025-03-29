import pygame
import random
import sys


pygame.init()
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")


font = pygame.font.SysFont("Times New Roman", 20)

clock = pygame.time.Clock()
snake = [(100, 100), (80, 100), (60, 100)] 
snake_dir = (20, 0) 
food_pos = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
score = 0
level = 1
speed = 10


def generate_food():
    while True:
        x = random.randrange(0, WIDTH, CELL_SIZE)
        y = random.randrange(0, HEIGHT, CELL_SIZE)
        if (x, y) not in snake:
            return (x, y)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and snake_dir != (0, 20):
        snake_dir = (0, -20)
    if keys[pygame.K_DOWN] and snake_dir != (0, -20):
        snake_dir = (0, 20)
    if keys[pygame.K_LEFT] and snake_dir != (20, 0):
        snake_dir = (-20, 0)
    if keys[pygame.K_RIGHT] and snake_dir != (-20, 0):
        snake_dir = (20, 0)

  
    new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
    
    
    if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
        break

   
    if new_head in snake:
        break

    
    snake.insert(0, new_head)

 
    if new_head == food_pos:
        score += 1
        food_pos = generate_food()

        
        if score % 4 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()

 
    screen.fill(WHITE)

  
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

   
    pygame.draw.rect(screen, RED, (food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))

   
    score_text = font.render(f"Счет: {score}", True, BLACK)
    level_text = font.render(f"Уровень: {level}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

    pygame.display.flip()
    clock.tick(speed)
# Полное объяснение кода ниже:

# 1. Мы импортируем необходимые библиотеки: pygame, random, sys.
# 2. Устанавливаем размеры окна игры и размеры клетки.
# 3. Задаем базовые цвета, шрифт и начальные параметры.
# 4. Создаем змею в виде списка кортежей с начальными координатами.
# 5. Начальное направление движения змеи - вправо.
# 6. Генерируем случайную позицию для еды, которая не должна совпадать с телом змеи.
# 7. В основном цикле:
#    - Проверяем события закрытия окна.
#    - Слушаем клавиши и меняем направление змеи, если нужно.
#    - Двигаем змею, добавляя новый сегмент головы.
#    - Проверяем столкновение с границей или собой.
#    - Если съедаем еду — увеличиваем счет, уровень и скорость.
#    - Если не съели — удаляем последний сегмент змеи (хвост).
# 8. Отрисовываем змею, еду, счет и уровень на экране.
# 9. Управляем скоростью игры в зависимости от текущего уровня.
# 10. Если игра заканчивается (столкновение) — программа выходит.