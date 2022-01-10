import csv

baseline = []
predictions = []
results = []

with open('data/truth.csv', mode ='r') as truthFile:
    truthReader = csv.reader(truthFile)
    subResult = []
    for resultArray in truthReader:
        result = resultArray[0]
        if (result != '==================================NEW_WEEK===================================='):
            subResult.append(result)
        elif (result == '==================================NEW_WEEK====================================' and len(subResult) > 0):
            results.append(subResult)
            subResult = []
results.append(subResult)

with open('data/result_baseline.csv', mode ='r') as resultFile:
    resultReader = csv.reader(resultFile)
    subResult = []
    for resultArray in resultReader:
        result = resultArray[0]
        if (result != '==================================NEW_WEEK===================================='):
            subResult.append(result)
        elif (result == '==================================NEW_WEEK====================================' and len(subResult) > 0):
            baseline.append(subResult[:10])
            subResult = []
baseline.append(subResult[:10])

with open('data/result_prediction.csv', mode ='r') as resultPredictionFile:
    resultPredictionReader = csv.reader(resultPredictionFile)
    subPredictionResult = []
    for resultPredictionArray in resultPredictionReader:
        result = resultPredictionArray[0]
        if (result != '==================================NEW_WEEK===================================='):
            subPredictionResult.append(result)
        elif (result == '==================================NEW_WEEK====================================' and len(subPredictionResult) > 0):
            predictions.append(subPredictionResult)
            subPredictionResult = []
predictions.append(subPredictionResult)

correctPrediction = 0
correctBaseline = 0
total = 0

for i, result in enumerate(results):
    # Check Matches From Initial Predictions
    for predict in predictions[i]:
        total += 1
        if predict in result:
            correctPrediction += 1
    for base in baseline[i]:
        if base in result:
            correctBaseline += 1

print("==================================FINAL RESULTS====================================")

print("Correct Predictions: " + str(correctPrediction))
accuracyPrediction = correctPrediction / total * 100
print("Prediction Accuracy: " + str(accuracyPrediction) + "%")

print("Correct Controls: " + str(correctBaseline))
accuracyBaseline = correctBaseline / total * 100
print("Prediction Accuracy: " + str(accuracyBaseline) + "%")

print("Total Predictions: " + str(total))

print("Performance: " + str(accuracyPrediction - accuracyBaseline) + "%")