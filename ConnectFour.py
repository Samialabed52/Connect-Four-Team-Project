#########################################################################################
# CSE 550: Software Engineering Fall 2020
# Team 6
# Sami Al-Abed
# Barret Gamber
# Logan Prestigiacomo
# Alex Judd
# Shayne Evans
#########################################################################################

import pygame
pygame.init()
from pygame.locals import *
import sys
import numpy as np
from random import randrange
import time
import random
import math


ROW_COUNT = 6
COLUMN_COUNT = 7
GRIDBOX = 140
RADIUS = int(GRIDBOX / 2 - 10)
width = COLUMN_COUNT * GRIDBOX
height = (ROW_COUNT + 1) * GRIDBOX
PLAYER = 0
AI = 1
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 4


class Game:
    def drop_gamepiece(board, row, col, gamepiece):
        board[row][col] = gamepiece

    def is_valid_location(board, col):
        if (board[0][col] == 0):
            return True

    def winning_move(board, piece):
        # Check horizontal locations for win
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT):
                if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                    c + 3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                    c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and \
                        board[r + 3][c + 3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and \
                        board[r - 3][c + 3] == piece:
                    return True
    
    #Checks for the next open row in the column
    def get_next_open_row(board, col):
        r = 0
        while (r in range(ROW_COUNT - 1) and board[r][col] == 0):  # looks at array from top down
            if (r <= 4 and board[r + 1][col] != 0):
                break
            r += 1
        return r  # returns first row = 0

    #Player vs. Player game
    def player_vs_player(board, history_array1, history_array2, gamepiece1_color, gamepiece2_color, difficulty):
        global game_over
        game_over = False
        global round_count
        round_count = 1
        global confirm_tie
        confirm_tie = 0

        while (game_over != True):
            Board.redraw_pvp_offline()
            pygame.draw.circle(screen, BLACK, (190, 170), RADIUS + 7)
            pygame.draw.circle(screen, gamepiece1_color, (190, 170), RADIUS)
            pygame.draw.circle(screen, BLACK, (1730, 170), RADIUS + 7)
            pygame.draw.circle(screen, gamepiece2_color, (1730, 170), RADIUS)
            Board.draw_board(board, gamepiece1_color, gamepiece2_color)
            pygame.draw.rect(screen, BLACK, connect4_board_divide_line)
            pygame.display.update()
            Player.player_move(board, 1, gamepiece1_color, gamepiece2_color, "Player1", history_array1, history_array2, 1, 0)
            pygame.draw.rect(screen, BLACK, connect4_board_divide_line)
            pygame.display.update()
            round_count += 1
            if (game_over == True):  # Need better idea than global variable...
                break
            Board.draw_board(board, gamepiece1_color, gamepiece2_color)
            pygame.draw.rect(screen, BLACK, connect4_board_divide_line)
            pygame.display.update()
            Player.player_move(board, 2, gamepiece1_color, gamepiece2_color, "Player2", history_array1, history_array2, 1, 0)
            round_count += 1

    # Player vs Computer
    def player_vs_computer(board, history_array1, history_array2, gamepiece1_color, gamepiece2_color, game_type, computer1_difficulty, computer2_difficulty):
        global game_over
        game_over = False
        global round_count
        round_count = 1
        global confirm_tie
        confirm_tie = False

        while (game_over != True):
            pygame.event.pump()
            Board.redraw_pvc()
            pygame.draw.circle(screen, BLACK, (190, 170), RADIUS + 7)
            pygame.draw.circle(screen, gamepiece1_color, (190, 170), RADIUS)
            pygame.draw.circle(screen, BLACK, (1730, 170), RADIUS + 7)
            pygame.draw.circle(screen, gamepiece2_color, (1730, 170), RADIUS)
            Board.draw_board(board, gamepiece1_color, gamepiece2_color)
            pygame.display.update()
            Player.player_move(board, 1, gamepiece1_color, gamepiece2_color, "Player1", history_array1, history_array2, 2, computer1_difficulty)
            round_count += 1
            if (game_over == True):  # Need better idea than global variable...
                break
            pygame.event.pump()
            Board.draw_board(board, gamepiece1_color, gamepiece2_color)
            pygame.display.update()
            Player.computer_move(board, computer1_difficulty, computer2_difficulty, 2, gamepiece1_color,gamepiece2_color, "Computer1", history_array1, history_array2, game_type)
            round_count += 1

    # Computer vs Computer
    def computer_vs_computer(board, history_array1, history_array2, gamepiece1_color, gamepiece2_color, game_type, computer1_difficulty, computer2_difficulty):
        global game_over
        game_over = False
        global round_count
        round_count = 1
        global confirm_tie
        confirm_tie = False

        while (game_over != True):
            pygame.event.pump()
            Board.redraw_cvc()
            pygame.draw.circle(screen, BLACK, (190, 170), RADIUS + 7)
            pygame.draw.circle(screen, gamepiece1_color, (190, 170), RADIUS)
            pygame.draw.circle(screen, BLACK, (1730, 170), RADIUS + 7)
            pygame.draw.circle(screen, gamepiece2_color, (1730, 170), RADIUS)
            Board.draw_board(board, gamepiece1_color, gamepiece2_color)
            pygame.display.update()
            Player.computer_move(board, computer1_difficulty, computer2_difficulty, 1, gamepiece1_color, gamepiece2_color, "Computer1", history_array1, history_array2, game_type)
            Board.draw_board(board, gamepiece1_color, gamepiece2_color)
            pygame.event.pump()
            pygame.display.update()
            round_count += 1
            # if game is over break from the while loop
            if (game_over == True):
                break
            Board.draw_board(board, gamepiece1_color, gamepiece2_color)
            pygame.display.update()
            Player.computer_move(board, computer1_difficulty, computer2_difficulty, 2, gamepiece1_color, gamepiece2_color, "Computer2", history_array1, history_array2, game_type)
            round_count += 1


class Board:
    #Initializes the game board
    def create_board():
        board = np.zeros((6, 7))
        return board
    
    #The end game options are drawn on the screen when a game concludes
    def end_game_screen(board, gamepiece, gamepiece1_color, gamepiece2_color, playerID, history_array1, history_array2, game_type, computer1_difficulty, computer2_difficulty):
        running = True
        while running:
            pygame.display.update()
            Board.redraw_end_game_options()
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if eg_rematch_option.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        history_array_player1 = Board.create_history()
                        history_array_player2 = Board.create_history()
                        board = Board.create_board()
                        if (game_type == 1):
                            Game.player_vs_player(board, history_array_player1, history_array_player2, gamepiece1_color, gamepiece2_color, 0)
                        if (game_type == 2):
                            Game.player_vs_computer(board, history_array_player1, history_array_player2, gamepiece1_color, gamepiece2_color, game_type, computer1_difficulty, 0)
                        if (game_type == 3):
                            Game.computer_vs_computer(board, history_array_player1, history_array_player2, gamepiece1_color, gamepiece2_color, game_type, computer1_difficulty, computer2_difficulty)
                    
                    if eg_replay_option.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        if (game_type == 1):
                            Board.show_game_history(history_array1, history_array2, 1, 2, "Player1", "Player2", gamepiece1_color, gamepiece2_color, game_type)
                        if (game_type == 2):
                            Board.show_game_history(history_array1, history_array2, 1, 2, "Player1", "Computer1", gamepiece1_color, gamepiece2_color, game_type)
                        if (game_type == 3):
                            Board.show_game_history(history_array1, history_array2, 1, 2, "Computer1", "Computer2", gamepiece1_color, gamepiece2_color, game_type)
                    if eg_main_menu_option.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        Board.main_menu()
                    # Quit game
                    if quitButton.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        running = False
                        pygame.quit()
                        # Open pvp window

    #Used to draw the gameboard when a player has made a move, takes ASCII board filled with 0s and 1s and replaces with the gamepiece1_color and gamepiece2_color to represent it in the GUI
    def draw_board(board, gamepiece1_color, gamepiece2_color):
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(screen, MENU_BUTTON_COLOR, (470 + c * GRIDBOX, r * GRIDBOX + GRIDBOX, GRIDBOX, GRIDBOX))
                pygame.draw.rect(screen, MENU_BUTTON_COLOR, (470 + c * GRIDBOX, 0, GRIDBOX, GRIDBOX - 4))

                if board[r][c] == 0:
                    pygame.draw.circle(screen, BLACK, (470 + c * GRIDBOX + GRIDBOX / 2, r * GRIDBOX + GRIDBOX + GRIDBOX / 2), RADIUS + 7)
                    pygame.draw.circle(screen, BROWN, (470 + c * GRIDBOX + GRIDBOX / 2, r * GRIDBOX + GRIDBOX + GRIDBOX / 2), RADIUS)
                elif board[r][c] == 1:
                    pygame.draw.circle(screen, BLACK, (470 + c * GRIDBOX + GRIDBOX / 2, r * GRIDBOX + GRIDBOX + GRIDBOX / 2), RADIUS + 7)
                    pygame.draw.circle(screen, gamepiece1_color, (470 + c * GRIDBOX + GRIDBOX / 2, r * GRIDBOX + GRIDBOX + GRIDBOX / 2), RADIUS)
                else:
                    pygame.draw.circle(screen, BLACK, (470 + c * GRIDBOX + GRIDBOX / 2, r * GRIDBOX + GRIDBOX + GRIDBOX / 2), RADIUS + 7)
                    pygame.draw.circle(screen, gamepiece2_color, (470 + c * GRIDBOX + GRIDBOX / 2, r * GRIDBOX + GRIDBOX + GRIDBOX / 2), RADIUS)

    #Used to intialize the global history arrays which are used to keep track of the moves each competitor has done (the column). This one dimensional array is has 42 spaces (42 total rounds in a tie game)
    #filled with 9s because 9 is an impossible column. So each move will be placed into the array for the very first 9 it sees, replacing the invalid move with a valid one
    def create_history():
        history = np.full(42, 9)
        return history
    
    #Replays the most recently concluded game by showing each move
    def show_game_history(history_array1, history_array2, gamepiece1, gamepiece2, ID1, ID2, gamepiece1_color, gamepiece2_color, game_type):
        pygame.event.get()
        if (game_type == 1):
            Board.redraw_pvp_offline()
        if (game_type == 2):
            Board.redraw_pvc()
        if (game_type == 3):
            Board.redraw_cvc()

        pygame.draw.circle(screen, BLACK, (190, 170), RADIUS + 7)
        pygame.draw.circle(screen, gamepiece1_color, (190, 170), RADIUS)
        pygame.draw.circle(screen, BLACK, (1730, 170), RADIUS + 7)
        pygame.draw.circle(screen, gamepiece2_color, (1730, 170), RADIUS)
        pygame.draw.rect(screen, SUB_MENU_COLOR, connect4_player1_turn_indicator_rect)
        pygame.draw.rect(screen, START_GAME_COLOR, connect4_player2_turn_indicator_rect)
        if (game_type == 1):
            screen.blit(player2_go, (1590 + (280 - player2_go.get_width()) / 2, 300 + ((680 - player2_go.get_height()) / 2)))
        elif (game_type == 2):
            screen.blit(computer1pvc_go, (1590 + (280 - computer1pvc_go.get_width()) / 2, 300 + ((680 - computer1pvc_go.get_height()) / 2)))
        elif (game_type == 3):
            screen.blit(computer2cvc_go, (1590 + (280 - computer2cvc_go.get_width()) / 2, 300 + ((680 - computer2cvc_go.get_height()) / 2)))

        last_game_board = Board.create_board()  # Creates board which will show the history of the previously played game
        # counter and length variables initializion
        i = 0
        j = 0
        length1 = 0
        length2 = 0
        global turn_counter
        turn_counter = 1
        # turn_counter_text = end_game_font.render("Round #: " + str(turn_counter), 1, (0,0,0))
        # pygame.draw.rect(screen, (0,0,0), turn_counter_outline)
        # pygame.draw.rect(screen, (SUB_MENU_COLOR), turn_counter_rect)
        # screen.blit(turn_counter_text,(564 + (796 - turn_counter_text.get_width()) / 2, 390 + ((458 - turn_counter_text.get_height()) / 2) - 200))
        # the size of each array is calculated by iterating through each array until a 9 is reached. The lengths of each array are added and stored into the
        # total_length variable which is used to specify the size of the combined array
        while (history_array1[length1] != 9):
            length1 += 1
        while (history_array2[length2] != 9):
            length2 += 1

        total_length = length1 + length2
        combined_history = np.full(total_length, 0)

        # Since player1 always goes first (could change in future builds) length1 will ALWAYS be either >= length2.
        # Using this fact two if statements are used to iterate through the two history arrays which have the columns the players selected
        # These column numbers are stored in the combined array in the order player1 move -> player2 move -> player1 move -> player 2 move ..... ->
        # Until j equals length1 (length1 > length2) or until j is not less than length1 (length1 == length2)
        if (length1 > length2):
            while (j != length1):
                combined_history[i] = history_array1[j]
                if (i + 1 != total_length):
                    combined_history[i + 1] = history_array2[j]
                i += 2
                j += 1
        elif (length1 == length2):
            while (j < length1):
                combined_history[i] = history_array1[j]
                combined_history[i + 1] = history_array2[j]
                i += 2
                j += 1

        # After the combined_history array has been created, the first move is automatically stored at the first index [0] of the last_game_board and printed for the user
        # The user than can choose to see the next move or exit to menu. If the user choose to continue then they will enter a while loop that executes until they choose
        # to return to main menu or the review ends.
        turn_counter = 0
        col = combined_history[0]
        turn_counter += 1
        row = Game.get_next_open_row(last_game_board, col)
        gamepiece_sound = random.randint(1,100)
        if(gamepiece_sound % 2 == 0):
            pygame.mixer.music.load('gamepiece_sound1.wav')
            pygame.mixer.music.play(0)
        else:
            pygame.mixer.music.load('gamepiece_sound2.wav')
            pygame.mixer.music.play(0)
        Game.drop_gamepiece(last_game_board, row, col, gamepiece1)
        Board.draw_board(last_game_board, gamepiece1_color, gamepiece2_color)

        #x variable is used to wait for user input in the while loop
        x = False
        while (x != True):
            pygame.display.update()
            Board.redraw_replay_game()
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if replay_continue.isOver(pos):
                        k = 1
                        x = True
                    if replay_main_menu_option.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        Board.main_menu()
                        x = True

        # While loop which starts at k=1 since by this point the first move has been added to the board. It will increment until k == total_length which signifies that each move
        # has been reviewed.
        # variable turn_counter is used to alternate which text should be displayed on the GUI
        while (k < total_length):
            pygame.display.update()
            Board.redraw_replay_game()
            col = combined_history[k]
            turn_counter += 1
            row = Game.get_next_open_row(last_game_board, col)

            # Player 1's/Computer 1 (cvc) turn
            if (turn_counter % 2 == 0):
                pygame.draw.rect(screen, SUB_MENU_COLOR, connect4_player2_turn_indicator_rect)
                pygame.draw.rect(screen, START_GAME_COLOR, connect4_player1_turn_indicator_rect)
                if (game_type == 1):
                    screen.blit(player1_go, (50 + (280 - player1_go.get_width()) / 2, 300 + ((680 - player1_go.get_height()) / 2)))
                elif (game_type == 2):
                    screen.blit(player1_go, (50 + (280 - player1_go.get_width()) / 2, 300 + ((680 - player1_go.get_height()) / 2)))
                elif (game_type == 3):
                    screen.blit(computer1cvc_go, (50 + (280 - computer1cvc_go.get_width()) / 2, 300 + ((680 - computer1cvc_go.get_height()) / 2)))
                
                gamepiece_sound = random.randint(1,100)
                if(gamepiece_sound % 2 == 0):
                    pygame.mixer.music.load('gamepiece_sound1.wav')
                    pygame.mixer.music.play(0)
                else:
                    pygame.mixer.music.load('gamepiece_sound2.wav')
                    pygame.mixer.music.play(0)
                Game.drop_gamepiece(last_game_board, row, col, gamepiece2)

            # Player 2's/Computer 2 turn
            else:
                pygame.draw.rect(screen, SUB_MENU_COLOR, connect4_player1_turn_indicator_rect)
                pygame.draw.rect(screen, START_GAME_COLOR, connect4_player2_turn_indicator_rect)
                if (game_type == 1):
                    screen.blit(player2_go, (1590 + (280 - player2_go.get_width()) / 2, 300 + ((680 - player2_go.get_height()) / 2)))
                elif (game_type == 2):
                    screen.blit(computer1pvc_go, (1590 + (280 - computer1pvc_go.get_width()) / 2, 300 + ((680 - computer1pvc_go.get_height()) / 2)))
                elif (game_type == 3):
                    screen.blit(computer2cvc_go, (1590 + (280 - computer2cvc_go.get_width()) / 2, 300 + ((680 - computer2cvc_go.get_height()) / 2)))
              
                gamepiece_sound = random.randint(1,100)
                if(gamepiece_sound % 2 == 0):
                    pygame.mixer.music.load('gamepiece_sound1.wav')
                    pygame.mixer.music.play(0)
                else:
                    pygame.mixer.music.load('gamepiece_sound2.wav')
                    pygame.mixer.music.play(0)
                Game.drop_gamepiece(last_game_board, row, col, gamepiece1)

            if (k == total_length - 1):
                break
            Board.draw_board(last_game_board, gamepiece1_color, gamepiece2_color)
           
           #x variable is used to wait for user input in the while loop
            x = False
            while (x != True):
                pygame.display.update()
                for event in pygame.event.get():
                    pos = pygame.mouse.get_pos()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if replay_continue.isOver(pos):
                            k += 1
                            x = True
                        if replay_main_menu_option.isOver(pos):
                            pygame.mixer.music.load('Button.wav')
                            pygame.mixer.music.play(0)
                            Board.main_menu()
                            x = True

        global confirm_tie
        if (round_count == 42 and Game.winning_move(last_game_board, gamepiece1) != True and Game.winning_move(last_game_board, gamepiece2) != True):
            confirm_tie = 1

        # Player 2 / Computer 2 WINS
        if (turn_counter % 2 == 0 and confirm_tie != 1):

            # if pvp
            if (game_type == 1):
                Board.redraw_pvp_offline()
                pygame.draw.circle(screen, BLACK, (190, 170), RADIUS + 7)
                pygame.draw.circle(screen, gamepiece1_color, (190, 170), RADIUS)
                pygame.draw.circle(screen, BLACK, (1730, 170), RADIUS + 7)
                pygame.draw.circle(screen, gamepiece2_color, (1730, 170), RADIUS)
                Board.draw_board(last_game_board, gamepiece1_color, gamepiece2_color)
                pygame.draw.rect(screen, GOLD, connect4_player2_turn_indicator_rect)
                pygame.draw.rect(screen, BROWN, connect4_player1_turn_indicator_rect)
                screen.blit(player1_loser_text, (50 + (280 - player1_loser_text.get_width()) / 2, 300 + ((680 - player1_loser_text.get_height()) / 2)))
                screen.blit(player2_winner_text, (1590 + (280 - player2_winner_text.get_width()) / 2,300 + ((680 - player2_winner_text.get_height()) / 2)))

            # if pvc
            if (game_type == 2):
                Board.redraw_pvc()
                pygame.draw.circle(screen, BLACK, (190, 170), RADIUS + 7)
                pygame.draw.circle(screen, gamepiece1_color, (190, 170), RADIUS)
                pygame.draw.circle(screen, BLACK, (1730, 170), RADIUS + 7)
                pygame.draw.circle(screen, gamepiece2_color, (1730, 170), RADIUS)
                Board.draw_board(last_game_board, gamepiece1_color, gamepiece2_color)
                pygame.draw.rect(screen, GOLD, connect4_player2_turn_indicator_rect)
                pygame.draw.rect(screen, BROWN, connect4_player1_turn_indicator_rect)
                screen.blit(player1_loser_text, (50 + (280 - player1_loser_text.get_width()) / 2, 300 + ((680 - player1_loser_text.get_height()) / 2)))
                screen.blit(computer1pvc_winner_text, (1590 + (280 - computer1pvc_winner_text.get_width()) / 2, 300 + ((680 - computer1pvc_winner_text.get_height()) / 2)))

            # if cvc
            if (game_type == 3):
                Board.redraw_cvc()
                pygame.draw.circle(screen, BLACK, (190, 170), RADIUS + 7)
                pygame.draw.circle(screen, gamepiece1_color, (190, 170), RADIUS)
                pygame.draw.circle(screen, BLACK, (1730, 170), RADIUS + 7)
                pygame.draw.circle(screen, gamepiece2_color, (1730, 170), RADIUS)
                Board.draw_board(last_game_board, gamepiece1_color, gamepiece2_color)
                pygame.draw.rect(screen, GOLD, connect4_player2_turn_indicator_rect)
                pygame.draw.rect(screen, BROWN, connect4_player1_turn_indicator_rect)
                screen.blit(computer1cvc_loser_text, (50 + (280 - computer1cvc_loser_text.get_width()) / 2, 300 + ((680 - computer1cvc_loser_text.get_height()) / 2)))
                screen.blit(computer2cvc_winner_text, (1590 + (280 - computer2cvc_winner_text.get_width()) / 2, 300 + ((680 - computer2cvc_winner_text.get_height()) / 2)))

        # Player 1/Computer 1 WINS
        elif (turn_counter % 2 != 0 and confirm_tie != 1):

            # if pvp
            if (game_type == 1):
                Board.redraw_pvp_offline()
                pygame.draw.circle(screen, BLACK, (190, 170), RADIUS + 7)
                pygame.draw.circle(screen, gamepiece1_color, (190, 170), RADIUS)
                pygame.draw.circle(screen, BLACK, (1730, 170), RADIUS + 7)
                pygame.draw.circle(screen, gamepiece2_color, (1730, 170), RADIUS)
                Board.draw_board(last_game_board, gamepiece1_color, gamepiece2_color)
                pygame.draw.rect(screen, BROWN, connect4_player2_turn_indicator_rect)
                pygame.draw.rect(screen, GOLD, connect4_player1_turn_indicator_rect)
                screen.blit(player1_winner_text, (50 + (280 - player1_winner_text.get_width()) / 2, 300 + ((680 - player1_winner_text.get_height()) / 2)))
                screen.blit(player2_loser_text, (1590 + (280 - player2_loser_text.get_width()) / 2, 300 + ((680 - player2_loser_text.get_height()) / 2)))

            # if pvc
            elif (game_type == 2):
                Board.redraw_pvc()
                pygame.draw.circle(screen, BLACK, (190, 170), RADIUS + 7)
                pygame.draw.circle(screen, gamepiece1_color, (190, 170), RADIUS)
                pygame.draw.circle(screen, BLACK, (1730, 170), RADIUS + 7)
                pygame.draw.circle(screen, gamepiece2_color, (1730, 170), RADIUS)
                Board.draw_board(last_game_board, gamepiece1_color, gamepiece2_color)
                pygame.draw.rect(screen, BROWN, connect4_player2_turn_indicator_rect)
                pygame.draw.rect(screen, GOLD, connect4_player1_turn_indicator_rect)
                screen.blit(player1_winner_text, (50 + (280 - player1_winner_text.get_width()) / 2, 300 + ((680 - player1_winner_text.get_height()) / 2)))
                screen.blit(computer1pvc_loser_text, (1590 + (280 - computer1pvc_loser_text.get_width()) / 2, 300 + ((680 - computer1pvc_loser_text.get_height()) / 2)))

            # if cvc
            elif (game_type == 3):
                Board.redraw_cvc()
                pygame.draw.circle(screen, BLACK, (190, 170), RADIUS + 7)
                pygame.draw.circle(screen, gamepiece1_color, (190, 170), RADIUS)
                pygame.draw.circle(screen, BLACK, (1730, 170), RADIUS + 7)
                pygame.draw.circle(screen, gamepiece2_color, (1730, 170), RADIUS)
                Board.draw_board(last_game_board, gamepiece1_color, gamepiece2_color)
                pygame.draw.rect(screen, BROWN, connect4_player2_turn_indicator_rect)
                pygame.draw.rect(screen, GOLD, connect4_player1_turn_indicator_rect)
                screen.blit(computer1cvc_winner_text, (50 + (280 - computer1cvc_winner_text.get_width()) / 2, 300 + ((680 - computer1cvc_winner_text.get_height()) / 2)))
                screen.blit(computer2cvc_loser_text, (1590 + (280 - computer2cvc_loser_text.get_width()) / 2, 300 + ((680 - computer2cvc_loser_text.get_height()) / 2)))

        # If game is tied
        elif (confirm_tie == 1):
            if (game_type == 1):
                Board.redraw_pvp_offline()
            elif (game_type == 2):
                Board.redraw_pvc()
            elif (game_type == 3):
                Board.redraw_cvc()
            pygame.draw.circle(screen, BLACK, (190, 170), RADIUS + 7)
            pygame.draw.circle(screen, gamepiece1_color, (190, 170), RADIUS)
            pygame.draw.circle(screen, BLACK, (1730, 170), RADIUS + 7)
            pygame.draw.circle(screen, gamepiece2_color, (1730, 170), RADIUS)
            Board.draw_board(last_game_board, gamepiece1_color, gamepiece2_color)
            pygame.draw.rect(screen, WHITE, connect4_player1_turn_indicator_rect)
            pygame.draw.rect(screen, WHITE, connect4_player2_turn_indicator_rect)
            screen.blit(tie_text, (50 + (280 - tie_text.get_width()) / 2, 300 + ((680 - tie_text.get_height()) / 2)))
            screen.blit(tie_text, (1590 + (280 - tie_text.get_width()) / 2, 300 + ((680 - tie_text.get_height()) / 2)))
            pygame.display.update()
            confirm_tie = 0
        pygame.display.update()

    #Draws the main menu to screen
    def redraw_MainMenu():
        screen.blit(main_menu_img, (0, 0))
        pvpButton.draw(screen, (0, 0, 0))
        pvcButton.draw(screen, (0, 0, 0))
        cvcButton.draw(screen, (0, 0, 0))
        quitButton.draw(screen, (0, 0, 0))

    #Draws the player vs computer menu to the screen
    def redraw_pvc_menu():
        screen.blit(sub_menu_img, (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), sub_menu_outline)
        pygame.draw.rect(screen, (159, 197, 232), sub_menu_rect)
        easyButton_pvc.draw(screen, (0, 0, 0))
        mediumButton_pvc.draw(screen, (0, 0, 0))
        hardButton_pvc.draw(screen, (0, 0, 0))
        screen.blit(pvcText, (window_w / 2 - 190, window_h / 2 - 100))
        quitButton.draw(screen, (0, 0, 0))
        backButton.draw(screen, (0, 0, 0))

    #Draws the computer vs computer menu to the screen
    def redraw_cvc_menu():
        screen.blit(sub_menu_img, (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), sub_menu_outline)
        pygame.draw.rect(screen, (159, 197, 232), sub_menu_rect)
        easyButton1_cvc.draw(screen, (0, 0, 0))
        mediumButton1_cvc.draw(screen, (0, 0, 0))
        hardButton1_cvc.draw(screen, (0, 0, 0))
        easyButton2_cvc.draw(screen, (0, 0, 0))
        mediumButton2_cvc.draw(screen, (0, 0, 0))
        hardButton2_cvc.draw(screen, (0, 0, 0))
        screen.blit(cvc_text1, (564 + (796 - cvc_text1.get_width()) / 2, 390 + ((458 - cvc_text1.get_height()) / 2) - 200))
        screen.blit(cvc_text2, (614 + (300 - cvc_text2.get_width()) / 2, 490 + (-120 + cvc_text2.get_height()) / 2))
        screen.blit(cvc_text3, (1010 + (300 - cvc_text3.get_width()) / 2, 490 + (-120 + cvc_text3.get_height()) / 2))
        quitButton.draw(screen, (0, 0, 0))
        backButton.draw(screen, (0, 0, 0))

    #Draws the player vs player offline menu to the screen
    def redraw_pvp_offline_menu():
        screen.blit(sub_menu_img, (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), sub_menu_outline)
        pygame.draw.rect(screen, SUB_MENU_COLOR, sub_menu_rect)
        quitButton.draw(screen, (0, 0, 0))
        backButton.draw(screen, (0, 0, 0))
        red_button1.draw(screen, (0, 0, 0))
        green_button1.draw(screen, (0, 0, 0))
        blue_button1.draw(screen, (0, 0, 0))
        yellow_button1.draw(screen, (0, 0, 0))
        orange_button1.draw(screen, (0, 0, 0))
        purple_button1.draw(screen, (0, 0, 0))
        cyan_button1.draw(screen, (0, 0, 0))
        pink_button1.draw(screen, (0, 0, 0))
        white_button1.draw(screen, (0, 0, 0))
        red_button2.draw(screen, (0, 0, 0))
        green_button2.draw(screen, (0, 0, 0))
        blue_button2.draw(screen, (0, 0, 0))
        yellow_button2.draw(screen, (0, 0, 0))
        orange_button2.draw(screen, (0, 0, 0))
        purple_button2.draw(screen, (0, 0, 0))
        cyan_button2.draw(screen, (0, 0, 0))
        pink_button2.draw(screen, (0, 0, 0))
        white_button2.draw(screen, (0, 0, 0))
        screen.blit(pvp_offline_text1, (564 + (796 - pvp_offline_text1.get_width()) / 2, 390 + ((458 - pvp_offline_text1.get_height()) / 2) - 200))
        screen.blit(player1_gamepiece_color, (614 + (300 - player1_gamepiece_color.get_width()) / 2, 490 + (-120 + player1_gamepiece_color.get_height()) / 2))
        screen.blit(player2_gamepiece_color, (1010 + (300 - player2_gamepiece_color.get_width()) / 2,490 + (-120 + player2_gamepiece_color.get_height()) / 2))
        pygame.draw.rect(screen, BLACK, sub_menu_divide_line1)
        pygame.draw.rect(screen, BLACK, sub_menu_divide_line2)

    #draws the player vs player offline game to the screen
    def redraw_pvp_offline():
        screen.blit(sub_menu_img, (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), connect4_player1_turn_indicator_rect_outline)
        pygame.draw.rect(screen, SUB_MENU_COLOR, connect4_player1_turn_indicator_rect)
        pygame.draw.rect(screen, BLACK, connect4_board_background_outline)
        pygame.draw.rect(screen, BLACK, connect4_player1_nameplate_outline)
        pygame.draw.rect(screen, SUB_MENU_COLOR, connect4_player1_nameplate)
        pygame.draw.rect(screen, BLACK, connect4_player2_nameplate_outline)
        pygame.draw.rect(screen, SUB_MENU_COLOR, connect4_player2_nameplate)
        pygame.draw.rect(screen, BLACK, connect4_player2_turn_indicator_rect_outline)
        pygame.draw.rect(screen, SUB_MENU_COLOR, connect4_player2_turn_indicator_rect)
        screen.blit(player1_name, (50 + (280 - player1_name.get_width()) / 2, 60 + ((180 - player1_name.get_height()) / 2) - 70))
        screen.blit(player2_name, (1590 + (280 - player2_name.get_width()) / 2, 60 + ((180 - player2_name.get_height()) / 2) - 70))

    #draws the player vs computer game to the screen
    def redraw_pvc():
        screen.blit(sub_menu_img, (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), connect4_player1_turn_indicator_rect_outline)
        pygame.draw.rect(screen, SUB_MENU_COLOR, connect4_player1_turn_indicator_rect)
        pygame.draw.rect(screen, BLACK, connect4_board_background_outline)
        pygame.draw.rect(screen, BLACK, connect4_player1_nameplate_outline)
        pygame.draw.rect(screen, SUB_MENU_COLOR, connect4_player1_nameplate)
        pygame.draw.rect(screen, BLACK, connect4_player2_nameplate_outline)
        pygame.draw.rect(screen, SUB_MENU_COLOR, connect4_player2_nameplate)
        pygame.draw.rect(screen, BLACK, connect4_player2_turn_indicator_rect_outline)
        pygame.draw.rect(screen, SUB_MENU_COLOR, connect4_player2_turn_indicator_rect)
        screen.blit(player1_name, (50 + (280 - player1_name.get_width()) / 2, 60 + ((180 - player1_name.get_height()) / 2) - 70))
        screen.blit(computer1_name, (1590 + (280 - computer1_name.get_width()) / 2, 60 + ((180 - computer1_name.get_height()) / 2) - 70))

    #draws the computer vs computer game to the screen
    def redraw_cvc():
        screen.blit(sub_menu_img, (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), connect4_player1_turn_indicator_rect_outline)
        pygame.draw.rect(screen, SUB_MENU_COLOR, connect4_player1_turn_indicator_rect)
        pygame.draw.rect(screen, BLACK, connect4_board_background_outline)
        pygame.draw.rect(screen, BLACK, connect4_player1_nameplate_outline)
        pygame.draw.rect(screen, SUB_MENU_COLOR, connect4_player1_nameplate)
        pygame.draw.rect(screen, BLACK, connect4_player2_nameplate_outline)
        pygame.draw.rect(screen, SUB_MENU_COLOR, connect4_player2_nameplate)
        pygame.draw.rect(screen, BLACK, connect4_player2_turn_indicator_rect_outline)
        pygame.draw.rect(screen, SUB_MENU_COLOR, connect4_player2_turn_indicator_rect)
        screen.blit(computer1_name, (50 + (280 - computer1_name.get_width()) / 2, 60 + ((180 - computer1_name.get_height()) / 2) - 70))
        screen.blit(computer2_name, (1590 + (280 - computer2_name.get_width()) / 2, 60 + ((180 - computer2_name.get_height()) / 2) - 70))

    #draws the end game options to the screen
    def redraw_end_game_options():
        eg_rematch_option.draw(screen, (0, 0, 0))
        eg_replay_option.draw(screen, (0, 0, 0))
        eg_main_menu_option.draw(screen, (0, 0, 0))

    #draws the replay game options to the screen
    def redraw_replay_game():
        replay_continue.draw(screen, (0, 0, 0))
        replay_main_menu_option.draw(screen, (0, 0, 0))

    #The main menu, what the user will first see when the program launches. Used to navigate to the Player vs. Player, Player vs. Computer, and Computer vs. Computer submenus.
    def main_menu():
        running = True
        while running:
            pygame.display.update()
            Board.redraw_MainMenu()
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pvpButton.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        Board.pvp_offline_menu()
                    if pvcButton.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        Board.pvc_menu()
                    if cvcButton.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        Board.cvc_menu()
                    # Quit game
                    if quitButton.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        running = False
                        pygame.quit()
                        # Open pvp windows

    #Player vs. Player menu. The players will have to choose a different color for their gamepieces then the start game button will appear where they can click it then play against eachother
    def pvp_offline_menu():
        green_selected, red_selected, blue_selected, yellow_selected, orange_selected, purple_selected, cyan_selected, pink_selected, white_selected = 0, 0, 0, 0, 0, 0, 0, 0, 0
        gamepiece1_color = SUB_MENU_COLOR
        gamepiece2_color = SUB_MENU_COLOR

        running = True
        while running:
            gamepiece1_outline = pygame.draw.circle(screen, BLACK, ((614 + (300 - player1_gamepiece_color.get_width()) / 2) + 50, 490 + (50 + player1_gamepiece_color.get_height()) / 2), 40)
            gamepiece1 = pygame.draw.circle(screen, gamepiece1_color, ((614 + (300 - player1_gamepiece_color.get_width()) / 2) + 50, 490 + (50 + player1_gamepiece_color.get_height()) / 2), 35)
            gamepiece2_outline = pygame.draw.circle(screen, BLACK, ((1010 + (300 - player2_gamepiece_color.get_width()) / 2) + 50, 490 + (50 + player2_gamepiece_color.get_height()) / 2), 40)
            gamepiece2 = pygame.draw.circle(screen, gamepiece2_color, ((1010 + (300 - player2_gamepiece_color.get_width()) / 2) + 50, 490 + (50 + player2_gamepiece_color.get_height()) / 2), 35)

            pygame.display.update()
            Board.redraw_pvp_offline_menu()

            if (gamepiece1_color != SUB_MENU_COLOR and gamepiece2_color != SUB_MENU_COLOR and gamepiece1_color != gamepiece2_color):
                pygame.draw.rect(screen, BLACK, start_rect_outline)
                pygame.draw.rect(screen, START_GAME_COLOR, start_rect)
                screen.blit(start_game_text, (
                610 + (704 - start_game_text.get_width()) / 2, 890 + (170 - start_game_text.get_height()) / 2))

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if green_button1.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        gamepiece1_color = GREEN

                    if red_button1.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        gamepiece1_color = RED

                    if blue_button1.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        gamepiece1_color = BLUE

                    if yellow_button1.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        gamepiece1_color = YELLOW

                    if orange_button1.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        gamepiece1_color = ORANGE

                    if purple_button1.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        gamepiece1_color = PURPLE

                    if cyan_button1.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        gamepiece1_color = CYAN

                    if pink_button1.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        gamepiece1_color = PINK

                    if white_button1.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        gamepiece1_color = WHITE

                    if green_button2.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        gamepiece2_color = GREEN

                    if red_button2.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        gamepiece2_color = RED

                    if blue_button2.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        gamepiece2_color = BLUE

                    if yellow_button2.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        gamepiece2_color = YELLOW

                    if orange_button2.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        gamepiece2_color = ORANGE

                    if purple_button2.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        gamepiece2_color = PURPLE

                    if cyan_button2.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        gamepiece2_color = CYAN

                    if pink_button2.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        gamepiece2_color = PINK

                    if white_button2.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        gamepiece2_color = WHITE

                    if (gamepiece1_color != SUB_MENU_COLOR and gamepiece2_color != SUB_MENU_COLOR and gamepiece1_color != gamepiece2_color):
                        if (start_rect.collidepoint(pos)):
                            pygame.mixer.music.load('Button.wav')
                            pygame.mixer.music.play(0)
                            history_array_player1 = Board.create_history()
                            history_array_player2 = Board.create_history()
                            board = Board.create_board()
                            Game.player_vs_player(board, history_array_player1, history_array_player2, gamepiece1_color, gamepiece2_color, 0)

                    if backButton.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        Board.main_menu()
                    if quitButton.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        running = False
                        pygame.quit()

    #Player vs. Computer menu. Player must select difficulty of the computer then the start game button appears. The player clicks it then the game will start versus the user selected difficulty computer
    def pvc_menu():
        computer_difficulty = 0
        easyButton_pvc.color, mediumButton_pvc.color, hardButton_pvc.color = MENU_BUTTON_COLOR, MENU_BUTTON_COLOR, MENU_BUTTON_COLOR

        running = True
        while running:
            pygame.display.update()
            Board.redraw_pvc_menu()

            if (computer_difficulty == 2 or computer_difficulty == 4 or computer_difficulty == 5):
                pygame.draw.rect(screen, BLACK, start_rect_outline)
                pygame.draw.rect(screen, START_GAME_COLOR, start_rect)
                screen.blit(start_game_text, (610 + (704 - start_game_text.get_width()) / 2, 890 + (170 - start_game_text.get_height()) / 2))

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if easyButton_pvc.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        easyButton_pvc.color, mediumButton_pvc.color, hardButton_pvc.color = GREEN, MENU_BUTTON_COLOR, MENU_BUTTON_COLOR
                        computer_difficulty = 2
                        pass
                    if mediumButton_pvc.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        easyButton_pvc.color, mediumButton_pvc.color, hardButton_pvc.color = MENU_BUTTON_COLOR, YELLOW, MENU_BUTTON_COLOR
                        computer_difficulty = 4
                        pass
                    if hardButton_pvc.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        easyButton_pvc.color, mediumButton_pvc.color, hardButton_pvc.color = MENU_BUTTON_COLOR, MENU_BUTTON_COLOR, RED
                        computer_difficulty = 5
                        pass

                    if backButton.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        Board.main_menu()

                    if (computer_difficulty == 2 or computer_difficulty == 4 or computer_difficulty == 5):
                        if (start_rect.collidepoint(pos)):
                            pygame.mixer.music.load('Button.wav')
                            pygame.mixer.music.play(0)
                            history_array_player1 = Board.create_history()
                            history_array_player2 = Board.create_history()
                            board = Board.create_board()
                            Game.player_vs_computer(board, history_array_player1, history_array_player2, CYAN, YELLOW, 2, computer_difficulty, 0)

                    if quitButton.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        running = False
                        pygame.quit()

    #Computer vs. Computer menu. The user selects difficulty for both computers then the start game button appears. They can click it to spectate the game between the two computers.
    def cvc_menu():
        computer1_difficulty, computer2_difficulty = 0, 0
        easyButton1_cvc.color, mediumButton1_cvc.color, hardButton1_cvc.color = MENU_BUTTON_COLOR, MENU_BUTTON_COLOR, MENU_BUTTON_COLOR
        easyButton2_cvc.color, mediumButton2_cvc.color, hardButton2_cvc.color = MENU_BUTTON_COLOR, MENU_BUTTON_COLOR, MENU_BUTTON_COLOR

        running = True
        while running:
            pygame.display.update()
            Board.redraw_cvc_menu()

            if ((computer1_difficulty == 2 or computer1_difficulty == 4 or computer1_difficulty == 5) and (computer2_difficulty == 2 or computer2_difficulty == 4 or computer2_difficulty == 5)):
                pygame.draw.rect(screen, BLACK, start_rect_outline)
                pygame.draw.rect(screen, START_GAME_COLOR, start_rect)
                screen.blit(start_game_text, (610 + (704 - start_game_text.get_width()) / 2, 890 + (170 - start_game_text.get_height()) / 2))

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if easyButton1_cvc.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        easyButton1_cvc.color, mediumButton1_cvc.color, hardButton1_cvc.color = GREEN, MENU_BUTTON_COLOR, MENU_BUTTON_COLOR
                        computer1_difficulty = 2

                    if mediumButton1_cvc.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        easyButton1_cvc.color, mediumButton1_cvc.color, hardButton1_cvc.color = MENU_BUTTON_COLOR, YELLOW, MENU_BUTTON_COLOR
                        computer1_difficulty = 4

                    if hardButton1_cvc.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        easyButton1_cvc.color, mediumButton1_cvc.color, hardButton1_cvc.color = MENU_BUTTON_COLOR, MENU_BUTTON_COLOR, RED
                        computer1_difficulty = 5

                    if easyButton2_cvc.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        easyButton2_cvc.color, mediumButton2_cvc.color, hardButton2_cvc.color = GREEN, MENU_BUTTON_COLOR, MENU_BUTTON_COLOR
                        computer2_difficulty = 2

                    if mediumButton2_cvc.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        easyButton2_cvc.color, mediumButton2_cvc.color, hardButton2_cvc.color = MENU_BUTTON_COLOR, YELLOW, MENU_BUTTON_COLOR
                        computer2_difficulty = 4

                    if hardButton2_cvc.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        easyButton2_cvc.color, mediumButton2_cvc.color, hardButton2_cvc.color = MENU_BUTTON_COLOR, MENU_BUTTON_COLOR, RED
                        computer2_difficulty = 5

                    if ((computer1_difficulty == 2 or computer1_difficulty == 4 or computer1_difficulty == 5) and (computer2_difficulty == 2 or computer2_difficulty == 4 or computer2_difficulty == 5)):
                        if (start_rect.collidepoint(pos)):
                            pygame.mixer.music.load('Button.wav')
                            pygame.mixer.music.play(0)
                            history_array1 = Board.create_history()
                            history_array2 = Board.create_history()
                            board = Board.create_board()
                            Game.computer_vs_computer(board, history_array1, history_array2, PINK, GREEN, 3, computer1_difficulty, computer2_difficulty)

                    if backButton.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        Board.main_menu()
                    if quitButton.isOver(pos):
                        pygame.mixer.music.load('Button.wav')
                        pygame.mixer.music.play(0)
                        running = False
                        pygame.quit()
                            
    #button subclass uses for GUI buttons
    class button():
        def __init__(self, color, x, y, width, height, text=''):
            self.color = color
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.text = text

        def draw(self, win, outline=None):
            # Call this method to draw the button on the screen
            if outline:
                pygame.draw.rect(win, outline, (self.x - 4, self.y - 4, self.width + 8, self.height + 7), 0)

            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

            if self.text != '':
                font = pygame.font.SysFont('timesnewroman', 30)
                text = font.render(self.text, 1, (0, 0, 0))
                # Centers the text in the button
                win.blit(text, (
                    self.x + (self.width / 2 - text.get_width() / 2),
                    self.y + (self.height / 2 - text.get_height() / 2)))

        def isOver(self, pos):
            # Pos is the mouse position or a tuple of (x,y) coordinates
            if pos[0] > self.x and pos[0] < self.x + self.width:
                if pos[1] > self.y and pos[1] < self.y + self.height:
                    return True


class Player:
    #Player move used when the player makes a move
    def player_move(board, gamepiece, gamepiece1_color, gamepiece2_color, playerID, history_array1, history_array2, game_type, computer_difficulty):
        waiter = 0
        while (waiter == 0):
            for event in pygame.event.get():
                pygame.display.update()
                if event.type == pygame.QUIT:
                    sys.exit()
                posx = pygame.mouse.get_pos()[0]
                #Draws an X above a filled column when users cursor is above it (invalid move)
                if (posx >= 535 and posx <= (470+ (979/7)) and board[0][0] != 0) \
                        or (posx >= (470+ (979/7)) and posx <= (470+ ((979/7)*2)) and board[0][1] != 0) \
                        or (posx >= (470+ (979/7)*2) and posx <= (470+ ((979/7)*3)) and board[0][2] != 0) \
                        or (posx >= (470+ (979/7)*3) and posx <= (470+ ((979/7)*4)) and board[0][3] != 0) \
                        or (posx >= (470+ (979/7)*4) and posx <= (470+ ((979/7)*5)) and board[0][4] != 0) \
                        or (posx >= (470+ (979/7)*5) and posx <= (470+ ((979/7)*6)) and board[0][5] != 0) \
                        or (posx >= (470+ (979/7)*6) and posx <= (1385) and board[0][6] != 0):
                    pygame.draw.rect(screen, MENU_BUTTON_COLOR, (470, 0, width, GRIDBOX))
                    pygame.draw.rect(screen, BLACK, connect4_board_divide_line)
                    pygame.draw.line(screen, RED, ((posx-60), int(GRIDBOX / 2) + 45), ((posx+60), int(GRIDBOX / 2) - 50), 30)
                    pygame.draw.line(screen, RED, (((posx-60), int(GRIDBOX / 2) - 50)), ((posx+60), int(GRIDBOX / 2) + 45), 30)
                    pygame.draw.rect(screen, BLACK, connect4_board_divide_line)

                    #Used so that the correct turn indication can be displayed to the GUI while also displaying an X. Without this the turn indicator would only appear after going to a valid column
                    if (playerID == "Player1"):
                        pygame.draw.rect(screen, SUB_MENU_COLOR, connect4_player2_turn_indicator_rect)
                        pygame.draw.rect(screen, START_GAME_COLOR, connect4_player1_turn_indicator_rect)
                        pygame.draw.rect(screen, BLACK, connect4_board_divide_line)
                        screen.blit(player1_go, (50 + (280 - player1_go.get_width()) / 2, 300 + ((680 - player1_go.get_height()) / 2)))

                    else:
                        pygame.draw.rect(screen, SUB_MENU_COLOR, connect4_player1_turn_indicator_rect)
                        pygame.draw.rect(screen, START_GAME_COLOR, connect4_player2_turn_indicator_rect)
                        pygame.draw.rect(screen, BLACK, connect4_board_divide_line)
                        screen.blit(player2_go, (1590 + (280 - player2_go.get_width()) / 2, 300 + ((680 - player2_go.get_height()) / 2)))

                    pygame.display.update()
                
                elif (posx >= 535 and posx <= 1385):
                    pygame.draw.rect(screen, MENU_BUTTON_COLOR, (470, 0, width, GRIDBOX))
                    pygame.draw.rect(screen, BLACK, connect4_board_divide_line)
                    
                    if (playerID == "Player1"):
                        pygame.draw.circle(screen, BLACK, (posx, int(GRIDBOX / 2)), RADIUS + 7)
                        pygame.draw.circle(screen, gamepiece1_color, (posx, int(GRIDBOX / 2)), RADIUS)
                        pygame.draw.rect(screen, SUB_MENU_COLOR, connect4_player2_turn_indicator_rect)
                        pygame.draw.rect(screen, START_GAME_COLOR, connect4_player1_turn_indicator_rect)
                        pygame.draw.rect(screen, BLACK, connect4_board_divide_line)
                        screen.blit(player1_go, (50 + (280 - player1_go.get_width()) / 2, 300 + ((680 - player1_go.get_height()) / 2)))
                    
                    else:
                        pygame.draw.circle(screen, BLACK, (posx, int(GRIDBOX / 2)), RADIUS + 7)
                        pygame.draw.circle(screen, gamepiece2_color, (posx, int(GRIDBOX / 2)), RADIUS)
                        pygame.draw.rect(screen, SUB_MENU_COLOR, connect4_player1_turn_indicator_rect)
                        pygame.draw.rect(screen, START_GAME_COLOR, connect4_player2_turn_indicator_rect)
                        pygame.draw.rect(screen, BLACK, connect4_board_divide_line)
                        screen.blit(player2_go, (1590 + (280 - player2_go.get_width()) / 2, 300 + ((680 - player2_go.get_height()) / 2)))
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx = event.pos[0]
                    if (posx >= 470 and posx <= 1449):
                        col = int(math.floor((posx - 470) / GRIDBOX))
                        Board.draw_board(board, gamepiece1_color, gamepiece2_color)
                        pygame.draw.rect(screen, BLACK, connect4_board_divide_line)
                        pygame.display.update()
                        # Until you get a valid location, continue this loop
                        if (Game.is_valid_location(board, col)):
                            if (playerID == "Player1"):
                                #When the value in history_array1 == 9 then replace with the selected column
                                move = 0
                                while (history_array1[move] != 9):
                                    move += 1
                                history_array1[move] = col
                                row = Game.get_next_open_row(board,col)  # Row is assigned based on the next available row in the column
                                #Randomly selects gamepiece dropping noise to play
                                gamepiece_sound = random.randint(1,100)
                                if(gamepiece_sound % 2 == 0):
                                    pygame.mixer.music.load('gamepiece_sound1.wav')
                                    pygame.mixer.music.play(0)
                                else:
                                    pygame.mixer.music.load('gamepiece_sound2.wav')
                                    pygame.mixer.music.play(0)
                                Game.drop_gamepiece(board, row, col, gamepiece)
                                waiter = 1
                            elif(playerID == "Player2"):
                               #When the value in history_array1 == 9 then replace with the selected column
                                move = 0
                                while (history_array2[move] != 9):
                                    move += 1
                                history_array2[move] = col
                                row = Game.get_next_open_row(board,col)  # Row is assigned based on the next available row in the column
                                #Randomly selects gamepiece dropping noise to play
                                gamepiece_sound = random.randint(1,100)
                                if(gamepiece_sound % 2 == 0):
                                    pygame.mixer.music.load('gamepiece_sound1.wav')
                                    pygame.mixer.music.play(0)
                                else:
                                    pygame.mixer.music.load('gamepiece_sound2.wav')
                                    pygame.mixer.music.play(0)
                                Game.drop_gamepiece(board, row, col, gamepiece)
                                waiter = 1

                            #If the move that was made is a winning move
                            if Game.winning_move(board, gamepiece) == True:
                                Board.draw_board(board, gamepiece1_color, gamepiece2_color)
                                pygame.display.update()
                                
                                #If the player that made the winning move has ID "Player1" and the game type is Player vs. Player
                                if (playerID == "Player1" and game_type == 1):
                                    pygame.draw.rect(screen, BROWN, connect4_player2_turn_indicator_rect)
                                    pygame.draw.rect(screen, GOLD, connect4_player1_turn_indicator_rect)
                                    screen.blit(player1_winner_text, (50 + (280 - player1_winner_text.get_width()) / 2, 300 + ((680 - player1_winner_text.get_height()) / 2)))
                                    screen.blit(player2_loser_text, (1590 + (280 - player2_loser_text.get_width()) / 2, 300 + ((680 - player2_loser_text.get_height()) / 2)))
                                    pygame.draw.rect(screen, BLACK, connect4_board_divide_line)
                                    Board.end_game_screen(board, gamepiece, gamepiece1_color, gamepiece2_color, playerID, history_array1, history_array2, game_type, 0, 0)

                                #If the player that made the winning move has ID "Player2" and the game type is Player vs. Player
                                if (playerID == "Player2" and game_type == 1):
                                    pygame.draw.rect(screen, BROWN, connect4_player1_turn_indicator_rect)
                                    pygame.draw.rect(screen, GOLD, connect4_player2_turn_indicator_rect)
                                    screen.blit(player1_loser_text, (50 + (280 - player1_loser_text.get_width()) / 2, 300 + ((680 - player1_loser_text.get_height()) / 2)))
                                    screen.blit(player2_winner_text, (1590 + (280 - player2_winner_text.get_width()) / 2, 300 + ((680 - player2_winner_text.get_height()) / 2)))
                                    pygame.draw.rect(screen, BLACK, connect4_board_divide_line)
                                    Board.end_game_screen(board, gamepiece, gamepiece1_color, gamepiece2_color, playerID, history_array1, history_array2, game_type, 0, 0)

                                #If the player that made the winning move has ID "Player1" and the game type is Player vs. Computer
                                if (playerID == "Player1" and game_type == 2):
                                    pygame.draw.rect(screen, BROWN, connect4_player2_turn_indicator_rect)
                                    pygame.draw.rect(screen, GOLD, connect4_player1_turn_indicator_rect)
                                    screen.blit(player1_winner_text, (50 + (280 - player1_winner_text.get_width()) / 2, 300 + ((680 - player1_winner_text.get_height()) / 2)))
                                    screen.blit(computer1pvc_loser_text, (1590 + (280 - computer1pvc_loser_text.get_width()) / 2, 300 + ((680 - computer1pvc_loser_text.get_height()) / 2)))
                                    pygame.draw.rect(screen, BLACK, connect4_board_divide_line)
                                    Board.end_game_screen(board, gamepiece, gamepiece1_color, gamepiece2_color, playerID, history_array1, history_array2, game_type, computer_difficulty, 0)

                                global game_over
                                game_over = 2

                            #If the game is a tie
                            elif (round_count == 42 and Game.winning_move(board, gamepiece) != True):
                                pygame.draw.rect(screen, WHITE, connect4_player1_turn_indicator_rect)
                                pygame.draw.rect(screen, WHITE, connect4_player2_turn_indicator_rect)
                                screen.blit(tie_text, (50 + (280 - tie_text.get_width()) / 2, 300 + ((680 - tie_text.get_height()) / 2)))
                                screen.blit(tie_text, (1590 + (280 - tie_text.get_width()) / 2, 300 + ((680 - tie_text.get_height()) / 2)))
                                Board.draw_board(board, gamepiece1_color, gamepiece2_color)
                                pygame.display.update()
                                confirm_tie = 1
                                game_over = 2
                                Board.end_game_screen(board, gamepiece, gamepiece1_color, gamepiece2_color, playerID, history_array1, history_array2, 1, computer_difficulty, 0)
                        #If player tries to make an invalid move then play an error noise
                        else:
                            pygame.mixer.music.load('Error.wav')
                            pygame.mixer.music.play(0)


    #Computer move
    def computer_move(board, computer1_difficulty, computer2_difficulty, gamepiece, gamepiece1_color, gamepiece2_color, ID, history_array1, history_array2, game_type):
        #If game type is Player vs. Computer, draw the correct name indicators on top left and top right
        if (game_type == 2):
            pygame.draw.rect(screen, SUB_MENU_COLOR, connect4_player1_turn_indicator_rect)
            pygame.draw.rect(screen, START_GAME_COLOR, connect4_player2_turn_indicator_rect)
            screen.blit(computer1pvc_go, (1590 + (280 - computer1pvc_go.get_width()) / 2, 300 + ((680 - computer1pvc_go.get_height()) / 2)))
            pygame.display.update()

        #If ID is Computer1 and game type is Player vs. Computer
        if(ID == "Computer1" and game_type == 2):
            pygame.draw.rect(screen, SUB_MENU_COLOR, connect4_player1_turn_indicator_rect)
            pygame.draw.rect(screen, START_GAME_COLOR, connect4_player2_turn_indicator_rect)
            screen.blit(computer1pvc_go, (1590 + (280 - computer1pvc_go.get_width()) / 2, 300 + ((680 - computer1pvc_go.get_height()) / 2)))
            pygame.display.update()
            col, score = Player.minimax(board, computer1_difficulty, -math.inf, math.inf, True)

        #If ID is Computer1 and game type is Computer vs. Computer
        if(ID == "Computer1" and game_type == 3):
            pygame.draw.rect(screen, SUB_MENU_COLOR, connect4_player2_turn_indicator_rect)
            pygame.draw.rect(screen, START_GAME_COLOR, connect4_player1_turn_indicator_rect)
            screen.blit(computer1cvc_go, (50 + (280 - computer1cvc_go.get_width()) / 2, 300 + ((680 - computer1cvc_go.get_height()) / 2)))
            pygame.display.update()
            col, score = Player.minimax(board, computer1_difficulty, -math.inf, math.inf, True)
        
        #If ID is Computer2 and game type is Computer vs Computer
        if(ID == "Computer2" and game_type == 3):
            pygame.draw.rect(screen, SUB_MENU_COLOR, connect4_player1_turn_indicator_rect)
            pygame.draw.rect(screen, START_GAME_COLOR, connect4_player2_turn_indicator_rect)
            screen.blit(computer2cvc_go, (1590 + (280 - computer2cvc_go.get_width()) / 2, 300 + ((680 - computer2cvc_go.get_height()) / 2)))
            pygame.display.update()
            col, score = Player.minimax(board, computer2_difficulty, -math.inf, math.inf, True)

        #The above if statements are done outside of the while loop below because we need to compute col before entering the while loop since it is used in the next if statement

        #i will be set to 2 and exit while loop when a valid location is selected
        i = 0
        while (i != 2):  # Until you get a valid location, continue this loop
            if (Game.is_valid_location(board, col)):

                #If 
                if (ID == "Computer1" and game_type == 2):
                    # Let's the user see that it is the computer's turn and waits 1.5 seconds before placing a move. This is necessary for easy and medium difficulty because they're so fast.
                    # This is because they have depths of 3 and 4 (can look 3 to 4 turns into the future) which is pretty quick, but hard depth = 5, which slows down quite a bit. As the game goes on
                    # past 10 turns we need the 1.5 delay for hard because the minimax algorithm gets quicker as there are less spaces to fill.
                    if(computer1_difficulty < 5 or computer1_difficulty == 5 and round_count >= 10):
                        time.sleep(1.5)
                    #When the value in history_array1 == 9 then replace with the selected column
                    move = 0
                    while (history_array2[move] != 9):
                        move += 1
                    history_array2[move] = col
                    row = Game.get_next_open_row(board,col)  # Row is assigned based on the next available row in the column
                    #Randomly selects gamepiece dropping noise to play
                    gamepiece_sound = random.randint(1,100)
                    if(gamepiece_sound % 2 == 0):
                        pygame.mixer.music.load('gamepiece_sound1.wav')
                        pygame.mixer.music.play(0)
                    else:
                        pygame.mixer.music.load('gamepiece_sound2.wav')
                        pygame.mixer.music.play(0)
                    Game.drop_gamepiece(board, row, col, gamepiece)

                elif (ID == "Computer1" and game_type == 3):
                    # Let's the user see that it is the computer's turn and waits 1.5 seconds before placing a move. This is necessary for easy and medium difficulty because they're so fast.
                    # This is because they have depths of 3 and 4 (can look 3 to 4 turns into the future) which is pretty quick, but hard depth = 5, which slows down quite a bit. As the game goes on
                    # past 10 turns we need the 1.5 delay for hard because the minimax algorithm gets quicker as there are less spaces to fill.
                    if(computer1_difficulty < 5 or computer1_difficulty == 5 and round_count >= 10):
                        time.sleep(1.5)
                    #When the value in history_array1 == 9 then replace with the selected column
                    move = 0
                    while (history_array1[move] != 9):
                        move += 1
                    history_array1[move] = col
                    row = Game.get_next_open_row(board, col)  # Row is assigned based on the next available row in the column
                    #Randomly selects gamepiece dropping noise to play
                    gamepiece_sound = random.randint(1,100)
                    if(gamepiece_sound % 2 == 0):
                        pygame.mixer.music.load('gamepiece_sound1.wav')
                        pygame.mixer.music.play(0)
                    else:
                        pygame.mixer.music.load('gamepiece_sound2.wav')
                        pygame.mixer.music.play(0)
                    Game.drop_gamepiece(board, row, col, gamepiece)
                elif (ID == "Computer2" and game_type == 3):
                    # Let's the user see that it is the computer's turn and waits 1.5 seconds before placing a move. This is necessary for easy and medium difficulty because they're so fast.
                    # This is because they have depths of 3 and 4 (can look 3 to 4 turns into the future) which is pretty quick, but hard depth = 5, which slows down quite a bit. As the game goes on
                    # past 10 turns we need the 1.5 delay for hard because the minimax algorithm gets quicker as there are less spaces to fill.
                    if(computer2_difficulty < 5 or computer2_difficulty == 5 and round_count >= 10):
                        time.sleep(1.5)
                    #When the value in history_array1 == 9 then replace with the selected column
                    move = 0
                    while (history_array2[move] != 9):
                        move += 1
                    history_array2[move] = col
                    row = Game.get_next_open_row(board, col)  # Row is assigned based on the next available row in the column
                    #Randomly selects gamepiece dropping noise to play
                    gamepiece_sound = random.randint(1,100)
                    if(gamepiece_sound % 2 == 0):
                        pygame.mixer.music.load('gamepiece_sound1.wav')
                        pygame.mixer.music.play(0)
                    else:
                        pygame.mixer.music.load('gamepiece_sound2.wav')
                        pygame.mixer.music.play(0)
                    Game.drop_gamepiece(board, row, col, gamepiece)
                i = 2
            else:
                col = Player.pick_best_move(board, AI_PIECE)

        #If last move that was made was a winning move
        if Game.winning_move(board, gamepiece) == True:
            Board.draw_board(board, gamepiece1_color, gamepiece2_color)
            pygame.display.update()

            #If Computer1 made the winning move and the game type is Player vs. Computer
            if (ID == "Computer1" and game_type == 2):
                pygame.draw.rect(screen, GOLD, connect4_player2_turn_indicator_rect)
                pygame.draw.rect(screen, BROWN, connect4_player1_turn_indicator_rect)
                screen.blit(player1_loser_text, (50 + (280 - player1_loser_text.get_width()) / 2, 300 + ((680 - player1_loser_text.get_height()) / 2)))
                screen.blit(computer1pvc_winner_text, (1590 + (280 - computer1pvc_winner_text.get_width()) / 2,300 + ((680 - player1_loser_text.get_height()) / 2)))
                Board.end_game_screen(board, gamepiece, gamepiece1_color, gamepiece2_color, ID, history_array1,history_array2, game_type, computer1_difficulty, 0)
            
            #If Computer1 made the winning move and the game type is Computer vs. Computer
            elif (ID == "Computer1" and game_type == 3):
                pygame.draw.rect(screen, BROWN, connect4_player2_turn_indicator_rect)
                pygame.draw.rect(screen, GOLD, connect4_player1_turn_indicator_rect)
                screen.blit(computer1cvc_winner_text, (50 + (280 - computer1cvc_winner_text.get_width()) / 2,300 + ((680 - computer1cvc_winner_text.get_height()) / 2)))
                screen.blit(computer2cvc_loser_text, (1590 + (280 - computer2cvc_loser_text.get_width()) / 2,300 + ((680 - computer2cvc_loser_text.get_height()) / 2)))
                Board.end_game_screen(board, gamepiece, gamepiece1_color, gamepiece2_color, ID, history_array1,history_array2, game_type, computer1_difficulty, computer2_difficulty)
           
            #If Computer2 made the winning move and the game type is Computer vs. Computer
            elif (ID == "Computer2" and game_type == 3):
                pygame.draw.rect(screen, GOLD, connect4_player2_turn_indicator_rect)
                pygame.draw.rect(screen, BROWN, connect4_player1_turn_indicator_rect)
                screen.blit(computer1cvc_loser_text, (50 + (280 - computer1cvc_loser_text.get_width()) / 2,300 + ((680 - computer1cvc_loser_text.get_height()) / 2)))
                screen.blit(computer2cvc_winner_text, (1590 + (280 - computer2cvc_winner_text.get_width()) / 2,300 + ((680 - computer2cvc_winner_text.get_height()) / 2)))
                Board.end_game_screen(board, gamepiece, gamepiece1_color, gamepiece2_color, ID, history_array1, history_array2, game_type, computer1_difficulty, computer2_difficulty)

            global game_over
            game_over = True

        #Else the game is a tie
        elif (round_count == 42 and Game.winning_move(board, gamepiece) != True):
            pygame.draw.rect(screen, WHITE, connect4_player1_turn_indicator_rect)
            pygame.draw.rect(screen, WHITE, connect4_player2_turn_indicator_rect)
            screen.blit(tie_text, (50 + (280 - tie_text.get_width()) / 2, 300 + ((680 - tie_text.get_height()) / 2)))
            screen.blit(tie_text, (1590 + (280 - tie_text.get_width()) / 2, 300 + ((680 - tie_text.get_height()) / 2)))
            Board.draw_board(board, gamepiece1_color, gamepiece2_color)
            pygame.display.update()
            confirm_tie = 1
            game_over = 2
            Board.end_game_screen(board, gamepiece, gamepiece1_color, gamepiece2_color, ID, history_array1, history_array2, game_type, computer1_difficulty, computer2_difficulty)

    # This function creates the score of certain moves
    def evaluate_window(window, piece):
        opp_piece = PLAYER_PIECE
        score = 0
        if piece == PLAYER_PIECE:
            opp_piece = AI_PIECE

        # if AI can get four in a row the score is raised by 100
        if window.count(piece) == 4:
            score += 100
        # if AI can get three in a row the score is raised by 5
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 7
        # if AI can get two in a row the score is raised by 2
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 2
        # if the user can get four in a row the score is decreased by 4
        if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
            score -= 4
        elif window.count(opp_piece) == 2 and window.count(EMPTY) == 2:
            score -= 2
        elif window.count(opp_piece) == 2 and window.count(EMPTY) == 3:
            score -= 1

        return score

    # This function scores a certain spot based on the current position of the board
    def score_position(board, piece):
        score = 0

        # scoring center column
        center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        # scoring horizontally
        for r in range(ROW_COUNT):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(COLUMN_COUNT - 3):
                window = row_array[c:c + WINDOW_LENGTH]
                score += Player.evaluate_window(window, piece)

        # scoring vertically
        for c in range(COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(ROW_COUNT - 3):
                window = col_array[r:r + WINDOW_LENGTH]
                score += Player.evaluate_window(window, piece)

        # scoring positive diagonally
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                window = [board[r + i][c + 1] for i in range(WINDOW_LENGTH)]
                score += Player.evaluate_window(window, piece)

        # scoring negative diagonally
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
                score += Player.evaluate_window(window, piece)

        return score

    # This creates an array of all possible valid columns to drop a piece into
    def get_valid_locations(board):
        valid_locations = []
        for col in range(COLUMN_COUNT):
            if Game.is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations

    # This takes the number of the column with the highest score and places a piece in that spot
    def pick_best_move(board, piece):
        valid_locations = Player.get_valid_locations(board)
        best_score = -1000
        for col in valid_locations:
            row = Game.get_next_open_row(board, col)
            temp_board = board.copy()
            Game.drop_gamepiece(temp_board, row, col, piece)
            score = Player.score_position(temp_board, piece)
            if score > best_score:
                best_score = score
                best_col = col
        return best_col

    def find_terminal_node(board):
        return Game.winning_move(board, PLAYER_PIECE) or Game.winning_move(board, AI_PIECE) or len(
            Player.get_valid_locations(board)) == 0

    def minimax(board, depth, alpha, beta, maximizingPlayer):
        valid_locations = Player.get_valid_locations(board)
        terminal_node = Player.find_terminal_node(board)
        if depth == 0 or terminal_node:
            if terminal_node:
                if Game.winning_move(board, AI_PIECE):
                    return (None, 600000000000000)
                elif Game.winning_move(board, PLAYER_PIECE):
                    return (None, -60000000000000)
                else:
                    return (None, 0)
            else:
                return (None, Player.score_position(board, AI_PIECE))
        if maximizingPlayer:
            score = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = Game.get_next_open_row(board, col)
                board2 = board.copy()
                Game.drop_gamepiece(board2, row, col, AI_PIECE)
                new_score = Player.minimax(board2, depth - 1, alpha, beta, False)[1]
                if new_score > score:
                    score = new_score
                    column = col
                alpha = max(alpha, score)
                if alpha >= beta:
                    break
            return column, score
        else:
            score = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = Game.get_next_open_row(board, col)
                board2 = board.copy()
                Game.drop_gamepiece(board2, row, col, PLAYER_PIECE)
                new_score = Player.minimax(board2, depth - 1, alpha, beta, True)[1]
                if new_score < score:
                    score = new_score
                    column = col
                beta = min(beta, score)
                if alpha >= beta:
                    break
            return column, score



################################################################################################################################COLORS
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
PINK = (255, 0, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BROWN = (165, 42, 42)
GOLD = (255, 215, 0)
SUB_MENU_COLOR = (159, 197, 232)
MENU_BUTTON_COLOR = (0, 102, 204)
START_GAME_COLOR = (5, 135, 88)

################################################################################################################################Buttons
pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.NOFRAME)
main_menu_img = pygame.image.load("C4_MM.png")
sub_menu_img = pygame.image.load("C4_SUBMENU.png")
surface = pygame.display.get_surface()
global window_w
window_w = surface.get_width()
global window_h
window_h = surface.get_height()

button = Board.button
# Main Menu Buttons
pvpButton = button((MENU_BUTTON_COLOR), window_w / 2 - 150, window_h / 2 - 50, 300, 50, 'Player vs. Player')
pvcButton = button((MENU_BUTTON_COLOR), window_w / 2 - 150, window_h / 2 + 50, 300, 50, 'Player vs. Computer')
cvcButton = button((MENU_BUTTON_COLOR), window_w / 2 - 150, window_h / 2 + 150, 300, 50, 'Computer vs. Computer')
quitButton = button((MENU_BUTTON_COLOR), window_w - 310, window_h - 60, 300, 50, 'Quit')

# Player Vs. Computer Buttons
easyButton_pvc = button((MENU_BUTTON_COLOR), window_w / 2 - 150, window_h / 2 - 50, 300, 50, 'Easy')
mediumButton_pvc = button((MENU_BUTTON_COLOR), window_w / 2 - 150, window_h / 2 + 50, 300, 50, 'Medium')
hardButton_pvc = button((MENU_BUTTON_COLOR), window_w / 2 - 150, window_h / 2 + 150, 300, 50, 'Hard')
backButton = button((MENU_BUTTON_COLOR), window_w - 310, window_h - 130, 300, 50, 'Back')

# Computer Vs. Computer Buttons
easyButton1_cvc = button((MENU_BUTTON_COLOR), window_w / 2 - 346, window_h / 2 - 50, 300, 50, 'Easy')
mediumButton1_cvc = button((MENU_BUTTON_COLOR), window_w / 2 - 346, window_h / 2 + 50, 300, 50, 'Medium')
hardButton1_cvc = button((MENU_BUTTON_COLOR), window_w / 2 - 346, window_h / 2 + 150, 300, 50, 'Hard')
easyButton2_cvc = button((MENU_BUTTON_COLOR), window_w / 2 + 50, window_h / 2 - 50, 300, 50, 'Easy')
mediumButton2_cvc = button((MENU_BUTTON_COLOR), window_w / 2 + 50, window_h / 2 + 50, 300, 50, 'Medium')
hardButton2_cvc = button((MENU_BUTTON_COLOR), window_w / 2 + 50, window_h / 2 + 150, 300, 50, 'Hard')

# Player vs. Player Buttons
online_button = button((MENU_BUTTON_COLOR), window_w / 2 - 150, window_h / 2, 300, 50, 'Online')
offline_button = button((MENU_BUTTON_COLOR), window_w / 2 - 150, window_h / 2 + 100, 300, 50, 'Offline')

# Offline Player vs. Players
red_button1 = button((RED), 633, 590, 70, 70)
green_button1 = button((GREEN), 723, 590, 70, 70)
blue_button1 = button((BLUE), 813, 590, 70, 70)
yellow_button1 = button((YELLOW), 633, 680, 70, 70)
orange_button1 = button((ORANGE), 723, 680, 70, 70)
purple_button1 = button((PURPLE), 813, 680, 70, 70)
cyan_button1 = button((CYAN), 633, 770, 70, 70)
pink_button1 = button((PINK), 723, 770, 70, 70)
white_button1 = button((WHITE), 813, 770, 70, 70)

red_button2 = button((RED), 1028, 590, 70, 70)
green_button2 = button((GREEN), 1118, 590, 70, 70)
blue_button2 = button((BLUE), 1208, 590, 70, 70)
yellow_button2 = button((YELLOW), 1028, 680, 70, 70)
orange_button2 = button((ORANGE), 1118, 680, 70, 70)
purple_button2 = button((PURPLE), 1208, 680, 70, 70)
cyan_button2 = button((CYAN), 1028, 770, 70, 70)
pink_button2 = button((PINK), 1118, 770, 70, 70)
white_button2 = button((WHITE), 1208, 770, 70, 70)

# End game options buttons
eg_rematch_option = button((MENU_BUTTON_COLOR), window_w / 2 - 482, 1010, 300, 50, 'Rematch')
eg_replay_option = button((MENU_BUTTON_COLOR), window_w / 2 - 150, 1010, 300, 50, 'View Replay')
eg_main_menu_option = button((MENU_BUTTON_COLOR), window_w / 2 + 185, 1010, 300, 50, 'Return to Main Menu')

# Replay buttons
replay_continue = button((MENU_BUTTON_COLOR), 1029 + 20, 1010, 300, 50, "Continue Replay")
replay_main_menu_option = button((MENU_BUTTON_COLOR), 1029 - 450, 1010, 300, 50, 'Return to Main Menu')

################################################################################################################################Fonts
game_font = pygame.font.SysFont('timesnewroman', 32)
game_font2 = pygame.font.SysFont('timesnewroman', 30)
end_game_font = pygame.font.SysFont('timesnewroman', 36)
start_game_font = pygame.font.SysFont('timesnewroman', 64)
char_limit_warning_font = pygame.font.SysFont('timesnewroman', 12)

################################################################################################################################text
pvcText = game_font.render("Select a Computer Difficulty!", 1, (0, 0, 0))
cvc_text1 = game_font.render("Select the Computer Difficulties!", 1, (0, 0, 0))
cvc_text2 = game_font.render("Computer 1", 1, (0, 0, 0))
cvc_text3 = game_font.render("Computer 2", 1, (0, 0, 0))
start_game_text = start_game_font.render("START GAME!", 1, (0, 0, 0))
pvp_offline_text1 = game_font.render("Please select two different gamepiece colors", 1, (0, 0, 0))
player1_gamepiece_color = game_font.render("Player1: ", 1, (0, 0, 0))
player2_gamepiece_color = game_font.render("Player2: ", 1, (0, 0, 0))
player1_name = game_font.render("Player1 Gamepiece:", 1, (0, 0, 0))
player2_name = game_font.render("Player2 Gamepiece:", 1, (0, 0, 0))
computer1_name = game_font2.render("Computer1 Gamepiece:", 1, (0, 0, 0))
computer2_name = game_font2.render("Computer2 Gamepiece:", 1, (0, 0, 0))

player1_go = game_font.render("Player1's Turn", 1, (0, 0, 0))
player2_go = game_font.render("Player2's Turn", 1, (0, 0, 0))
computer1pvc_go = game_font.render("Computer1's Turn", 1, (0, 0, 0))
computer1cvc_go = game_font.render("Computer1's Turn", 1, (0, 0, 0))
computer2cvc_go = game_font.render("Computer2's Turn", 1, (0, 0, 0))
player1_winner_text = end_game_font.render("Player1 Wins!", 1, (0, 0, 0))
player1_loser_text = end_game_font.render("Player1 Loses...", 1, (255, 255, 255))
player2_winner_text = end_game_font.render("Player2 Wins!", 1, (0, 0, 0))
player2_loser_text = end_game_font.render("Player2 Loses...", 1, (255, 255, 255))
tie_text = end_game_font.render("The game is a tie!", 1, (0, 0, 0))
computer1pvc_winner_text = end_game_font.render("Computer1 Wins!", 1, (0, 0, 0))
computer1pvc_loser_text = end_game_font.render("Computer1 Loses...", 1, (255, 255, 255))
computer1cvc_winner_text = end_game_font.render("Computer1 Wins!", 1, (0, 0, 0))
computer1cvc_loser_text = end_game_font.render("Computer1 Loses...", 1, (255, 255, 255))
computer2cvc_winner_text = end_game_font.render("Computer2 Wins!", 1, (0, 0, 0))
computer2cvc_loser_text = end_game_font.render("Computer2 Loses...", 1, (255, 255, 255))

################################################################################################################################shapes used for GUI
start_rect_outline = pygame.Rect(600, 880, 724, 199)
start_rect = pygame.Rect(610, 890, 704, 179)
sub_menu_outline = pygame.Rect(554, 380, 816, 478)
sub_menu_rect = pygame.Rect(564, 390, 796, 458)
sub_menu_divide_line1 = pygame.Rect(957, 450, 6, 398)
sub_menu_divide_line2 = pygame.Rect(564, 444, 796, 6)

connect4_board_background_outline = pygame.Rect(460, 0, 1000, 990)
connect4_board_divide_line = pygame.Rect(470, 136, 980, 3)
connect4_player1_turn_indicator_rect_outline = pygame.Rect(40, 290, 300, 700)
connect4_player1_turn_indicator_rect = pygame.Rect(50, 300, 280, 680)
connect4_player1_nameplate_outline = pygame.Rect(40, 50, 300, 200)
connect4_player1_nameplate = pygame.Rect(50, 60, 280, 180)
connect4_player2_nameplate_outline = pygame.Rect(1580, 50, 300, 200)
connect4_player2_nameplate = pygame.Rect(1590, 60, 280, 180)
connect4_player2_turn_indicator_rect_outline = pygame.Rect(1580, 290, 300, 700)
connect4_player2_turn_indicator_rect = pygame.Rect(1590, 300, 280, 680)

###############################################################################################################################################################################################################################################################

########### Main ###########
# Creating display surface object
Board.main_menu()