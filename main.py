import pygame
import random
import time

import asyncio

pygame.init()

# Установка размеров экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Арифметические головоломки")

# Задание цветов RGB
white = (255, 255, 255)
black = (0, 0, 0)

# Шрифты
font_small = pygame.font.Font(None, 36)
font_big = pygame.font.Font(None, 72)

# Таймер игры
game_time = 30

# Дизайн
background_image = pygame.image.load('games_src/bg.png')
main_menu_bg = pygame.image.load('games_src/menu_bg.png')

# Уровни сложности задач
difficulty_levels = {
    'easy': {
        'min_num': 1,
        'max_num': 10,
        'operators': ['+', '-']
    },
    'medium': {
        'min_num': 10,
        'max_num': 50,
        'operators': ['+', '-', '*', '/']
    },
    'hard': {
        'min_num': 50,
        'max_num': 100,
        'operators': ['*', '/']
    }
}


async def choose_difficulty():
    difficulty_text = font_big.render("Выберите уровень сложности", True, white)
    easy_text = font_small.render("Легкий (1-10)", True, white)
    medium_text = font_small.render("Средний (10-50)", True, white)
    hard_text = font_small.render("Сложный (50-100)", True, white)
    difficulty_rects = [easy_text.get_rect(center=(screen_width/2, screen_height/2)),
                        medium_text.get_rect(center=(screen_width/2, screen_height/2 + 50)),
                        hard_text.get_rect(center=(screen_width/2, screen_height/2 + 100))]
    while True:
        screen.blit(main_menu_bg, (0, 0))
        screen.blit(difficulty_text, difficulty_text.get_rect(midtop=(screen_width/2, 100)))
        for i, text in enumerate([easy_text, medium_text, hard_text]):
            screen.blit(text, difficulty_rects[i])
        pygame.display.update()
        await asyncio.sleep(0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(difficulty_rects):
                    if rect.collidepoint(event.pos):
                        if i == 0:
                            return 'easy'
                        elif i == 1:
                            return 'medium'
                        else:
                            return 'hard'


# Функция для генерации случайных задач
def generate_question(difficulty):
    min_num = difficulty['min_num']
    max_num = difficulty['max_num']
    operator = random.choice(difficulty['operators'])
    if operator == '-':
        num1 = random.randint(min_num, max_num)
        num2 = random.randint(min_num, num1)
    else:
        num2 = random.randint(1, 10) if operator == '/' else random.randint(min_num, max_num)
        if operator == '/':
            num1 = random.randint(min_num, max_num) * num2
        else:
            num1 = random.randint(min_num, max_num)
    if operator == '+':
        answer = num1 + num2
    elif operator == '-':
        answer = num1 - num2
    elif operator == '*':
        answer = num1 * num2
    else:
        answer = num1 / num2
    question = f"{num1} {operator} {num2} = ?"
    return question, answer


# Функция для вывода задачи на экран
def draw_question(question):
    text = font_big.render(question, True, white)
    text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2))
    screen.blit(text, text_rect)


async def game_over_screen(score):
    # Display final score and options to restart or quit
    text = font_big.render(f"Время закончилось!\nОчки: {score}", True, white)
    text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2 - 50))
    restart_text = font_small.render("Начать заново", True, white)
    restart_rect = restart_text.get_rect(center=(screen_width / 2, screen_height / 2 + 50))
    while True:
        screen.blit(background_image, (0, 0))
        screen.blit(text, text_rect)
        screen.blit(restart_text, restart_rect)
        pygame.display.update()
        await asyncio.sleep(0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    await game_loop()


async def game_loop():
    global seconds
    difficulty = await choose_difficulty()
    answer = ''
    answer_str = ''
    question, current_answer = generate_question(difficulty_levels[difficulty])
    running = True
    score = 0
    start_ticks = pygame.time.get_ticks()
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isdigit():
                    answer_str += event.unicode
                elif event.key == pygame.K_RETURN:
                    try:
                        answer = int(answer_str)
                        if answer == current_answer:
                            score += 1
                        answer_str = ''
                        question, current_answer = generate_question(difficulty_levels[difficulty])
                    except ValueError:
                        answer_str = ''
                elif event.key == pygame.K_BACKSPACE:
                    answer_str = answer_str[:-1]

        screen.blit(background_image, (0, 0))
        question_text = font_big.render(question, True, white)
        question_text_rect = question_text.get_rect(center=(screen_width / 2, screen_height / 2 - 50))
        answer_text = font_big.render(answer_str, True, white)
        answer_text_rect = answer_text.get_rect(center=(screen_width / 2, screen_height / 2 + 50))
        score_text = font_small.render(f"Очков: {score}", True, white)
        score_text_rect = score_text.get_rect(topright=(screen_width - 10, 10))
        screen.blit(question_text, question_text_rect)
        screen.blit(answer_text, answer_text_rect)
        screen.blit(score_text, score_text_rect)

        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        time_left = game_time - seconds
        if time_left <= 0:
            running = False
            await game_over_screen(score)

        timer_text = font_small.render(f"Время: {int(time_left)}", True, white)
        timer_text_rect = timer_text.get_rect(topleft=(10, 10))
        screen.blit(timer_text, timer_text_rect)

        pygame.display.update()
        await asyncio.sleep(0)


if __name__ == '__main__':
    asyncio.run(game_loop())
