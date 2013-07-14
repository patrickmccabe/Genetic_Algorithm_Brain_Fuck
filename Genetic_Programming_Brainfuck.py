import random
import time


def example():
    randomProgram = createRandomPrograms(10,20,"Hi!")
    main(randomProgram)


def createRandomPrograms(numberOfPrograms,lengthOfPrograms, goalOutput):
    instructions = ['>','<','+','-','.','[',']'] # all the possible instructions
    newProgramChars = ""
    programList = []

    i = 0
    while i <= numberOfPrograms: # iterate through the number of programs
        k = 0
        newProgramChars = ""

        while k <= lengthOfPrograms: # iterate through the length of each program
            newProgramChars += instructions[random.randint(0,len(instructions)-1)] # add a random instruction
            k +=1                                       
                                            
        newProgram = Program(newProgramChars, goalOutput) # create the new program
        if newProgram.bracketsAreGood(): # check to see if brackets are good
            programList.append(Program(newProgramChars, goalOutput)) # if they are then add the program to the list
            i += 1  # create the next program

    return programList



def sortPrograms(programs): # sorts the programs from most to least fit and returns the sorted list
    return sorted(programs,key = lambda program:program.fitness())




def runPrograms(programs): # takes a list of programs and runs them
    output = []
    for i in range(len(programs)):
        programs[i].run()
        output.append(programs[i].outputString)

    return output


def main(programs):
    startTime = time.time()
    runPrograms(programs)
    programs = sortPrograms(programs)
    generation = 0
    solutionFound = False
    keepSolutions = len(programs)/3 # keep 3 solutions
    
    while solutionFound == False:

        for i in range(keepSolutions):# iterate through the programs we are keeping
            programs[i] = programs[i].cleanUp() # clean them up for later
            pass

        
        for i in range(keepSolutions,len(programs)):
            copyProgram = programs[random.randint(0,keepSolutions-1)]
            newProgram = Program(copyProgram.programChars,copyProgram.goalOutput).crossOver(programs[random.randint(0,keepSolutions-1)]) # preform cross over
            #newProgram = programs[random.randint(0,keepSolutions-1)]
            newProgram = newProgram.mutate(generation) # preform mutation
            programs[i] = newProgram # save new program
            
        runPrograms(programs)
        programs = sortPrograms(programs)
        generation += 1

        if generation%500 == 0:
            elapsedTime = time.gmtime(time.time() - startTime)
            strTime = time.strftime("%H:%M:%S", elapsedTime)
            print "generation: %d" % (generation)
            print "time elasped: %s" % strTime
            print "fitness: %d" % (programs[0].fitness())
            print(programs[0])
            print programs[0].outputString
            print "fitness: %d" % (programs[1].fitness())
            print(programs[1])
            print programs[1].outputString
            print "fitness: %d" % (programs[2].fitness())
            print(programs[2])
            print programs[2].outputString
            print ""

    
        for k in range(len(programs)):
            if programs[k].goalOutput == programs[k].outputString:
                elapsedTime = time.gmtime(time.time() - startTime)
                strTime = time.strftime("%H:%M:%S", elapsedTime)
                print ""
                print "--------Solution Found!--------"
                print "Generation: %d" % (generation)
                print "Programs Per Generation: %d" % (len(programs)-1)
                print "Time Elasped: %s" % strTime
                print(programs[k].fitness())
                print(programs[k])
                print ""
                print "Cleaned up version:"
                print programs[k].cleanUp()
                print programs[k].outputString
                solutionFound == True
                return programs


    

