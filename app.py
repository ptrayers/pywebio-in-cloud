from pywebio.input import *
from pywebio.output import *
import random

def main():
    
    # Guess the number game

    guessesTaken = 0

    put_markdown('Hello! What is your name?')
    myName = input()

    number = random.randint(1, 20)
    put_markdown('Ok `%s`, I\'m thinking of number between 1 and `%.1f`', % (myName, number))

    for guessesTaken in range(6):
        #put_markdown('Take a guess.') # 4 spaces to indent
        guess = input("Take a guess.", type=FLOAT)
        #guess = int(guess)
        if guess < number:
            put_markdown('Your guess is too low.') # Eight spaces indent
        if guess > number:
            put_markdown('Your guess is too high.')

        if guess == number:
            break

    if guess == number:
        guessesTaken = str(guessesTaken + 1)
        put_markdown('Good job, `%s`! You guessed number in `%.1f` guesses!' % (myName, guessesTaken))

    if guess != number:
        number = str(number)
        print('Bad luck! The number I was thinking of was `%.1f`.' % (number))
    

if __name__ == '__main__':
    import argparse
    from pywebio.platform.tornado_http import start_server as start_http_server
    from pywebio import start_server as start_ws_server

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    parser.add_argument("--http", action="store_true", default=False, help='Whether to enable http protocol for communicates')
    args = parser.parse_args()

    if args.http:
        start_http_server(main, port=args.port)
    else:
        # Since some cloud server may close idle connections (such as heroku),
        # use `websocket_ping_interval` to  keep the connection alive
        start_ws_server(main, port=args.port, websocket_ping_interval=30)

