from pymycobot.mycobot import MyCobot
import pymycobot
from pymycobot import PI_PORT, PI_BAUD 
import time
import os
import sys
from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle, Coord

DigPos =    [[265.9, 63.8, 104.7, -179.02, 2.73, -43.74], 
            [266.1, 8.9, 111.1, 176.67, 6.94, -55.83],
            [258.6, -42.1, 114.7, 179.35, 4.66, -56.98],
            [203.8, 64.1, 117.3, -178.96, 5.05, -14.81],
            [208.4, 17.0, 123.0, 177.22, 4.84, -26.92],
            [207.3, -39.3, 112.3, 179.17, 2.93, -42.24],
            [165.3, 50.0, 112.9, 179.72, 10.36, -11.21],
            [161.2, 8.3, 114.0, -176.97, 0.48, 43.92],
            [167.6, -38.5, 115.2, -176.4, 3.62, 26.65]]

abovePos = [[265.9, 63.8, 170, -179.02, 2.73, -43.74], 
            [266.1, 8.9, 170, 176.67, 6.94, -55.83],
            [258.6, -42.1, 170, 179.35, 4.66, -56.98],
            [203.8, 64.1, 170, -178.96, 5.05, -14.81],
            [208.4, 17.0, 170, 177.22, 4.84, -26.92],
            [207.3, -39.3, 170, 179.17, 2.93, -42.24],
            [165.3, 50.0, 170, 179.72, 10.36, -11.21],
            [161.2, 8.3, 170, -176.97, 0.48, 43.92],
            [167.6, -38.5, 170, -176.4, 3.62, 26.65]]
            
DigAngles = [[32.78, -37.96, -100.72, 52.73, -0.7, 10.89],#a11
             [16.69, -39.46, -87.71, 31.81, 3.6, 11.07],#a12
             [4.04, -39.99, -87.71, 34.27, 1.66, 11.07],#a13
             [41.83, -22.41, -126.47, 57.83, 0.43, 5.0],#a21
             [21.0, -21.0, -130.69, 61.34, 5.62, 3.77],#a22
             [4.13, -19.59, -130.6, 60.29, 2.46, 1.14],#a23
             [48.77, -16.52, -151.08, 77.6, 8.52, 27.68],#a31
             [21.88, 1.05, -152.13, 55.72, 8.34, 14.06],#a32
             [2.46, -1.66, -152.13, 59.85, 4.65, 13.62]]#a33
               # Digit Hard Code

XAng = [69.08, -31.28, -113.73, 53.87, 4.21, 11.33] #pick_point ang
AirAng = [0.96, -21.35, -54.4, 6.06, -0.52, -20.91]# air ang
            
XPos = [142.6, 154.9, 95, 179.08, 1.29, -60.3] #Pick Point
AirPos = [206.3, -12.7, 216.6, 177.34, 7.74, -169.83] #Air

#mc = MyCobot("/dev/ttyACM1", 115200)

import random

