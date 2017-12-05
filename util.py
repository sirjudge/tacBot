import sys


class Field:

    # initializes the entire board to be blank
    def __init__(self):
        self.__EMPTY_FIELD = "."  # value for an empty field on microboard
        self.__AVAILABLE_FIELD = "-1"  # you can move on the macroboard
        self.__NUM_COLS = 9  # number of columns
        self.__NUM_ROWS = 9  # number of rows
        self.__mBoard = []  # micro board
        self.__mMacroboard = []  # macro board
        self.__myId = 0
        self.__opponentId = 0

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

    def evalMacroboard(self):
        outEval = ''
        for row in self.__mMacroboard:
            for val in row:
                if val == self.getMyId():
                    outEval += '1'
                elif val == self.getOpponentId():
                    outEval += '0'
                else:
                    outEval += '_'
        return outEval


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

    # Returns true if space x,y is an empty field
    def isActiveSpace(self, x, y):
        return self.__mBoard[x][y] == self.__EMPTY_FIELD

    # returns a list of available moves
    # ie. any space that hasn't been set in a miniboard that hasn't been finished
    def getAvailableMoves(self):
        moves = []
        for y in range(self.__NUM_ROWS):
            for x in range(self.__NUM_COLS):
                if self.isInActiveMicroboard(x, y) and (self.__mBoard[x][y] == self.__EMPTY_FIELD):
                    moves.append(Move(x, y))
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


    @staticmethod
    def eval(sList):
        # Counter variable for X and O
        p1Count = 0
        p2Count = 0
        # loop through elements in the passed in list of moves for the board
        # each move is either 'X', 'O', or '_'
        # set up counter variables

        # sList will be horzEval, vertEval, diagEval
        # X is current player
        # Y is opponent
        # _ is a blank space
        evalList = []
        for typeEval in sList:
            for move in typeEval:
                if move == 'X':
                    p1Count += 1
                elif move == 'O':
                    p2Count += 1
            evalList.append([typeEval, p1Count, p2Count])
        # Evaluates what case the board is in
        # not important
        if p1Count == 0 and p2Count == 0:
            return 1
        # not important
        elif p1Count == 1 and p2Count == 0:
            return 2
        # win for player 1, lose for player 2
        elif p1Count == 2 and p2Count == 0:
            return 3
        # not important
        elif p1Count == 0 and p2Count == 1:
            return 4
        # not important
        elif p1Count == 1 and p2Count == 1:
            return 5
        # win for player 1, lose for player 2
        elif p1Count == 2 and p2Count == 1:
            return 6
        # lose for player 1, win for player 2
        elif p1Count == 0 and p2Count == 2:
            return 7
        # lose for player 1, win for player 2
        elif p1Count == 1 and p2Count == 2:
            return 8
        # Tie for both
        elif p1Count == 2 and p2Count == 2:
            return 9
    
    # moves are done using playerID not X or O - usually an integer, 0 or 1
    # getPlayerID method takes an x and a y argument for where in the board you go
    # checks how close a win case is for horizontal, vertical, and horizontal
    def horizontal(self):
        currRow = []
        rowEvals = []
        bNumList = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

        for x in bNumList:
            for y in x:
                if self.__mMacroboard[y] == self.getMyId():
                    currRow.append('X')
                elif self.__mMacroboard[y] == self.__EMPTY_FIELD or self.__mMacroboard[y] == self.__AVAILABLE_FIELD:
                    currRow.append('_')
                else:
                    currRow.append('O')
            rowEvals.append((self.eval(currRow), currRow))
            currRow = []
        return rowEvals

    def vertical(self):
        currRow = []
        colEvals = []
        bNumList = [[0, 3, 4], [1, 4, 7], [2, 5, 8]]  # three different columns

        for x in bNumList:
            for y in x:
                if self.__mMacroboard[y] == self.getMyId():
                    currRow.append('X')
                elif self.__mMacroboard[y] == self.__EMPTY_FIELD or self.__mMacroboard[y] == self.__AVAILABLE_FIELD:
                    currRow.append('_')
                else:
                    currRow.append('O')
            colEvals.append((self.eval(currRow), currRow))
            currRow = []
        return colEvals

    # works similar to vertical and horizontal, see above comments
    def diagonal(self):
        currDiag = []
        bNumList = [[0, 4, 8], [2, 4, 6]]
        diagEvals = []
        for x in bNumList:
            for y in x:
                if self.__mMacroboard[y] == self.getMyId():
                    currDiag.append('X')
                elif self.__mMacroboard[y] == self.__EMPTY_FIELD or self.__mMacroboard[y] == self.__AVAILABLE_FIELD:
                    currDiag.append('_')
                else:
                    currDiag.append('O')
            diagEvals.append((self.eval(currDiag), currDiag))
        return diagEvals

    @staticmethod
    def threevalToEncode(horz, vert, diag):
        row1 = horz[1][0]
        row2 = horz[1][1]
        row3 = horz[1][2]
        currBoard = row1 + row2 + row3

        for a in horz:
            print('horz[' + a + '] = ' + horz[a])
            for b in a:
                print('horz[' + a + ']' + '[' + b + '] = ' + horz[a][b])

        for c in vert:
            print('vert[' + c + '] = ' + vert[c])
            for d in c:
                print('vert[' + c + ']' + '[' + d + '] = ' + vert[c][d])

        for e in diag:
            print('diag[' + e + '] = ' + diag[e])
            for f in e:
                print('diag[' + e + ']' + '[' + f + '] = ' + diag[e][f])

        print('Board = ' + currBoard)
        winList = []
        # (e1,e2,e3)
        for g in range(0, 2):
            if horz[0][g] >= 2:
                winList.append('horz' + str(g))
        for h in range(0, 2):
            if horz[0][h] >= 2:
                winList.append('vert' + str(h))
        for i in range(0, 1):
            if diag[0][i] >= 1:
                winList.append('diag' + str(i))
        # good move to make
        goodMoves = []
        # gooder move to make
        gooderMoves = []
        # Loop through winList and filter good + gooder moves
        for q in winList:
            if winList[q][0:3] == 'horz':
                if winList[q][4] == 2:
                    gooderMoves.append(winList[q])
                elif winList[q][4] == 1:
                    goodMoves.append(winList[q])
            if winList[q][0:3] == 'vert':
                if winList[q][4] == 2:
                    gooderMoves.append(winList[q])
                elif winList[q][4] == 1:
                    goodMoves.append(winList[q])
            if winList[q][0:3] == 'diag':
                if winList[q][4] == 2:
                    gooderMoves.append(winList[q])
                elif winList[q][4] == 1:
                    goodMoves.append(winList[q])


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
