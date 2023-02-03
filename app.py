import sqlite3
import random
from os import system, name
from hangman_stages import *

letters_unused = list()
letters_used = list()
act_stage = 0

def clear():
    if name == "nt":
        _ = system("cls")

    else:
        _ = system("clear")

def init_letters_unused():
    del letters_unused[0:len(letters_unused)]
    for i in range(97, 123):
        letters_unused.append(chr(i))

def init_letters_used():
    del letters_used[0:len(letters_used)]

def format_rnd_word(w):
    _word_in_underscores = list()

    for letter in w:
        _word_in_underscores.append("_ ")

    return _word_in_underscores


def fetch_words_from_db() -> list:
    _words_from_sql = list()

    with sqlite3.connect("words_db.db") as con:
        cur = con.cursor()
        res = cur.execute("select * from words")
        _words_from_sql = res

    if _words_from_sql:
        return list(_words_from_sql)

while 1:
    act_stage = 0
    init_letters_unused()
    init_letters_used()
    words_from_db = fetch_words_from_db()
    rnd_index = random.randint(0, len(words_from_db) - 1)
    
    act_word = words_from_db[rnd_index][0]

    list_word_underscores = format_rnd_word(act_word)

    while 1:
        clear()
        render_stage(eval(f"stage{act_stage}"))
        print("")
        print(*list_word_underscores)
        print("")
        print("Unused letters: " + ", ".join(letters_unused))
        print("Letters that were already used: " + ", ".join(letters_used))
        print("")

        check_word = [letter for letter in [l for l in act_word] + list_word_underscores if letter not in list_word_underscores]

        if not check_word:
            print("Congrats! You win!")
            break

        if act_stage == 9:
            print("OH NO! You lost!")
            break

        usr_input = input("Which letter do you choose?").lower()

        if usr_input in letters_unused:
            if usr_input in act_word:
                for i, letter in enumerate(act_word):
                    if letter == usr_input:
                        list_word_underscores[i] = letter 
                letters_used.append(usr_input)
                letters_unused.remove(usr_input)
                input("Correct!")
                continue

            if usr_input not in act_word:
                act_stage += 1
                letters_used.append(usr_input)
                letters_unused.remove(usr_input)
                input("Wrong!")
            continue
                
        if usr_input in letters_used:
            input("OH NO! It seems like you already used this letter! Please choose a different one, will ya.")
            continue
        
        if usr_input not in letters_unused and usr_input not in [chr(i) for i in range(97, 123)]:
            input("Hmmm... the character you gave me isn't in the list of available letters. Try again.")
            continue

        break
    
    try_again = input("Do you want to try again? [Y/n]").lower()

    if try_again == "y":
        continue
    else:
        clear()
        break