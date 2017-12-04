import random
import os
import sys
from random import randint

"""
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
"""

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

    # Method simply creates 500 random strategies
    # Will create 10 encodings
    @staticmethod
    def createRandomFile():
        sList = ['0', '1', '_']
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
    def moveToArchive(self):
        generationNum = str(self.generationNumber)
        os.system('mkdir /home/nico/Documents/CompSci/440/tacBot/archivedLogs/gen' + generationNum)
        for encodingNum in range(0, 10):
            fname = 'encoding' + str(encodingNum) + '.txt'
            os.system(
                'cp /home/nico/Documents/CompSci/440/tacBot/' + fname
                + ' /home/nico/Documents/CompSci/440/tacBot/archivedLogs/gen0/' + fname)

    @staticmethod
    def howManyLines(fname):
        file = open(fname)
        i = 0
        for line in file:
            i += 1
        return i

    def crossbreed(self, f1, f2):
        file1 = open(f1)
        file2 = open(f2)
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
                print('crosspoint = ' + str(i))
                if i < crossPoint:
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

        mutateBit = randint(0, len(stratEnc) - 1)
        mutateBit2 = randint(0, len(stratEnc) - 1)
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
                outEnc = boardEnc + stratEnc[0:mutateBit2 - 1] + mutateChar1 + stratEnc[mutateBit2 + 1:-1] + mutateChar2
            # if position of the second bit to switch is the last in the queue
            elif mutateBit2 == len(stratEnc):
                outEnc = boardEnc + stratEnc[0:mutateBit - 1] + mutateChar2 + stratEnc[mutateBit + 1:-1] + mutateChar1
            else:
                outEnc = boardEnc + stratEnc[0:minBit - 1] + stratEnc[minBit + 1:maxBit]
        return outEnc


# outside Encoding class
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

    e = Encoding()                      # Create the list of encodings
    #e.createRandomFile()

    currEncoding = e.getEncoding()      # create local variable for encoding list

    # Spawns a new main each time it's run. will run 10 mains at a time, 1 for each encoding
    # java -jar match-wrapper-1.3.2.jar "$(cat wrapper-commands.json)"
    for x in range(0, 10):
        print('running encoding ' + str(x))
        spawn('java', '-jar', 'match-wrapper-1.3.2.jar', "$(cat wrapper-commands.json)")

    # Do crossbreeding and mutate and clean up here
    for encNum in range(0, 8):
        fname1 = 'encoding' + str(encNum)
        fname2 = 'encoding' + str(encNum + 1)
        e.crossbreed(fname1, fname2)
    e.moveToArchive()
