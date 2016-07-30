import string
import copy
from collections import Counter
#from scipy import spatial



class Question:

    def __init__(self):
        # Each rocket has an (x,y) position.
        self.text = ''
        self.topics = []
        self.vSpace = []
        
    def printQuestion(self):
        print "T: " + str(self.topics) + "Q: " + str(self.text)

    def printText(self):
        print self.text

    
    def printComparison(self):
        print "T: " + str(self.topics) + "Q: " + str(self.text) + str(self.vSpace)


class Brain:
    def __init__(self):
        self.numTrainQs = 0
        self.numEvalsQs = 0
        self.trainQs = [] #Note this is list of type questions
        self.evalQs = []  #Note this is list of type questions
        self.cTrainQs = [] 
        self.cEvalQs = [] 
        self.wordVec = []
        self.wordDict = {}
        self.df = {}
        self.tf = {}

    def printBrain(self):
        print "Number of Training Quesetions: " + self.numTrainQs
        print "Number of Evaluation Questions: " + self.numEvalQs
        
        print "Training Questions: " 
        for i in range(0, len(self.trainQs)):
            self.trainQs[i].printQuestion()
            self.cTrainQs[i].printText()

            
        print "Evaluation Questions: " 
        for i in range(0, len(self.evalQs)):
            self.evalQs[i].printQuestion()
            self.cEvalQs[i].printText()

        #print "Clean Training Questions: "
        #for i in range(0, len(self.cTrainQs)):
            #self.cTrainQs[i].printText()

        #print "Clean Evaluation Questions: "
        #for i in range(0, len(self.cEvalQs)):
            #self.cEvalQs[i].printText()

        print "Word Vector: " 
        print self.wordVec

        print "Word Dictionary: " 
        print self.wordDict
        
        print self.df
        print self.tf
                
    def printQuick(self):
        print "Number of Training Quesetions: " + self.numTrainQs
        print "Number of Evaluation Questions: " + self.numEvalQs

        #print "Word Vector: " 
        #print self.wordVec

        print "Word Dictionary: " 
        print self.wordDict
        
        print self.df
        print self.tf


    
def buildWordDict(data): # O(n^2) need to watch this function
    data.wordDict = {}
    for i in range(0, len(data.cTrainQs)):
        listOfWords = data.cTrainQs[i].text.split()
        for j in range(0, len(listOfWords)):
            if listOfWords[j] in data.wordDict:
                data.wordDict[listOfWords[j]] = data.wordDict[listOfWords[j]] + 1
            else:
                data.wordDict[listOfWords[j]] = 1
    #print data.wordDict

        
def buildWordVector(data):
    data.wordVec = sorted( data.wordDict.keys() )


def assignVectorSpace(data):   #NEEDS WORK - count() finds substrings too :(
    for i in range(0, len(data.cTrainQs)):
        vectorSpace = []

        for j in range(0, len(data.wordVec)):
            vectorSpace.append(data.cTrainQs[i].text.count(data.wordVec[j] ) )

            #if data.cTrainQs[j].text == data.wordVec[i]:
        data.trainQs[i].vSpace = vectorSpace

    for i in range(0, len(data.cEvalQs)):
        vectorSpace = []

        for j in range(0, len(data.wordVec)):
            vectorSpace.append(data.cEvalQs[i].text.count(data.wordVec[j] ) )

            #if data.cTrainQs[j].text == data.wordVec[i]:
        data.evalQs[i].vSpace = vectorSpace
        

    
def cleanQs(data): #remove punctuation *******Improvement spot******

    #exclude = set( ["'s", string.punctuation  )
    #s = ''.join(ch for ch in s if ch not in exclude)
    
    data.cTrainQs = copy.deepcopy(data.trainQs)
    data.cEvalQs = copy.deepcopy(data.evalQs)
    for i in range(0, len(data.cTrainQs)):
        data.cTrainQs[i].text = data.cTrainQs[i].text.translate(string.maketrans("",""), string.punctuation).lower()
    for i in range(0, len(data.cEvalQs)):
        data.cEvalQs[i].text = data.cEvalQs[i].text.translate(string.maketrans("",""), string.punctuation ).lower()
        
def readQuestions(t, e):
    f = open('small_sample.in', 'r' )
    numbers = f.readline()
    qArray = [] #to speed this up I could form to 2t + e + 1 size
    eArray = []
    for i in range(0, int(t)):
        q = Question()
        q.topics = f.readline()
        q.text = f.readline()
        qArray.append(q)
    for i in range(0, int(e)):
        q = Question()
        q.text = f.readline()
        eArray.append(q)
    '''
    for i in range(0, len(qArray)):
        qArray[i].printQuestion()
    for i in range(0, len(eArray)):
        eArray[i].printQuestion()
    '''
    return [qArray, eArray]


def getNumbers():
    f = open('small_sample.in', 'r' )
    numbers = f.readline()
    trainQs = numbers.split()[0]
    evalQs = numbers.split()[1]
    f.close
    array = [ trainQs, evalQs ]
    return array
    

def main():
    #Data Store
    data = Brain() #everything goes in here

    #Numbers
    nums = getNumbers()
    data.numTrainQs = nums[0]
    data.numEvalQs = nums[1]
    #print "Training Questions: " + data.numTrainQs
    #print "Evaluation Questions: " + data.numEvalQs

    #Questions to Memory
    qData = readQuestions(data.numTrainQs, data.numEvalQs)
    data.trainQs = qData[0]
    data.evalQs = qData[1]

    #build the clean questions
    cleanQs(data)
    
    #get word Dictionary
    buildWordDict(data)

    #get Word Vector
    buildWordVector(data)



    #questions 
    assignVectorSpace(data)

    #assignVectorSpace(evalData)



    #print only after the build functions are called 
    data.printBrain()

    #Vector Space Cos/Jaccard/Euclid

    for i in data.trainQs:
        i.printComparison()

    for i in data.evalQs:
        i.printComparison()


    #for i in range(0, len(data.trainQs)):
        #for j in range(0, len(data.evalQs)):
            #print 1 - spatial.distance.cosine(data.trainQs[i], data.evalsQs[j])
                   
    
    #KNN

    #
    

    

if __name__ == '__main__':
    main()
