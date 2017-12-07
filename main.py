#!/usr/bin/env python3
from util import *
import random
import json
import subprocess
from util import Log


def go():
    # create a botStarter object
    bot = BotStarter()
    # create a parser for the bot
    parser = BotParser(bot)
    # Comment/uncomment the line below to start/stop the parser from actually running
    parser.run()
    bot.outLog.close()


class BotStarter:
    outLog = Log()
    # Holds the current gene number we are working with
    currGene = ''
    currFilename = ''

    def __init__(self):
        self.outLog.write('starting initialization of BotStarter\n')
        random.seed()  # helps create a more random environment
        # set the current gene num we are working with
        self.currGene = open('geneList.txt', 'r+').readline()[:-1]
        self.outLog.write('Working with gene number ' + str(self.currGene) + '\n')
        # set the current file name of the encoding
        self.currFilename = 'encoding' + str(self.currGene) + '.txt'
        #  delete the first line of the file so we know that we have done that particular run
        self.delFirstLine('geneList.txt')
        self.outLog.write('finished initializing BotStarter\n')

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
    def grepSearch(self, searchString, fileName):
        strat = ''
        hosts_process = subprocess.Popen(['grep', searchString, fileName], stdout=subprocess.PIPE)
        hosts_out, hosts_err = hosts_process.communicate()
        # if it found the lookup return that
        if hosts_out:
            stratLookup = str(hosts_out)[2:-3]
            eandsList = stratLookup.split(',')
            self.outLog.write('strat found, encoding:' + eandsList[1] + '\n')
            return eandsList
        # if it didn't find the lookup randomly move
        else:
            randomList = random.sample(range(9), 9)
            for elem in randomList:
                strat += str(elem)
            self.outLog.write('start not found, using encoding:' + strat + '\n')
            return [searchString, strat]

    @staticmethod
    def isInAvailableMoves(state, x, y):
        currField = state.getField()
        moves = currField.getAvailableMoves()
        if Move(x, y) in moves:
            return True
        else:
            return False

    # What would brody do 2: the superior version of wwbd().
    # It takes in a state will return a move based on the strat for the given board encoding
    def wwbd2(self, state):
        self.outLog.write('starting wwbd2\n')
        fileOut = open('out.txt', 'r+')
        fileOut.truncate()
        # Return the current field object
        currField = state.getField()
        evalReturn = currField.evalMacroboard()
        fileOut.write(currField.toString())
        encodingNeeded = self.grepSearch(evalReturn, self.currFilename)[1]
        self.outLog.write('encodingNeeded:' + encodingNeeded + '\n')
        eandsList = encodingNeeded
        # if it returns the move 42,42 then we are screwed :(
        # For each box in the preferredBoxes
        #   depending on the box number -> choose x and y values for everything in that microboard
        #   loop through all the spaces in that mini board
        #   if the space is free and the board is active:
        #       return that move
        #   else if board is not active:
        #       go check the next box
        # 012345678
        availableBox = []
        fileOut.write('is board 0 active? ' + str(currField.isInActiveMicroboard(0, 0)) + '\n')
        fileOut.write('is board 1 active? ' + str(currField.isInActiveMicroboard(3, 0)) + '\n')
        fileOut.write('is board 2 active? ' + str(currField.isInActiveMicroboard(6, 0)) + '\n')
        fileOut.write('is board 3 active? ' + str(currField.isInActiveMicroboard(0, 3)) + '\n')
        fileOut.write('is board 4 active? ' + str(currField.isInActiveMicroboard(3, 3)) + '\n')
        fileOut.write('is board 5 active? ' + str(currField.isInActiveMicroboard(6, 3)) + '\n')
        fileOut.write('is board 6 active? ' + str(currField.isInActiveMicroboard(0, 6)) + '\n')
        fileOut.write('is board 7 active? ' + str(currField.isInActiveMicroboard(3, 6)) + '\n')
        fileOut.write('is board 8 active? ' + str(currField.isInActiveMicroboard(6, 6)) + '\n')

        # print the macro board
        countey = 0
        for thing in currField.getMacroBoard():
            for thingy in thing:
                fileOut.write('box:' + str(countey) + '=' + thingy + '\n')
                countey += 1

        for x in range(0, 9):
            # fileOut.write('when checking available box x=' + str(x) +'\n')
            for y in range(0, 9):
                # fileOut.write('when checking available box y=' + str(y) + '\n')
                if currField.isInActiveMicroboard(x, y):
                    fileOut.write('x:' + str(x) + '  y:' + str(y) + '\n')
                    # ROW ONE #
                    if 0 <= x <= 2 and 0 <= y <= 2:
                        availableBox.append(0)
                    elif 3 <= x <= 5 and 0 <= y <= 2:
                        availableBox.append(1)
                    elif 6 <= x <= 8 and 0 <= y <= 2:
                        availableBox.append(2)
                    # ROW TWO #
                    elif 0 <= x <= 2 and 3 <= y <= 5:
                        availableBox.append(3)
                    elif 3 <= x <= 5 and 3 <= y <= 5:
                        availableBox.append(4)
                    elif 6 <= x <= 8 and 3 <= y <= 5:
                        availableBox.append(5)
                    # ROW THREE #
                    elif 0 <= x <= 2 and 6 <= y <= 8:
                        availableBox.append(6)
                    elif 2 <= x <= 5 and 6 <= y <= 8:
                        availableBox.append(7)
                    elif 6 <= x <= 8 and 6 <= y <= 8:
                        availableBox.append(8)
        # checked
        topLeft = [
            (0, 0), (3, 0), (6, 0), (0, 3), (3, 3), (6, 3), (0, 6), (3, 6), (6, 6)
        ]
        # checked
        topMiddle = [
            (1, 0), (4, 0), (7, 0), (1, 3), (4, 3), (7, 3), (1, 6), (4, 6), (7, 6)
        ]
        # checked
        topRight = [
            (2, 0), (5, 0), (8, 0), (2, 3), (5, 3), (8, 3), (2, 6), (5, 6), (8, 6)
        ]
        # checked
        # This one was wrong lol
        middleLeft = [
            (0, 1), (3, 1), (6, 1), (0, 4), (3, 4), (6, 4), (0, 7), (3, 7), (6, 7)
        ]
        # checked
        middleMiddle = [
            (1, 1), (4, 1), (7, 1), (1, 4), (4, 4), (7, 4), (1, 7), (4, 7), (7, 7)
        ]
        # checked
        middleRight = [
            (2, 1), (5, 1), (8, 1), (2, 4), (5, 4), (8, 4), (2, 7), (5, 7), (8, 7)
        ]
        # checked
        bottomLeft = [
            (0, 2), (3, 2), (6, 2), (0, 5), (3, 5), (6, 5), (0, 8), (3, 8), (6, 8)
        ]
        # checked
        bottomMiddle = [
            (1, 2), (4, 2), (7, 2), (1, 5), (4, 5), (7, 5), (1, 8), (4, 8), (7, 8)
        ]
        bottomRight = [
            (2, 2), (5, 2), (8, 2), (2, 5), (5, 5), (8, 5), (2, 8), (5, 8), (8, 8)
        ]

        # availableBox = list(set(availableBox))
        for openBox in encodingNeeded:
            fileOut.write('openBox:' + str(openBox) + '\n')
            avBox = availableBox[0]
            if openBox == '0':
                # top left
                """for x in topLeft:
                    fileOut.write('x:' + str(x[0]) + '  y:' + str(x[1]) + '\n')
                    fileOut.write('if statement:' + str(currField.isActiveSpace(x[0], x[1])
                                                        and currField.isInActiveMicroboard(x[0], x[1])) + '\n')
                    #if currField.isActiveSpace(x[0], x[1]):
                    #    return Move(x[0], x[1])"""
                if currField.isActiveSpace(topLeft[avBox][0], topLeft[avBox][1]):
                    Move(topLeft[avBox][0], topLeft[avBox][1])

            elif openBox == '1':
                # top middle
                """for x in topMiddle:
                    fileOut.write('x:' + str(x[0]) + '  y:' + str(x[1]) + '\n')
                    fileOut.write('if statement:' + str(currField.isActiveSpace(x[0], x[1])
                                                        and currField.isInActiveMicroboard(x[0], x[1])) + '\n')
                    if currField.isActiveSpace(x[0], x[1]):
                        return Move(x[0], x[1])"""
                if currField.isActiveSpace(topMiddle[avBox][0], topMiddle[avBox][1]):
                    return Move(topMiddle[avBox][0], topMiddle[avBox][1])

            elif openBox == '2':
                #top right
                """
                # top right
                for x in topRight:
                    fileOut.write('x:' + str(x[0]) + '  y:' + str(x[1]) + '\n')
                    fileOut.write('if statement:' + str(currField.isActiveSpace(x[0], x[1])
                                                        and currField.isInActiveMicroboard(x[0], x[1])) + '\n')
                    if currField.isActiveSpace(x[0], x[1]):
                        return Move(x[0], x[1])"""
                if currField.isActiveSpace(topRight[avBox][0], topRight[avBox][1]):
                    return Move(topRight[avBox][0], topRight[avBox][1])

            elif openBox == '3':
                # Middle left
                """for x in middleLeft:
                    fileOut.write('x:' + str(x[0]) + '  y:' + str(x[1]) + '\n')
                    fileOut.write('if statement:' + str(currField.isActiveSpace(x[0], x[1])
                                                        and currField.isInActiveMicroboard(x[0], x[1])) + '\n')
                    if currField.isActiveSpace(x[0], x[1]):
                        return Move(x[0], x[1])"""
                if currField.isActiveSpace(middleLeft[avBox][0], middleLeft[avBox][1]):
                    return Move(middleLeft[avBox][0], middleLeft[avBox][1])

            elif openBox == '4':
                # Middle middle
                """for x in middleMiddle:
                    fileOut.write('x:' + str(x[0]) + '  y:' + str(x[1]) + '\n')
                    fileOut.write('if statement:' + str(currField.isActiveSpace(x[0], x[1])
                                                        and currField.isInActiveMicroboard(x[0], x[1])) + '\n')
                    #if currField.isActiveSpace(x[0], x[1]):
                    #    return Move(x[0], x[1])"""
                if currField.isActiveSpace(middleMiddle[avBox][0], middleMiddle[avBox][1]):
                    return Move(middleMiddle[avBox][0], middleMiddle[avBox][1])

            elif openBox == '5':
                # Middle right
                """for x in middleRight:
                    fileOut.write('x:' + str(x[0]) + '  y:' + str(x[1]) + '\n')
                    fileOut.write('if statement:' + str(currField.isActiveSpace(x[0], x[1])
                                                        and currField.isInActiveMicroboard(x[0], x[1])) + '\n')
                    if currField.isActiveSpace(x[0], x[1]):
                        return Move(x[0], x[1])"""
                if currField.isActiveSpace(middleRight[avBox][0], middleRight[avBox][1]):
                    return Move(middleRight[avBox][0], middleRight[avBox][1])

            elif openBox == '6':

                # Bottom left
                """for x in bottomLeft:
                    fileOut.write('x:' + str(x[0]) + '  y:' + str(x[1]) + '\n')
                    fileOut.write('if statement:' + str(currField.isActiveSpace(x[0], x[1])
                                                        and currField.isInActiveMicroboard(x[0], x[1])) + '\n')
                    if currField.isActiveSpace(x[0], x[1]):
                        return Move(x[0], x[1])"""
                if currField.isActiveSpace(bottomLeft[avBox][0], bottomLeft[avBox][1]):
                    return Move(bottomLeft[avBox][0], bottomLeft[avBox][1])

            elif openBox == '7':
                # Bottom middle
                """for x in bottomMiddle:
                    fileOut.write('x:' + str(x[0]) + '  y:' + str(x[1]))
                    fileOut.write('if statement:' + str(currField.isActiveSpace(x[0], x[1])
                                                        and currField.isInActiveMicroboard(x[0], x[1])))
                    if currField.isActiveSpace(x[0], x[1]):
                        return Move(x[0], x[1])"""
                if currField.isActiveSpace(bottomMiddle[avBox][0], bottomMiddle[avBox][1]):
                    return Move(bottomMiddle[avBox][0], bottomMiddle[avBox][1])

            elif openBox == '8':
                # Bottom right
                """for x in bottomRight:
                    fileOut.write('x:' + str(x[0]) + '  y:' + str(x[1]) + '\n')
                    fileOut.write('if statement:' + str(currField.isActiveSpace(x[0], x[1])
                                                        and currField.isInActiveMicroboard(x[0], x[1])) + '\n')
                    if currField.isActiveSpace(x[0], x[1]):
                        return Move(x[0], x[1])"""
                if currField.isActiveSpace(bottomRight[avBox][0], bottomRight[avBox][1]):
                    return Move(bottomRight[avBox][0], bottomRight[avBox][1])

            """for box in eandsList:
                # Row 1
                if box ==also m '0':
                    xRange = [0, 1, 2]
                    yRange = [0, 1, 2]
                elif box == '1':
                    xRange = [3, 4, 5]
                    yRange = [0, 1, 2]
                elif box == '2':
                    xRange = [6, 7, 8]
                    yRange = [0, 1, 2]
                # Row 2
                elif box == '3':
                    xRange = [0, 1, 2]
                    yRange = [3, 4, 5]
                elif box == '4':
                    xRange = [3, 4, 5]
                    yRange = [3, 4, 5]
                elif box == '5':
                    xRange = [6, 7, 8]
                    yRange = [3, 4, 5]
                # Row 3
                elif box == '3':
                    xRange = [0, 1, 2]
                    yRange = [6, 7, 8]
                elif box == '4':
                    xRange = [3, 4, 5]
                    yRange = [6, 7, 8]
                elif box == '5':
                    xRange = [6, 7, 8]
                    yRange = [6, 7, 8]


        BELOW IS CODE I WROTE THAT MAYBE DOESN'T WORK I DON'T KNOW ANYMORE
        WHAT IS REALITY
        I AM A FRACTURED VERSION OF MY OWN SELF
        * E X E S T E N T I A L    D R E A D *
        for box in eandsList:
            fileOut.write('Box:' + str(box) + '\n')
            # ROW 1
            # =============================
            if box == '0':
                for x in range(0, 3):
                    for y in range(0, 3):
                        # Print Statements
                        #fileOut.write('x:' + str(x) + ' y:' + str(y) + '\n')
                        #fileOut.write('isInActiveMicroboard:' + str(currField.isInActiveMicroboard(x, y)) + '\n')
                        #fileOut.write('isAcitveSpace:' + str(currField.isActiveSpace(x, y)) + '\n')
                        #fileOut.write('isInAvailableMoves:' + str(self.isInAvailableMoves(state, x, y)) + '\n')

                        # if microBoard is active and the space is empty
                        if currField.isInActiveMicroboard(x, y) and currField.isActiveSpace(x, y):
                        #if self.isInAvailableMoves(state, x, y):
                            fileOut.write('Move:(' + str(x) + ',' + str(y) + ')\n')
                            return Move(x, y)
            elif box == '1':
                for x in range(3, 6):
                    for y in range(0, 3):
                        #fileOut.write('x:' + str(x) + ' y:' + str(y) + '\n')
                        #fileOut.write('isInActiveMicroboard:' + str(currField.isInActiveMicroboard(x, y)) + '\n')
                        #fileOut.write('isAcitveSpace:' + str(currField.isActiveSpace(x, y)) + '\n')
                        #fileOut.write('isInAvailableMoves:' + str(self.isInAvailableMoves(state, x, y)) + '\n')

                        # if microBoard is active and the space is empty
                        #if self.isInAvailableMoves(state, x, y):
                        if currField.isInActiveMicroboard(x,y) and currField.isActiveSpace(x, y):
                            fileOut.write('Move:(' + str(x) + ',' + str(y) + ')\n')
                            return Move(x, y)
            elif box == '2':
                for x in range(6, 9):
                    for y in range(0, 3):
                        #fileOut.write('x:' + str(x) + ' y:' + str(y) + '\n')
                        #fileOut.write('isInActiveMicroboard:' + str(currField.isInActiveMicroboard(x, y)) + '\n')
                        #fileOut.write('isAcitveSpace:' + str(currField.isActiveSpace(x, y)) + '\n')
                        #fileOut.write('isInAvailableMoves:' + str(self.isInAvailableMoves(state, x, y)) + '\n')

                        # if microBoard is active and the space is empty
                        if currField.isInActiveMicroboard(x,y) and currField.isActiveSpace(x, y):
                        #if self.isInAvailableMoves(state, x, y):
                            fileOut.write('Move:(' + str(x) + ',' + str(y) + ')\n')
                            return Move(x, y)
            # ROW 2
            # =============================
            elif box == '3':
                for x in range(0, 3):
                    for y in range(3, 6):
                        #fileOut.write('x:' + str(x) + ' y:' + str(y) + '\n')
                        #fileOut.write('isInActiveMicroboard:' + str(currField.isInActiveMicroboard(x, y)) + '\n')
                        #fileOut.write('isAcitveSpace:' + str(currField.isActiveSpace(x, y)) + '\n')
                        #fileOut.write('isInAvailableMoves:' + str(self.isInAvailableMoves(state, x, y)) + '\n')

                        # if microBoard is active and the space is empty
                        if currField.isInActiveMicroboard(x,y) and currField.isActiveSpace(x, y):
                        #if self.isInAvailableMoves(state, x, y):
                            fileOut.write('Move:(' + str(x) + ',' + str(y) + ')\n')
                            return Move(x, y)
            elif box == '4':
                for x in range(3, 6):
                    for y in range(3, 6):
                        # Print Statements
                        #fileOut.write('x:' + str(x) + ' y:' + str(y) + '\n')
                        #fileOut.write('isInActiveMicroboard:' + str(currField.isInActiveMicroboard(x, y)) + '\n')
                        #fileOut.write('isAcitveSpace:' + str(currField.isActiveSpace(x, y)) + '\n')
                        #fileOut.write('isInAvailableMoves:' + str(self.isInAvailableMoves(state, x, y)) + '\n')

                        # if microBoard is active and the space is empty
                        if currField.isInActiveMicroboard(x, y) and currField.isActiveSpace(x, y):
                        # if self.isInAvailableMoves(state, x, y):
                            return Move(x, y)
            elif box == '5':
                for x in range(6, 9):
                    for y in range(3, 6):
                        # Print Statements
                        #fileOut.write('x:' + str(x) + ' y:' + str(y) + '\n')
                        #fileOut.write('isInActiveMicroboard:' + str(currField.isInActiveMicroboard(x, y)) + '\n')
                        #fileOut.write('isAcitveSpace:' + str(currField.isActiveSpace(x, y)) + '\n')
                        #fileOut.write('isInAvailableMoves:' + str(self.isInAvailableMoves(state, x, y)) + '\n')
                        #if currField.isInActiveMicroboard(x,y) and currField.isActiveSpace(x, y):
                        # if microBoard is active and the space is empty
                        if self.isInAvailableMoves(state, x, y):
                            fileOut.write('Move:(' + str(x) + ',' + str(y) + ')\n')
                            return Move(x, y)
            # ROW 3
            # =============================
            elif box == '6':
                for x in range(0, 3):
                    for y in range(6, 9):
                        # Print Statements
                        #fileOut.write('x:' + str(x) + ' y:' + str(y) + '\n')
                        #fileOut.write('isInActiveMicroboard:' + str(currField.isInActiveMicroboard(x, y)) + '\n')
                        #fileOut.write('isAcitveSpace:' + str(currField.isActiveSpace(x, y)) + '\n')
                        #fileOut.write('isInAvailableMoves:' + str(self.isInAvailableMoves(state, x, y)) + '\n')

                        if currField.isInActiveMicroboard(x, y) and currField.isActiveSpace(x, y):
                            # if microBoard is active and the space is empty
                            # if self.isInAvailableMoves(state, x, y):
                            fileOut.write('Move:(' + str(x) + ',' + str(y) + ')\n')
                            return Move(x, y)
            elif box == '7':
                for x in range(3, 6):
                    for y in range(6, 9):
                        # Print Statements
                        #fileOut.write('x:' + str(x) + ' y:' + str(y) + '\n')
                        #fileOut.write('isInActiveMicroboard:' + str(currField.isInActiveMicroboard(x, y)) + '\n')
                        #fileOut.write('isAcitveSpace:' + str(currField.isActiveSpace(x, y)) + '\n')
                        #fileOut.write('isInAvailableMoves:' + str(self.isInAvailableMoves(state, x, y)) + '\n')

                        # if microBoard is active and the space is empty
                        #if self.isInAvailableMoves(state, x, y):
                        if currField.isInActiveMicroboard(x,y) and currField.isActiveSpace(x, y):
                            fileOut.write('Move:(' + str(x) + ',' + str(y) + ')\n')
                            return Move(x, y)
            elif box == '8':
                for x in range(6, 9):
                    for y in range(6, 9):
                        # Print Statements
                        #fileOut.write('x:' + str(x) + ' y:' + str(y) + '\n')
                        #fileOut.write('isInActiveMicroboard:' + str(currField.isInActiveMicroboard(x, y)) + '\n')
                        #fileOut.write('isAcitveSpace:' + str(currField.isActiveSpace(x, y)) + '\n')
                        #fileOut.write('isInAvailableMoves:' + str(self.isInAvailableMoves(state, x, y)) + '\n')
                        # if microBoard is active and the space is empty
                        if currField.isInActiveMicroboard(x,y) and currField.isActiveSpace(x, y):
                        #if self.isInAvailableMoves(state, x, y):
                            fileOut.write('Move:(' + str(x) + ',' + str(y) + ')\n')
                            return Move(x, y)
        # should never actually reach this, if it does I don't know how to help :(
        fileOut.write('EMERGENCY, I SHOULD NOT HAVE RETURNED. IF YOU SEE THIS SOMETHING IS VERY WRONG \n')
        return Move(42, 42)"""

    def doMove(self, state):

        bestMove = self.wwbd2(state)
        if bestMove == Move(41, 42):
            moves = state.getField().getAvailableMoves()
            if len(moves) > 0:
                return moves[random.randrange(len(moves))]
        # self.outLog.write('moveX:' + str(bestMove.getX()()) + ' moveY:' + str(bestMove.getY()))
        else:
            return bestMove
        """
        moves = state.getField().getAvailableMoves()
        if len(moves) > 0:
            return moves[random.randrange(len(moves))]
        else:
            return None
        """

if __name__ == '__main__':
    go()
