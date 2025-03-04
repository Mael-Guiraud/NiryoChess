import params
import pygame
import chess
import os
import tkinter as tk
from tkinter import simpledialog
def load_img_pieces():
    pieces = params.global_state["pieces"]
    for piece in "KQRBNP":
        pieces[piece] = pygame.image.load(os.path.join(params.PIECE_PATH, f"Chess_{piece}lt45.png"))
        pieces[piece.lower()] = pygame.image.load(os.path.join(params.PIECE_PATH, f"Chess_{piece}dt45.png"))



def select_stockfish_level():
    root = tk.Tk()
    root.withdraw()  # Cache la fenêtre principale de Tkinter

    levels = [1, 5, 10, 15, 20]
    level = simpledialog.askinteger("Stockfish Level", "Choose level (1-20):", minvalue=1, maxvalue=20)

    return level if level is not None else 10  # Si l'utilisateur ferme, niveau par défaut = 10

def init_board():
    pygame.init()
    params.global_state["screen"] = pygame.display.set_mode((params.WIDTH, params.HEIGHT))
    pygame.display.set_caption("Chess against a robot")
    params.global_state["font"] = pygame.font.Font(None, 40)
    load_img_pieces()
def draw_board(board, time_white, time_black):
    screen = params.global_state["screen"]
    screen.fill((50, 50, 50))  

    colors = [(200, 200, 200), (100, 100, 100)]
    pastel_red = (255, 160, 160)  
    board_size = params.BOARD_SIZE
    sq_size = params.SQ_SIZE

    font = pygame.font.SysFont("Arial", 24)
    text_color = (255, 255, 255)  

    
    selected_square = params.global_state.get("selected_square", None)

    #Draw the chessboard and pieces
    for row in range(8):
        for col in range(8):
            rect_x = col * sq_size
            rect_y = row * sq_size

            file = 7 - col  
            rank = row
            square_id = chess.square(file, rank)

           
            if selected_square is not None and square_id == selected_square:
                color = pastel_red
            else:
                color = colors[(row + col) % 2]

            pygame.draw.rect(screen, color, (rect_x, rect_y, sq_size, sq_size))

            piece = board.piece_at(square_id)
            if piece:
                img = pygame.transform.scale(params.global_state["pieces"][piece.symbol()], (sq_size, sq_size))
                screen.blit(img, (rect_x, rect_y))

    
    for i in range(8):
        #Draw the letters (a-h) at the bottom
        letter = chr(ord('h') - i)
        text_surf = font.render(letter, True, text_color)
        text_x = i * sq_size + sq_size // 2 - text_surf.get_width() // 2
        text_y = board_size + 10  # Aligné sous l'échiquier
        screen.blit(text_surf, (text_x, text_y))

        #Draw the numbers (1-8) on the left
        number = str(i + 1)
        text_surf = font.render(number, True, text_color)
        text_x = board_size + 10  # Collé à gauche
        text_y = i * sq_size + sq_size // 2 - text_surf.get_height() // 2
        screen.blit(text_surf, (text_x, text_y))



    w_str = f"{int(time_white) // 60}:{int(time_white) % 60:02d}"
    b_str = f"{int(time_black) // 60}:{int(time_black) % 60:02d}"
    if board.is_checkmate():
        w_surf = font.render(f"Checkmate !", True, (255, 255, 255))
        screen.blit(w_surf, (20, board_size + 40))
    else:
        if params.TIMERS:
            w_surf = font.render(f"Stockfish (White) : {w_str}", True, (255, 255, 255))
            b_surf = font.render(f"Human (Black) : {b_str}", True, (255, 255, 255))

            screen.blit(w_surf, (20, board_size + 40))
            screen.blit(b_surf, (20, board_size + 90))

    pygame.display.update()
