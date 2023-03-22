import aiml
import time
time.clock = time.time

kernel = aiml.Kernel()
kernel.learn('std-startup.xml')
kernel.respond('load aiml b')

while True:
    input_text = input('Human: ').upper()
    if input_text == 'EXIT':
        print('Exiting program')
        break
    else:
        response = kernel.respond(input_text)
        print('Bot: ' +response)