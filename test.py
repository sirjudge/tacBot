import random
import os
from random import randint
import sys
import subprocess
from util import Move

def crossbreed(fname1, fname2):
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
        newEncList1[lineNum] = mutateLine(line1)
        newEncList2[lineNum] = mutateLine(line2)
    print(newEncList1)
    print(newEncList2)
    return newEncList1, newEncList2


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

    oldEnc1 = stratEnc
    newEnc1 = ''

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
    newEnc1 = outEnc
    print('newEnc:' + newEnc1)
    print('oldEnc:' + oldEnc1)
    return outEnc


def moveToArchive(genNum):
    generationNum = str(genNum)
    os.system('mkdir /home/nico/Documents/CompSci/440/tacBot/archivedLogs/gen' + generationNum)
    for encodingNum in range(0, 10):
        fname = 'encoding' + str(encodingNum) + '.txt'
        os.system('cp /home/nico/Documents/CompSci/440/tacBot/' + fname + ' /home/nico/Documents/CompSci/440/tacBot/archivedLogs/gen0'+ '/' + fname)
# ==================================
# OLD TESTING STUFF ABOVE THIS LINE
# ==================================

def grepSearch(searchString, fileName):
    hosts_process = subprocess.Popen(['grep', searchString, fileName], stdout=subprocess.PIPE)
    hosts_out, hosts_err = hosts_process.communicate()
    stratLookup = str(hosts_out)[2:-3]
    print(stratLookup)
    eandsList = stratLookup.split(',')
    return eandsList

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
    # crossbreed('encoding0.txt', 'encoding1.txt')
    # moveToArchive(0)
    list = grepSearch('1_01_0__0', 'encoding0.txt')
    print(list[0])
    # spawn('java', '-jar', 'match-wrapper-1.3.2.jar', "$(cat wrapper-commands.json)")