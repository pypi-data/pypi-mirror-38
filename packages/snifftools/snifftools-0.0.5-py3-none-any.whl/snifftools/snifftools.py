#snifftools

def emailcheck(email : str):
    if email.find("@") == -1:
        return(False)
    else:
        return(True)

def reverse(text):
    return(text[::-1])

def join(text1, text2):
    return(text1 + text2)

def encrypt(message):
    message = message[::-1]
    alphabet = "abcdefghijklmnopqrstuvwxyz.!? /:"
    replacea = "zyxwvutsrqponmlkjihgfedcba!./ ?:"
    secret = ""
    message = message.lower()
    for character in message:		
        i = alphabet.index(character)
        secret = secret + replacea[i]
    return(secret)
