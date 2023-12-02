"""
This is a library of functions which are aimed to calculate 
the similarities between speeches
"""

# Find similarities based on either simhash
import hashlib
import numpy as np

# code = 'Hashed dcode'


def _hashString(code: str, bits = 64):
    """
    This function hashes a string and returns a hash value (integer).
    :param code: the string to be hashed
    :return i: the integer representation of its hash
    """
    code = code.encode('utf-8')
    i = int.from_bytes(hashlib.sha256(code).digest(), 'little') % 2**bits # we can handle 64 bits at most, at once
    i = np.uint64(i)
    # because we are in 64-bit architecture computers

    return i
    #digits = [int(d) for d in str(i)]
    #print('i:', i)
    #print('digits:',digits)

def _intToArrayOfDigits(i):
    """
    This function converts an integer to an array, which has all
    the digits of it 
    :param i: the integer to be converted
    :return digits: the array of the integer's digits
    """
    digits = [int(d) for d in (bin(i)[2:])]
    if (len(digits) < 64):
        for i in range(64 - len(digits)):
            digits.insert(1, 0)
    return digits

def _applyFeatureWeight(sig: list, l: list, w: int):
    # e for element
    # idx for index
    # l for list of sum of weights
    # sig for signature of 1s and 0s
    # w for weight (tfidf probably) of each word
    # The following procedure is described in the PDF 
    # IR-Advanced-Hashing by prof A.P.
    # print('length of l:', len(l))
    # print('length of sig:', len(sig))
    l = [e+w if sig[idx] == 1 else e-w for idx, e in enumerate(l)] 
    return l
"""
l = [0, 0, 0]
w = 2
sig = [1, 0, 1]

l = applyFeatureWeight(sig, l, w)
print(l)
"""
def _getFinalSignature(l: list):
    """
    This function returns an integer representation (for faster calculations) 
    of the signature for the given document
    :param l: a list of the final integers, after applying the weights
    :return bit_int: a bit sequence represented as an integer
    """
    r = [1 if e > 0 else 0 for e in  l]
    bit_int = 0
    # the following line was taken from
    # https://www.geeksforgeeks.org/python-binary-list-to-integer/
    for e in r:
        bit_int = (bit_int << 1) | e
    # bit_int = (bit_int << idx) | e for idx, e in enumerate(r)
    # print('bit_int',bit_int)
    return bit_int
"""
signature = getFinalSignature(l)

print('signature in int:',signature)
print('signature in bits:',bin(signature))
"""

def getSignatureOfSpeech(speech:str, weights: dict):
    """
    This function generates a signature for each speech, given the speech and
    the weight of each word in the form of a dictionary
    :param speech: the speech to consider
    :param weights: the weights of all words in this speech
    :return sig: the signature of this speech in integer form
    """
    words = speech.split(' ')
    l = np.zeros(64)
    
    for word in words:
        # hash the given word
        hashedWord = _hashString(word)
        # convert it to an array of digits
        digits = _intToArrayOfDigits(hashedWord)
        
        if (word not in weights.keys()): # if a word has no registered weight
            weight = 0 # consider it irrelevant? or consider it super important? in which case weight = 1 
        else :
            weight = weights[word]
        l = _applyFeatureWeight(digits, l, weight)
    sig = _getFinalSignature(l)
    return sig