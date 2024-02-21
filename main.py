import pygame

#добавляем задержку скорости кадров
clock = pygame.time.Clock()
#подключаем биьлиотеку
pygame.init()
#добавляем разрешение нашей игры
screen = pygame.display.set_mode((618, 359))
#добавляем название
pygame.display.set_caption("PyGame game")
#добавляем иконку для игры
icon = pygame.image.load('images/other/raccenew.png')
#добавляем иконку
pygame.display.set_icon(icon)

#добавляем бэк граунд
bg = pygame.image.load('images/other/background.png').convert_alpha()

#движение персонажа в лево, в соответствии с нашими картинками
walk_left = [
    pygame.image.load('images/left/left1.png').convert_alpha(),
    pygame.image.load('images/left/left2.png').convert_alpha(),
    pygame.image.load('images/left/left3.png').convert_alpha(),
    pygame.image.load('images/left/left4.png').convert_alpha()
]
#движение персонажа в право, в соответствии с нашими картинками
walk_right = [
    pygame.image.load('images/right/right1.png').convert_alpha(),
    pygame.image.load('images/right/right2.png').convert_alpha(),
    pygame.image.load('images/right/right3.png').convert_alpha(),
    pygame.image.load('images/right/right4.png').convert_alpha()
]

#загрузка картинки приведения и установления параметра, где он будет спавниться
ghost = pygame.image.load('images/other/ghost.png').convert_alpha()
#ghost_x = 620
#создание массива для призраков
ghost_list_in_game = []
#создание функций для дальнейшей анимации нашего персонажа и заднего фона
player_anim_count = 0
bg_x = 0
#скорость игрока
player_speed = 5
#отображенеие самого игрока
player_x = 150
player_y = 250

#добавление музыки
bg_sound = pygame.mixer.Sound('musik/becko.mp3')
bg_sound.play()
#!
#реализация прыжка
is_jump = False
#на столько пунктов будет прыгать наш персонаж
jump_count = 8

#назначаем через какое время будет появляться призрак
#создаем таймер
ghost_timer = pygame.USEREVENT + 1
#настраиваем таймер (1000 - 1 сек)
pygame.time.set_timer(ghost_timer, 1500)
#вывод надписи о проигрыше
label = pygame.font.Font('Fonts/shrift.ttf', 35)
lose_label = label.render('You die!!!', False, 'Red')
#добавляем надпись рестарта игры
restart_label = label.render('Play again', False, 'Blue')
restart_label_rect = restart_label.get_rect(topleft=(220,183))

#добавляем ограничение по фаерболам
bullets_left = 5
#добавляем картинку пули
bullet = pygame.image.load('images/other/fireball.png').convert_alpha()
#список для всех наших пуль
bullets = []
#реализация системы проигрыша
gameplay = True
#!
#добавление цикла
running = True
while running:
    #движение нашего фона
    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 618, 0))

    #движение призрака
    #screen.blit(ghost, (ghost_x, 250))

    #реализуем систему проигрыша
    if gameplay:
    #создаем область вокруг игрока и призрака
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        if ghost_list_in_game:
            for (i, element) in enumerate(ghost_list_in_game):
                screen.blit(ghost, element)
                element.x -= 15

                if element.x < -10:
                    ghost_list_in_game.pop(i)
        #выводи на экран сообщение, если наши области соприкаснулись
                if player_rect.colliderect(element):
                    gameplay = False

        #переменная для отслеживания клавиш отслеживание клавиш
        keys = pygame.key.get_pressed()
        #ходьба
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

    #отслеживание клавиш
        #нажатие на стрелочку "Влево" и ограничение ходьбы в зависимости от положения персонажа
        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        # нажатие на стрелочку "Вправо" и ограничение ходьбы в зависимости от положения персонажа
        elif keys[pygame.K_RIGHT] and player_x < 200:
            player_x += player_speed

        # реализация прыжка
        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8
        #сдвиг картинки вместе с игроком
        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1
        #движение фона вместе с ходьбой
        bg_x -= 2
        if bg_x == -618:
            bg_x = 0
        #скорость нашего призрака
        #ghost_x -= 10

        # реализовываем наш фаербол
        # ЗАДАЕМ скорость пули
        if bullets:
            for (i,element) in enumerate(bullets):
                screen.blit(bullet, (element.x, element.y))
                element.x += 4
                #удаляем изображение фаербола
                if element.x > 630:
                    bullets.pop(i)
                #удаляем изображение монстра и фаербола, когда они будут соприкасаться
                if ghost_list_in_game:
                    for (index, ghost_el) in enumerate(ghost_list_in_game):
                        if element.colliderect(ghost_el):
                            ghost_list_in_game.pop(index)
                            bullets.pop(i)
    else:
        screen.fill("Black")
        screen.blit(lose_label, (240, 150))
        #добавляем возможность рестарта игры
        screen.blit(restart_label, restart_label_rect)
        #добавляем возможность нажатием left clicka рестартнуть игру
        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            ghost_list_in_game.clear()
            bullets.clear()
            #возобновляем кол-во снарядов при перезапуске
            bullets_left = 5



    #обновленеи нашей картинки
    pygame.display.update()
    #способность выйти
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        #если наш таймер истек - создаем нового призрака
        if event.type == ghost_timer:
            #добавляем в массив призрака
            ghost_list_in_game.append(ghost.get_rect(topleft=(620, 250)))
        # реализовываем наш фаербол
        # биндим кнопку и задаем ее рассположение
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_g and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 20, player_y + 10)))
            bullets_left -= 1
    #устанавливаем кол-во кадров в секунду
    clock.tick(20)
