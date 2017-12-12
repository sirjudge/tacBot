import random
import os
from random import randint
import subprocess
from util import*
import json

def moveToArchive(genNum):
    generationNum = str(genNum)
    os.system('mkdir /home/nico/Documents/CompSci/440/tacBot/archivedLogs/gen' + generationNum)
    for encodingNum in range(0, 10):
        fname = 'encoding' + str(encodingNum) + '.txt'
        os.system('cp /home/nico/Documents/CompSci/440/tacBot/' + fname +
                  ' /home/nico/Documents/CompSci/440/tacBot/archivedLogs/gen0'+ '/' + fname)
# ==================================
# OLD TESTING STUFF ABOVE THIS LINE
# ==================================


# Use grep command to search through encoding file for the first line that the string is in
def grepSearch(searchString, fileName):
    hosts_process = subprocess.Popen(['grep', searchString, fileName], stdout=subprocess.PIPE)
    hosts_out, hosts_err = hosts_process.communicate()
    if hosts_out:
        stratLookup = str(hosts_out)[2:-3]
        eandsList = stratLookup.split(',')
        return eandsList
    else:
        randomList = random.sample(range(9), 9)
        strat = ''
        for x in randomList:
            strat += str(x)
        return [searchString, strat]


# Thank you Julian for these two methods
def load_from_json():
    with open('resultfile.json') as f:
        data = json.load(f)
    winner = jsonDataToWinner(data)
    f.close()
    return winner


def jsonDataToWinner(data):
    return json.loads(data['details'])['winner']


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
        assert False, 'execvp failed!'        # os.exec call never returns hered


def delFirstLine(fName):
    # reads file and loads it into data variable
    with open(fName, 'r') as fin:
        data = fin.read().splitlines(True)
    # open the file again in write mode, and rewrite the file line by line ignoring the first line in the file
    with open(fName, 'w') as fout:
        fout.writelines(data[1:])
    fout.close()
    fin.close()


def createRandomFile():
    sList = ['0', '1', '_']
    # Creates 10 files
    for notOriginalName in range(0, 10):
        fname = 'encoding' + str(notOriginalName) + '.txt'
        file = open(fname, 'w')
        # Clear the file
        file.truncate()
        # Write the Generation Number
        file.write('0\n')
        # Write the encoding name
        file.write(str(notOriginalName) + '\n')
        # Create 500 random strats
        for encoNum in range(0, 500):
            for y in range(0, 9):
                i = randint(0, 2)
                file.write(sList[i])
            randomList = random.sample(range(9), 9)
            encString = ''
            for z in randomList:
                encString = encString + str(z)
            file.write(',' + encString + '\n')

# def crossbreed(gene1, gene2):
def crossbreed():
    newGen = 42 + 1
    # fname1 = 'encoding' + gene1 + '.txt'
    # fname2 = 'encoding' + gene2 + '.txt'
    fname1 = 'encoding0.txt'
    fname2 = 'encoding1.txt'

    # nfname1 = 'ne' + str(gene1) + '.txt'
    # nfname2 = 'ne' + str(gene2) + '.txt'
    nfname1 = 'ne0.txt'
    nfname2 = 'ne1.txt'

    # open the two actual encoding files
    file1 = open(fname1, 'r')
    file2 = open(fname2, 'r')
    # open two new encoding files that will replace the old files
    newFile1 = open(nfname1, 'w')
    newFile2 = open(nfname2, 'w')
    # increment the current generation number
    # currGenerationNum = int(self.generationNumber) + 1
    currGenerationNum = newGen
    # write the new generation num to the new files
    newFile1.write(str(currGenerationNum) + '\n')
    newFile2.write(str(currGenerationNum) + '\n')
    # write the gene numbers of the respective files
    newFile1.write(str(0) + '\n')
    newFile2.write(str(1) + '\n')

    # the code below replaces the first line of a file with the next generation number
    # os.system("sed -i '1c\\'" + str(newGen) + " " + f1)
    # os.system("sed -i '1c\\:'" + str(newGen) + " " + f2)

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
        print('len of enc1:' + str(len(encList1)))
        print('len of enc2:' + str(len(encList2)))
        pass
    # choose a random point to switch encodings
    crossPoint = randint(0, len(encList1))
    # create a random number between 0-100
    crossChance = randint(0, 100)
    print('CrossChance:' + str(crossChance) + '\nCrossPoint:' + str(crossPoint))

    # 10% chance to crossbreed
    if crossChance <= 30:
        for i in range(len(encList1)):
            # go up to the crosspoint in both lists, append them to their normal spots,
            # but switch the second parts of each list
            # ex.
            # new_encoding_1 = first_half_enc1 + second_half_enc2
            # new_encoding_2 = first_half_enc2 + second_half_enc1
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
    else:
        for x in range(len(encList1)):
            newEncList1.append(encList1[x])
            newEncList2.append(encList2[x])
    newFile1.writelines(newEncList1)
    newFile1.flush()
    newFile2.writelines(newEncList2)
    newFile2.flush()
    # close each of the files
    file1.close()
    file2.close()
    newFile1.close()
    newFile2.close()
    # delete the current gene encoding and replace it with the new encoding
    # remove the previous encoding files

    # TODO: This code works
    os.system('rm ' + fname1)
    os.system('rm ' + fname2)

    # rename the two files from tmp name to actual name
    # ie. ne0.txt changes to encoding0.txt
    os.system('cp ' + nfname1 + ' ' + fname1)
    os.system('cp ' + nfname2 + ' ' + fname2)


def mutateLine(encLine):
    # 0123456789012345678
    # 123456789,123456789
    # second half of encoding is 10-18
    # If I change the encoding change the following lines to reflect a longer encoding
    stratEnc = encLine[10:19]
    boardEnc = encLine[0:9]
    # set what part of the strings I choose to split at
    mutateBit = randint(0, (len(stratEnc) - 1))
    mutateBit2 = randint(0, (len(stratEnc) - 1))
    # random number between 100, needs to be above whatever I set the number below at
    mutateChance = randint(0, 100)

    # 30% chance of mutation
    if mutateChance <= 30:
        print('mutation occured')
        # Make sure we didn't choose the same two numbers for the mutate bit
        while mutateBit == mutateBit2:
            if mutateBit == len(stratEnc):
                mutateBit2 -= 1
            elif mutateBit == 0:
                mutateBit2 = mutateBit2 + 1
            else:
                mutateBit2 = randint(0, len(stratEnc))
        # find the characters we want to switch
        mutateChar1 = stratEnc[mutateBit]
        mutateChar2 = stratEnc[mutateBit2]
        # create a temp string, loop through the old enc, and switch the two numbers
        tmpString = ''
        for x in stratEnc:
            if x == mutateChar1:
                tmpString += mutateChar2
            elif x == mutateChar2:
                tmpString += mutateChar1
            else:
                tmpString += x
        # log that we mutated
        print('original encoding:' + encLine + '\n')
        print(' Mutated encoding:' + boardEnc + ',' + tmpString + '\n')
        return boardEnc + ',' + tmpString
    else:
        print('Mutation did not occur, original encoding:' + encLine + '\n')
        return encLine


def resetGeneFile():
    file = open('geneList.txt', 'w')
    file.truncate()
    for x in range(0, 9):
        file.write(str(x) + '\n')
    file.write('!' + '\n')
    file.close()


if __name__ == '__main__':
    # resetGeneFile()
    createRandomFile()
    # line = mutateLine('10000110_,170368245')
    # print('line:' + line)
    #crossbreed()