#Robot IP on your network
robot_ip = "192.168.0.101"

#For the windown on the screen select the width of the board (in px)
BOARD_SIZE = 600
#height of the info bar (in px)
INFO_HEIGHT = 100

#0 for real game (with robot), 1 for simulated game (just the chess engine)
SIMULATED = 1

#0 for no timers, 1 for timers
TIMERS = 1

#time (in seconds) for each player
TIME_WHITE = 600
TIME_BLACK = 600

#path of the stockfish executable
STOCKFISH_PATH = "/usr/games/stockfish"

#path of the pieces images
PIECE_PATH = "./pieces_png"




#Don't touch this
WIDTH, HEIGHT = BOARD_SIZE + 30, BOARD_SIZE + INFO_HEIGHT+30
SQ_SIZE = BOARD_SIZE // 8
global_state={"pieces":{}}
