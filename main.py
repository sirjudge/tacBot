#!/usr/bin/env python3
from util import *
import robotStarter
import random
import json
import subprocess


def go():
    file = open('geneList.txt')

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
        # TODO: Create a file, its sole purpose is to hold a single number. That number will be the current gene I am on
        # TODO: every time I finish a game I should erase the file and write the next number until I get to 10
        # TODO: if count == 10: count = 0
        # TODO: that way I can easily keep track of stuff

    def load_from_json(self):
        with open('resultfile.txt') as f:
            data = json.load(f)
        winner = self.jsonDataToWinner(data)
        return winner

    @staticmethod
    def jsonDataToWinner(data):
        return json.loads(data['details'])['winner']

    # this method has been named wwbd() or better known as what would brody do, an adaptation of the popular
    # phrase, 'what would jesus do'. This is where the encoding will be evaluated and return a move based on
    # what the current encodings are

    # Use grep command to search through encoding file for the first line that the string is in
    @staticmethod
    def grepSearch(searchString, fileName):
        hosts_process = subprocess.Popen(['grep', searchString, fileName], stdout=subprocess.PIPE)
        hosts_out, hosts_err = hosts_process.communicate()
        stratLookup = str(hosts_out)[2:-3]
        print(stratLookup)
        eandsList = stratLookup.split(',')
        return eandsList

    # What would brody do 2: the superior version of wwbd().
    # It takes in a state and a file name and will return a move based on the strat for the given board encoding
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

        # For each box in the preferredBoxes
        #   depending on the box number -> choose x and y values for everything in that microboard
        #   loop through all the spaces in that mini board
        #   if the space is free and the board is active:
        #       return that move
        #   else if board is not active:
        #       go check the next box
        for box in eandsList[1]:
            # ROW 1
            # =============================
            if box == 0:
                for x in range(0, 2):
                    for y in range(0, 2):
                        if not state.getField().isInActiveMicroBoard(x, y):
                            break
                        if state.getField().isInActiveMicroBoard(x, y) and state.getField().isisActiveSpace(x, y):
                            return Move(x, y)
            elif box == 1:
                for x in range(3, 5):
                    for y in range(0, 2):
                        if not state.getField().isInActiveMicroBoard(x, y):
                            break
                        if state.getField().isInActiveMicroBoard(x, y) and state.getField().isisActiveSpace(x, y):
                            return Move(x, y)
            elif box == 2:
                for x in range(6, 8):
                    for y in range(0, 2):
                        if not state.getField().isInActiveMicroBoard(x, y):
                            break
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
        bestMove = self.wwbd2(state)
        file = open('out.txt')
        file.write('MoveX:' + str(bestMove.getX()) + ' MoveY:' + str(bestMove.getY()))
        return bestMove


if __name__ == '__main__':
    go()
