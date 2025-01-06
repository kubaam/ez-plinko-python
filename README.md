# Plinko - Enhanced Version

A Python-based Plinko game using `tkinter` for an engaging, interactive experience. Players drop balls through a pyramid of obstacles, aiming to land in reward slots that multiply the ball price.

## Features

- **Dynamic Plinko Board**: The pyramid and reward slots are drawn dynamically based on the canvas size.
- **Customizable**: Users can set the starting balance and ball price.
- **Real-Time Updates**: Balance and ball price are updated live as the game progresses.
- **Threading for Smooth Animation**: The ball simulation runs in a separate thread to keep the UI responsive.

## Prerequisites

Ensure you have Python 3 installed on your system. This program uses the standard library, so no additional dependencies are required.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/kubaam/ez-plinko-python.git
   cd plinko-enhanced
   ```

2. Run the script:
   ```bash
   python plinko.py
   ```

## How to Play

1. Enter the starting balance in the **Starting Balance** field.
2. Optionally, update the ball price in the **Ball Price** field and click "Update Price."
3. Click **Start Game** to begin.
4. Drop a ball by clicking the **Drop Ball** button.
5. Watch the ball fall and see where it lands. Rewards are added to your balance automatically.

## File Structure

```
plinko-enhanced/
├── plinko.py       # Main game script
├── README.md       # Project documentation
└── .gitignore      # Git ignore file
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

Enjoy playing the Plinko game and customize it to your liking! Contributions are welcome; feel free to submit issues and pull requests.
