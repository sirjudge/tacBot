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

    def setGeneList(self, encode):
        self.geneList = encode

    def getGeneList(self):
        return self.geneList

    def getGenerationNum(self):
        return self.generationNumber

    def getDNANum(self):
        return self.generationNumber

    def setDNANum(self, num):
        self.dnaNum = num

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


class Encoding:
    # Master list of all sets of encodings
    encodingList = []
    # Current Generation Number
    generationNumber = -1
    # GeneNum
    geneNum = -1

    # Line in encoding log will be
    # board encoding, strategy/policy, fitness score
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
                    decodeList.append(line.split(','))
            self.encodingList.append(decodeList)

    # Getters and Setters
    def setGenerationNumber(self, genNum):
        self.generationNumber = genNum

    def setEncoding(self, encode):
            self.encodingList = encode

    def getEncoding(self):
        return self.encodingList

    def getGenerationNum(self):
        return self.generationNumber

    # TODO: These need to change
    def writeToLog(self):
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
            self.encodingList.append(decodeList)

    # Moves an encoding file to archived folder
    @staticmethod
    def moveToArchive():
        for encodingNum in range(0, 10):
            fname = 'encoding' + str(encodingNum) + '.txt'
            # My Linux machine
            os.rename('/home/nico/Documents/CompSci/440/tacBot/' + fname
                      , "/home/nico/Documents/CompSci/440/tacBot/archivedLogs/gen" + str(encodingNum) + '/' + fname)
            # My Windows machine
            # os.rename()

    @staticmethod
    def howManyLines(fname):
        file = open(fname)
        i = 0
        for line in file:
            i += 1
        return i

    def crossbreed(self, fname1, fname2):
        file1 = open(fname1)
        file2 = open(fname2)
        # List of two encodings
        encList1 = []
        encList2 = []
        # return list of crossbred lists
        newEncList1 = []
        newEncList2 = []
        lineCount = 0
        # lineCount = 0: gen num
        # lineCount = 1: gene num
        # lineCount >= 2: encoding lists
        for line in file1:
            if lineCount >= 2:
                encList1.append(line)
            lineCount += 1
        lineCount = 0
        for line in file2:
            if lineCount >= 2:
                encList2.append(line)
            lineCount += 1
        # If the length of the two lists is not equal then quit
        if not len(encList1) == len(encList2):
            print('encoding lists are different sizes')
            pass
        # choose a random point to switch encodings
        crossPoint = random.randint(0, len(encList1))
        # create a random number between 0-100
        crossChance = random.randint(0, 100)
        # 10% chance to crossbreed
        if crossChance <= 10:
            for i in range(len(encList1)):
                # go up to the crosspoint in both lists, append them to their normal spots,
                # but switch the second parts of each list
                # ex.
                # new_encoding_1 = first_half_enc1 + second_half_enc2
                # new_encoding_2 = first_half_enc2 + second_half_enc1

                if x < crossPoint:
                    newEncList1.append(encList1[i])
                    newEncList2.append(encList2[i])
                else:
                    newEncList1.append(encList2[i])
                    newEncList2.append(encList1[i])
        # Why make two for loops when you can just write one?
        for lineNum in range(len(newEncList1)):
            line1 = newEncList1[lineNum]
            line2 = newEncList2[lineNum]
            # before adding it to the new encoding list we have to mutate each one
            newEncList1[lineNum] = self.mutateLine(line1)
            newEncList2[lineNum] = self.mutateLine(line2)
        return newEncList1, newEncList2

    @staticmethod
    def mutateLine(encLine):
        # 0123456789012345678
        # 123456789,123456789
        # second half of encoding is 10-18
        # If I change the encoding change the following lines to reflect a longer encoding

        stratEnc = encLine[10:18]
        boardEnc = encLine[0:8]

        mutateBit = randint(0, len(stratEnc))
        mutateBit2 = randint(0, len(stratEnc))
        mutateChance = randint(0, 100)

        maxBit = max(mutateBit, mutateBit2)
        minBit = min(mutateBit, mutateBit2)
        outEnc = ''
        mutateChar1 = stratEnc[mutateBit]
        mutateChar2 = stratEnc[mutateBit2]
        if mutateChance < 5:
            # Make sure we didn't choose the same two numbers
            # and if we did choose the same 2 numbers keep reassigning them until we get it
            # we only need to change bit2
            while mutateBit == mutateBit2:
                    if mutateBit == len(stratEnc):
                        mutateBit2 -= 1
                    elif mutateBit == 0:
                        mutateBit2 += 1
                    else:
                        mutateBit2 = randint(0, len(stratEnc))

            # if position of the first bit to switch is the last in the queue
            if mutateBit == len(stratEnc):
                outEnc = boardEnc + stratEnc[0:mutateBit2-1] + mutateChar1 + stratEnc[mutateBit2+1:-1] + mutateChar2
            # if position of the second bit to switch is the last in the queue
            elif mutateBit2 == len(stratEnc):
                outEnc = boardEnc + stratEnc[0:mutateBit-1] + mutateChar2 + stratEnc[mutateBit+1:-1] + mutateChar1
            else:
                outEnc = boardEnc + stratEnc[0:minBit-1] + stratEnc[minBit + 1:maxBit]
        return outEnc

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