class Program():
    def __init__(self,programChars,goalOutput):
        self.programChars = programChars
        self.goalOutput = goalOutput


    def bracketsAreGood(self): # checks to see if the brackets balance
        bracketBalance = 0

        for character in self.programChars:
            if character == '[':
                bracketBalance += 1
            elif character == ']':
                if bracketBalance == 0:
                    return False
                else:
                    bracketBalance -= 1

        if bracketBalance != 0:
            return False


        bracketBalance = 0
        for character in reversed(self.programChars):
            if character == '[':
                if bracketBalance == 0:
                    return False
                else:
                    bracketBalance += 1
            elif character == ']':
                bracketBalance -= 1
                
        if bracketBalance != 0:
            return False
        else:
            return True



    def run(self): # runs the program
        if(self.bracketsAreGood() == False):
            self.outputString = ""
            return False
        else:
            pointer = 0
            numberOfInstructions = 0
            data = [0]*1000
            timeOutLength = len(self.programChars)*5
            self.outputString = ""

            i = 0 # the instruction pointer that goes through the characters of the program
            while i < len(self.programChars):
                currentChar = self.programChars[i]

                if currentChar == '>': # increment the data pointer
                    pointer += 1
                    
                elif currentChar == '<': # decrement the data pointer
                    pointer -= 1
                    
                elif currentChar == '+': # increment the value at the pointer index
                    if data[pointer] == 255: # wrap the value if too large
                        data[pointer] = 0
                    else:
                        data[pointer] = data[pointer] + 1

                elif currentChar == '-': # decrement the value at the pointer index
                    if data[pointer] == 0: # wrap the value if too small
                        data[pointer] = 255
                    else:
                        data[pointer] = data[pointer] - 1
    
                elif currentChar == '.': #print the value (char) at the data pointer
                    self.outputString += (chr(data[pointer]))
                    #print chr(data[pointer])
    
                elif currentChar == '[':
                    if data[pointer] == 0: # if this is true then jump to the closing bracket
                        i += self.findClosingBracket(i)
                    else:
                        pass # do nothing, the instruction pointer will increment like normal
    
                elif currentChar == ']':
                    if data[pointer] != 0: # if this is true then jump to the opening bracket
                        i += self.findOpeningBracket(i)
                    else:
                        pass # do nothing, the instruction pointer will increment like normal
    
                if pointer < 0: # wrap the pointer if it is negative
                    pointer += len(data)
                if pointer >= len(data): # wrap the pointer if it is larger than the data list length
                    pointer -= len(data)
                        
                numberOfInstructions += 1
    
                if numberOfInstructions > timeOutLength:
                    self.outputString = ""
                    return False

                i += 1
    
            return True


    def findClosingBracket(self,indexOfOpeningBracket): # returns the number of chars away the closing bracket is
        bracketBalance = 1 # set the balance to 1 since we know there is one opening bracket
        numberOfCharsAway = 1 # the number of chars away the opening bracket is from the closing

        for i in range(indexOfOpeningBracket+1,len(self.programChars)): # iterate through the program
            currentChar = self.programChars[i]

            if currentChar == '[':
                bracketBalance += 1
            if currentChar == ']':
                bracketBalance -= 1
            if bracketBalance == 0:
                return numberOfCharsAway

            numberOfCharsAway += 1

        return 0

    

    def findOpeningBracket(self,indexOfClosingBracket): # returns the number of chars away the opening bracket is
        bracketBalance = -1 # set the balance to -1 since we know there is one closing bracket
        numberOfCharsAway = -1 # the number of chars away the opening bracket is from the closing

        i = indexOfClosingBracket - 1
        while i >= 0: # iterate through the program
            currentChar = self.programChars[i]

            if currentChar == '[':
                bracketBalance += 1
            if currentChar == ']':
                bracketBalance -= 1
            if bracketBalance == 0:
                return numberOfCharsAway

            numberOfCharsAway -= 1
            i -= 1

        return 0

    

    def displayOutput(self): # print the output of the program
        
        for i in range(len(self.outputString)):
            print(self.outputString[i])



    def __str__(self): # allows the printing of a program
        return self.programChars



    def fitness(self): # returns the fitness of the program (lower is better)
        self.fitnessValue = 0
        i = 0

        while i < len(self.goalOutput):
            if len(self.outputString) > i:
                currentOutputValue = ord(self.outputString[i])
                currentGoalValue = ord(self.goalOutput[i])
                difference = abs(currentOutputValue - currentGoalValue)
                self.fitnessValue += (difference)
            else:
                self.fitnessValue += ord(self.goalOutput[i])
            i += 1

        if len(self.outputString) > len(self.goalOutput):
            k = i
            while k < len(self.outputString):
                self.fitnessValue += ord(self.outputString[i])
                k += 1
            
        if len(self.outputString) == 0: # programs that print nothing are not fit
            self.fitnessValue = 100000    # so they get a high fitness value
        
        self.fitnessValue += len(self.programChars) / 10 # penalize long programs (10)       
        return self.fitnessValue



    def crossOver(self, motherProgram):
        
        crossOverChance = random.randint(1,10) # 1 in 10 chance of crossover
        
        if crossOverChance == 1:
            crossType = random.randint(1,4) # randomly choose the cross over time
            fatherProgramChars = self.programChars[:]
            motherProgramChars = motherProgram.programChars[:]
            crossOverLocationFather = random.randint(len(fatherProgramChars)/2,len(fatherProgramChars)-1) # randomly select a cross over location on the father
            crossOverLocationMother = random.randint(len(motherProgramChars)/2,len(motherProgramChars)-1) # randomly select a cross over location on the mother

            crossOverLocationFatherSub1 = random.randint(0,len(fatherProgramChars)-1)
            crossOverLocationFatherSub2 = random.randint(0,len(fatherProgramChars)-1)
            crossOverLocationMotherSub1 = random.randint(0,len(motherProgramChars)-1)
            crossOverLocationMotherSub2 = random.randint(0,len(motherProgramChars)-1)
            
                                                         
            if crossType == 1:
                newProgramChars = fatherProgramChars[:crossOverLocationFather+1] + motherProgramChars[crossOverLocationMother:]
                return Program(newProgramChars, self.goalOutput)
            elif crossType == 2:
                newProgramChars = motherProgramChars[:crossOverLocationMother+1] + fatherProgramChars[crossOverLocationFather:]
            elif crossType == 3:
                newProgramChars = fatherProgramChars[:crossOverLocationFatherSub1+1] + motherProgramChars[crossOverLocationMotherSub1:crossOverLocationMotherSub2+1] + fatherProgramChars[crossOverLocationFatherSub2:]
            elif crossType == 4:
                newProgramChars = motherProgramChars[:crossOverLocationMotherSub1+1] + fatherProgramChars[crossOverLocationFatherSub1:crossOverLocationFatherSub2+1] + motherProgramChars[crossOverLocationMotherSub2:]
            return Program(newProgramChars, self.goalOutput)

        else:
            return self
    
        
    def mutate(self,generation):
        characterToChoose = ['>','<','+','-','.','[',']'] # a list of character to randomly choose from
        mutateChance = 80                                 # 1 out of 80 characters will mutate (lower seems to work better)
        newProgramChars = self.programChars[:]            # make the new program equal to the current one

        
        for i in range(len(newProgramChars)):       # iterate through the program
            mutationType = random.randint(1,3)      # randomly choose a mutation type
            if random.randint(1,mutateChance) == 1: # if the odds are satisfied
                if mutationType == 1: # replacement
                    randomCharacter = characterToChoose[random.randint(0,len(characterToChoose)-1)] # choose a random character
                    newProgramChars = newProgramChars[:i] + randomCharacter + newProgramChars[i+1:] # execute the mutation
                if mutationType == 2: # deletion
                    newProgramChars = newProgramChars[:i] + newProgramChars[i+1:]                   # execute the mutation
                if mutationType == 3: # insertion
                    randomCharacter = characterToChoose[random.randint(0,len(characterToChoose)-1)] # choose a random character
                    newProgramChars = newProgramChars[:i] + randomCharacter + newProgramChars[i:]   # execute the mutation


        return Program(newProgramChars, self.goalOutput)

                

    def cleanUp(self): # removes pieces of code that undo each other
        i = 0
        newChars = ""
        while i < len(self.programChars):
            cleaned =  False
            if i != len(self.programChars)-1:
                if self.programChars[i] == '<':
                    if self.programChars[i+1] == '>':
                        cleaned = True
                elif self.programChars[i] == '>':
                    if self.programChars[i+1] == '<':
                        cleaned = True
                elif self.programChars[i] == '+':
                    if self.programChars[i+1] == '-':
                        cleaned = True
                elif self.programChars[i] == '-':
                    if self.programChars[i+1] == '+':
                        cleaned = True

            if cleaned == False:
                newChars += (self.programChars[i])
            else:
                i += 1

            i += 1
        return Program(newChars,self.goalOutput)
