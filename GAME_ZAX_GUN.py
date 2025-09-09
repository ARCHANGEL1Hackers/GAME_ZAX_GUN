import tkinter as tk
import random
from tkinter import PhotoImage

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PLAYER_SIZE = 50
PLAYER_SPEED = 5
BULLET_SPEED = 10
ENEMY_SIZE = 50  
ENEMY_SPEED = 2
MAX_ENEMY_LIVES = 3
ENEMY_BULLET_SPEED = 7
PLAYER_MAX_LIVES = 3
ENEMIES_PER_LEVEL = 10


root = tk.Tk()
root.title("KAZYS SHOOTER GUN QUAD")
canvas = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg="black")
canvas.pack()


player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_SIZE]
player = canvas.create_rectangle(
    player_pos[0], player_pos[1],
    player_pos[0] + PLAYER_SIZE, player_pos[1] + PLAYER_SIZE,
    fill="red"
)


bullets = []
enemies = []
enemy_bullets = []
player_lives = PLAYER_MAX_LIVES
player_life_rects = []
particles = []
enemies_killed = 0
progress_bar = None
progress_bar_bg = None
progress_text = None


enemy_images_paths = [
    r"D:\ARCHANGEL PROJECT PROGRAMIC\GAME KAZYS\GAME_ZAX_GUN\GAME_ZAX_GUN\art\enemy.png",
    r"D:\ARCHANGEL PROJECT PROGRAMIC\GAME KAZYS\GAME_ZAX_GUN\GAME_ZAX_GUN\art\coxel.png",
    r"D:\ARCHANGEL PROJECT PROGRAMIC\GAME KAZYS\GAME_ZAX_GUN\GAME_ZAX_GUN\art\ped.png"
]
enemy_images = [PhotoImage(file=path) for path in enemy_images_paths]
class Enemy:
    def __init__(self, x, y):
       
        self.image = random.choice(enemy_images)
        self.sprite = canvas.create_image(x, y, image=self.image)
        self.lives = 3
        enemies = [
    Enemy(100, 100),
    Enemy(200, 150),
    Enemy(300, 200),
    Enemy(400, 250)
]

def get_random_enemy_image():
    return random.choice(enemy_images)
enemy_img = get_random_enemy_image()


def draw_player_lives():
    global player_life_rects
    for rect in player_life_rects:
        canvas.delete(rect)
    player_life_rects = []
    for i in range(player_lives):
        rect = canvas.create_rectangle(
            10 + i * 25, SCREEN_HEIGHT - 10,
            30 + i * 25, SCREEN_HEIGHT - 10,
            fill="red"
        )
        player_life_rects.append(rect)

def move_player(event):
    x1, y1, x2, y2 = canvas.coords(player)
    if event.keysym == 'Up' and y1 > 0:
        canvas.move(player, 0, -PLAYER_SPEED)
    elif event.keysym == 'Down' and y2 < SCREEN_HEIGHT:
        canvas.move(player, 0, PLAYER_SPEED)
    elif event.keysym == 'Left' and x1 > 0:
        canvas.move(player, -PLAYER_SPEED, 0)
    elif event.keysym == 'Right' and x2 < SCREEN_WIDTH:
        canvas.move(player, PLAYER_SPEED, 0)
    elif event.keysym == 'space':
        shoot_bullet()

def shoot_bullet():
    x1, y1, x2, y2 = canvas.coords(player)
    bullet_x = (x1 + x2) / 2
    bullet_y = y1
    bullet = canvas.create_rectangle(
        bullet_x - 5, bullet_y,
        bullet_x + 5, bullet_y - 10,
        fill="yellow"
    )
    bullets.append(bullet)

def move_bullets():
    for bullet in bullets[:]:
        canvas.move(bullet, 0, -BULLET_SPEED)
        if canvas.coords(bullet)[1] < 0:
            canvas.delete(bullet)
            bullets.remove(bullet)
    canvas.after(50, move_bullets)

def create_enemy():
    enemy_x = random.randint(0, SCREEN_WIDTH - PLAYER_SIZE)
    enemy = canvas.create_image(
        enemy_x + PLAYER_SIZE // 2, 0,
        image=enemy_img
    )
    enemy_lives = MAX_ENEMY_LIVES
    enemies.append((enemy, enemy_lives, []))
    draw_enemy_lives()

def draw_enemy_lives():
    for enemy, lives, life_rects in enemies:
        for rect in life_rects:
            canvas.delete(rect)
        life_rects.clear()
        ex, ey = canvas.coords(enemy)
        for i in range(lives):
            rect = canvas.create_rectangle(
                ex - PLAYER_SIZE // 2 + 5 + i * 15, ey - PLAYER_SIZE // 2 - 15,
                ex - PLAYER_SIZE // 2 + 15 + i * 15, ey - PLAYER_SIZE // 2 - 5,
                fill="red"
            )
            life_rects.append(rect)

def move_enemies():
    for index in range(len(enemies) - 1, -1, -1):
        enemy, lives, life_rects = enemies[index]
        canvas.move(enemy, 0, ENEMY_SPEED)
        for rect in life_rects:
            canvas.move(rect, 0, ENEMY_SPEED)
        if canvas.coords(enemy)[1] > SCREEN_HEIGHT:
            for rect in life_rects:
                canvas.delete(rect)
            canvas.delete(enemy)
            enemies.pop(index)
    canvas.after(100, move_enemies)

