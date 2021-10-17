#
# TODO:
# 1. Dont ask for user's name after each retry
# 2. Reorg code: standalone, server versions
# 3. Clean up cloud app

import pywebio
import random
from pywebio.input import *
from pywebio.output import put_text, put_html, put_markdown, put_table, put_buttons
from pywebio.session import *

op = {}
op['Try Again'] = 'window.location.reload()'
op['Close window'] = 'window.close()'

def tab_operation(choice):
    run_js(op[choice])
    
def guess_num():
    # Guess the number game

    maxNum = 100
    maxGuesses = 15
    guessesTaken = 0

    #put_markdown('Hello! What is your name?')
    myName = input("Hello! What is your name?")

    #while True:
    number = random.randint(1, maxNum)
    put_markdown('Ok %s, I\'m thinking of number between 1 and %.0f' % (myName, maxNum))

    for guessesTaken in range(0, maxGuesses):

        guessesLeft = (maxGuesses - guessesTaken - 1)
 
        inc = 0.10
        percentGuessesLeft = guessesLeft / maxGuesses
        status_emojis = [(1.0, ''),
                         (inc*6, '\U0001F92D'), #\N{face with hand over mouth}'),
                         (inc*5, '\N{thinking face}'), 
                         (inc*4, '\U0001F92B'), #\N{shushing face}'),
                         (inc*3, '\U0001F633'), #\N{⊛ face with open eyes and hand over mouth}'),
                         (inc*2, '\U0001F62C'),
                         (inc, '\U0001F631')] #\N{⊛ face with peeking eye}')]
                         #(float('inf'), 'Severely obese')]

        statusMsg = 'You have `%s` guesses left.' % (guessesLeft)
        emoj = ''
        for guesses, emoj in status_emojis:
            if percentGuessesLeft <= guesses:
                statusMsg = 'You have `%s` guesses left. %s' % (guessesLeft, emoj)


        #put_markdown('Take a guess.') # 4 spaces to indent
        try:
            guess = input("Take a guess.", type=NUMBER)
            guess = int(guess)
        except:    
            put_markdown('That\'s not a number %s! %s' % (myName, statusMsg))
            continue

        if guess == number:
            break
        elif guess < number:
            put_markdown('Your guess is too low. ' + statusMsg)
        elif guess > number:
            put_markdown('Your guess is too high. ' + statusMsg)

    if guess == number:
        guessesTaken = str(guessesTaken + 1)
        put_text('Good job, %s! You guessed number in %s guesses! %s' % (myName, guessesTaken, "\U0001F60A \U0001F64C"))

    if guess != number:
        put_text('Hard luck! The number I was thinking of was %0.f. %s' % (number, "\U0001F62D"))

    put_buttons(op.keys(), onclick=tab_operation)
    hold()

if __name__ == '__main__':
    import argparse
    from pywebio.platform.tornado_http import start_server as start_http_server
    from pywebio import start_server as start_ws_server

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    parser.add_argument("--http", action="store_true", default=False, help='Whether to enable http protocol for communicates')
    args = parser.parse_args()

    if args.http:
        start_http_server(guess_num, port=args.port)
    else:
        # Since some cloud server may close idle connections (such as heroku),
        # use `websocket_ping_interval` to  keep the connection alive
        start_ws_server(guess_num, port=args.port, websocket_ping_interval=30)

