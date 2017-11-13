import random
import main

class Encoding:
    encodingList = []
    generationNumber = -1
    # will be a list of tuples
    # (encoding,fitness score)

    # Line in encoding log will be
    # encoding, fitness score
    def __init__(self):
        log = open('encoding.txt', 'r+')
        for lineNum in range(0, self.file_len(log)):
            # if it's the first line of the file it will be the generation number
            if lineNum == 1:
                self.generationNumber = log[lineNum]
            # otherwise it is an encoding,fitness pair
            else:
                self.encodingList.append(log[lineNum].split(','))

    # Getters and Setters
    def setGenerationNumber(self,genNum):
        self.generationNumber = genNum

    def setEncodingList(self, encode):
            self.encodingList = encode

    def getEncoding(self):
        return self.encodingList

    def getGenerationNum(self):
        return self.generationNumber

    # Actual Methods
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
        fName = 'log_gen' + genNum
        file = open(fName, 'w')
        fName.write(genNum)
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
        for x in encoding:
            # 1% chance to mutate to a random strat
            if mutateChance == 42:
                out = out + (random.randint(0, 5))
            # 99% chance to keep the same strat
            else:
                out = out + x
        return out


if __name__ == '__main__':
    e = Encoding()
    newEncodeList = []
    currFitness = -1
    currEncoding = ''
    newFitness = -1
    newEncoding = ''

    currEncoding = e.getEncoding()

    for x in currEncoding:
        print(e)
        currEncoding = e[0]
        currFitness = e[1]
        # start a new bot for each of the encodings
        main.go()
        # returns a fitness score f eventually
        newEncodeList.append((newFitness, newEncoding))
    # TODO: figure out how to pass in the generation number
    e.archiveLog(42)
    e.setEncodingList(newEncodeList)

    # go through the list of encodings and crossbreed/mutate them
    for x in range(0,len(e-1)):
        # separates the two encodings
        e1 = e[x][0]
        e2 = e[x+1][0]
        # places the returned crossbred encodings in a temp list
        tmpList = e.crossbreed(e1, e2)
        # replaces the old encodings with the new encodings
        e[x][0] = tmpList[1]
        e[x+1][0] = tmpList[2]
