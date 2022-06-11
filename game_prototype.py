import random, pygame, os, sys
from pygame.locals import *
pygame.init()

# Colors
white = (255, 255, 255)
yellow = (255, 255, 102)
grey = (211, 211, 211)
green = (0, 255, 0)
lightGreen = (153, 255, 204)
black = (0, 0, 0)

# Words
font = pygame.font.SysFont("Helvetica neue", 40)
bigFont = pygame.font.SysFont("Helvetica neue", 80)

youWin      = bigFont.render("You Win!",        True, lightGreen)
youLose     = bigFont.render("You Lose!",       True, lightGreen)
playAgain   = bigFont.render("Play Again?",     True, lightGreen)


#_______________________________________________________________
#=============================FUNCTION==========================
#_______________________________________________________________

""" Draw Guess Function
    Given the list of colors, draw the squares
"""
def drawGuess(turns, userGuess, guessColorCode, window):
    renderList = ["", "", "", "", ""]

    list(userGuess)

    for x in range(5):
        renderList[x] = font.render(userGuess[x], True, black)
        pygame.draw.rect(window, guessColorCode[x], pygame.Rect(60 + x * 80, 50 + (turns*80), 50, 50))
        window.blit(renderList[x], (60 + x * 80, 50 + (turns*80)))
        
""" Naive Guess Checking Function
    Given turns, word, user guess, and windows, check the guess 
    in two passes, this is the simple and foolproof way to that
    ensures all the green and yellow squares are correct.
"""
def checkGuessNaive(turns, word, userGuess, window):
    guessColorCode = [grey, grey, grey, grey, grey]

    indices = list(range(5))

    wordList = list(word)

    # First Pass, only take in perfect matches 
    for i in range(5):
        if wordList[i] == userGuess[i]:
            # Make guessColorCode Green
            guessColorCode[i] = green
            # Remove letter in word
            wordList[i] = ' '
            # Remove index
            indices.remove(i)

    # Second Pass, Check for any letters in the word 
    for i in indices:
        if userGuess[i] in wordList:
            # Make guessColorCode Yellow
            guessColorCode[i] = yellow
            # Remove letter in word
            wordList[i] = ' '

    drawGuess(turns, userGuess, guessColorCode, window)

    return guessColorCode == [green, green, green, green, green]        

def checkGuess(turns, word, userGuess, window):
    renderList = ["", "", "", "", ""]
    spacing = 0
    guessColorCode = [grey, grey, grey, grey, grey]

    # TODO: There are still a few kinks, 
    #        ALARM: 1 A will light up yellow for both 
    #        Guess AAAAA: All yellow


    # Initialize Dictionary
    leDict = {}

    for c in userGuess:
        leDict[c] = 0
    for c in word:
        leDict[c] = 0

    # Ref Count the guess
    for c in userGuess:
        leDict[c] += 1

    print(leDict)

    # Start guessing
    for i in range(5):
        print(word[i])
        if leDict[word[i]] > 0:
            print("YELLOW")
            guessColorCode[i] = yellow
            leDict[word[i]] -= 1

            if word[i] == userGuess[i]:
                print("GREEN")
                guessColorCode[i] = green
            print(leDict)


    list(userGuess)

    for x in range(5):
        renderList[x] = font.render(userGuess[x], True, black)
        pygame.draw.rect(window, guessColorCode[x], pygame.Rect(60 + spacing, 50 + (turns*80), 50, 50))
        window.blit(renderList[x], (60 + spacing, 50 + (turns*80)))
        spacing += 80

    if guessColorCode == [green, green, green, green, green]:
        return True

    return False






#_______________________________________________________________
#=============================MAIN==============================
#_______________________________________________________________
def main():
    file = open("words\\wordle-answers-alphabetical.txt", "r")
    wordList = file.readlines()
    # word = wordList[random.randint(0, len(wordList) - 1)].upper()
    word = "ALARM"

    height = 600
    width = 500

    FPS = 30
    clock = pygame.time.Clock()
    
    window = pygame.display.set_mode((width, height))
    window.fill(black)

    guess = ""

    print(word)

    for x in range(5):
        for y in range(5):
            pygame.draw.rect(window, grey, pygame.Rect(60+(x*80), 50 +(y*80), 50, 50), 2)

    pygame.display.set_caption("Wordle!")

    turns = 0
    win = False


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.exit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                guess += event.unicode.upper()

                if event.key == pygame.K_RETURN and win == True:
                    main()

                if event.key == pygame.K_BACKSPACE:
                    guess = guess[:-2]

                if len(guess) > 5:
                    guess = guess[:-1]


                if event.key == pygame.K_RETURN and len(guess) > 4:
                    win = checkGuessNaive(turns, word, guess, window)
                    turns += 1
                    guess = ""
                    window.fill(black, (0, 500, 500, 200))
        
        window.fill(black, (0, 500, 500, 200))
        renderGuess = font.render(guess, True, grey)
        window.blit(renderGuess, (180, 530))

        if win == True:
            window.blit(youWin, (90, 200))
            window.blit(playAgain, (60, 300))
            
        if turns == 6 and win != True:
            window.blit(youLose, (90, 200))
            window.blit(playAgain, (60, 300))
        pygame.display.update()
        clock.tick(FPS)

main()


