class Player:
    def __init__(self, canvas, x, y, size, color="red"):
        self.canvas = canvas
        self.size = size
        self.lives = PLAYER_MAX_LIVES
        self.id = canvas.create_rectangle(
            x, y, x + size, y + size, fill=color
        )
        self.life_rects = []

    def move(self, dx, dy):
        self.canvas.move(self.id, dx, dy)

    def get_coords(self):
        return self.canvas.coords(self.id)

    def draw_lives(self):
        for rect in self.life_rects:
            self.canvas.delete(rect)
        self.life_rects = []
        for i in range(self.lives):
            rect = self.canvas.create_rectangle(
                10 + i * 25, SCREEN_HEIGHT - 30,
                30 + i * 25, SCREEN_HEIGHT - 10,
                fill="red"
            )
            self.life_rects.append(rect)