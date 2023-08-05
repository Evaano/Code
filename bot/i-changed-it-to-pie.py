import re
import aiml
import random
import time

time.clock = time.time

def preprocessSingleInput(bot, theInput):
    subbed1 = bot._subbers['normal'].sub(theInput).upper()
    subbed2 = re.sub(bot._brain._puncStripRE, " ", subbed1)
    return subbed2

debug = False
debug2 = False
theAIMLfile = 'idk.aiml'
theQuestionsFileName = "coursework-questions-and-responses.txt"
responsesFileName = theAIMLfile[:-5] + "-responses.txt"
feedbackFileName = theAIMLfile[:-5] + "-feedback.txt"
NUMQS = 45
NUMCONTEXTQS = 3
contextQuestions = [35, 42, 44]

questions = []
responses = []

qFile = open(theQuestionsFileName, 'r')
thisQ = 0

while True:
    line = qFile.readline()
    if not line:
        print("unexpected end of file")
        break
    elif (line[0] != 'Q'):
        print("didn't get expected question marker Q")
        break
    elif (int(line[1:3]) != thisQ):
        print("question had wrong number")
        break
    else:
        questions.append(line[5:-1])
        if debug2:
            print("question {} is: {}".format(thisQ, questions[thisQ]))

    line = qFile.readline()
    if not line:
        print("unexpected end of file")
        break
    elif (line[0] != 'A'):
        print("didn't get expected answer marker A")
        break
    elif (int(line[1:3]) != thisQ):
        print("answer had wrong number")
        break
    else:
        responses.append(line[5:-1])
        if debug2:
            print("response {} is: {}".format(thisQ, responses[thisQ]))

    thisQ += 1
    line = qFile.readline()

    if not line:
        break
    if debug2:
        print("")

qFile.close()

CQ1 = contextQuestions[0]
CQ2 = contextQuestions[1]
CQ3 = contextQuestions[2]
toremove = [(CQ1 - 1), CQ1, (CQ2 - 1), CQ2, (CQ3 - 1), CQ3]

order = []
for i in range(NUMQS):
    if i not in toremove:
        order.append(i)
random.shuffle(order)

order.insert(10, (CQ1 - 1))
order.insert(11, CQ1)
order.insert(20, (CQ2 - 1))
order.insert(21, CQ2)
order.insert(30, (CQ3 - 1))
order.insert(31, CQ3)

for i in range(NUMQS):
    if i not in order:
        print("{} is missing".format(i))

if thisQ < NUMQS:
    print("error, only {} question-answer pairs read".format(thisQ))
elif len(questions) < NUMQS or len(responses) < NUMQS:
    print("error, somehow the questions or responses have not all be saved")
    if debug:
        print(" {} questions and {} responses read, thisQ = {}".format(len(questions), len(responses), thisQ))
else:
    print('{} question-response pairs read for testing your bot'.format(thisQ))

checkBot = aiml.Kernel()
checkBot.verbose(True)

checkBot.resetBrain()
checkBot.learn(theAIMLfile)

numCategories = checkBot.numCategories()
print("After reading your file the bot has {} categories".format(numCategories))
print("Remember that the bot will overwrite categories with the same pattern, that, and topic".format(numCategories))
print('This number should help you fix misformed categories if needed\n')

file2 = open(theAIMLfile, 'r')
srai_count = 0
set_count = 0
wildcard_count = 0
starslash_count = 0
that_count = 0
condition_count = 0

while True:
    line = file2.readline()
    if not line:
        break
    if "<srai>" in line:
        srai_count += 1
    if "<set" in line:
        set_count += 1
    if ("*" in line) or ("_" in line) or ("^" in line) or ("#" in line):
        wildcard_count += 1
    if "<star" in line:
        starslash_count += 1
    if "<that" in line:
        that_count += 1
    if "<that" in line:
        condition_count += 1

file2.close()

numCorrect = 0
numContextQsCorrect = 0
numNoMatch = 0
responsesFile = open(responsesFileName, 'w')

for q in range(NUMQS):
    thisQ = order[q]
    botResponse = checkBot.respond(questions[thisQ])
    if botResponse == "":
        numNoMatch += 1
    responsesFile.write('Q{:2d}: {}\n'.format(thisQ, questions[thisQ]))
    responsesFile.write('Expected response: {}\n'.format(responses[thisQ]))
    responsesFile.write('Your bot response: {}\n'.format(botResponse))
    if botResponse == responses[thisQ]:
        responsesFile.write('*** Question answered correctly\n\n')
        numCorrect += 1
        if thisQ in contextQuestions:
            numContextQsCorrect += 1
    else:
        responsesFile.write('Question answered incorrectly\n\n')
        if debug:
            theInput = questions[thisQ]
            print('Q{} {}\n gets preprocessed as:{}'.format(thisQ, theInput, preprocessSingleInput(checkBot, theInput)))
            print(' expected :' + responses[thisQ])
            print(' got      :' + botResponse)
            lastThat = checkBot.getPredicate("_outputHistory")

responsesFile.write(' In total you got {} questions correct'.format(numCorrect))
responsesFile.close()

feedbackFile = open(feedbackFileName, 'w')

finalScore = numCorrect
if numCorrect == NUMQS:
    if numCategories < 10:
        finalScore = 100
    else:
        finalScore = 90 - numCategories

feedbackFile.write('<SCORE>{}</SCORE>\n'.format(finalScore))

fstart = "<MESSAGE>"
fend = "</MESSAGE>\n"

feedback = fstart + "After removing duplicates, your bot used " + str(numCategories) + " categories" + fend
feedbackFile.write(feedback)

if numCorrect < NUMQS:
    feedback = fstart + "Your bot answered one or more questions incorrectly." + fend
    feedbackFile.write(feedback)
    feedback = fstart + "File " + responsesFileName + " has more details of your bot's responses." + fend
    feedbackFile.write(feedback)
    feedback = fstart + "Common mistakes are typos or extra spaces" + fend
    feedbackFile.write(feedback)

    if numNoMatch > 0:
        feedback = fstart + "For " + str(numNoMatch) + " questions, your bot did not have a matching category." + fend
        feedbackFile.write(feedback)
    contextErrors = NUMCONTEXTQS - numContextQsCorrect
    if contextErrors > 0:
        feedback = fstart + "Your bot answered incorrectly for " + str(contextErrors) + " questions that require a sense of context." + fend
        feedbackFile.write(feedback)

else:
    feedback = fstart + "Your bot answered every question correctly using " + str(numCategories) + " categories" + fend
    feedbackFile.write(feedback)
    if srai_count == 0 or wildcard_count == 0 or starslash_count == 0:
        feedback = fstart + "You can improve your score by generalizing using srai and wildcards." + fend
        feedbackFile.write(feedback)
    if set_count == 0 or that_count == 0:
        feedback = fstart + "You can improve your score by remembering context and what the conversation is talking about." + fend
        feedbackFile.write(feedback)
    if condition_count == 0:
        feedback = fstart + "You can use <condition> to change behavior within a category." + fend
        feedbackFile.write(feedback)
    if numCategories <= 11:
        feedback = fstart + "Congratulations, you have matched Jim's score!" + fend
        feedbackFile.write(feedback)

feedbackFile.close()
