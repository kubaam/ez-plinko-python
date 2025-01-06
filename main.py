import tkinter as tk
import random
import math

class PlinkoGameMultiBalls:
    def __init__(self, root):
        self.root = root
        self.root.title("EZ Plinko - Multi-Balls with Smaller Multipliers")
        self.root.configure(bg="#1E1E1E")

        # ------------------- Configurable Settings -------------------
        # Reduced the 5x multipliers to 3x
        self.rows = 10
        self.rewards = [3, 2, 1, 0.5, 0.25, 0.1, 0.1, 0.25, 0.5, 1, 2, 3]  
        self.ball_radius = 12
        self.obstacle_radius = 4
        self.obstacle_spacing = 60
        self.row_height = 50
        self.gravity = 0.25
        self.default_ball_price = 1.0

        # ------------------- Game State Variables -------------------
        self.balance = 0.0
        self.ball_price = self.default_ball_price
        self.game_running = False
        self.paused = False
        self.obstacles = []

        # Each ball is stored as a dict {id, tag, x, y, vx, vy}
        self.balls = []
        self.ball_counter = 0  # Unique ID counter for each ball

        # Canvas dimensions recalculated on resize
        self.canvas_width = len(self.rewards) * 50 + 175
        self.canvas_height = self.rows * self.row_height + 60

        # ------------------- GUI Setup -------------------
        self._create_widgets()
        self._layout_widgets()

        # Draw obstacles and slots
        self._draw_pyramid()
        self._update_slots()

        # Bind for dynamic resizing
        self.canvas.bind("<Configure>", self._on_resize)

        # Start the animation loop
        self._update_balls()

    # ------------------- GUI Creation -------------------
    def _create_widgets(self):
        self.settings_frame = tk.Frame(self.root, bg="#1E1E1E")

        # Balance input
        tk.Label(
            self.settings_frame, text="Starting Balance ($):",
            bg="#1E1E1E", fg="#FFFFFF", font=("Arial", 10)
        ).grid(row=0, column=0, padx=5, sticky="e")
        self.balance_entry = tk.Entry(
            self.settings_frame, font=("Arial", 10),
            bg="#333333", fg="#FFFFFF", insertbackground="#FFFFFF"
        )
        self.balance_entry.grid(row=0, column=1, padx=5)

        # Ball price input
        tk.Label(
            self.settings_frame, text="Ball Price ($):",
            bg="#1E1E1E", fg="#FFFFFF", font=("Arial", 10)
        ).grid(row=1, column=0, padx=5, sticky="e")
        self.ball_price_entry = tk.Entry(
            self.settings_frame, font=("Arial", 10),
            bg="#333333", fg="#FFFFFF", insertbackground="#FFFFFF"
        )
        self.ball_price_entry.insert(0, str(self.ball_price))
        self.ball_price_entry.grid(row=1, column=1, padx=5)

        # Update price button
        self.update_price_btn = tk.Button(
            self.settings_frame, text="Update Price",
            command=self.update_ball_price,
            bg="#0ACF83", fg="#1E1E1E", font=("Arial", 10, "bold")
        )
        self.update_price_btn.grid(row=1, column=2, padx=5)

        # Start game button
        self.start_btn = tk.Button(
            self.settings_frame, text="Start Game",
            command=self.start_game, bg="#3498DB", fg="#FFFFFF",
            font=("Arial", 10, "bold")
        )
        self.start_btn.grid(row=2, columnspan=3, pady=10)

        # Labels
        self.balance_label = tk.Label(
            self.root, text=f"Balance: ${self.balance:.2f}",
            bg="#1E1E1E", fg="#FFFFFF", font=("Arial", 12, "bold")
        )
        self.ball_price_label = tk.Label(
            self.root, text=f"Ball Price: ${self.ball_price:.2f}",
            bg="#1E1E1E", fg="#FFFFFF", font=("Arial", 12, "bold")
        )

        # Canvas
        self.canvas = tk.Canvas(
            self.root, width=self.canvas_width, height=self.canvas_height,
            bg="#282828", bd=0, highlightthickness=0
        )

        # Control buttons
        self.drop_btn = tk.Button(
            self.root, text="Drop Ball", command=self.drop_ball,
            bg="#FF6F61", fg="#FFFFFF", font=("Arial", 10, "bold"),
            state=tk.DISABLED
        )
        self.pause_btn = tk.Button(
            self.root, text="Pause", command=self.toggle_pause,
            bg="#FFD700", fg="#1E1E1E", font=("Arial", 10, "bold"),
            state=tk.DISABLED
        )
        self.reset_btn = tk.Button(
            self.root, text="Reset / New Game", command=self.reset_game,
            bg="#C0392B", fg="#FFFFFF", font=("Arial", 10, "bold"),
            state=tk.DISABLED
        )

    def _layout_widgets(self):
        self.settings_frame.pack(pady=10)
        self.balance_label.pack(pady=5)
        self.ball_price_label.pack(pady=5)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.drop_btn.pack(pady=5)
        self.pause_btn.pack(pady=5)
        self.reset_btn.pack(pady=5)

    # ------------------- Game Control -------------------
    def start_game(self):
        """Sets starting balance and enables game buttons."""
        try:
            self.balance = float(self.balance_entry.get())
            self.balance_label.config(text=f"Balance: ${self.balance:.2f}")
            self.game_running = True
            self.drop_btn.config(state=tk.NORMAL)
            self.pause_btn.config(state=tk.NORMAL)
            self.reset_btn.config(state=tk.NORMAL)
        except ValueError:
            self.balance_label.config(text="Invalid. Enter a number!")

    def reset_game(self):
        """Clears everything to start a new game."""
        self.balance = 0.0
        self.ball_price = self.default_ball_price
        self.game_running = False
        self.paused = False
        self.balance_entry.delete(0, tk.END)
        self.balance_entry.insert(0, "0")
        self.ball_price_entry.delete(0, tk.END)
        self.ball_price_entry.insert(0, str(self.ball_price))
        self.balance_label.config(text=f"Balance: ${self.balance:.2f}")
        self.ball_price_label.config(text=f"Ball Price: ${self.ball_price:.2f}")

        # Remove all existing balls
        for ball in self.balls:
            self.canvas.delete(ball["id"])
        self.balls.clear()

        # Disable buttons until a new game is started
        self.drop_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.DISABLED)
        self.reset_btn.config(state=tk.DISABLED)

    def update_ball_price(self):
        """Updates ball price from user input."""
        try:
            self.ball_price = float(self.ball_price_entry.get())
            self.ball_price_label.config(text=f"Ball Price: ${self.ball_price:.2f}")
        except ValueError:
            self.ball_price_label.config(text="Invalid input!")

    def drop_ball(self):
        """Creates a new ball if possible and assigns a unique ID."""
        if not self.game_running:
            return

        if self.balance < self.ball_price:
            self.balance_label.config(text="Insufficient balance!")
            return

        # Deduct the cost of the ball
        self.balance -= self.ball_price
        self.balance_label.config(text=f"Balance: ${self.balance:.2f}")

        # Assign a unique tag to this ball
        ball_name = f"ball_{self.ball_counter}"
        self.ball_counter += 1

        # Random horizontal spawn near center
        random_x = (self.canvas_width // 2) + random.randint(-60, 60)
        ball_y = self.row_height // 2 - self.ball_radius

        # Random initial velocity
        vx = random.uniform(-2.0, 2.0)
        vy = 0

        # Create the ball on the canvas with a unique tag
        ball_id = self.canvas.create_oval(
            random_x - self.ball_radius, ball_y - self.ball_radius,
            random_x + self.ball_radius, ball_y + self.ball_radius,
            fill="#FF6F61", outline="#FF3D00", width=1,
            tags=(ball_name,)
        )

        # Store the ball in the list
        self.balls.append({
            "id": ball_id,
            "tag": ball_name,
            "x": random_x,
            "y": ball_y,
            "vx": vx,
            "vy": vy
        })

    def toggle_pause(self):
        """Pause/Resume the physics loop."""
        if not self.game_running:
            return
        self.paused = not self.paused
        self.pause_btn.config(text="Resume" if self.paused else "Pause")

    # ------------------- Animation Loop -------------------
    def _update_balls(self):
        """Updates positions, collisions, and rewards for all balls."""
        if not self.paused and self.balls:
            for ball in self.balls[:]:
                # Apply gravity
                ball["vy"] += self.gravity

                # Horizontal drift
                move_choice = random.choices([-1, 0, 1], weights=[1, 4, 1], k=1)[0]
                ball["vx"] += move_choice * 0.3

                # Update position
                ball["x"] += ball["vx"]
                ball["y"] += ball["vy"]

                # Left boundary
                if ball["x"] - self.ball_radius < 0:
                    ball["x"] = self.ball_radius
                    ball["vx"] = abs(ball["vx"]) * 0.7

                # Right boundary
                elif ball["x"] + self.ball_radius > self.canvas_width:
                    ball["x"] = self.canvas_width - self.ball_radius
                    ball["vx"] = -abs(ball["vx"]) * 0.7

                # Obstacle collisions
                for (ox, oy) in self.obstacles:
                    dist = math.sqrt((ox - ball["x"])**2 + (oy - ball["y"])**2)
                    if dist < (self.obstacle_radius + self.ball_radius):
                        overlap = (self.obstacle_radius + self.ball_radius) - dist
                        angle = math.atan2(ball["y"] - oy, ball["x"] - ox)
                        ball["x"] += math.cos(angle) * overlap
                        ball["y"] += math.sin(angle) * overlap
                        # Bounce
                        ball["vx"] += math.cos(angle) * 1.0
                        ball["vy"] = -abs(ball["vy"]) * 0.8

                # Update canvas position
                self.canvas.coords(
                    ball["id"],
                    ball["x"] - self.ball_radius, ball["y"] - self.ball_radius,
                    ball["x"] + self.ball_radius, ball["y"] + self.ball_radius
                )

                # Check if ball has fallen below the last row
                if ball["y"] > self.rows * self.row_height:
                    slot_width = self.canvas_width / len(self.rewards)
                    slot_index = int(ball["x"] // slot_width)
                    if 0 <= slot_index < len(self.rewards):
                        winnings = self.rewards[slot_index] * self.ball_price
                        self.balance += winnings
                        self.balance_label.config(text=f"Balance: ${self.balance:.2f}")

                    # Remove ball from canvas & list
                    self.canvas.delete(ball["id"])
                    self.balls.remove(ball)

        # Schedule next frame
        self.root.after(20, self._update_balls)

    # ------------------- Drawing Methods -------------------
    def _draw_pyramid(self):
        """Creates a pyramid of circle obstacles."""
        self.canvas.delete("obstacle")
        self.obstacles.clear()
        for row in range(self.rows):
            for col in range(row + 1):
                x = (self.canvas_width // 2) - (row * self.obstacle_spacing // 2) + col * self.obstacle_spacing
                y = row * self.row_height + self.row_height // 2
                self.obstacles.append((x, y))
                self.canvas.create_oval(
                    x - self.obstacle_radius, y - self.obstacle_radius,
                    x + self.obstacle_radius, y + self.obstacle_radius,
                    fill="#00C9FF", outline="#00A5E0", width=1, tags="obstacle"
                )

    def _update_slots(self):
        """Draws the reward slots at the bottom of the canvas."""
        self.canvas.delete("slots")
        slot_width = self.canvas_width / len(self.rewards)
        for i, multiplier in enumerate(self.rewards):
            sx_start = i * slot_width
            sx_end = (i + 1) * slot_width
            self.canvas.create_rectangle(
                sx_start, self.rows * self.row_height,
                sx_end, self.rows * self.row_height + 20,
                fill="#0ACF83", outline="#0ACF83", tags="slots"
            )
            self.canvas.create_text(
                (sx_start + sx_end) / 2, self.rows * self.row_height + 10,
                text=f"x{multiplier:.2f}", fill="white",
                font=("Arial", 9, "bold"), tags="slots"
            )

    # ------------------- Resizing -------------------
    def _on_resize(self, event):
        self.canvas_width = event.width
        self.canvas_height = event.height
        self.canvas.config(width=self.canvas_width, height=self.canvas_height)
        self._draw_pyramid()
        self._update_slots()

# ------------------- Main -------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = PlinkoGameMultiBalls(root)
    root.mainloop()
