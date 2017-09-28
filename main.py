#!/usr/bin/env python3

import sys
import random
from util import *


# def run():
#     while not sys.stdin.closed:
#         try:
#             rawline = sys.stdin.readline()
#             line = rawline.strip()
#             handle_message(line)
#         except EOFError:
#             sys.stderr.write('EOF')
#     return
    
# def handle_message(message):
#     sys.stderr.write("bot received: {}\n".format(message))
#     parts = message.split()
#     if not parts:
#         sys.stderr.write("Unable to parse line (empty)\n")
#     elif parts[0] == 'hello':
#         out('hello back')
#     else:
#         sys.stderr.write("Unable to parse line\n") 
        
# def out(message):
#     sys.stdout.write(message + '\n')
#     sys.stdout.flush()

def go():
    bot = BotStarter()
    parser = BotParser(bot)
    parser.run()


class BotStarter:
    def __init__(self):
        random.seed()
        
    def doMove(self, state):
        moves = state.getField().getAvailableMoves()
        if (len(moves) > 0):
            return moves[random.randrange(len(moves))]
        else:
            return None

if __name__ == '__main__':
    go()
