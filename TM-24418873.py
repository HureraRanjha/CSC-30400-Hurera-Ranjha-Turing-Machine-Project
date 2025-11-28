import sys
import os
from io import StringIO

#Start Capturing Terminal Output
real_stdout = sys.stdout
sys.stdout = StringIO()

#The User passes in the Machine Description File and the Test Tape File
if len(sys.argv) < 3:
    print("Usage: python tm.py <machine_file> <tape_file>")
    sys.exit(1)


#Machnine Configuration Variables
machineFilename = sys.argv[1]
tapeFilename = sys.argv[2]
machineName = ""                   #This will be line one the name of the TM
numTapes = 0
#If the tape exceeds Max Tape Length and Max Steps the simulator will halt and give error message
maxTapeLength = 0    
maxNumSteps = 0        
tapeOneAlphabet = []
states = []
startState = ""
acceptState = ""
rejectState = ""
tapeAlphabet = []
transitions = {}

#Read Machine File
a = open(machineFilename, "r")
lineCount = 1 
ruleNum = 1

for line in a:
    seperateLine = line.strip()
    # print(line)

    rawSections = seperateLine.split(",")
    sections = []
    for symbols in rawSections:
        sections.append(symbols.strip())
    if lineCount == 1:                             #Machine Name, Number of Tapes, Max Tape Length, Max Number of Steps
        machineName = sections[0]
        numTapes = int(sections[1])
        maxTapeLength = int(sections[2])
        maxNumSteps = int(sections[3])
    elif lineCount == 2:                          #Tape Alphabet
        for section in sections:
            tapeOneAlphabet.append(section)
    elif lineCount == 3:                          #State Alphabet
        for section in sections:
            states.append(section)
    elif lineCount == 4:                          #Start State
        startState = sections[0]
    elif lineCount == 5:                          #Accept State, Reject State
        acceptState = sections[0]
        rejectState = sections[1]
    elif 6 <= lineCount <= 5 + numTapes :         #Tape Alphabet
        tapeAlphabet.append(sections)
    else:                                         #Input Symbols, New State, New Tape Symbol, Direction
        initialState = sections[0]
        inputSymbol = []

        for i in range(numTapes):
            inputSymbol.append(sections[i + 1])
        newState = sections[numTapes + 1]

        newTapeSymbol = []
        for i in range(numTapes):
            newTapeSymbol.append(sections[numTapes + i + 2])
        
        direction = []
        for i in range(numTapes):
            direction.append(sections[numTapes + numTapes + i + 2])
        
        #Store Transition Rule
        rule = { 
            "initialState" : initialState,
            "inputSymbol" : inputSymbol,
            "newState" : newState,
            "newTapeSymbol" : newTapeSymbol,
            "direction" : direction
        }
        transitions[ruleNum] = rule

        ruleLineParts = [initialState]
        for i in range(numTapes):
            ruleLineParts.append(inputSymbol[i])
        ruleLineParts.append(newState)
        for i in range(numTapes):
            ruleLineParts.append(newTapeSymbol[i])
        for i in range(numTapes):
            ruleLineParts.append(direction[i])

        #Print Rule
        print(str(ruleNum) + ":" + ",".join(ruleLineParts))
        ruleNum += 1

    lineCount += 1

a.close()
# print(tapeFileName)


#Read Tape File 
b = open(tapeFilename, "r")

lineCount = 1 
lines = []
for line in b:
    seperateLine = line.strip()
    lines.append(seperateLine)
    lineCount += 1

b.close()

tests = []
for i in range(0, len(lines), numTapes):
     test = []
     for j in range(numTapes):
        test.append(lines[i + j])
     tests.append(test)

#Load Test Case
def loadTestCase(test):
    tapes = []
    tapeHeads = []

    #Each tape is filled with underscores
    for i in range(numTapes):
        row = ["_"] * maxTapeLength
        inputString = test[i]

        #Copy initial input to tape
        for j in range(len(inputString)):
            row[j] = inputString[j]
        
        tapes.append(row)
        tapeHeads.append(0)                      #Start at the beginning of the tape
    
    return tapes, tapeHeads