def enemy_shoot():
    for enemy, lives, _ in enemies:
        if random.random() < 0.02:
            ex, ey = canvas.coords(enemy)
            bullet_x = ex
            bullet_y = ey + PLAYER_SIZE // 2
            bullet = canvas.create_rectangle(
                bullet_x - 5, bullet_y,
                bullet_x + 5, bullet_y + 10,
                fill="white"
            )
            enemy_bullets.append(bullet)
    canvas.after(200, enemy_shoot)

def move_enemy_bullets():
    global player_lives
    for bullet in enemy_bullets[:]:
        canvas.move(bullet, 0, ENEMY_BULLET_SPEED)
        bx1, by1, bx2, by2 = canvas.coords(bullet)
        if by2 > SCREEN_HEIGHT:
            canvas.delete(bullet)
            enemy_bullets.remove(bullet)
            continue
        px1, py1, px2, py2 = canvas.coords(player)
        if bx1 < px2 and bx2 > px1 and by1 < py2 and by2 > py1:
            canvas.delete(bullet)
            enemy_bullets.remove(bullet)
            player_lives -= 1
            draw_player_lives()
            if player_lives <= 0:
                game_over()
            break
    canvas.after(50, move_enemy_bullets)

def game_over():
    canvas.create_text(
        SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
        text="GAME OVER YOU GAY", fill="white", font=("Arial", 40)
    )
    root.unbind("<KeyPress>")
    root.unbind("<space>")

def clear_all():
    global progress_bar, progress_bar_bg, progress_text
    for enemy, lives, life_rects in enemies:
        canvas.delete(enemy)
        for rect in life_rects:
            canvas.delete(rect)
    enemies.clear()
    for bullet in enemy_bullets:
        canvas.delete(bullet)
    enemy_bullets.clear()
    for bullet in bullets:
        canvas.delete(bullet)
    bullets.clear()
    if progress_bar:
        canvas.delete(progress_bar)
        progress_bar = None
    if progress_bar_bg:
        canvas.delete(progress_bar_bg)
        progress_bar_bg = None
    if progress_text:
        canvas.delete(progress_text)
        progress_text = None
    for particle in particles:
        canvas.delete(particle["id"])
    particles.clear()
    for rect in player_life_rects:
        canvas.delete(rect)
    player_life_rects.clear()

def check_collisions():
    global player_lives, enemies_killed
    for bullet in bullets[:]:
        bullet_coords = canvas.coords(bullet)
        for index in range(len(enemies) - 1, -1, -1):
            enemy, lives, life_rects = enemies[index]
            ex, ey = canvas.coords(enemy)
            enemy_left = ex - PLAYER_SIZE // 2
            enemy_top = ey - PLAYER_SIZE // 2
            enemy_right = ex + PLAYER_SIZE // 2
            enemy_bottom = ey + PLAYER_SIZE // 2
            if (bullet_coords[0] < enemy_right and
                bullet_coords[2] > enemy_left and
                bullet_coords[1] < enemy_bottom and
                bullet_coords[3] > enemy_top):
                canvas.delete(bullet)
                bullets.remove(bullet)
                lives -= 1
                if lives > 0:
                    enemies[index] = (enemy, lives, life_rects)
                else:
                    for rect in life_rects:
                        canvas.delete(rect)
                    spawn_particles(ex, ey, "red")
                    canvas.delete(enemy)
                    enemies.pop(index)
                    enemies_killed += 1
                    draw_progress_bar()
                    if enemies_killed >= ENEMIES_PER_LEVEL:
                        clear_all()
                        canvas.create_text(
                            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                            text="YOU WIN HORNY!", fill="white", font=("Arial", 32)
                        )
                draw_enemy_lives()
                break

    px1, py1, px2, py2 = canvas.coords(player)
    for enemy, lives, life_rects in enemies:
        ex1, ey1 = canvas.coords(enemy)
        ex2 = ex1 + PLAYER_SIZE
        ey2 = ey1 + PLAYER_SIZE
        if px1 < ex2 and px2 > ex1 and py1 < ey2 and py2 > ey1:
            player_lives -= 1
            draw_player_lives()
            if player_lives <= 0:
                game_over()
            break

    canvas.after(50, check_collisions)

def spawn_particles(x, y, color):
    for _ in range(20):
        dx = random.uniform(-3, 3)
        dy = random.uniform(-3, 3)
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

def draw_progress_bar():
    global progress_bar, progress_bar_bg, progress_text
    if progress_bar:
        canvas.delete(progress_bar)
    if progress_bar_bg:
        canvas.delete(progress_bar_bg)
    if progress_text:
        canvas.delete(progress_text)
    
    bar_x = 100
    bar_y = SCREEN_HEIGHT - 25
    bar_width = 150
    bar_height = 15
    progress_bar_bg = canvas.create_rectangle(
        bar_x, bar_y,
        bar_x + bar_width, bar_y + bar_height,
        outline="white"
    )
    fill = enemies_killed / ENEMIES_PER_LEVEL
    progress_bar = canvas.create_rectangle(
        bar_x, bar_y,
        bar_x + int(bar_width * fill), bar_y + bar_height,
        fill="white", outline=""
    )
    progress_text = canvas.create_text(
        bar_x + bar_width // 2, bar_y + bar_height // 2,
        text=f"{enemies_killed}/{ENEMIES_PER_LEVEL}",
        fill="red", font=("Arial", 10)
    )

def spawn_enemy():
    if enemies_killed < ENEMIES_PER_LEVEL:
        create_enemy()
        root.after(2000, spawn_enemy)


draw_player_lives()
draw_progress_bar()
move_bullets()
move_enemies()
check_collisions()
enemy_shoot()
move_enemy_bullets()
animate_particles()
spawn_enemy()

root.bind("<KeyPress>", move_player)
root.mainloop()