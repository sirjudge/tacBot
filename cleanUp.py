import os
import subprocess
from random import randint, sample


class Encoding:
    # Master list of all sets of encodings
    # Current Generation Number
    generationNumber = -1
    # GeneNum
    geneNum = -1
    fitnessTupleList = []

    # Line in encoding log will be
    # board encoding, strategy/policy, fitness score
    def __init__(self):
        for notOriginalName in range(0, 10):
            fname = 'encoding' + str(notOriginalName) + '.txt'
            file = open(fname, 'r+')
            i = 0
            for line in file:
                if i == 0:
                    self.generationNumber = line[:-1]
                    # print('genNum:' + str(self.generationNumber))
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

    @staticmethod
    def file_len(fname):
        with open(fname) as f:
            q = 0
            for q, l in enumerate(f):
                pass
        return q + 1

    def crossbreed(self, gene1, gene2):
        fname1 = 'encoding' + str(gene1) + '.txt'
        fname2 = 'encoding' + str(gene2) + '.txt'

        nfname1 = 'ne' + str(gene1) + '.txt'
        nfname2 = 'ne' + str(gene2) + '.txt'

        # checking the file size of each gene file
        print('old file size for ' + gene1 + ' and ' + gene2)
        print(str(self.file_len(fname1)))
        print(str(self.file_len(fname1)))

        # open the two actual encoding files
        file1 = open(fname1, 'r')
        file2 = open(fname2, 'r')
        # open two new encoding files that will replace the old files
        newFile1 = open(nfname1, 'w')
        newFile2 = open(nfname2, 'w')

        # List of two encodings
        encList1 = []
        encList2 = []

        # return list of crossbred lists
        newEncList1 = []
        newEncList2 = []
        lineCount = 0
        # get all the info we need in file1
        for line in file1:
            if lineCount == 0:
                currGen1 = line.strip()
            elif lineCount >= 2:
                encList1.append(line)
            lineCount += 1
        # get all the info in file2
        lineCount = 0
        for line in file2:
            if lineCount == 0:
                currGen2 = line.strip()
            elif lineCount == 1:
                currGene = line.strip()
            elif lineCount >= 2:
                encList2.append(line)
            lineCount += 1
        if not currGen1 == currGen2:
            print('generations are not the same, using currGen1 as the generation number')
            currGen2 = currGen1
        newGen = int(currGen1) + 1
        newFile1.write(str(newGen) + '\n')
        newFile2.write(str(newGen) + '\n')
        # write the gene numbers of the respective files
        newFile1.write(gene1 + '\n')
        newFile2.write(gene2 + '\n')
        # If the length of the two lists is not equal then quit
        if not len(encList1) == len(encList2):
            print('encoding lists are different sizes for gene' + str(gene1) + ' and ' + gene2)
            print('len of ' + gene1 + ':' + str(len(encList1)))
            print('len of ' + gene2 + ':' + str(len(encList2)))
            pass
        # choose a random point to switch encodings
        crossPoint = randint(0, len(encList1)-1)
        # create a random number between 0-100
        crossChance = randint(0, 100)
        # 10% chance to crossbreed
        if crossChance <= 100:
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
        else:
            for t in range(len(encList1)):
                newEncList1.append(encList1[t])
                newEncList2.append(encList2[t])
        # write each of the encodings to the new file
        for encList1x in newEncList1:
            newFile1.write(encList1x.strip() + '\n')
        for encList2x in newEncList2:
            newFile2.write(encList2x.strip() + '\n')
        # close each of the files we opened so all the buffers are written
        file1.close()
        file2.close()
        newFile1.close()
        newFile2.close()
        # remove the old files because we already archived them
        os.system('rm ' + fname1)
        os.system('rm ' + fname2)
        # rename the two files from tmp name to actual name
        # ie. ne0.txt changes to encoding0.txt
        os.system('cp ' + nfname1 + ' ' + fname1)
        os.system('cp ' + nfname2 + ' ' + fname2)
        # remove the two temporary files we made
        os.system('rm ' + nfname1)
        os.system('rm ' + nfname2)

        print('new file size for ' + gene1 + ' and ' + gene2)
        print(str(self.file_len(fname1)))
        print(str(self.file_len(fname1)))

    @staticmethod
    def mutateLine(encLine):
        # random number between 100, needs to be above whatever I set the number below at
        mutateChance = randint(0, 100)
        if mutateChance <= 30:
            # print('mutation occured')
            # 0123456789012345678
            # 123456789,123456789
            # second half of encoding is 10-18
            # If I change the encoding change the following lines to reflect a longer encoding
            stratEnc = encLine[10:19]
            boardEnc = encLine[0:9]
            # set what part of the strings I choose to split at
            mutateBit = randint(0, (len(stratEnc)) - 1)
            mutateBit2 = randint(0, (len(stratEnc)) - 1)
            # Make sure we didn't choose the same two numbers for the mutate bit
            while mutateBit == mutateBit2:
                if mutateBit == len(stratEnc):
                    mutateBit2 -= 1
                elif mutateBit == 0:
                    mutateBit2 = mutateBit2 + 1
                else:
                    mutateBit2 = randint(0, len(stratEnc)-1)
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
            # print('original encoding:' + encLine + '\n')
            # print(' Mutated encoding:' + boardEnc + ',' + tmpString + '\n')
            return boardEnc + ',' + tmpString
        else:
            # print('Mutation did not occur, original encoding:' + encLine + '\n')
            return encLine

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
            currLine = line.strip().split(',')
            currGene = currLine[0]
            currFit = currLine[1]
            print('currGene:' + currGene)
            print('currFit:' + currFit)
            self.fitnessTupleList.append([currGene, currFit])

    # using the given number of genes, create twice as many
    # TODO: finish this
    # at the end of the while loop we have to increment n and count to move on to next things
    @staticmethod
    def createMore(winnerGeneList):
        # winnerGeneList will contain top 5 scoring gene IDs
        # 0,1  || total Run = 0   num = 0
        # 2,3  || total Run = 1   num = 2
        # 3,4  || total Run = 2   num = 3
        num = 0
        totalRun = 0
        pairList = [[0, 1], [2, 3], [3, 4]]
        # Run the while loop three times, one for each of the pairs above
        while totalRun < 3:
            # print('num at the beginning of while loop:' + str(num))
            # print('totalRun at beginning of while loop:' + str(totalRun))

            # store the gene Number of each of the winning files
            g1 = str(winnerGeneList[num])
            g2 = str(winnerGeneList[num + 1])
            currPair = pairList.pop()

            # set the file names for both the old encoding file and the temp encoding file
            fname1 = 'encoding' + g1 + '.txt'
            nfname1 = 'te' + str(currPair[0]) + '.txt'
            fname2 = 'encoding' + g2 + '.txt'
            nfname2 = 'te' + str(currPair[1]) + '.txt'

            print('fname1:' + fname1)
            print('fname2:' + fname2)
            print('nfname1:' + nfname1)
            print('nfname2:' + nfname2)

            # open all the files
            file1 = open(fname1, 'r')
            nfile1 = open(nfname1, 'w')
            file2 = open(fname2, 'r')
            nfile2 = open(nfname2, 'w')
            # initialize variables
            currGen1 = '-41'
            currGen2 = '-42'
            enc1 = []
            enc2 = []
            lineCount = 0
            # for each line in file1 extract variables
            for line in file1:
                if lineCount == 0:
                    print('currGen = ' + line)
                    currGen1 = line.strip()
                elif lineCount >= 2:
                    enc1.append(line.strip())
                lineCount += 1

            lineCount = 0
            # for each line in file2 extract variables
            for line in file2:
                if lineCount == 0:
                    print('currGen = ' + line)
                    currGen2 = line.strip()
                elif lineCount >= 2:
                    enc2.append(line.strip())
                lineCount += 1

            if not currGen1 == currGen2:
                print('currGen1 does not equal currGen2, using currGen1 as the generation number')
                currGen2 = currGen1

            print('currGen1:' + currGen1)
            print('currGen2:' + currGen2)

            # write gen num and gene num to each of the files
            nfile1.write(str(currGen1) + '\n')
            nfile2.write(str(currGen2) + '\n')
            nfile1.write(str(currPair[0]) + '\n')
            nfile2.write(str(currPair[1]) + '\n')

            # write all the encodings to each respective file
            for enc in enc1:
                nfile1.write(enc + '\n')
            for enc in enc2:
                nfile2.write(enc + '\n')
            # Increment count variables
            if totalRun == 0:
                totalRun += 1
                num += 2
            elif totalRun == 2:
                totalRun += 1
                num += 1
            else:
                totalRun += 1
            # close all the files
            file1.close()
            nfile1.close()
            file2.close()
            nfile2.close()

        # end of while loop
        # remove all files that start with the string 'encoding'
        print('removing all encoding.txt files')
        os.system('rm encoding*')
        currGen1 = '-1'
        currGen2 = '-2'
        pairList = [0, 1], [2, 3], [3, 4]
        outList = [5, 6, 7, 8, 9]
        outListCount = 0
        print('starting for loop that creates a batch of new files')
        for geneNumPair in pairList:
            # open each pair of encoding sets
            tfname1 = 'te' + str(geneNumPair[0]) + '.txt'
            tfname2 = 'te' + str(geneNumPair[1]) + '.txt'
            # file name
            print('geneNum1:' + str(geneNumPair[0]))
            print('geneNum2:' + str(geneNumPair[1]))
            print('renaming the temp files to the real files')

            # Experimental code vvvvvvvvvvv
            tmpFile1 = open(tfname1, 'r+')
            tmpFile2 = open(tfname2, 'r+')

            reinitialFile1 = open('encoding' + str(geneNumPair[0]) + '.txt', 'w')
            reinitialFile2 = open('encoding' + str(geneNumPair[1]) + '.txt', 'w')

            encList1ToCopy = []
            encList2ToCopy = []

            # populate encList1
            lineCount = 0
            for line in tmpFile1:
                if lineCount == 0:
                    currGen1 = line.strip()
                elif lineCount >= 2:
                    encList1ToCopy.append(line.strip())
                lineCount += 1
            # populate encList2
            lineCount = 0
            for line in tmpFile2:
                if lineCount == 0:
                    currGen2 = line.strip()
                elif lineCount >= 2:
                    encList2ToCopy.append(line.strip())
                lineCount += 1

            # write the gen number first
            if currGen1 == '-1':
                print('gen number has not been correctly initialized')
                reinitialFile1.write('?' + '\n')
            else:
                reinitialFile1.write(currGen1 + '\n')

            if currGen2 == '-2':
                print('gen number has not been correctly initialized')
                reinitialFile2.write('?' + '\n')
            else:
                reinitialFile2.write(currGen2 + '\n')

            # write the gene number
            reinitialFile1.write(str(geneNumPair[0]) + '\n')
            reinitialFile2.write(str(geneNumPair[1]) + '\n')

            print('len of encList1ToCopy:' + str(len(encList1ToCopy)))
            print('len of encList2ToCopy:' + str(len(encList2ToCopy)))

            # write each list to their respective copies
            for encToWrite in encList1ToCopy:
                reinitialFile1.write(encToWrite + '\n')
            for encToWrite2 in encList2ToCopy:
                reinitialFile2.write(encToWrite2 + '\n')

            reinitialFile1.close()
            reinitialFile2.close()
            tmpFile1.close()
            tmpFile2.close()
            # Experimental code ^^^^^^^^^^^

            # list of encoding numbers for tmp files
            tmpFileNums = [0, 1], [2, 3], [3, 4], [1, 3]
            tmpFileNumCounter = 0

            while len(outList) > 0 and tmpFileNumCounter < 4:
                print('starting to write new encodings to the new file'
                      '\n=================================================='
                      '\n=================================================='
                      '\n==================================================')
                print('te' + str(tmpFileNums[tmpFileNumCounter]) + '.txt')
                print('te' + str(tmpFileNums[tmpFileNumCounter]) + '.txt')
                tfname1 = 'te' + str(tmpFileNums[tmpFileNumCounter][0]) + '.txt'
                tfname2 = 'te' + str(tmpFileNums[tmpFileNumCounter][1]) + '.txt'

                print('the new file names I created are \n')
                print('tfname1:' + str(tfname1))
                print('tfname2:' + str(tfname2))


                newGeneNum = str(outList.pop())
                nfname = 'encoding' + newGeneNum + '.txt'
                print('newGeneNum:' + newGeneNum)
                print('nfname:' + nfname)
                file1 = open(tfname1, 'r+')
                file2 = open(tfname2, 'r+')
                newFile = open(nfname, 'w')
                lineCount = 0
                enc1List = []
                enc2List = []
                for line in file1:
                    if lineCount >= 2:
                        enc1List.append(line.strip())
                    lineCount += 1
                lineCount = 0
                for line in file2:
                    if lineCount >= 2:
                        enc2List.append(line.strip())
                    lineCount += 1
                # write the generation number
                # write the new gene number
                newFile.write(currGen1 + '\n')
                newFile.write(newGeneNum + '\n')
                # create the actual new file
                crossPoint = randint(0, len(enc1List))
                for lineNum in range(0, len(enc1List)):
                    if lineNum < crossPoint:
                        newFile.write(enc1List[lineNum] + '\n')
                    else:
                        newFile.write(enc2List[lineNum] + '\n')
                newFile.close()
                file1.close()
                file2.close()
                tmpFileNumCounter += 1
        # remove all temp files in the curr dier
        # os.system('rm te*')


