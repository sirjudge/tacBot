#!/usr/bin/env python3
from util import *
import robotStarter
import re
import random
import json
from random import randint


# decoding list is a list of tuples (encoding,fitness)
class Decoding:
    decodingList = []
    generationNumber = -1
    tmpFile = open('encoding.txt', 'r+')

    def __init__(self):
        e = robotStarter.Encoding()
        self.decodingList = e.getEncoding()

    # Method simply creates 500 random strategies
    # Will create 10 encodings
    def createRandomFile(self):
        sList = ['0', '1', '*']

        for notOriginalName in range(0, 10):
            fname = 'encoding' + str(notOriginalName) + '.txt'
            file = open(fname, 'r+')
            for x in range(0, 500):
                for y in range(0, 9):
                    i = randint(0, 2)
                    file.write(sList[i])
                randomList = random.sample(range(9), 9)
                encString = ''
                for z in randomList:
                    encString = encString + str(z)
                file.write(',' + encString + '\n')

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
        tmpFile = open('encoding.txt', 'r+')
        with self.tmpFile as fin:
            data = fin.read().splitlines(True)
        with self.tmpFile as fout:
            fout.writelines(data[1:])

    def getFirstLine(self):
        tmpFile = open('encoding.txt', 'r+')
        with self.tmpFile as f:
            first_line = f.readline()
            efl = first_line.split(',')
        return efl[0]

    def resetFile(self):
        self.tmpFile.truncate()
        self.tmpFile.write(str(self.generationNumber) + '\n')
        for q in self.getDecodingList():
            self.tmpFile.write(q[0] + ',' + q[1] + '\n')

def go():
    bot = BotStarter()
    parser = BotParser(bot)
    # Comment/uncomment the line below to start/stop the parser from actually running
    #parser.run()
    file = open('out.txt', 'r+')
    file.write('Winner = ' + str(bot.whoWon()))


class BotStarter:
    currEncoding = ''

    def __init__(self):
        random.seed()  # helps create a more random environment
        d = Decoding()
        d.createRandomFile()

        # self.currEncoding = d.getFirstLine()
        # d.delFirstLine()

        # read the encoding
        # delete that line from the encoding file from a temp file
        # temp file acts as queue
        # if number of moves is greater than 0 make a random move

    # TODO come back to this later
    def load_from_json(self):
        with open('resultfile.txt') as f:
            data = json.load(f)
        winner = self.json_data_to_winner(data)
        return winner

    @staticmethod
    def jsonDataToWinner(data):
        return json.loads(data['details'])['winner']

    # using the regex 'winner\"\d' search the file to find the winner's ID number
    @staticmethod
    def whoWon():
        resultFile = open('resultfile.json')
        winnerID = 42
        # Regex stuff
        # s = mmap.mmap(resultFile.fileno(), 0, access=mmap.ACCESS_READ)
        # regex = re.compile('.*winner\":.*')
        # reads the file, closes the file, using regex searches for who won the game
        resultRead = resultFile.read()
        # tries to find a pattern to match the string <"winner\":1>
        matches = re.findall('"winner\":\d', resultRead)
        print(matches)
        # winnerID = matches[]
        return winnerID

    # this method has been named wwbd() or better known as what would brody do, an adaptation of the popular
    # phrase, 'what would jesus do'. This is where the encoding will be evaluated and return a move based on
    # what the current encodings are

    # Bot Encoding
    #  Macro       box 1       box 2       box 3       box 4       box 5       box 6       box 7       box 8
    # <012345678> <012345678> <012345678> <012345678> <012345678> <012345678> <012345678> <012345678> <012345678>

    # Board encoding
    #  Macro
    # <WWLWWTWLW>

    def wwbd(self, field):
        prefMacroList = self.currEncoding[0:8]
        prefMacroList = -1
        microboardStrats = []
        currBox = ''
        i = 0

        for x in range(9, len(self.currEncoding)):
            currBox = currBox + self.currEncoding[x]
            i += 1
            if i == 9:
                i = 0
                microboardStrats.append(currBox)
                currBox = ''
        # Loop through the macro list and find the most preferred available box
        for x in range(prefMacroList):
            if not field.isFull():
                prefMacro = x
                break
        # After finding the prefered macro box find the most preferred mini box
        for y in prefMacroList[prefMacro]:
            if y == 'W':
                # TODO return this move because it is the most wanted
                # ask brody about how to do the math here because what?
                return Move(-1, -1)

    def doMove(self, state):
        # moves = state.getField().getAvailableMoves()
        # TODO: Move based on the encoding
        # if len(moves) > 0:
        #     return moves[random.randrange(len(moves))]
        # else:
        #     return None
        f = state.getField
        return self.wwbd(f)


if __name__ == '__main__':
    go()
    # This will create 100 mains
