import os
import subprocess
from random import randint, sample


class Encoding:
    # Master list of all sets of encodings
    encodingList = []
    # Current Generation Number
    generationNumber = -1
    # GeneNum
    geneNum = -1
    fitnessTupleList = []

    # Line in encoding log will be
    # board encoding, strategy/policy, fitness score
    def __init__(self):
        with open('encoding0.txt') as f:
            self.generationNumber = f.readline()
            f.close()

        for notOriginalName in range(0, 10):
            fname = 'encoding' + str(notOriginalName) + '.txt'
            file = open(fname, 'r+')
            i = 0
            line = ''
            for line in file:
                if i == 0:
                    self.generationNumber = line[:-1]
                    # print('genNum:' + str(self.generationNumber))
                else:
                    self.encodingList.append(line)
                i += 1
            file.close()

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
            file.write('0\n')
            # Write the encoding name
            file.write(str(notOriginalName) + '\n')
            # Create 500 random strats
            for encoNum in range(0, 500):
                for y in range(0, 9):
                    i = randint(0, 2)
                    file.write(sList[i])
                randomList = sample(range(9), 9)
                encString = ''
                for z in randomList:
                    encString = encString + str(z)
                file.write(',' + encString + '\n')
            file.close()

    # Getters and Setters
    def setGenerationNumber(self, genNum):
        self.generationNumber = genNum

    def getGenerationNum(self):
        return self.generationNumber

    # Moves an encoding file to archived folder
    def moveToArchive(self):
        generationNum = str(self.generationNumber)
        # Check to see if the directory exists or not
        if os.path.isdir('archivedLogs/gen' + generationNum):
            print('directory already exists')
        else:
            os.system('mkdir /home/nico/Documents/CompSci/440/tacBot/archivedLogs/gen' + generationNum)
            for encodingNum in range(0, 10):
                fname = 'encoding' + str(encodingNum) + '.txt'
                os.system(
                    'cp /home/nico/Documents/CompSci/440/tacBot/' + fname
                    + ' /home/nico/Documents/CompSci/440/tacBot/archivedLogs/gen0/' + fname)

    def crossbreed(self, gene1, gene2):


        newGen = int(self.generationNumber) + 1

        fname1 = 'encoding' + gene1 + '.txt'
        fname2 = 'encoding' + gene2 + '.txt'

        nfname1 = 'ne' + str(gene1)
        nfname2 = 'ne' + str(gene2)

        print('genNum:' + str(newGen))
        print('gene1:' + str(gene1))
        print('gene2:' + str(gene2))
        print('fname1:' + fname1)
        print('fname2:' + fname2)
        print('nfname1:' + nfname1)
        print('nfname1:' + nfname2)

        # open the two actual encoding files
        file1 = open(fname1, 'r')
        file2 = open(fname2, 'r')
        # open two new encoding files that will replace the old files
        newFile1 = open(nfname1, 'w')
        newFile2 = open(nfname2, 'w')
        # increment the current generation number
        currGenerationNum = int(self.generationNumber) + 1
        # write the new generation num to the new files
        newFile1.write(str(currGenerationNum))
        newFile2.write(str(currGenerationNum))
        # write the gene numbers of the respective files
        newFile1.write(str(gene1))
        newFile2.write(str(gene2))

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
        #print('CrossChance:' + str(crossChance) + '\nCrossPoint:' + str(crossPoint))

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
            newEncList1[lineNum] = self.mutateLine(line1)
            newEncList2[lineNum] = self.mutateLine(line2)

        for winnerEncoding in newEncList1:
            newFile1.write(winnerEncoding + '\n')
        for winnerEncoding in newEncList2:
            newFile2.write(winnerEncoding + '\n')
        # close each of the files
        file1.close()
        file2.close()
        newFile1.close()
        newFile2.close()
        # delete the current gene encoding and replace it with the new encoding
        # remove the previous encoding files
        os.system('rm ' + fname1)
        os.system('rm ' + fname2)
        # rename the two files from tmp name to actual name
        # ie. ne0.txt changes to encoding0.txt
        os.system('mv ' + nfname1 + ' ' + fname1)
        os.system('mv ' + nfname2 + ' ' + fname2)

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
        if mutateChance <= 5:
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

    @staticmethod
    def resetGeneFile():
        file = open('geneList.txt', 'r+')
        file.truncate()
        for el in range(0, 9):
            file.write(str(el) + '\n')
        file.write('!' + '\n')
        file.close()

    def evalFitness(self):
        fitnessFile = open('gymScores.txt', 'r')
        for line in fitnessFile:
            currLine = line.split(',')
            currGene = currLine[0]
            currFit = currLine[1]
            self.fitnessTupleList.append([currGene, currFit])
        #self.fitnessTupleList = self.fitnessTupleList.sort(key=lambda x: x[1])

    def createNewEncodings(self):
        pass


def startUp():
    # change double quotes to single quotes
    bashCommand = 'java -jar match-wrapper-1.3.2.jar "$(cat wrapper-commands.json)"'
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print('Error with running bash command')
    print(error)

if __name__ == '__main__':
    e = Encoding()
    print('encoding created, moving encodings to archive folder')
    e.moveToArchive()
    # Do crossbreeding and mutate and clean up here
    print('evaluating fitness now')
    e.evalFitness()

    winList = []
    loseList = []

    for tup in e.fitnessTupleList:
        if tup[1] == 1:
            winList.append(str(tup[0]))
        else:
            loseList.append(str(tup[0]))

    c = 0
    while len(winList) < 5:
        winList.append(loseList[c])
        c += 1

    for winner in range(0, len(winList)-1):
        e.crossbreed(winList[winner], winList[winner + 1])

    e.resetGeneFile()

