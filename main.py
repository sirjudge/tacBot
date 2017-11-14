#!/usr/bin/env python3
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

def go(encoding):
    bot = BotStarter()
    parser = BotParser(bot)
    parser.run()
    # TODO: needs to return a fitness score


class BotStarter:
    def __init__(self):
        random.seed()  # helps create a more random environment

    # if number of moves is greater than 0 make a random move
    def doMove(self, state):
        moves = state.getField().getAvailableMoves()
        # TODO: instead of moving somehwere random based off available moves use encoding here
        if len(moves) > 0:
            return moves[random.randrange(len(moves))]
        else:
            return None


if __name__ == '__main__':
    go(42)
    # This will create 100 mains
