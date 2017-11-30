import random
import os
import sys
from random import randint


# decoding list is a list of tuples (encoding,fitness)
class Decoding:
    geneList = []
    generationNumber = -1
    dnaNum = -1

    def __init__(self):
        for notOriginalName in range(0, 10):
            fname = 'encoding' + str(notOriginalName) + '.txt'
            file = open(fname, 'r+')
            i = 0
            decodeList = []
            for line in file:
                if i == 0:
                    self.generationNumber = line
                elif i == 1:
                    self.dnaNum = line
                else:
                    decodeList.append(line)
            self.geneList.append(decodeList)

    # Getters and Setters
    def setGenerationNumber(self, genNum):
        self.generationNumber = genNum

    def setEncoding(self, encode):
        self.encodingList = encode

    def getEncoding(self):
        return self.encodingList

    def getGenerationNum(self):
        return self.generationNumber

    # Method simply creates 500 random strategies
    # Will create 10 encodings
    @staticmethod
    def createRandomFile():
        sList = ['0', '1', '*']
        # Creates 10 files
        for notOriginalName in range(0, 10):
            fname = 'encoding' + str(notOriginalName) + '.txt'
            file = open(fname, 'r+')
            # Clear the file
            file.truncate()
            # Write the Generation Number
            file.write('0')
            # Write the encoding name
            file.write(str(notOriginalName))
            # Create 500 random strats
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

    # TODO: go through and change all logic involving get decoding list
    def getDecodingList(self):
        return self.geneList

    # TODO: delFirstLIne is should longer used as a function
    def delFirstLine(self):
        tmpFile = open('encoding.txt', 'r+')
        with self.tmpFile as fin:
            data = fin.read().splitlines(True)
        with self.tmpFile as fout:
            fout.writelines(data[1:])

    # TODO: getFirstLIne should longer used as a function in conjunction iwth delFirstLine
    def getFirstLine(self):
        tmpFile = open('encoding.txt', 'r+')
        with self.tmpFile as f:
            first_line = f.readline()
            efl = first_line.split(',')
        return efl[0]

    # TODO: rewrite this, it is using old logic and also still uses tmpFile, which should not really exist anymore
    def resetFile(self):
        self.tmpFile.truncate()
        self.tmpFile.write(str(self.generationNumber) + '\n')
        self.tmpFile.write
        for q in self.getDecodingList():
            self.tmpFile.write(q[0] + ',' + q[1] + '\n')


class Encoding:
    encodingList = []
    generationNumber = -1
    geneNum = -1
    log = open('encoding.txt', 'r+')

    # Line in encoding log will be
    # board encoding, strategy/policy, fitness score
    def __init__(self):
        for i, line in enumerate(self.log):
            # First line of a file is generation number
            if i == 0:
                self.generationNumber = line
            elif i == 1:
                self.geneNum = line
            # Otherwise it will be a tuple of (encoding,fitness level) so we split the line up by ','
            else:
                self.encodingList.append(line.split(','))

    # Getters and Setters
    def setGenerationNumber(self, genNum):
        self.generationNumber = genNum

    def setEncoding(self, encode):
            self.encodingList = encode

    def getEncoding(self):
        return self.encodingList

    def getGenerationNum(self):
        return self.generationNumber

    def resetFile(self):
        self.log.truncate()
        self.log.write(str(self.getGenerationNum()))
        for q in self.getEncoding():
            self.log.write(str(q) + '\n')

    # returns the length of a file
    @staticmethod
    def file_len(fname):
        i = 0
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1

    def writeToLog(self):
        log = open('encoding.txt', 'r+')
        log.truncate()
        log.write('' + str(self.generationNumber) + '\n')
        for enc in self.encodingList:
            log.write(enc[0][0] + ',' + enc[0][1] + ',' + enc[0][2] + '\n')

    def archiveLog(self):
        genNum = self.getGenerationNum
        fName = 'archivedLogs/log_gen' + str(genNum)
        file = open(fName, 'r+')
        file.write(genNum)
        for enc in self.encodingList:
            file.write(enc[0][0] + ',' + enc[0][1] + ',' + enc[0][2] + '\n')

    def crossbreed(self, encoding1, encoding2):
        # TODO: fix the logic. Have to open each file, put each file into a list, swap half the list
        # TODO: Maybe consider just writing a whole new method and then deleting this one
        # First part of both encodings
        e1f = ''
        e2f = ''
        # Second part of both encodings
        e1s = ''
        e2s = ''
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
        # TODO: Fix the logic with this one. It's just full wrong.
        # Choose a random number between 1 and 100 to be our chance to mutate
        mutateChance = random.randint(0, 100)
        out = ''
        # for each number in the encoding
        for eChar in encoding:
            # 1% chance to mutate to a random strat
            if mutateChance == 42:
                out = out + (random.randint(0, 5))
            # 99% chance to keep the same strat
            else:
                out = out + eChar
        return out


