#Abdullah Mohammed 914923231

#This function takes threshold and adjustment factors which are numbers, initWeights which is the initial set of weights supplied for our perceptron in list format,
#examples which is a list, and correctPasses which is the number of passes our perceptron should make through the list of examples 
#This function prints the starting weights, threshold and adjustment, and makes a call to the perceptron recursive function perceptronRecur 
#This function doesn't return anything 
def perceptron(threshold, adjFactor, initWeights, examples, correctPasses):
    print("Starting weights:", stringifyArr(initWeights))
    print("Threshold:", threshold, "Adjustment:", adjFactor, end ="\n\n")

    perceptronRecur(initWeights[:], adjFactor, 1, examples, threshold, correctPasses)
    
    return

#This function takes the adjusted weights which is a list of numbers, the adjustment factor which is how much to adjust our adjWeights list by, 
#passNum which keeps track of how many passes through the example cases have occurred, the list of examples to modify our weights based on,
#the threshold which is a number, and correctPasses which is the number of times we want our perceptron to make a pass through the example cases 
#This function prints the current pass we are at, the inputs in the example case being run, our prediction and the correct answer,
#and the adjusted values after running each example(adjusted values are calculated using the examples input). 
#This function doesn't return anything 
def perceptronRecur(adjWeights, adjFactor, passNum, examples, threshold, correctPasses):
    #Base case: we have passed through the examples the number of times specified 
    if passNum > correctPasses:
        return 

    #New pass has to be run 
    print("Pass", passNum, end = "\n\n")

    #Run the pass
    for val in examples:
        answer = val[0]
        exampleArr = val[1]
        totalPerceptronVal = 0
        prediction = False #arbritrary initialization

        print("inputs:", stringifyArr(exampleArr))

        for i in range(0, len(exampleArr)):
            totalPerceptronVal += exampleArr[i] * adjWeights[i]
        
        if totalPerceptronVal > threshold:
            prediction = True
        elif totalPerceptronVal <= threshold:
            prediction = False
        
        print("prediction:", prediction, "answer:", answer)

        #If prediction differs from the answer modify our weights 
        if prediction == False and answer == True:
            for i in range(0, len(exampleArr)):
                if exampleArr[i] == 1:
                    adjWeights[i] += adjFactor
        elif prediction == True and answer == False:
            for i in range(0, len(exampleArr)):
                if exampleArr[i] == 1:
                    adjWeights[i] -= adjFactor
        
        print("adjusted weights:", stringifyArr(adjWeights))

    #Only add a newline if we have to run another pass
    if passNum < correctPasses: 
        print(end = "\n")

    perceptronRecur(adjWeights, adjFactor, passNum + 1, examples, threshold, correctPasses)

#This function takes in an array of numbers as a parameter 
#This function converts the array to a string in a readable format as specified by the prompt
#This function returns the array converted into a string 
def stringifyArr(arr):
    stringified = "["

    for i in range(0, len(arr)):
        stringified += str(arr[i])

        if i < len(arr) - 1:
            stringified += ", "
        else:
            stringified += "]"
    

    return stringified
