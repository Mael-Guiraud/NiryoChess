import params
import pygame
import chess
import os
import arm_robot
import tkinter as tk
from tkinter import simpledialog
def load_img_pieces():
    pieces = params.global_state["pieces"]
    for piece in "KQRBNP":
        pieces[piece] = pygame.image.load(os.path.join(params.PIECE_PATH, f"Chess_{piece}lt45.png"))
        pieces[piece.lower()] = pygame.image.load(os.path.join(params.PIECE_PATH, f"Chess_{piece}dt45.png"))

def select_stockfish_level():
    """
    Opens a Tkinter dialog to select Stockfish level and playing color (white or black).
    Closes Tkinter completely before continuing.
    """
    root = tk.Tk()
    root.withdraw()  

    arm_robot.play_robot_sound("welcome.mp3")
    level = simpledialog.askinteger("Stockfish Level", "Choose level (1-20):", minvalue=1, maxvalue=20)
    if level is None:
        level = 10  
    color_window = tk.Toplevel(root)
    color_window.title("Select Your Side")
    color_window.geometry("300x150")

    tk.Label(color_window, text="Choose your Side:", font=("Arial", 14)).pack(pady=10)

    color = None  

    def set_color(choice):
        nonlocal color
        color = 0 if choice == "white" else 1
        color_window.destroy() 
        root.quit()  
    tk.Button(color_window, text="Play as White", command=lambda: set_color("white"), width=15).pack(pady=5)
    tk.Button(color_window, text="Play as Black", command=lambda: set_color("black"), width=15).pack(pady=5)
    arm_robot.play_robot_sound("side_selection.mp3")
    color_window.grab_set()  
    root.mainloop()  

    root.destroy()  

    return level, color if color is not None else 1  

def init_board():
    pygame.init()
    params.global_state["screen"] = pygame.display.set_mode((params.WIDTH, params.HEIGHT))
    pygame.display.set_caption("Chess against a robot")
    icon = pygame.image.load(os.path.join(params.SCRIPT_DIR, ".logo.png"))
    pygame.display.set_icon(icon)
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

            file = 7 - col if params.global_state["side"] == 1 else  col
            rank = row if params.global_state["side"] == 1 else  7- row
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
        letter = chr(ord('h') - i) if params.global_state["side"] == 1 else  chr(ord('a') + i)
        text_surf = font.render(letter, True, text_color)
        text_x = i * sq_size + sq_size // 2 - text_surf.get_width() // 2
        text_y = board_size + 10  # Aligné sous l'échiquier
        screen.blit(text_surf, (text_x, text_y))

        #Draw the numbers (1-8) on the left
        number = str(i + 1) if params.global_state["side"] == 1 else  str(8-i)
        text_surf = font.render(number, True, text_color)
        text_x = board_size + 10  # Collé à gauche
        text_y = i * sq_size + sq_size // 2 - text_surf.get_height() // 2
        screen.blit(text_surf, (text_x, text_y))



    w_str = f"{int(time_white) // 60}:{int(time_white) % 60:02d}"
    b_str = f"{int(time_black) // 60}:{int(time_black) % 60:02d}"
    if board.is_checkmate():
        font_large = pygame.font.SysFont("Arial", 72, bold=True) 
        checkmate_text = "CHECKMATE !"
        text_surf = font_large.render(checkmate_text, True, (255, 0, 0))  

  
        text_x = (params.WIDTH - text_surf.get_width()) // 2
        text_y = (params.HEIGHT - text_surf.get_height()) // 2

    
        screen.blit(text_surf, (text_x, text_y))

    else:
        if params.TIMERS:
            w_surf = font.render(f"Stockfish (White) : {w_str}", True, (255, 255, 255))
            b_surf = font.render(f"Human (Black) : {b_str}", True, (255, 255, 255))

            screen.blit(w_surf, (20, board_size + 40))
            screen.blit(b_surf, (20, board_size + 90))
    # Load and display the logo in the bottom-right corner
    logo = pygame.image.load(os.path.join(params.SCRIPT_DIR, ".logo.png"))  
    logo = pygame.transform.scale(logo, (80, 80)) 
    logo_x = params.WIDTH - 90  # Position at bottom-right
    logo_y = params.HEIGHT - 90
    screen.blit(logo, (logo_x, logo_y))

    pygame.display.update()

    if params.global_state.get("promot") == 1:
        show_promotion_menu(screen)

    pygame.display.update()

def show_promotion_menu(screen):
    menu_width, menu_height = 200, 150
    menu_x, menu_y = (params.WIDTH - menu_width) // 2, (params.HEIGHT - menu_height) // 2

    side = params.global_state["side"]  
    piece_color = chess.WHITE if side == 0 else chess.BLACK

  
    options = [
        (chess.QUEEN, "Q"),
        (chess.ROOK, "R"),
        (chess.BISHOP, "B"),
        (chess.KNIGHT, "N")
    ]

    button_size = 50 
    button_margin = 10
    button_x = menu_x + 10
    button_y = menu_y + 10

    buttons = []

    for piece_type, piece_symbol in options:
        button_rect = pygame.Rect(button_x, button_y, button_size, button_size)
        buttons.append((button_rect, piece_type))

        pygame.draw.rect(screen, (255, 255, 255), button_rect)
        pygame.draw.rect(screen, (0, 0, 0), button_rect, 2)

 
        piece_img = params.global_state["pieces"][chess.Piece(piece_type, piece_color).symbol()]
        piece_img = pygame.transform.scale(piece_img, (button_size, button_size))
        screen.blit(piece_img, (button_x, button_y))

  
        button_x += button_size + button_margin

    pygame.display.update()

    selecting = True
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for button_rect, piece in buttons:
                    print(button_rect,piece,mouse_x,mouse_y)
                    if button_rect.collidepoint(mouse_x, mouse_y):
                        params.global_state["promotion_piece"] = piece
                        print(piece)
                        params.global_state["promot"] = 0  
                        selecting = False
