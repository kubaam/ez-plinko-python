import tkinter as tk
import random
import math
from threading import Thread
import time

# Global variables
balance = 0.0  # Initial balance
ball_price = 1.0  # Default ball price
rows = 10  # Number of obstacle rows
rewards = [5, 2, 1, 0.5, 0.25, 0.1, 0.1, 0.25, 0.5, 1, 2, 5]  # Multipliers
slot_width = 50  # Width of each reward slot
row_height = 50  # Height between rows
obstacle_spacing = 60  # Spacing between obstacles in a row
obstacles = []
ball_id = 0  # Unique ID for each ball
canvas = None  # Canvas instance

# Dynamic canvas size
canvas_width = len(rewards) * slot_width + 50  # Canvas width
canvas_height = rows * row_height + 25  # Canvas height


def start_game():
    global balance
    try:
        balance = float(balance_entry.get())
        balance_label.config(text=f"Balance: ${balance:.2f}")
        drop_button.config(state=tk.NORMAL)
    except ValueError:
        balance_label.config(text="Invalid input. Please enter a valid number!")


def update_ball_price():
    global ball_price
    try:
        ball_price = float(ball_price_entry.get())
        ball_price_label.config(text=f"Ball Price: ${ball_price:.2f}")
    except ValueError:
        ball_price_label.config(text="Invalid input!")


def drop_ball():
    if balance < ball_price:
        balance_label.config(text="Insufficient balance!")
        return

    Thread(target=simulate_ball).start()


def simulate_ball():
    global balance, ball_price, ball_id
    balance -= ball_price
    ball_x = canvas_width // 2
    ball_y = row_height // 2 - 10
    velocity_x = 0
    velocity_y = 0
    gravity = 0.2
    has_hit_peak = False

    ball_tag = f"ball_{ball_id}"
    ball_id += 1

    while ball_y < rows * row_height:
        if not has_hit_peak and ball_y >= obstacles[0][1] - 5:
            has_hit_peak = True
            velocity_x = random.choice([-1, 1]) * 1.5
            velocity_y = gravity
        else:
            velocity_y += gravity

            move_choice = random.choices(
                population=[-1, 0, 1],
                weights=[1, 5, 1],
                k=1
            )[0]
            velocity_x += move_choice * 0.5
            ball_x += velocity_x
            ball_y += velocity_y

            if ball_x < 10:
                ball_x = 10
                velocity_x = abs(velocity_x) * 0.8
            elif ball_x > canvas_width - 10:
                ball_x = canvas_width - 10
                velocity_x = -abs(velocity_x) * 0.8

            for i, (ox, oy) in enumerate(obstacles):
                distance = math.sqrt((ox - ball_x) ** 2 + (oy - ball_y) ** 2)
                if distance < 6:
                    overlap = 6 - distance
                    angle = math.atan2(ball_y - oy, ball_x - ox)
                    ball_x += math.cos(angle) * overlap
                    ball_y += math.sin(angle) * overlap
                    if i == 0:
                        velocity_y = gravity
                        velocity_x = random.choice([-1, 1]) * 1.5
                    else:
                        velocity_x += math.cos(angle) * 1.2
                        velocity_y = -abs(math.sin(angle) * velocity_y * 0.8)

        canvas.delete(ball_tag)
        canvas.create_oval(
            ball_x - 5, ball_y - 5, ball_x + 5, ball_y + 5,
            fill="#FF6F61", outline="#FF3D00", width=1, tags=ball_tag
        )
        canvas.update()
        time.sleep(0.02)

    slot_index = int(ball_x // slot_width)
    if 0 <= slot_index < len(rewards):
        winnings = rewards[slot_index] * ball_price
        balance += winnings

    canvas.delete(ball_tag)
    update_slots()
    balance_label.config(text=f"Balance: ${balance:.2f}")


def draw_pyramid():
    global obstacles
    obstacles = []

    for row in range(rows):
        for col in range(row + 1):
            x = (canvas_width // 2) - (row * obstacle_spacing // 2) + col * obstacle_spacing
            y = row * row_height + row_height // 2
            obstacles.append((x, y))
            canvas.create_oval(
                x - 4, y - 4, x + 4, y + 4, fill="#00C9FF", outline="#00A5E0", width=1, tags="obstacle"
            )


def update_slots():
    canvas.delete("slots")
    for i, multiplier in enumerate(rewards):
        slot_x_start = i * (canvas_width / len(rewards))
        slot_x_end = (i + 1) * (canvas_width / len(rewards))
        canvas.create_rectangle(
            slot_x_start, rows * row_height, slot_x_end, rows * row_height + 20,
            fill="#0ACF83", outline="#0ACF83", tags="slots"
        )
        canvas.create_text(
            (slot_x_start + slot_x_end) / 2, rows * row_height + 10,
            text=f"x{multiplier:.2f}", fill="white", font=("Arial", 9, "bold"), tags="slots"
        )


def resize(event):
    global canvas_width, canvas_height
    canvas_width = event.width
    canvas_height = event.height
    canvas.config(width=canvas_width, height=canvas_height)
    canvas.delete("all")
    draw_pyramid()
    update_slots()


# GUI Setup
root = tk.Tk()
root.title("EZ Plinko Python")
root.configure(bg="#1E1E1E")

settings_frame = tk.Frame(root, bg="#1E1E1E")
settings_frame.pack(pady=10)

tk.Label(settings_frame, text="Starting Balance ($):", bg="#1E1E1E", fg="#FFFFFF", font=("Arial", 10)).grid(row=0, column=0, padx=5)
balance_entry = tk.Entry(settings_frame, font=("Arial", 10), bg="#333333", fg="#FFFFFF", insertbackground="#FFFFFF")
balance_entry.grid(row=0, column=1, padx=5)

tk.Label(settings_frame, text="Ball Price ($):", bg="#1E1E1E", fg="#FFFFFF", font=("Arial", 10)).grid(row=1, column=0, padx=5)
ball_price_entry = tk.Entry(settings_frame, font=("Arial", 10), bg="#333333", fg="#FFFFFF", insertbackground="#FFFFFF")
ball_price_entry.insert(0, str(ball_price))
ball_price_entry.grid(row=1, column=1, padx=5)

update_button = tk.Button(settings_frame, text="Update Price", command=update_ball_price, bg="#0ACF83", fg="#1E1E1E", font=("Arial", 10, "bold"))
update_button.grid(row=1, column=2, padx=5)

start_button = tk.Button(settings_frame, text="Start Game", command=start_game, bg="#3498DB", fg="#FFFFFF", font=("Arial", 10, "bold"))
start_button.grid(row=2, columnspan=3, pady=10)

balance_label = tk.Label(root, text=f"Balance: ${balance:.2f}", bg="#1E1E1E", fg="#FFFFFF", font=("Arial", 12, "bold"))
balance_label.pack(pady=5)

ball_price_label = tk.Label(root, text=f"Ball Price: ${ball_price:.2f}", bg="#1E1E1E", fg="#FFFFFF", font=("Arial", 12, "bold"))
ball_price_label.pack(pady=5)

canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="#282828", bd=0, highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)
canvas.bind("<Configure>", resize)

drop_button = tk.Button(root, text="Drop Ball", command=drop_ball, bg="#FF6F61", fg="#FFFFFF", font=("Arial", 10, "bold"), state=tk.DISABLED)
drop_button.pack(pady=10)

draw_pyramid()
update_slots()

root.mainloop()