class Tic(object):

    global mc
    winning_combos = (
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6])
    winners = ('X-win', 'Draw', 'O-win')

    

    def __init__(self, squares=[]):
        """Initialize either custom or deafult board"""
        self.mc=None
        if len(squares) == 0:
            self.squares = [None for i in range(9)]
        else:
            self.squares = squares

    def jay_init(self):
        self.mc = MyCobot("/dev/ttyACM1", 115200)
        self.mc.sync_send_angles([0,0,0,0,0,0], 30, 2)
        time.sleep(2)

    def show(self):
        """Print game progress"""
        for element in [
                self.squares[i: i + 3] for i in range(0, len(self.squares), 3)]:
            print(element)

    def available_moves(self):
        return [k for k, v in enumerate(self.squares) if v is None]

    def available_combos(self, player):
        return self.available_moves() + self.get_squares(player)

    def complete(self):
        """Check if game has ended"""
        if None not in [v for v in self.squares]:
            return True
        if self.winner() is not None:
            return True
        return False

    def X_won(self):
        return self.winner() == 'X'

    def O_won(self):
        return self.winner() == 'O'

    def tied(self):
        return self.complete() and self.winner() is None

    def winner(self):
        for player in ('X', 'O'):
            positions = self.get_squares(player)
            for combo in self.winning_combos:
                win = True
                for pos in combo:
                    if pos not in positions:
                        win = False
                if win:
                    return player
        return None

    def get_squares(self, player):
        """Returns squares belonging to a player"""
        return [k for k, v in enumerate(self.squares) if v == player]

    def make_move(self, position, player):
        self.squares[position] = player


    def move_cobot(self, position):
        global DigPos, XPos, AirPos, XAng, AirAng
        speeds = 30
        positionInt = int(position)
        #mc.set_color(0,0,255) #blue light on
        #Pick position
        

        #self.mc.sync_send_coords(AirPos, speeds, 1)
        self.mc.sync_send_angles(AirAng,speeds,2)
        print("Air")
        time.sleep(3)

        #self.mc.sync_send_angles([61.69, -33.92, -42.89, -15.82, 5.53, -172.26],speeds,1) # Above Pick
        self.mc.sync_send_coords([115.8, 177.3, 210.6, 178.06, -0.92, -6.11],speeds,1)
        print("Above Pick")

        self.mc.sync_send_coords(XPos, speeds, 1)
        print("Pick")
        time.sleep(3)
        #Turn on Suction
        self.pump_on()
        time.sleep(3)
        #Air position
        #self.mc.sync_send_coords(AirPos, speeds, 1)
        self.mc.sync_send_angles(AirAng,speeds,2)
        print("Air")
        time.sleep(3)

        #if positionInt == 7 or positionInt == 8 or positionInt == 9:
        #    self.mc.sync_send_angles([48.6, -17.84, -119.79, 42.36, 5.0, 161.8],speeds,2)
        #    time.sleep(2)
        #self.mc.sync_send_coords(AirPos, speeds, 1)
        #print("Air")
        
        #time.sleep(3)
        self.mc.sync_send_coords(abovePos[positionInt], speeds, 1)
        print("Pos")
        time.sleep(3)


        #Place position
        self.mc.sync_send_coords(DigPos[positionInt], speeds, 1)
        print("Pos")
        time.sleep(3)

        #Place Angles
        #mc.send_angles(DigAngles[position],speeds)
        #time.sleep(5)

        #Turn Off Suction
        self.pump_off()
        time.sleep(4)


    def pump_on(self):
        self.mc.set_basic_output(2, 0)
        self.mc.set_basic_output(5, 0)

    def pump_off(self):
        self.mc.set_basic_output(2, 1)
        self.mc.set_basic_output(5, 1)

    def alphabeta(self, node, player, alpha, beta):
        """Alphabeta algorithm"""
        if node.complete():
            if node.X_won():
                return -1
            elif node.tied():
                return 0
            elif node.O_won():
                return 1

        for move in node.available_moves():
            node.make_move(move, player)
            val = self.alphabeta(node, get_enemy(player), alpha, beta)
            node.make_move(move, None)
            if player == 'O':
                if val > alpha:
                    alpha = val
                if alpha >= beta:
                    return beta
            else:
                if val < beta:
                    beta = val
                if beta <= alpha:
                    return alpha
        return alpha if player == 'O' else beta


def get_enemy(player):
    if player == 'X':
        return 'O'
    return 'X'


def determine(board, player):
    """Determine best possible move"""
    a = -2
    choices = []
    if len(board.available_moves()) == 9:
        return 4
    for move in board.available_moves():
        board.make_move(move, player)
        val = board.alphabeta(board, get_enemy(player), -2, 2)
        board.make_move(move, None)
        if val > a:
            a = val
            choices = [move]
        elif val == a:
            choices.append(move)
    return random.choice(choices)


if __name__ == '__main__':
    board = Tic()
    board.show()
    board.jay_init()
    digitSel = 0
    
    while not board.complete():
        player = 'X'
        player_move = int(input('Next Move: ')) - 1
        if player_move not in board.available_moves():
            continue
        board.make_move(player_move, player)
        board.move_cobot(player_move)
        print(DigPos[player_move])
        board.show()

        if board.complete():
            break
        player = get_enemy(player)
        computer_move = determine(board, player)
        board.make_move(computer_move, player)
        board.move_cobot(computer_move)
        print(DigPos[computer_move])
        print(computer_move+1)
        board.show()
    print('Winner is', board.winner())