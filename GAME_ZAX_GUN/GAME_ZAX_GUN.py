import tkinter as tk
import random

screen_width, screen_height = 800, 600
player_size = 50
player_speed = 5
bullet_speed = 10
enemy_speed = 2
max_enemy_lives = 3
enemy_bullet_speed = 7
player_max_lives = 3

root = tk.Tk()
root.title("Simple Movement")
canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg="black")
canvas.pack()

player_pos = [screen_width // 2, screen_height - player_size]
player = canvas.create_rectangle(player_pos[0], player_pos[1], player_pos[0] + player_size, player_pos[1] + player_size, fill="red")

bullets = []
enemies = []
enemy_bullets = []
player_lives = player_max_lives
player_life_rects = []
particles = []

def draw_player_lives():
    global player_life_rects
    for rect in player_life_rects:
        canvas.delete(rect)
    player_life_rects = []
    for i in range(player_lives):
        rect = canvas.create_rectangle(10 + i*25, screen_height-30, 30 + i*25, screen_height-10, fill="red")
        player_life_rects.append(rect)

def move_player(event):
    if event.keysym == 'Up':
        canvas.move(player, 0   , -player_speed)
    elif event.keysym == 'Down':
        canvas.move(player, 0, player_speed)
    elif event.keysym == 'Left':
        canvas.move(player, -player_speed, 0)
    elif event.keysym == 'Right':
        canvas.move(player, player_speed, 0)
    elif event.keysym == 'space':
        shoot_bullet(event)         

def shoot_bullet(event):
    x1, y1, x2, y2 = canvas.coords(player)
    bullet_x = (x1 + x2) / 2
    bullet_y = y1
    bullet = canvas.create_rectangle(bullet_x - 5, bullet_y, bullet_x + 5, bullet_y - 10, fill="yellow")
    bullets.append(bullet)

def move_bullets():
    for bullet in bullets[:]:
        canvas.move(bullet, 0, -bullet_speed)
        if canvas.coords(bullet)[1] < 0:
            canvas.delete(bullet)
            bullets.remove(bullet)
    canvas.after(50, move_bullets)  

def create_enemy():
    enemy_x = random.randint(0, screen_width - player_size)
    enemy_color = random.choice(["green", "blue", "orange", "purple", "pink"])
    enemy = canvas.create_rectangle(enemy_x, 0, enemy_x + player_size, player_size, fill=enemy_color)
    enemy_lives = max_enemy_lives
    enemies.append((enemy, enemy_lives, []))  # третий элемент — список жизней (отрисовка)
    draw_enemy_lives()

def draw_enemy_lives():
    # Удаляем старые квадраты жизней
    for enemy, lives, life_rects in enemies:        
        for rect in life_rects:
            canvas.delete(rect)
        life_rects.clear()
    # Рисуем новые квадраты жизней
    for idx, (enemy, lives, life_rects) in enumerate(enemies):
        ex1, ey1, ex2, ey2 = canvas.coords(enemy)
        for i in range(lives):
            rect = canvas.create_rectangle(
                ex1 + 5 + i*15, ey1 - 15, ex1 + 15 + i*15, ey1 - 5, fill="red"
            )
            life_rects.append(rect)

def move_enemies():
    for index in range(len(enemies)-1, -1, -1):
        enemy, lives, life_rects = enemies[index]
        canvas.move(enemy, 0, enemy_speed)
        for rect in life_rects:
            canvas.move(rect, 0, enemy_speed)
        if canvas.coords(enemy)[1] > screen_height:
            for rect in life_rects:
                canvas.delete(rect)
            canvas.delete(enemy)
            enemies.pop(index)
    canvas.after(100, move_enemies)

def enemy_shoot():
    for enemy, lives, _ in enemies:
        if random.random() < 0.02:  # шанс выстрела
            ex1, ey1, ex2, ey2 = canvas.coords(enemy)
            bullet_x = (ex1 + ex2) / 2
            bullet_y = ey2
            bullet = canvas.create_rectangle(bullet_x - 5, bullet_y, bullet_x + 5, bullet_y + 10, fill="white")
            enemy_bullets.append(bullet)
    canvas.after(200, enemy_shoot)

def move_enemy_bullets():
    global player_lives
    for bullet in enemy_bullets[:]:
        canvas.move(bullet, 0, enemy_bullet_speed)
        bx1, by1, bx2, by2 = canvas.coords(bullet)
        if by2 > screen_height:
            canvas.delete(bullet)
            enemy_bullets.remove(bullet)
            continue
        # Проверка столкновения с игроком
        px1, py1, px2, py2 = canvas.coords(player)
        if bx1 < px2 and bx2 > px1 and by1 < py2 and by2 > py1:
            canvas.delete(bullet)
            enemy_bullets.remove(bullet)
            player_lives -= 1
            draw_player_lives()
            if player_lives <= 0:
                canvas.create_text(screen_width//2, screen_height//2, text="GAME OVER", fill="white", font=("Arial", 40))
                root.unbind("<KeyPress>")
                root.unbind("<space>")
            break
    canvas.after(50, move_enemy_bullets)

def check_collisions():
    global player_lives, enemies_killed
    # Проверка попадания пули игрока во врага
    for bullet in bullets[:]:
        bullet_coords = canvas.coords(bullet)
        for index in range(len(enemies)-1, -1, -1):
            enemy, lives, life_rects = enemies[index]
            enemy_coords = canvas.coords(enemy)
            if (bullet_coords[0] < enemy_coords[2] and bullet_coords[2] > enemy_coords[0] and
                bullet_coords[1] < enemy_coords[3] and bullet_coords[3] > enemy_coords[1]):
                canvas.delete(bullet)
                bullets.remove(bullet)
                lives -= 1
                if lives > 0:
                    enemies[index] = (enemy, lives, life_rects)
                else:
                    for rect in life_rects:
                        canvas.delete(rect)
                    ex1, ey1, ex2, ey2 = enemy_coords
                    spawn_particles((ex1+ex2)//2, (ey1+ey2)//2, canvas.itemcget(enemy, "fill"))
                    canvas.delete(enemy)
                    enemies.pop(index)
                    enemies_killed += 1
                    draw_progress_bar()
                    # Если все враги уничтожены — уровень пройден
                    if enemies_killed >= enemies_per_level:
                        canvas.create_text(
                            screen_width//2, screen_height//2,
                            text="GAME WIN HORNY", fill="white", font=("Arial", 32)
                        )
                draw_enemy_lives()
                break

    # Проверка столкновения игрока с врагом
    px1, py1, px2, py2 = canvas.coords(player)
    for enemy, lives, life_rects in enemies:
        ex1, ey1, ex2, ey2 = canvas.coords(enemy)
        if px1 < ex2 and px2 > ex1 and py1 < ey2 and py2 > ey1:
            player_lives -= 1
            draw_player_lives()
            if player_lives <= 0:
                canvas.create_text(screen_width//2, screen_height//2, text="GAME OVER", fill="white", font=("Arial", 40))
                root.unbind("<KeyPress>")
                root.unbind("<space>")
            break

    canvas.after(50, check_collisions)

particles = []

def spawn_particles(x, y, color):
    for _ in range(20):  # количество частиц
        angle = random.uniform(0, 2 * 3.1415)
        speed = random.uniform(2, 6)
        dx = speed * random.uniform(0.5, 1.0) * random.choice([-1, 1])
        dy = speed * random.uniform(0.5, 1.0) * random.choice([-1, 1])
        size = random.randint(2, 5)
        particle = {
            "id": canvas.create_oval(x, y, x + size, y + size, fill=color, outline=""),
            "dx": dx,
            "dy": dy,
            "life": random.randint(10, 20)
        }
        particles.append(particle)

def animate_particles():
    for particle in particles[:]:
        canvas.move(particle["id"], particle["dx"], particle["dy"])
        particle["life"] -= 1
        if particle["life"] <= 0:
            canvas.delete(particle["id"])
            particles.remove(particle)
    canvas.after(30, animate_particles)

current_wave = 1
enemies_per_wave = 10
enemies_spawned = 0
enemies_killed = 0
wave_in_progress = False
progress_bar = None
progress_bar_bg = None
progress_text = None
enemies_per_level = 10  # Количество врагов на уровень
enemies_killed = 0

def draw_progress_bar():
    global progress_bar, progress_bar_bg, progress_text
    # Удаляем старую полосу и текст
    if progress_bar is not None:
        canvas.delete(progress_bar)
    if progress_bar_bg is not None:
        canvas.delete(progress_bar_bg)
    if progress_text is not None:
        canvas.delete(progress_text)
    # Параметры полосы
    bar_x = 100 + 10  # справа от жизней
    bar_y = screen_height - 25
    bar_width = 150
    bar_height = 15
    # Фон полосы
    progress_bar_bg = canvas.create_rectangle(bar_x, bar_y, bar_x + bar_width, bar_y + bar_height, outline="white")
    # Заполненная часть
    fill = (enemies_killed / enemies_per_level) if enemies_per_level else 0
    progress_bar = canvas.create_rectangle(bar_x, bar_y, bar_x + int(bar_width * fill), bar_y + bar_height, fill="white", outline="")
    # Текст прогресса
    progress_text = canvas.create_text(bar_x + bar_width // 2, bar_y + bar_height // 2, text=f"{enemies_killed}/{enemies_per_level}", fill="black", font=("Arial", 10))

# Измените функцию check_collisions, чтобы обновлять прогресс:
def check_collisions():
    global player_lives, enemies_killed
    # Проверка попадания пули игрока во врага
    for bullet in bullets[:]:
        bullet_coords = canvas.coords(bullet)
        for index in range(len(enemies)-1, -1, -1):
            enemy, lives, life_rects = enemies[index]
            enemy_coords = canvas.coords(enemy)
            if (bullet_coords[0] < enemy_coords[2] and bullet_coords[2] > enemy_coords[0] and
                bullet_coords[1] < enemy_coords[3] and bullet_coords[3] > enemy_coords[1]):
                canvas.delete(bullet)
                bullets.remove(bullet)
                lives -= 1
                if lives > 0:
                    enemies[index] = (enemy, lives, life_rects)
                else:
                    for rect in life_rects:
                        canvas.delete(rect)
                    ex1, ey1, ex2, ey2 = enemy_coords
                    spawn_particles((ex1+ex2)//2, (ey1+ey2)//2, canvas.itemcget(enemy, "fill"))
                    canvas.delete(enemy)
                    enemies.pop(index)
                    enemies_killed += 1
                    draw_progress_bar()
                    # Если все враги уничтожены — уровень пройден
                    if enemies_killed >= enemies_per_level:
                        canvas.create_text(
                            screen_width//2, screen_height//2,
                            text="GAME WIN HORNY", fill="white", font=("Arial", 32)
                        )
                draw_enemy_lives()
                break

    # Проверка столкновения игрока с врагом
    px1, py1, px2, py2 = canvas.coords(player)
    for enemy, lives, life_rects in enemies:
        ex1, ey1, ex2, ey2 = canvas.coords(enemy)
        if px1 < ex2 and px2 > ex1 and py1 < ey2 and py2 > ey1:
            player_lives -= 1
            draw_player_lives()
            if player_lives <= 0:
                canvas.create_text(screen_width//2, screen_height//2, text="GAME OVER", fill="white", font=("Arial", 40))
                root.unbind("<KeyPress>")
                root.unbind("<space>")
            break

    canvas.after(50, check_collisions)

# В функции create_enemy увеличьте enemies_per_level, если хотите больше врагов на уровень
def spawn_enemy():
    if enemies_killed < enemies_per_level:
        create_enemy()
        root.after(2000, spawn_enemy)

# В начале игры нарисуйте полосу прогресса
draw_player_lives()
draw_progress_bar()
move_bullets()
move_enemies()
check_collisions()
enemy_shoot()
move_enemy_bullets()
animate_particles()  # Запуск анимации частиц

spawn_enemy()
root.bind("<KeyPress>", move_player)
root.mainloop()