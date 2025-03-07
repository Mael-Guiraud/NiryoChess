# Chess with a Robotic Arm

♟️🤖📚 This project explores the intersection of algorithmic decision-making and robotic manipulation through a chess engine (Stockfish) interfaced with a Niryo robotic arm. The system integrates a graphical interface (`pygame`) and precise robotic control (`pyniryo`).

## Installation

### Requirements
- Python 3.x
- A chessboard
- Stockfish (chess engine)
- **A Niryo robotic arm controllable with pyniryo in python**

### Installing Dependencies

```bash
pip install pygame python-chess pyniryo
```

If you are using a linux system, you may need to install the tk-inter package:
```bash
sudo apt-get install python3-tk

```

### Configuration

1. **Download and install Stockfish** 🎯📥♞
   - Obtain the latest version from the official website: [Stockfish](https://stockfishchess.org/download/), or using the following command (Linux):
     ```bash
     sudo apt update && sudo apt install stockfish
     ```

2. **Fill the `params.py` file with your local informations** 🛠️
    - Modify `robot_ip` in `params.py` to match your Niryo's arm network address.
    - Configure `STOCKFISH_PATH` to reference the correct executable ("/usr/games/stockfish" if installed via `apt`).
    - Set `SIMULATED = 1` to run the simulation mode (without the robotic arm).
    - Set `TIMERS = 1` to enable time control for each player.
    - Modify `PIECE_PATH` to specify the directory containing chess piece images (default: "./pieces_png").
    - Set `PROMOTION_RESERVE=1` if you have some reserve pieces in case of promotion (the positions of the pieces must be saved, following next step).
   

3. **Calibrate and store key positions in the robotic arm’s memory** 📍⚙️🧠
   If you use the niryo arm, the following positional references must be pre-saved in the robotic system:
     - `A1`: Bottom-left corner of the board, when the robot is facing the board. (If the player choose to play as white, the positions will automatically be adjusted). 
     - `H8`: Top-right corner of the board, when the robot is facing the board.
     - `wait_robot`: Standby position to optimize movement efficiency.
     - `dead_pieces`: Position to store captured pieces. (Usually outside the board, but close to the "a1" position is recommended).
     - `promotQ`, `promotR`, `promotB`, `promotN`: Positions of reserve pieces for promotion, if you have some (otherwise, you can ignore this step and let `PROMOTION_RESERVE = 0` in `params.py`).


    You can use the script `save_one_pos.py` to save a single position in the robotic arm's memory, ensuring you save the four positions mentioned above with the corresponding names.

4. **Fix the chessboard in place** 📏♟️🔧
   - Any displacement post-calibration will disrupt movement precision. The chessboard must remain stationary throughout operation.

5. **Optionnal: Save the sounds in the arm memory** 🎶🔊🧠
   - If you want to use the sounds, you can save them in the robotic arm's memory. The sounds are in the `sounds` folder. We provide an english and a french version of the sounds. You must import them into the ned's memory using niryo studio. DO NOT CHANGE THE NAME OF THE FILES. You can then set the `SOUND_ON` parameter to `1` in the `params.py` file.
## Usage

### Launch the Game 🚀♞🎲

Run the following command:
```bash
python3 main.py
```

### How It Works ⚡♟️🤖
- **The game starts with the robotic arm in the standby position.** The player choose a difficulty level and side.
- **Stockfish executes moves autonomously.** The robotic arm physically manipulates the chess pieces according to the computed strategy.
- **The human player interacts via the graphical interface.** Use the mouse to select and move pieces.

### Controls 🖱️🔚🎮
- **To exit the game**, either close the window or terminate execution using `Ctrl + C` in the terminal.

### Known issues 🐞🔍🔧
- **Arm range issue:** The arm may not be able to reach the edge of the board in. If this occurs, use a smaller chessboard.
- **Gripper open range:** The gripper could open too wide, causing pieces to fall. Adjust the gripper's opening range directly in the niryo files (`catkin_ws/install/release/share/niryo_robot_tools_commander/config/[YOUR_NED_VERSION]/nano tools_definition.yaml`). 


## Project Structure 🏗️📁📜

```
/
├── /pieces_png      # Chess piece images
├── save_position.py # Script to save a single position in the robotic arm's memory
├── arm_robot.py     # Robotic arm control functions
├── graphisms.py     # Chess game graphical interface
├── main.py          # Core gameplay logic
├── params.py        # System parameters and configurations
└── README.md        # Documentation
```

