import sys
import random

# TODO
# 1) Right now evaluations are in a list for each row/col/diag so we have
#    2 or 3 evals to look at. Do something with that
# 2) We need to do something with the evals to turn them into an encoding
# 3) Once we have that encoding we need to log it to a file so we have a log
#    so write to file?
# 4) Also I need to actually evaluate a move first, so do that please
# 5) Make sure mutate function mutates correctly
# 6) Using encoding base class add functionality so that the encodings are
#    actually being used
# 7) Probably create encodings and tweak crossbreed and mutate chance
# 8) Create fitness evaluation function will be based off win/loss/tie rate
#    plus take into account who went first


class Encoding:
    encodingList = []
    # will be a list of tuples
    # (encoding,fitness score)

    def __init__(self):
        log = open('encoding.txt', 'r+')
        for line in log:
            self.encodingList.append(line)

    def writeToLog(self):
        log = open('encoding.txt', 'r+')
        log.truncate()
        for enc in self.encodingList:
            log.write(enc[0] + '\n')
            log.write(enc[1] + '\n')

    def crossbreed(self, encoding1, encoding2):
        crossChance = random.randint(0, 100)
        crossPlace = random.randint(0, len(encoding1) - 1)
        # Has a 10% chance to crossbreed
        if crossChance <= 10:
            # Separate first encoding
            e1f = encoding1[0:crossPlace]
            e1s = encoding1[0:crossPlace + 1]
            # Separate second encoding
            e2f = encoding2[0:crossPlace]
            e2s = encoding2[0:crossPlace + 1]
        # combine first half of encoding 1 with second half of encoding 2
        ne1 = e1f + e2s
        # combine first half of encoding 2 with second half of encoding 1
        ne2 = e2f + e1s
        # Run both encodings through mutate function
        ne1 = self.mutate(ne1)
        ne2 = self.mutate(ne2)
        # return both encodings
        return ne1, ne2

    @staticmethod
    def mutate(encoding):
        # Choose a random number between 1 and 100 to be our chance to mutate
        mutateChance = random.randint(0, 100)
        out = ''
        # for each number in the encoding
        for x in encoding:
            # 1% chance to mutate to a random strat
            if mutateChance == 42:
                out = out + (random.randint(0, 5))
            # 99% chance to keep the same strat
            else:
                out = out + x
        return out