#Read Tape
def readTape(tapes, tapeHeads):
    tapeChars = []
    for t in range(numTapes):
        headPosition = tapeHeads[t]
        tapeChars.append(tapes[t][headPosition])
    return tapeChars

#Find Correct Transition
def findCorrectTransition(currentState, inputSymbol):
    for ruleNumber in transitions:
        rule = transitions[ruleNumber]

        #Check if the current state matches the initial state of the rule
        if rule["initialState"] == currentState:
            #Check if the input symbol matches the input symbol of the rule
            matches = True
            for i in range(numTapes):
                checkStar = rule["inputSymbol"][i]
                if checkStar != "*" and checkStar != inputSymbol[i]:
                    matches = False
                    break
            if matches:
                return ruleNumber, rule
    return None, None

#Use Transition
def useTransition(rule, tapes, tapeHeads):
    #write new character
    for i in range(numTapes):
        newSymbol = rule["newTapeSymbol"][i]
        if newSymbol != "*":
            tapes[i][tapeHeads[i]] = newSymbol
    
    #Move tape head
    for i in range(numTapes):
        moveDirection = rule["direction"][i]
        if moveDirection == "R":
            tapeHeads[i] += 1
        elif moveDirection == "L":
            tapeHeads[i] -= 1
        
        #Check if tape head is out of bounds
        if tapeHeads[i] < 0 or tapeHeads[i] >= maxTapeLength:
            return False
    return True

#Check Tape Input
def checkTapeInput(test):
    for i in range(numTapes):
        allowed = tapeAlphabet[i] + ["_"]
        for character in test[i]:
            if character not in allowed:
                return False
    return True

#Simulate Machine
def simulateMachine(test):
    tapes, tapeHeads = loadTestCase(test)
    currentState = startState
    steps = 0

    while True: 
        #Check if maximum number of steps has been exceeded
        if steps >= maxNumSteps:
            return "Error: Exceeded maximum number of steps", tapes
        
        tapeChars = readTape(tapes, tapeHeads)

        #Check if tape has reached the accept/reject state
        if currentState == acceptState:
            return "ACCEPTED",tapes
        if currentState == rejectState:
            return "REJECTED",tapes
        
        #Find Correct Transition
        ruleNumberFound, rule = findCorrectTransition(currentState, tapeChars)
        if rule is None:
            return "Error: No correct transition", tapes
        
        #Print Fields
        printFields = []

        printFields.append(str(steps))              # step
        printFields.append(str(ruleNumberFound))    # rule

        for i in range(numTapes):                   
            printFields.append(str(tapeHeads[i]))   # tape head positions

        printFields.append(currentState)            # state

        for i in range(numTapes):                   # input symbols
            printFields.append(tapeChars[i])

        printFields.append(rule["newState"])        # new state

        for i in range(numTapes):                   # new symbols
            printFields.append(rule["newTapeSymbol"][i])

        for i in range(numTapes):                   # directions
            printFields.append(rule["direction"][i])

        print(",".join(printFields))
        
        
        correct = useTransition(rule, tapes, tapeHeads)
        if not correct:
            return "Error: Transition failed", tapes
        
        currentState = rule["newState"]
        steps += 1

print("MACHINE: " + machineName)
print("TAPES: " + str(numTapes))
print("MAX STEPS: " + str(maxNumSteps))
print("TAPE FILE:", str(tapeFilename))
print("_" * 40)

#Run Tests
for test in tests:
    #Print Tape
    for t in range(numTapes):
        print("Tape " + str(t+1) + ":" + test[t])
    
    #Check Tape Input
    if not checkTapeInput(test):
        print("Error")
        continue
    
    status, finalTapes = simulateMachine(test)

    print(status)

    if status != "ACCEPTED":
        print("REJECTED")


    
    # Show first part of each tape
    for t in range(numTapes):
        tapeStr = "".join(finalTapes[t]).rstrip("_")
        print("Tape " + str(t+1) + ":" + tapeStr)
    print("-" * 50)


full_output = sys.stdout.getvalue()   # capture everything printed
sys.stdout = real_stdout

#Write Results to File
output_name = os.path.join(os.getcwd(), "results-" + os.path.basename(tapeFilename))
with open(output_name, "w") as f:
    f.write(full_output)