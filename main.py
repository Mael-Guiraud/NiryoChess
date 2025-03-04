#!/usr/bin/env python3

import chess
import pygame
import chess.engine
import time
import params
import graphisms
import arm_robot
from pyniryo import PoseObject

def configure_stockfish(level):
    """
    Configures Stockfish settings based on the selected skill level.
    
    :param level: Skill level from 0 (easiest) to 20 (hardest)
    """
    level = max(0, min(20, level))  # Ensure level is within valid range

    config = {}

    if level <= 5:
        # Beginner level - Stockfish makes intentional mistakes
        config = {
            "Skill Level": level,  # Lower skill means more blunders
            "UCI_LimitStrength": True,  # Disabling Elo constraint to allow more errors
            "UCI_Elo":1350,  # Between 1400 and 2500
        }
        params.global_state["Move Time"]= 0.1
    elif level <= 15:
        # Intermediate level - More accurate but still makes some mistakes
        config = {
            "Skill Level": level,
            "UCI_LimitStrength": True,
        }
        params.global_state["Move Time"]= 0.5
    else:
        # Advanced level - Stockfish plays at near-max strength
        config = {
            "Skill Level": level,
            "UCI_LimitStrength": False,  # Full power mode
            "UCI_Elo": 3000,  # Grandmaster strength
        }
        params.global_state["Move Time"]=3.0

    params.global_state["stockfish_config"] = config


def play_best_move(board, engine):
    if board.is_checkmate():
        print("Checkmate ! ")
        return

    start_time = time.time()
    move = engine.play(board, chess.engine.Limit(time=params.global_state["Move Time"])).move
    move_san = board.san(move)
    print(f"Stockfish plays : {move_san}")
    if not params.SIMULATED:
        piece = board.piece_at(move.from_square)
        if piece and piece.piece_type == chess.PAWN:
            pick_func = arm_robot.pick_position_pawn_forward
            place_func = arm_robot.place_position_pawn_forward
        else:
            pick_func = arm_robot.pick_position
            place_func = arm_robot.place_position
        pos_from = arm_robot.get_pose_from_square(str(move)[:2])
        pos_to = arm_robot.get_pose_from_square(str(move)[-2:])
        
        if 'x' in move_san:
            piece = board.piece_at(move.to_square)
            if piece and piece.piece_type == chess.PAWN:
                pick_func = arm_robot.pick_position_pawn
                place_func = arm_robot.place_position_pawn
            else:
                pick_func = arm_robot.pick_position
                place_func = arm_robot.place_position
            pick_func(pos_to)
            place_func(params.global_state["dead_pieces"])
            params.global_state["dead_pieces"] = PoseObject(
                params.global_state["dead_pieces"].x+0.04, params.global_state["dead_pieces"].y, params.global_state["dead_pieces"].z,
                params.global_state["dead_pieces"].roll, params.global_state["dead_pieces"].pitch, params.global_state["dead_pieces"].yaw
            )
        if str(move) == "e1g1":
            pick_func(arm_robot.get_pose_from_square("h1"))
            place_func(arm_robot.get_pose_from_square("f1"))
        if str(move) == "e1c1":
            pick_func(arm_robot.get_pose_from_square("a1"))
            place_func(arm_robot.get_pose_from_square("d1"))

        pick_func(pos_from)
        place_func(pos_to)
        params.global_state["robot"].move(params.global_state["wait_white"])
    
    board.push(move)
    end_time = time.time()
    params.global_state["time_white"] -= (end_time - start_time)

    params.global_state["turn"] = chess.BLACK

def handle_human_move(board,x, y):
    
    params.global_state["selected_square"]
    if params.global_state["turn"] == chess.WHITE:
        return
    if board.is_checkmate():
        print("Checkmate ! ")
        return

    col = x // params.SQ_SIZE
    row = y // params.SQ_SIZE

    file = 7 - col
    rank = row
    square_id = chess.square(file, rank)

    if params.global_state["selected_square"] is None:
        piece = board.piece_at(square_id)
        if piece and piece.color == chess.BLACK:
            params.global_state["selected_square"] = square_id

    else:
        move = chess.Move(params.global_state["selected_square"], square_id)
        if move in board.legal_moves:
            start_time = time.time()
            print(f"Human plays : {board.san(move)}")
            board.push(move)
            end_time = time.time()

            params.global_state["time_black"] -= (end_time - start_time)
            params.global_state["selected_square"] = None
            params.global_state["turn"] = chess.WHITE

        else:
            print("Illegal move ! ")
            params.global_state["selected_square"] = None


if __name__ == "__main__":
    if not params.SIMULATED:
        arm_robot.init_position()
    configure_stockfish(graphisms.select_stockfish_level())
    params.global_state["turn"] = chess.WHITE
    params.global_state["time_white"] = params.TIME_WHITE
    params.global_state["time_black"] = params.TIME_BLACK
    graphisms.init_board()
    
    running = True
    params.global_state["selected_square"] = None
    engine = chess.engine.SimpleEngine.popen_uci(params.STOCKFISH_PATH)
    for key, value in params.global_state["stockfish_config"].items():
        engine.configure({key: value})

    clock = pygame.time.Clock()
    board = chess.Board()
    graphisms.draw_board(board, params.global_state["time_white"], params.global_state["time_black"])
    play_best_move(board, engine)


    # Stockfish starts
    last_time = time.time()

    while running:
        current_time = time.time()
        elapsed = current_time - last_time

        if elapsed >= 1:
            if params.global_state["turn"] == chess.WHITE:
                params.global_state["time_white"] = max(0, params.global_state["time_white"] - elapsed)
            else:
                params.global_state["time_black"] = max(0, params.global_state["time_black"] - elapsed)
            last_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                if (not params.TIMERS)  or (params.global_state["time_white"] > 0 and params.global_state["time_black"] > 0):
                    x, y = event.pos
                    if y < params.BOARD_SIZE and x < params.BOARD_SIZE:
                        handle_human_move(board,x, y)
                        if params.global_state["turn"] == chess.WHITE and ( (not params.TIMERS) or params.global_state["time_white"] > 0):
                            play_best_move(board, engine)
        graphisms.draw_board(board, params.global_state["time_white"], params.global_state["time_black"])
        if params.global_state["time_white"] <= 0:
            print("Time is up ! Human (black) wins.")
            running = False
        elif params.global_state["time_black"] <= 0:
            print("Time is up ! Stockfish (white) wins.")
            running = False

        

    engine.quit()
    pygame.quit()