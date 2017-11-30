#!/usr/bin/env python3
from util import *
import robotStarter
import re
import random
import json
import subprocess


def go():
    bot = BotStarter()
    parser = BotParser(bot)
    # Comment/uncomment the line below to start/stop the parser from actually running
    parser.run()
    file = open('out.txt', 'r+')
    file.write('Winner = ' + bot.load_from_json())


class BotStarter:
    currEncoding = ''

    def __init__(self):
        random.seed()  # helps create a more random environment
        d = robotStarter.Decoding()
        # Uncomment below if you want to re-create a random set of encodings AKA Gen 1
        # d.createRandomFile()


    # TODO come back to this later
    def load_from_json(self):
        with open('resultfile.txt') as f:
            data = json.load(f)
        winner = self.jsonDataToWinner(data)
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

    """def wwbd(self, field):
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
    
    ABOVE THIS IS OLD CODE. IT DOES NOT WORK FUTURE NICO DON'T USE ANY OF THIS PLEASE. THANK YOU. 
    """
    @staticmethod
    def grepSearch(searchString, fileName):
        hosts_process = subprocess.Popen(['grep', searchString, fileName], stdout=subprocess.PIPE)
        hosts_out, hosts_err = hosts_process.communicate()
        stratLookup = str(hosts_out)[2:-3]
        print(stratLookup)
        eandsList = stratLookup.split(',')
        return eandsList

    def wwbd2(self, fname, state):
        currField = state.getField()
        horzEval = currField.horizontal()
        vertEval = currField.vertical()
        diagEval = currField.diagonal()
        stateList = [horzEval, vertEval, diagEval]
        print(stateList)
        evalReturn = currField.evalMacroboard()
        encodingNeeded = self.grepSearch(evalReturn, fname)
        eandsList = encodingNeeded

        # Below searches for the needed strategy for the given encoding at the time of the move
        # encoding of board
        print(eandsList[0])
        # given strategy for that board
        print(eandsList[1])

        # For each box in the preferedBoxes
        for box in eandsList[1]:
            # ROW 1
            # =============================
            if box == 0:
                for x in range(0, 2):
                    for y in range(0, 2):
                        if state.getField().isInActiveMicroBoard(x, y) and state.getField().isisActiveSpace(x, y):
                            return Move(x, y)
            elif box == 1:
                for x in range(3, 5):
                    for y in range(0, 2):
                        if state.getField().isInActiveMicroBoard(x, y) and state.getField().isisActiveSpace(x, y):
                            return Move(x, y)
            elif box == 2:
                for x in range(6, 8):
                    for y in range(0, 2):
                        if state.getField().isInActiveMicroBoard(x, y) and state.getField().isisActiveSpace(x, y):
                            return Move(x, y)
            # ROW 2
            # =============================
            elif box == 3:
                for x in range(0, 2):
                    for y in range(3, 5):
                        if state.getField().isInActiveMicroBoard(x, y) and state.getField().isisActiveSpace(x, y):
                            return Move(x, y)
            elif box == 4:
                for x in range(3, 5):
                    for y in range(0, 2):
                        if state.getField().isInActiveMicroBoard(x, y) and state.getField().isisActiveSpace(x, y):
                            return Move(x, y)
            elif box == 5:
                for x in range(6, 8):
                    for y in range(3, 5):
                        if state.getField().isInActiveMicroBoard(x, y) and state.getField().isisActiveSpace(x, y):
                            return Move(x, y)
            # ROW 3
            # =============================
            elif box == 6:
                for x in range(0, 2):
                    for y in range(6, 8):
                        if state.getField().isInActiveMicroBoard(x, y) and state.getField().isisActiveSpace(x, y):
                            return Move(x, y)
            elif box == 7:
                for x in range(3, 5):
                    for y in range(6, 8):
                        if state.getField().isInActiveMicroBoard(x, y) and state.getField().isisActiveSpace(x, y):
                            return Move(x, y)
            elif box == 8:
                for x in range(6, 8):
                    for y in range(6, 8):
                        if state.getField().isInActiveMicroBoard(x, y) and state.getField().isisActiveSpace(x, y):
                            return Move(x, y)

    def doMove(self, state):
        # TODO: this logic is wrong. fix it

        moves = state.getField().getAvailableMoves()
        # TODO: Move based on the encoding
        if len(moves) > 0:
            return moves[random.randrange(len(moves))]
        else:
            return None

if __name__ == '__main__':
    go()
    # This will create 100 mains
