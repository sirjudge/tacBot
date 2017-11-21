#!/usr/bin/env python3
from util import *
import robotStarter
import re
import random


class Decoding:
    decodingList = []
    generationNumber = -1
    tmpFile = open('encoding.txt', 'r+')
    numLines = -1

    def __init__(self):
        e = robotStarter.Encoding()
        self.decodingList = e.getEncoding()

    @staticmethod
    def file_len(fname):
        i = 0
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1

    def getDecodingList(self):
        return self.decodingList

    def delFirstLine(self):
        with self.tmpFile as fin:
            data = fin.read().splitlines(True)
        with self.tmpFile as fout:
            fout.writelines(data[1:])

    def getFirstLine(self):
        with self.tmpFile as f:
            first_line = f.readline()
            efl = first_line.split(',')
        return efl[0]

    def getNumLines(self):
        return self.numLines

    # TODO:
    # this method has been named wwbd() or better known as what would brody do, an adaptation of the popular
    # phrase, 'what would jesus do'. This is where the encoding will be evaluated and return a move based on
    # what the current encodings are
    def wwbd(self, moves):
        winIndexes = []
        moveBox = []
        # Search through current board and see if any of the spaces have a chance to be won
        for x in range(len(self.decodingList)):
            if self.decodingList == 'W':
                winIndexes.append(x)
        # Loop through the boxes you can win, if any are in available moves then that becomes the move
        for y in range(len(winIndexes)):
            if winIndexes[y] in moves:
                moveBox.append(winIndexes[y])
                break
        return moveBox[random.randint(0, len(moveBox))]


def go():
    bot = BotStarter()
    parser = BotParser(bot)
    parser.run()
    file = open('out.txt')
    file.write('Winner = ' + str(bot.whoWon()))


class BotStarter:
    currEncoding = ''

    def __init__(self):
        random.seed()  # helps create a more random environment
        d = Decoding()
        self.currEncoding = d.getFirstLine()
        d.delFirstLine()
        # read the encoding
        # delete that line from the encoding file from a temp file
        # temp file acts as queue
        # if number of moves is greater than 0 make a random move

    # using the regex 'winner\"\d' search the file to find the winner's ID number
    @staticmethod
    def whoWon():
        resultFile = open('resultfile.json')

        # Regex stuff
        # s = mmap.mmap(resultFile.fileno(), 0, access=mmap.ACCESS_READ)
        # regex = re.compile('.*winner\":.*')

        # reads the file, closes the file, using regex searches for who won the game
        resultRead = resultFile.read()
        resultFile.close()
        matches = re.findall('winner\":\d', resultRead)
        print(matches)
        winnerID = matches[0][10]
        return winnerID

    def doMove(self, state):
        moves = state.getField().getAvailableMoves()
        # TODO: Move based on the encoding
        if len(moves) > 0:
            return moves[random.randrange(len(moves))]
        else:
            return None


if __name__ == '__main__':
    go()
    # This will create 100 mains
