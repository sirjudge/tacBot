import random
import os
import sys


class Encoding:
    encodingList = []
    generationNumber = -1
    # will be a list of tuples
    # (encoding,fitness score)

    # Line in encoding log will be
    # encoding, fitness score
    def __init__(self):
        log = open('encoding.txt', 'r+')
        for i, line in enumerate(log):
            if i == 25:
                self.generationNumber = int(line)
            else:
                self.encodingList.append(line.split(','))
        log.close()

    # Getters and Setters
    def setGenerationNumber(self, genNum):
        self.generationNumber = genNum

    def setEncoding(self, encode):
            self.encodingList = encode

    def getEncoding(self):
        return self.encodingList

    def getGenerationNum(self):
        return self.generationNumber

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
        log.write('' + self.generationNumber + '\n')
        for enc in self.encodingList:
            log.write(enc[0][0] + ',' + enc[0][1] + '\n')

    def ArchiveLog(self, genNum):
        # TODO: this should put the file in a folder for easier file management
        fName = 'log_gen' + genNum
        file = open(fName, 'w')
        file.write(genNum)
        for enc in self.encodingList:
            file.write(enc[0][0] + ',' + enc[0][1] + '\n')

    def crossbreed(self, encoding1, encoding2):
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
        # Choose a random number between 1 and 100 to be our chance to mutate
        mutateChance = random.randint(0, 100)
        out = ''
        # for each number in the encoding
        for enco in encoding:
            # 1% chance to mutate to a random strat
            if mutateChance == 42:
                out = out + (random.randint(0, 5))
            # 99% chance to keep the same strat
            else:
                out = out + x
        return out


def spawn(prog, *args):                       # pass progname, cmdline args
    stdinFd = sys.stdin.fileno()             # get descriptors for streams
    stdoutFd = sys.stdout.fileno()            # normally stdin=0, stdout=1

    parentStdin, childStdout = os.pipe()     # make two IPC pipe channels
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
    e = Encoding()
    newEncodeList = []
    currFitness = -1
    currEncoding = ''
    newFitness = -1
    newEncoding = ''
    currEncoding = e.getEncoding()
    e.archiveLog()
    # java -jar match-wrapper-1.3.2.jar "$(cat wrapper-commands.json)"
    for x in currEncoding:
        print(e)
        currEncoding = x[0]
        currFitness = x[1]
        # create a new bot for each encoding
        spawn('Java', '-jar', 'match-wrapper-1.3.2.jar', "$(cat wrapper-commands.json)")
        # returns a fitness score f eventually
        newEncodeList.append((newFitness, newEncoding))
    e.setEncoding(newEncodeList)
    currList = e.getEncoding()
    # go through the list of encodings and crossbreed/mutate them
    for x in range(0, len(currList.getEncoding()-1)):
        # separates the two encodings
        e1 = currList.getEncoding()[x][0]
        e2 = currList.getEncoding()[x+1][0]
        # places the returned crossbred encodings in a temp list
        tmpList = e.crossbreed(e1, e2)
        # replaces the old encodings with the new encodings
        currList[x][0] = tmpList[1]
        currList[x+1][0] = tmpList[2]
        e.setEncoding(currList)
