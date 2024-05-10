import json
import re

with open("test.txt", "r") as file:
  lines = file.readlines()

result = []
i = 1

for j in range(len(lines)):
  re.sub(r'\n+', '\n', lines[j])
  lines[j] = lines[j].replace("  ", " ")

for j in range(len(lines)):
  question = {}

  if lines[j].startswith("Question ID:") or lines[j].startswith("\section*{Question ID:"):
    # Adding the Question Number.
    question["questionNumber"] = i
    i += 1

    # Extracting the Question ID.
    splitLines = lines[j].split(": ")
    questionID = splitLines[1].replace("}\n", "").replace("\n", "")
    question["questionId"] = questionID

    # Extracting the Question Text.
    questionText = lines[j+2]
    k = j+3
    while not (lines[k].startswith("(A)")):
      questionText += lines[k]
      k += 1
    questionText = questionText.replace("\n\n", "\n")
    question["questionText"] = questionText

    #Extracting Question Options.
    options = []
    tempOpts = []
    while not (lines[k].startswith("\section*{Answer") or lines[k].startswith("Answer")):
      tempOpts.append(lines[k])
      k += 1
    splitted = lines[k].split("(")
    correct = splitted[1][0]
    correct = ord(correct) - ord('A') + 1
    tempOpts = [item for item in tempOpts if item != '\n']
    tempOpts[0] = tempOpts[0].replace("(A) ", "").replace("A. ", "").replace("\n", "")
    tempOpts[1] = tempOpts[1].replace("(B) ", "").replace("B. ", "").replace("\n", "")
    tempOpts[2] = tempOpts[2].replace("(C) ", "").replace("C. ", "").replace("\n", "")
    tempOpts[3] = tempOpts[3].replace("(D) ", "").replace("D. ", "").replace("\n", "")
    for l in range(4):
      option = {}
      option["optionNumber"] = l + 1
      option["optionText"] = tempOpts[l]
      option["isCorrect"] = (correct == l + 1)
      options.append(option)
    question["options"] = options

    # Extracting the Solution Text.
    solutionText = ""
    k += 2
    while k < len(lines) and not (lines[k].startswith("\section*{Question ID:") or lines[k].startswith("Question ID:")):
      solutionText += lines[k]
      k += 1
    solutionText = solutionText.replace("\n\n", "\n").replace("Sol. ", "")
    question["solutionText"] = solutionText

    # Appending the question.
    result.append(question)

with open('result.json', 'w') as jsonFile:
  json.dump(result, jsonFile, indent=2)