class Field:
    __EMPTY_FIELD = "."  # value for an empty field on microboard
    __AVAILABLE_FIELD = "-1"  # you can move on the macroboard
    __NUM_COLS = 9  # number of columns
    __NUM_ROWS = 9  # number of rows
    __mBoard = []  # micro board
    __mMacroboard = []  # macro board
    __myId = 0
    __opponentId = 0

    # initializes the entire board to be blank
    def __init__(self):
        null_row = []  # create an empty row
        for col in range(self.__NUM_COLS):  # for every column add an empty_field variable
            null_row.append(self.__EMPTY_FIELD)
        for row in range(self.__NUM_ROWS):  # for every row append the empty column list
            self.__mBoard.append(list(null_row))
        # Macroboard
        # Does the same thing as above but for the big outside board
        null_row = []
        for col in range(self.__NUM_COLS // 3):
            null_row.append(self.__EMPTY_FIELD)
        for row in range(self.__NUM_ROWS // 3):
            self.__mMacroboard.append(list(null_row))

    # sets the values of the board from a given string s of inputs
    def parseFromString(self, s):
        s = s.replace(";", ",")  # replaces ';' with ','
        r = s.split(",")  # separates the new string into a list using , as the split point
        counter = 0  # Counter variable
        # Loop through the board and set the value of board[x][y] to be the
        # correct value from the input list r -> ie X or O
        for y in range(self.__NUM_ROWS):
            for x in range(self.__NUM_COLS):
                self.__mBoard[x][y] = r[counter]
                counter += 1

    # Similar to the above method except for the Macroboard instead of the microboard
    def parseMacroboardFromString(self, s):
        r = s.split(",")
        counter = 0
        for y in range(3):
            for x in range(3):
                self.__mMacroboard[x][y] = r[counter]
                counter += 1

    # returns a list of available moves
    # ie. any space that hasn't been set in a miniboard that hasn't been finished
    def getAvailableMoves(self):
        moves = []
        for y in range(self.__NUM_ROWS):
            for x in range(self.__NUM_COLS):
                if self.isInActiveMicroboard(x, y) and (self.__mBoard[x][y] == self.__EMPTY_FIELD):
                    moves.append(Move(x, y))
                    # TODO
                    # based off this list of moves we have to look at our encodings and move
        return moves

    # Returns false if the the micro board has been finished
    def isInActiveMicroboard(self, x, y):
        return self.__mMacroboard[x // 3][y // 3] == self.__AVAILABLE_FIELD

    # gets called when trying to print out a field object. Creates a more readable print statement
    def toString(self):
        r = ""
        counter = 0
        for y in range(self.__NUM_ROWS):
            for x in range(self.__NUM_COLS):
                if counter > 0:
                    r += ","
                r += self.__mBoard[x][y]
                counter += 1
        return r

    # if every cell in the board if full return true, else return false
    def isFull(self):
        for y in range(self.__NUM_ROWS):
            for x in range(self.__NUM_COLS):
                if self.__mBoard[x][y] == self.__EMPTY_FIELD:
                    return False
        return True

    # searches through mBoard and if one of the values is empty return true, else return false
    def isEmpty(self):
        for y in range(self.__NUM_ROWS):
            for x in range(self.__NUM_COLS):
                if self.__mBoard[x][y] != self.__EMPTY_FIELD:
                    return False
        return True

    # Getter and setter methods
    def getNrColumns(self):
        return self.__NUM_COLS

    def getNrRows(self):
        return self.__NUM_ROWS

    def getPlayerID(self, x, y):
        return self.__mBoard[x][y]

    def getMyId(self):
        return self.__myId

    def setMyId(self, i):
        self.__myId = i

    def getOpponentId(self):
        return self.__opponentId

    def setOpponentId(self, i):
        self.__opponentId = i

    def eval(self, sList):
        # Counter variable for X and O
        p1Count = 0
        p2Count = 0
        # loop through elements in the passed in list of moves for the board
        # each move is either 'X', 'O', or '_'
        # set up counter variables

        # sList will be horzEval,vertEval,diagEval
        for x in sList:
            for y in x:
                if y == 'X':
                    p1Count += 1
                elif y == 'O':
                    p2Count += 1


        #BELOW THIS IS OLD CODE
        for x in sList:
            if x == 'X':
                p1Count += 1
            elif x == 'O':
                p2Count += 1
        # Evaluates what case the board is in
        # TODO --> add a table here that says what each thing does
        if p1Count == 2 and p2Count == 0:
            return 3
        elif p1Count == 1 and p2Count == 0:
            return 2
        elif p1Count == 0 and p2Count == 0:
            return 1
        if p2Count == 2 and p1Count == 0:
            return 4
        if p2Count == 1 and p1Count == 0:
            return 5
    # ABOVE THIS IS OLD CODE

    # TODO: moves are done using playerID not X or O - usually an integer, 0 or 1
    # checks how close a win case is for horizontal, vertical, and horizontal
    def horizontal(self):
        currRow = []
        rowEvals = []
        bNumList = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

        for x in bNumList:
            for y in x:
                if self.__mMacroboard[y] == self.getPlayerID():
                    currRow.append('X')
                elif self.__mMacroboard[y] == self.__EMPTY_FIELD or self.__mMacroboard[x] == self.__AVAILABLE_FIELD:
                    currRow.append('_')
                else:
                    currRow.append('O')
            rowEvals.append(self.eval(currRow), currRow)
            currRow = []
        return rowEvals

    def vertical(self):
        currRow = []
        colEvals = []
        bNumList = [[0, 3, 4], [1, 4, 7], [2, 5, 8]] #three different columns

        for x in bNumList:
            for y in x:
                if self.__mMacroboard[y] == self.getPlayerID():
                    currRow.append('X')
                elif self.__mMacroboard[y] == self.__EMPTY_FIELD or self.__mMacroboard[y] == self.__AVAILABLE_FIELD:
                    currRow.append('_')
                else:
                    currRow.append('O')
            colEvals.append(self.eval(currRow), currRow)
            currRow = []
        return colEvals

    # works similar to vertical and horizontal, see above comments
    def diagonal(self):
        currDiag = []
        bNumList = [[0, 4, 8], [2, 4, 6]]
        diagEvals = []
        for x in bNumList:
            for y in x:
                if self.__mMacroboard[y] == self.getPlayerID():
                    currDiag.append('X')
                elif self.__mMacroboard[y] == self.__EMPTY_FIELD or self.__mMacroboard[y] == self.__AVAILABLE_FIELD:
                    currDiag.append('_')
                else:
                    currDiag.append('O')
            diagEvals.append(self.eval(currDiag), currDiag)
        return diagEvals

    def threevalToEncode(self, horz, vert, diag):
        # one eval for each row
        horzEval1 = horz[0][0]
        horzEval2 = horz[0][1]
        horzEval3 = horz[0][2]

        # One eval for each column
        vertEval1 = vert[0][0]
        vertEval2 = vert[0][1]
        vertEval3 = vert[0][2]

        # One eval for each diagonal
        diagEval1 = diag[0][0]
        diagEval2 = diag[0][1]

        row1 = horz[1][0]
        row2 = horz[1][1]
        row3 = horz[1][2]

        currBoard = row1 + row2 + row3
        # TODO: This is where the encoding should be made


# pretty self explanatory class. It has the x and y values of the move you want to make
class Move:
    __x = -1
    __y = -1

    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def toString(self):
        return "place_move {} {}".format(self.__x, self.__y)


# Class for creating a player
class Player:
    __name = ""

    def __init__(self, name):
        self.__name = name


# class for keeping track of current state
class BotState:
    __MAX_TIMEBANK = -1
    __TIME_PER_MOVE = -1

    __roundNumber = -1
    __moveNumber = -1

    __timebank = -1
    __myName = ""
    __players = {}

    __field = None

    def __init__(self):
        self.__field = Field()
        self.__players = {}

    # getter and setter methods
    # they get and set variables....pretty neato stuff
    def setTimebank(self, value):
        self.__timebank = value

    def setMaxTimebank(self, value):
        self.__MAX_TIMEBANK = value

    def setTimePerMove(self, value):
        self.__TIME_PER_MOVE = value

    def setMyName(self, myName):
        self.__myName = myName

    def setRoundNumber(self, roundNumber):
        self.__roundNumber = roundNumber

    def setMoveNumber(self, moveNumber):
        self.__moveNumber = moveNumber

    def getTimebank(self):
        return self.__timebank

    def getRoundNumber(self):
        return self.__roundNumber

    def getMoveNumber(self):
        return self.__moveNumber

    def getPlayers(self):
        return self.__players

    def getField(self):
        return self.__field

    def getMyName(self):
        return self.__myName

    def getMaxTimebank(self):
        return self.__MAX_TIMEBANK

    def getTimePerMove(self):
        return self.__TIME_PER_MOVE


# Class handles parsing of variables and acts upon those variables passed in
class BotParser:
    __bot = None
    __currentState = None
    __log = None

    def __init__(self, bot):
        self.__bot = bot
        self.__currentState = BotState()
        self.__log = Log()

    # prints to stdout when error occurs
    def output(self, msg):
        self.__log.write("Sending: " + msg + " to stdout.")
        print(msg)
        sys.stdout.flush()

    # Until you reach the end of a file and stdin has not been closed, parse the given input
    # and call handle_message() on each input
    def run(self):
        while not sys.stdin.closed:  # while program has not been stopped
            try:
                rawline = sys.stdin.readline()  # read one line from stdin
                # returnss a copy of the string in which all chars have been stripped from the beginning
                # and the end of the string (default whitespace characters)
                line = rawline.strip()
                self.handle_message(line)
            except EOFError:  # if there's an end of file error write to log and close
                self.__log.write('EOF')
                self.__log.close()
        return

    # Handles which method to call when parsing command line
    # sets values using getters and setters
    def handle_message(self, message):
        self.__log.write("bot received: {}\n".format(message))
        parts = message.split(" ")
        if not parts:  # if there is no line to parse then log error
            self.__log.write("Unable to parse line (empty)\n")
        elif parts[0] == 'settings':  # if first word is settings, parse the next to words
            self.parseSettings(parts[1], parts[2])
        elif parts[0] == 'update':
            if parts[1] == "game":
                self.parseGameData(parts[2], parts[3])
        elif parts[0] == 'action':
            if parts[1] == "move":
                if len(parts) > 2:
                    self.__currentState.setTimebank(int(parts[2]))
                move = self.__bot.doMove(self.__currentState)
                if move is not None:
                    # sys.stdout.write(move.toString())
                    self.output(move.toString())
                else:
                    # sys.stdout.write("pass")
                    self.output("pass")
        else:
            self.__log.write("Unknown command: {} \n".format(message))

    # Uses getters and setters to set game values of the board
    def parseSettings(self, key, value):
        try:
            if key == "timebank":
                time = int(value)
                self.__currentState.setMaxTimebank(time)
                self.__currentState.setTimebank(time)
            elif key == "time_per_move":
                self.__currentState.setTimePerMove(int(value))
            elif key == "player_names":
                playerNames = value.split(",")
                for playerName in playerNames:
                    player = Player(playerName)
                    (self.__currentState.getPlayers())[playerName] = player  # Check this
            elif key == "your_bot":
                self.__currentState.setMyName(value)
            elif key == "your_botid":
                myId = int(value)
                opponentId = 2 - myId + 1
                self.__currentState.getField().setMyId(myId)
                self.__currentState.getField().setOpponentId(opponentId)
            else:
                self.__log.write("Unable to parse settings input with key {}".format(key))
        except:
            self.__log.write("Unable to parse settings value {} for key {}".format(value, key))
            # e.printStackTrace()

    # sets game data from passed in inputs
    def parseGameData(self, key, value):
        try:
            if key == "round":
                self.__currentState.setRoundNumber(int(value))
            elif key == "move":
                self.__currentState.setMoveNumber(int(value))
            elif key == "macroboard":
                self.__currentState.getField().parseMacroboardFromString(value)
            elif key == "field":
                self.__currentState.getField().parseFromString(value)
            else:
                self.__log.write("Cannot parse game data input with key {}".format(key))
        except:
            self.__log.write("Cannot parse game data value {} for key {}".format(value, key))
            # e.printStackTrace()


# Class to create, open, and close a log file
class Log:
    __FNAME = "/tmp/bot-log.txt"

    def __init__(self, fname=None):
        if fname is None:
            import os
            pid = os.getpid()
            self.__FNAME = "/tmp/bot-log" + str(pid) + ".txt"
        else:
            self.__FNAME = fname

        self.__FILE = open(self.__FNAME, 'w')

    def write(self, msg):
        self.__FILE.write(msg)

    def close(self):
        self.write("Closing log file.")
        self.__FILE.close()
