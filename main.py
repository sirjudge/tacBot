#!/usr/bin/env python3
from util import *
import random
import json
import subprocess


def go():
    # create a botStarter object
    bot = BotStarter()
    # create a parser for the bot
    parser = BotParser(bot)
    # Comment/uncomment the line below to start/stop the parser from actually running
    parser.run()


class BotStarter:
    # Holds the current gene number we are working with
    currGene = ''
    currFilename = ''

    def __init__(self):
        random.seed()  # helps create a more random environment
        # Uncomment below if you want to re-create a random set of encodings AKA Gen 1
        # d.createRandomFile()
        # set the current gene num we are working with
        # outFile = open('out.txt', 'r+')
        # outFile.truncate()
        self.currGene = open('geneList.txt', 'r+').readline()
        if len(self.currGene) > 1:
            self.currGene = self.currGene[0]
        # outFile.write('currGene = <' + self.currGene + '>\n')
        # set the current file name of the encoding
        self.currFilename = 'encoding' + str(self.currGene) + '.txt'
        #  delete the first line of the file so we know that we have done that particular run
        self.delFirstLine(self.currFilename)
        # outFile.write('finished initializing botStarter\n')

    @staticmethod
    def delFirstLine(fName):
        # reads file and loads it into data variable
        with open(fName, 'r') as fin:
            data = fin.read().splitlines(True)
        # open the file again in write mode, and rewrite the file line by line ignoring the first line in the file
        with open(fName, 'w') as fout:
            fout.writelines(data[1:])
        fout.close()
        fin.close()

    def getGene(self):
        return self.currGene

    # Thank you Julian for these two methods
    def load_from_json(self):
        with open('resultfile.json') as f:
            data = json.load(f)
        winner = self.jsonDataToWinner(data)
        f.close()
        return winner

    @staticmethod
    def jsonDataToWinner(data):
        return json.loads(data['details'])['winner']

    # Use grep command to search through encoding file for the first line that the string is in
    @staticmethod
    def grepSearch(searchString, fileName):
        hosts_process = subprocess.Popen(['grep', searchString, fileName], stdout=subprocess.PIPE)
        hosts_out, hosts_err = hosts_process.communicate()
        stratLookup = str(hosts_out)[2:-3]
        eandsList = stratLookup.split(',')
        return eandsList

    # What would brody do 2: the superior version of wwbd().
    # It takes in a state will return a move based on the strat for the given board encoding
    def wwbd2(self, state):
        currField = state.getField()
        outFile = open('out.txt', 'r+')
        outFile.truncate()
        outFile.truncate(str(currField))
        evalReturn = currField.evalMacroboard()
        encodingNeeded = self.grepSearch(evalReturn, self.currFilename)
        # if the length of the
        if len(encodingNeeded) == 0:
            randomList = random.sample(range(9), 9)
            for box in randomList:
                if box == 0:
                    for x in range(0, 2):
                        for y in range(0, 2):
                            if state.getField().isInActiveMicroBoard(x, y) and state.getField().isisActiveSpace(x, y):
                                return Move(x, y)
                if box == 1:
                    for x in range(3, 5):
                        for y in range(0, 2):
                            if state.getField().isInActiveMicroBoard(x, y) and state.getField().isisActiveSpace(x, y):
                                return Move(x, y)
                if box == 2:
                    for x in range(6, 8):
                        for y in range(0, 2):
                            if state.getField().isInActiveMicroBoard(x, y) and state.getField().isisActiveSpace(x, y):
                                return Move(x, y)
                    # ROW 2
                    # =============================
                if box == 3:
                    for x in range(0, 2):
                        for y in range(3, 5):
                            if state.getField().isInActiveMicroBoard(x, y) and state.getField().isisActiveSpace(x, y):
                                return Move(x, y)
                if box == 4:
                    for x in range(3, 5):
                        for y in range(0, 2):
                            if state.getField().isInActiveMicroBoard(x, y) and state.getField().isisActiveSpace(x, y):
                                return Move(x, y)
                if box == 5:
                    for x in range(6, 8):
                        for y in range(3, 5):
                            if state.getField().isInActiveMicroBoard(x, y) and state.getField().isisActiveSpace(x, y):
                                return Move(x, y)
                    # ROW 3
                    # =============================
                if box == 6:
                    for x in range(0, 2):
                        for y in range(6, 8):
                            if state.getField().isInActiveMicroBoard(x, y) and state.getField().isisActiveSpace(x, y):
                                return Move(x, y)
                if box == 7:
                    for x in range(3, 5):
                        for y in range(6, 8):
                            if state.getField().isInActiveMicroBoard(x, y) and state.getField().isisActiveSpace(x, y):
                                return Move(x, y)
                if box == 8:
                    for x in range(6, 8):
                        for y in range(6, 8):
                            if state.getField().isInActiveMicroBoard(x, y) and state.getField().isisActiveSpace(x, y):
                                return Move(x, y)
        else:
            eandsList = encodingNeeded
            # Below searches for the needed strategy for the given encoding at the time of the move
            # encoding of board
            # print(eandsList[0])
            # given strategy for that board
            # print(eandsList[1])

            # For each box in the preferredBoxes
            #   depending on the box number -> choose x and y values for everything in that microboard
            #   loop through all the spaces in that mini board
            #   if the space is free and the board is active:
            #       return that move
            #   else if board is not active:
            #       go check the next box

            for box in eandsList:
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
        bestMove = self.wwbd2(state)
        # outFile = open('out.txt', 'r+')
        # outFile.truncate()
        # outFile.write('moveX:' + str(bestMove.getX()()) + ' moveY:' + (bestMove.getY()))
        return bestMove


if __name__ == '__main__':
    go()
