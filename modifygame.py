import tkinter as tk
import random


class BrickBreakerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Brick Breaker Game")
        self.width = 600
        self.height = 400
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        # Variabel utama
        self.level = 1
        self.score = 0
        self.lives = 3
        self.running = False

        # Objek game
        self.paddle = None
        self.ball = None
        self.bricks = []
        self.power_ups = []

        # Tekstur UI
        self.score_text = None
        self.lives_text = None
        self.level_text = None

        # Mulai permainan
        self.setup_game()
        self.root.bind("<Left>", lambda event: self.move_paddle(-20))
        self.root.bind("<Right>", lambda event: self.move_paddle(20))
        self.root.bind("<space>", lambda event: self.start_game())

    def setup_game(self):
        self.create_paddle()
        self.create_ball()
        self.create_bricks()
        self.update_ui()

    def create_paddle(self):
        if self.paddle:
            self.canvas.delete(self.paddle)
        paddle_width = 100
        paddle_height = 10
        x_start = (self.width / 2) - (paddle_width / 2)
        y_start = self.height - 30
        self.paddle = self.canvas.create_rectangle(
            x_start, y_start, x_start + paddle_width, y_start + paddle_height, fill="blue"
        )

    def create_ball(self):
        if self.ball:
            self.canvas.delete(self.ball)
        ball_size = 10
        self.ball = self.canvas.create_oval(
            self.width / 2 - ball_size,
            self.height / 2 - ball_size,
            self.width / 2 + ball_size,
            self.height / 2 + ball_size,
            fill="white",
        )
        self.ball_dx = random.choice([-3, 3])
        self.ball_dy = -3

    def create_bricks(self):
        for brick in self.bricks:
            self.canvas.delete(brick)
        self.bricks.clear()
        rows = self.level + 2
        cols = 10
        brick_width = 50
        brick_height = 20
        padding = 5
        for row in range(rows):
            for col in range(cols):
                x_start = col * (brick_width + padding) + padding
                y_start = row * (brick_height + padding) + padding + 30
                color = random.choice(["red", "green", "yellow", "purple"])
                brick = self.canvas.create_rectangle(
                    x_start, y_start, x_start + brick_width, y_start + brick_height, fill=color
                )
                self.bricks.append(brick)

    def move_paddle(self, dx):
        if self.running:
            paddle_coords = self.canvas.coords(self.paddle)
            if 0 < paddle_coords[0] + dx and paddle_coords[2] + dx < self.width:
                self.canvas.move(self.paddle, dx, 0)

    def start_game(self):
        if not self.running:
            self.running = True
            self.game_loop()

    def game_loop(self):
        if self.running:
            self.move_ball()
            self.check_collisions()
            self.root.after(20, self.game_loop)

    def move_ball(self):
        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        ball_coords = self.canvas.coords(self.ball)

        # Pantulan dari dinding
        if ball_coords[0] <= 0 or ball_coords[2] >= self.width:
            self.ball_dx *= -1
        if ball_coords[1] <= 0:
            self.ball_dy *= -1

        # Bola jatuh ke bawah
        if ball_coords[3] >= self.height:
            self.lives -= 1
            self.update_ui()
            if self.lives == 0:
                self.running = False
                self.canvas.create_text(
                    self.width / 2,
                    self.height / 2,
                    text="GAME OVER!",
                    fill="white",
                    font=("Helvetica", 24),
                )
            else:
                self.create_ball()

    def check_collisions(self):
        ball_coords = self.canvas.coords(self.ball)
        # Pantulan dari paddle
        paddle_coords = self.canvas.coords(self.paddle)
        if (
            paddle_coords[0] < ball_coords[2]
            and paddle_coords[2] > ball_coords[0]
            and paddle_coords[1] < ball_coords[3]
            and paddle_coords[3] > ball_coords[1]
        ):
            self.ball_dy *= -1

        # Pantulan dan penghancuran balok
        for brick in self.bricks:
            brick_coords = self.canvas.coords(brick)
            if (
                brick_coords[0] < ball_coords[2]
                and brick_coords[2] > ball_coords[0]
                and brick_coords[1] < ball_coords[3]
                and brick_coords[3] > ball_coords[1]
            ):
                self.bricks.remove(brick)
                self.canvas.delete(brick)
                self.ball_dy *= -1
                self.score += 10
                self.update_ui()

                # Peluang power-up muncul
                if random.random() < 0.2:
                    self.spawn_power_up(brick_coords)

        # Jika semua balok hancur
        if not self.bricks:
            self.level += 1
            self.create_bricks()
            self.create_ball()
            self.update_ui()

    def spawn_power_up(self, brick_coords):
        x_start = (brick_coords[0] + brick_coords[2]) / 2
        y_start = (brick_coords[1] + brick_coords[3]) / 2
        power_up = self.canvas.create_oval(
            x_start - 10, y_start - 10, x_start + 10, y_start + 10, fill="gold"
        )
        self.power_ups.append(power_up)

    def update_ui(self):
        if self.score_text:
            self.canvas.delete(self.score_text)
        if self.lives_text:
            self.canvas.delete(self.lives_text)
        if self.level_text:
            self.canvas.delete(self.level_text)

        self.score_text = self.canvas.create_text(
            50, 10, text=f"Score: {self.score}", fill="white", font=("Helvetica", 12)
        )
        self.lives_text = self.canvas.create_text(
            150, 10, text=f"Lives: {self.lives}", fill="white", font=("Helvetica", 12)
        )
        self.level_text = self.canvas.create_text(
            250, 10, text=f"Level: {self.level}", fill="white", font=("Helvetica", 12)
        )


# Menjalankan game
if __name__ == "__main__":
    root = tk.Tk()
    game = BrickBreakerGame(root)
    root.mainloop()