import aiml
import time
time.clock = time.time

kernel = aiml.Kernel()
kernel.learn('chat_base.aiml')

while True:
    input_text = input('User: ').upper()
    if input_text == 'EXIT':
        print('Exiting program')
        break
    else:
        response = kernel.respond(input_text)
        print('Bot: ' +response)