def countTheLength():
    for x in range(0, 10):
        i = 0
        print('counting len of encoding:' + str(x))
        file = open('encoding' + str(x) + '.txt')
        for line in file:
            i += 1
        file.close()
        print('len of encoding' + str(x) + ' is ' + str(i))


def assassinate(fileName):
    os.system('rm ' + fileName)


def startUp():
    # change double quotes to single quotes
    bashCommand = 'java -jar match-wrapper-1.3.2.jar "$(cat wrapper-commands.json)"'
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print('Error with running bash command')
    print(error)


if __name__ == '__main__':
    # create our encoding object
    e = Encoding()
    winnerList = [2, 3, 4, 5, 6]
    # uncomment the following two lines to archive things
    print('encoding created, moving encodings to archive folder')
    e.moveToArchive()

    # Do crossbreeding and mutate and clean up here
    print('evaluating fitness now')
    e.evalFitness()
    winList = []
    loseList = []
    # go through each tuple in the fitness list and see if they won or lost their game
    for tup in e.fitnessTupleList:
        if tup[1] == '1':
            print('winner:' + str(tup))
            winList.append(tup[0])
        else:
            print('loser:' + str(tup))
            loseList.append(tup[0])

    # Bug fixing print statements
    print('\n\n\nWinList\n')
    for x in winList:
        print(x)
    print('\n\n\n')

    # if the length of winList is not 5 or more
    c = 0
    if len(winList) < 6:
        while len(winList) < 6:
            winList.append(loseList[c])
            print('appending encoding' + loseList[c][[0]])
            c += 1

    # for loser in loseList:
    #    geneNum = loser[0]
    #    assassinate('encoding' + str(geneNum) + '.txt')

    # Crossbreed and mutate each bot that won
    i = 0
    while i < len(winList) - 1:
        print('crossbreeding encoding lists: [' + str(i) + ',' + str(i + 1) + ']')
        e.crossbreed(winList[i], winList[i + 1])
        i += 2
    # create more encodings
    e.createMore(winnerList)
    # e.crossbreed('0', '1')
    # reset the gene file
    e.resetGeneFile()
    countTheLength()