def spawn(prog, *args):                       # pass progname, cmdline args
    stdinFd = sys.stdin.fileno()              # get descriptors for streams
    stdoutFd = sys.stdout.fileno()            # normally stdin=0, stdout=1
    parentStdin, childStdout = os.pipe()      # make two IPC pipe channels
    childStdin,  parentStdout = os.pipe()     # pipe returns (inputfd, outoutfd)
    pid = os.fork()                           # make a copy of this process
    if pid:
        os.close(childStdout)                 # in parent process after fork:
        os.close(childStdin)                  # close child ends in parent
        os.dup2(parentStdin,  stdinFd)        # my sys.stdin copy  = pipe1[0]
        os.dup2(parentStdout, stdoutFd)       # my sys.stdout copy = pipe2[1]
    else:
        os.close(parentStdin)                 # in child process after fork:
        os.close(parentStdout)                # close parent ends in child
        os.dup2(childStdin,  stdinFd)         # my sys.stdin copy  = pipe2[0]
        os.dup2(childStdout, stdoutFd)        # my sys.stdout copy = pipe1[1]
        args = (prog,) + args
        os.execvp(prog, args)                 # new program in this process
        assert False, 'execvp failed!'        # os.exec call never returns here


if __name__ == '__main__':
    # TODO: Double check this stuff. I think some of it may also be wrong
    e = Encoding()                      # Create the list of encodings
    newEncodeList = []                  # set variable stuff
    currFitness = -1
    currEncoding = ''
    newFitness = -1
    newEncoding = ''

    currEncoding = e.getEncoding()      # create local variable for encoding list
    e.archiveLog()
    # java -jar match-wrapper-1.3.2.jar "$(cat wrapper-commands.json)"

    # For each encoding in the encoding list, create a new process that starts a new main.py
    # this for loop is what starts all my bots
    for x in currEncoding:
        print(e)
        currEncoding = x[0]
        currFitness = x[1]
        # create a new bot for each encoding
        spawn('Java', '-jar', 'match-wrapper-1.3.2.jar', "$(cat wrapper-commands.json)")

    # TODO: This maybe shouldn't happen here but we need to write the new encodings down
    newEncodeList.append((newFitness, newEncoding))

    e.setEncoding(newEncodeList)
    currList = e.getEncoding()

    # go through the list of encodings and crossbreed/mutate them
    # the crossbreed method will crossbreed them first and then mutate them
    for x in range(0, len(currList.getEncoding()-1)):
        # separates the two encodings
        e1 = currList.getEncoding()[x][1]
        e2 = currList.getEncoding()[x+1][1]
        # places the returned crossbred encodings in a temp list
        tmpList = e.crossbreed(e1, e2)
        # replaces the old encodings with the new encodings
        currList[x][0] = tmpList[1]
        currList[x+1][0] = tmpList[2]
        e.setEncoding(currList)
    e.resetFile()
