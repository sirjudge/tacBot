#!/usr/bin/env python3
from util import *
import random, subprocess, json


# Thank you Julian for these two methods
def load_from_json():
    with open('resultfile.json') as f:
        data = json.load(f)
    winner = jsonDataToWinner(data)
    f.close()
    return winner


def jsonDataToWinner(data):
    return json.loads(data['details'])['winner']


def go():
    # create a botStarter object
    bot = BotStarter()
    # create a parser for the bot
    parser = BotParser(bot)
    # Comment/uncomment the line below to start/stop the parser from actually running
    parser.run()
    with open('gymScores.txt', 'r+') as fileOut:
        winnerID = load_from_json()
        if winnerID == 0:
            fscore = 1
        else:
            fscore = -1
        fileOut.write(str(bot.getGene()) + ',' + str(fscore) + '\n')
        fileOut.close()
        bot.outLog.write("is this working or not working\n")
    bot.outLog.close()


class BotStarter:
    outLog = Log()
    # Holds the current gene number we are working with
    currGene = ''
    currFilename = ''

    def __init__(self):
        random.seed()  # helps create a more random environment
        # set the current gene num we are working with
        self.currGene = open('geneList.txt', 'r+').readline()[:-1]
        # set the current file name of the encoding
        self.currFilename = 'encoding' + str(self.currGene) + '.txt'
        #  delete the first line of the file so we know that we have done that particular run
        self.delFirstLine('geneList.txt')


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
        # Return the current field object
        currField = state.getField()
        evalReturn = currField.evalMacroboard()
        encodingNeeded = self.grepSearch(evalReturn, self.currFilename)[1]
        availableBox = []
        for x in range(0, 9):
            for y in range(0, 9):
                if currField.isInActiveMicroboard(x, y):
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
            avBox = availableBox[0]
            if openBox == '0':
                # top left
                if currField.isActiveSpace(topLeft[avBox][0], topLeft[avBox][1]):
                    Move(topLeft[avBox][0], topLeft[avBox][1])

            elif openBox == '1':
                # top middle
                if currField.isActiveSpace(topMiddle[avBox][0], topMiddle[avBox][1]):
                    return Move(topMiddle[avBox][0], topMiddle[avBox][1])

            elif openBox == '2':
                # top right
                if currField.isActiveSpace(topRight[avBox][0], topRight[avBox][1]):
                    return Move(topRight[avBox][0], topRight[avBox][1])

            elif openBox == '3':
                # Middle left
                if currField.isActiveSpace(middleLeft[avBox][0], middleLeft[avBox][1]):
                    return Move(middleLeft[avBox][0], middleLeft[avBox][1])

            elif openBox == '4':
                # Middle middle
                if currField.isActiveSpace(middleMiddle[avBox][0], middleMiddle[avBox][1]):
                    return Move(middleMiddle[avBox][0], middleMiddle[avBox][1])

            elif openBox == '5':
                # Middle right
                if currField.isActiveSpace(middleRight[avBox][0], middleRight[avBox][1]):
                    return Move(middleRight[avBox][0], middleRight[avBox][1])

            elif openBox == '6':
                # Bottom left
                if currField.isActiveSpace(bottomLeft[avBox][0], bottomLeft[avBox][1]):
                    return Move(bottomLeft[avBox][0], bottomLeft[avBox][1])

            elif openBox == '7':
                # Bottom middle
                if currField.isActiveSpace(bottomMiddle[avBox][0], bottomMiddle[avBox][1]):
                    return Move(bottomMiddle[avBox][0], bottomMiddle[avBox][1])

            elif openBox == '8':
                # Bottom right
                if currField.isActiveSpace(bottomRight[avBox][0], bottomRight[avBox][1]):
                    return Move(bottomRight[avBox][0], bottomRight[avBox][1])

    def doMove(self, state):
        bestMove = self.wwbd2(state)
        if bestMove == Move(42, 42):
            self.outLog.write('bestMove returned 42,42 YOU HAVE AN ERROR DUMMY')
            moves = state.getField().getAvailableMoves()
            if len(moves) > 0:
                return moves[random.randrange(len(moves))]
        else:
            return bestMove


if __name__ == '__main__':
    go()
