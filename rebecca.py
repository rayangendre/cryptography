import sys
import os
import random

from collections import defaultdict, Counter

def main():
    message = input("Enter plaintext or ciphertext: ")
    process = input("Enter 'encrypt' or 'decrypt': ")

    while process not in ('encrypt', 'decrypt'):
        process = input("Invalid process")

    shift = int(input("Shift value (1-366) =  "))
    while not 1 <= shift <= 366:
        shift = int(input("Invalid Enter Shift value (1-366) =  "))
    
    infile = input("Enter a filename with the extension: ")

    if not os.path.exists(infile):
        print("File {} not found. Ending program".format(infile), file=sys.stderr)
        sys.exit(1)
    text = load_file(infile)
    char_dict = make_dict(text, shift)

    if process == 'encrypt':
        ciphertext = encrypt(message, char_dict)
        if check_for_fail(ciphertext):
            print("Problem finding unique keys, try again", file=sys.stderr)
            sys.exit()
        # print("\nCharacter and number of occurences in char_dict")
        # print("{: >10}{: >10}{: >10}".format('Character', 'Unicode', 'Count'))
        # for key in sorted(char_dict.keys()):
        #     print('{:>10}{:>10}{:>10}'.format(repr(key)[1:-1], str(ord(key)), len(char_dict[key])))
        # print('\nNumber of distinct characters: {}'.format(len(char_dict)))
        # print('\nTotal number of characters: {:,}'.format(len(text)))

        print("Encrypted cipher text = \n {}\n".format(ciphertext))
        print("Decrypted plaintext = ")

        for i in ciphertext:
            print(text[i - shift], end='', flush=True)
        
        print()
        
    elif process == 'decrypt':
        plaintext = decrypt(message, text, shift)
        print("\ndecrypted plaintext = {}\n".format(plaintext))


def load_file(infile):
    with open(infile) as f:
        loaded_string = f.read().lower()
    return loaded_string

def make_dict(text, shift):
    char_dict = defaultdict(list)
    for index, char in enumerate(text):
        char_dict[char].append(index + shift)
    return char_dict

def encrypt(message, char_dict):
    encrypted = []
    for char in message.lower():
        if len(char_dict[char]) > 1:
            index = random.choice(char_dict[char])
        elif len(char_dict[char]) == 1:
            index = char_dict[char][0]
        elif len(char_dict[char]) == 0:
            print("\nCharacter {} not in dictionary.".format(char), file=sys.stderr)
            continue
        encrypted.append(index)
    return encrypted

def decrypt(message, text, shift):
    plaintext = ''
    indexes = [s.replace(',', '').replace('[', '').replace(']', '') for s in message.split()]
    for i in indexes:
        plaintext += text[int(i) - shift]
    return plaintext

def check_for_fail(ciphertext):
    check = [k for k, v in Counter(ciphertext).items() if v > 1]
    if len(check) > 0:
        return True
    
if __name__ == '__main__':
    main()