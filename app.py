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
from timeit import default_timer as timer

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

        emoj = ''
        for guesses, emoj in status_emojis:
            if percentGuessesLeft <= guesses:
                break  # emoj has been set by loop ;)
        extraMsgs = [
            '.', '.', '.', '.',
            ',so you have.', ',so you have.', ',so you have.', 
            ' in the most exciting game ever invented.', 
            '. Do you think that %s guesses is too easy for up to %s?' % (maxGuesses, maxNum),
            '. Do you think that %s guesses is too hard for up to %s?' % (maxGuesses, maxNum),
            '. Should the maximum number be bigger like %s?' % (maxNum * 2),
            '. Are you remembering which numbers you entered already in your head? If it\'s too hard you can try writing them down!',
            ]
        statusMsg = 'You have %s guesses left%s %s' % (guessesLeft, random.choice(extraMsgs), emoj)

        #put_markdown('Take a guess.') # 4 spaces to indent
        try:
            guess = input("Take a guess.", type=NUMBER)
            guess = int(guess)
        except:    
            put_text('That\'s not a number %s! %s' % (myName, statusMsg))
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
        put_text('\U0001F64C').style('font-size: 144px')
        #put_text('Good job, %s! You guessed Daddy\'s age today! %s' % (myName, "\U0001F60A \U0001F64C"))
        #put_text('\U0001F388 \U00000035 \U00000030 \U0001F389').style('font-size: 144px')
    else:
        put_text('Hard luck! The number I was thinking of was %0.f. %s' % (number, "\U0001F62D"))

def times_tables():
    # times tables

    maxQuestions = 10
    maxSeconds = 30
    times = 8  # x time tables
    maxNum = 12  # max number the user is asked to multiply times with 

    #put_markdown('Hello! What is your name?')
    myName = "Adam" # input("Hello! What is your name?")
    put_markdown('You will have about %.0f minutes to get as many questions as possible correct, starting from time you answer the first one' % (maxSeconds / 60))

    #while True:
    #for questions in range(0, maxQuestions):
    correctAnswers = 0
    incorrectAnswers = 0
    start = 0
    firstIter = True
    while ( (timer() - start <= maxSeconds) or firstIter):
        number = random.randint(1, maxNum)
        answer = times * number

        #put_markdown('Take a guess.') # 4 spaces to indent
        try:
            userAnswer = input ('Ok %s, What is %.0f x %.0f' % (myName, times, number), type=NUMBER)
            userAnswer = int(userAnswer)
        except:    
            put_text('That\'s not a number %s!' % (myName))
            continue

        if userAnswer == answer:
            put_text('Correct')
            correctAnswers += 1
        else:
            put_text('Incorrect')
            incorrectAnswers += 1
        
        if firstIter:
            start = timer()
            firstIter = False
    end = timer()
    put_text('You got %.0f questions right and only %.0f wrong in %.0f seconds' % (correctAnswers, incorrectAnswers, (end - start))) # Time in seconds, e.g. 5.38091952400282


if __name__ == '__main__':
    import argparse
    from pywebio.platform.tornado_http import start_server as start_http_server
    from pywebio import start_server as start_ws_server

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    parser.add_argument("--http", action="store_true", default=False, help='Whether to enable http protocol for communicates')
    args = parser.parse_args()

    if args.http:
        start_http_server(times_tables, port=args.port)
    else:
        # Since some cloud server may close idle connections (such as heroku),
        # use `websocket_ping_interval` to  keep the connection alive
        start_ws_server(times_tables, port=args.port, websocket_ping_interval=30)

