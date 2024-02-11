import numpy as np
import scipy as sp
from random import shuffle
speeches = ["this is some speech related to animal rights", 
            "yet some other speech about human rights", 
            "blue shark in the ocean waters",]

# print(speeches[0])

def shingle(text: str, ):
    """
    This function takes a string of text, tokenizes it
    and returns a set of shingles/k-grams
    text: the text we want to extract shingles from
    return: a set of shingles/k-grams
    """
    if (type(text) is list):
        return set(text)
    tokens = text.split(' ') # tokenize text
    return set(tokens)

# print(shingle(speeches[0]))

# somehow we need to do one-hot-encoding now
# first let's do it the simple way

def build_vocabulary(*shingles):
    """
    Build a vocabulary (a set) based on all available tokens/words
    shingles: an iterable with tokens as elements
    return: a vocabulary (a set) of all possible tokens 
    """
    vocab = set()
    for shingle_set in shingles:
        vocab = vocab.union(shingle_set)
    return vocab

a = shingle(speeches[0])
b = shingle(speeches[1])
c = shingle(speeches[2])

voc = build_vocabulary(a,b,c)

print(voc)
# now, one-hot-encoding time
# simple first

def one_hot_encode(shingle_set: set, vocab: list):
    """
    For the given shingle set and the global vocabulary, 
    return a SPARSE?? vector with ones whereever 
    an element appears on the vocabulary.
    TODO doesn't this require an ordered vocabulary?
        might be possible if done with a dictionary
        of the sort {key: [list as value]}
        (where key is the)
        or each value of a returned iterable (possibly set) 
        can be a position of a one
        no, each key will be a position/token in the vocabulary
        and each value 
    """
    
    if type(vocab) is not list:
        raise TypeError('vocab must first be turned into a list!')
    
    # this can also be achieved with numpy/scipy arrays !!!
    onehot = [1 if word in shingle_set else 0 for word in vocab]
    return onehot

voc = list(voc) # very importan line!!
a_onehot = one_hot_encode(a, voc)
b_onehot = one_hot_encode(b, voc)
c_onehot = one_hot_encode(c, voc)
print(a_onehot)

def prime_generator(n=300):
    """
    n is the number of prime numbers we want to generate,
    and by extension the number of permutations we're going to perform,
    or in other words the size of our minhash value in bits (?)
    """
    primes = []
    num = 2
    while len(primes) < n:
        is_prime = True
        for prime in primes:
            if num % prime == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
            yield num
        num += 1

# Generate the first 300 prime numbers
# prime_list = list(prime_generator())
n=200

# now it's time to MINHASH
def create_hash_function(vocab: list):
    """Function that creates the hash vector/function"""
    hash_ex = list(range(1, len(vocab) + 1))
    shuffle(hash_ex)
    return hash_ex
    # return ((a * index + b) * prime) % size

def build_hashes_function(vocab, nbits=200):
    """Function for building multiple minhash vectors"""
    hashes = []
    for _ in range(nbits):
        hashes.append(create_hash_function(vocab))
    return hashes

_hashes = build_hashes_function(voc, 20)
print(_hashes[0])

def create_hash(onehot_vector: list, hashes: list, vocab: list):
    """This functions creates our signature"""
    signature = []
    for func in hashes:
        for i in range(1, len(vocab)+ 1):
            idx = func.index(i)
            signature_val = onehot_vector[idx]
            if signature_val == 1:
                signature.append(idx)
                break
    return signature

a_hashed = create_hash(a_onehot, _hashes, voc)
b_hashed = create_hash(b_onehot, _hashes, voc)
c_hashed = create_hash(c_onehot, _hashes, voc)

print(a_hashed)

def jaccard(x: set,y: set):
    return len(x.intersection(y)) / len(x.union(y))

print('Jaccard a,b:', jaccard(set(a), set(b)), jaccard(set(a_hashed), set(b_hashed)))
print('Jaccard c,b:', jaccard(set(c), set(b)), jaccard(set(c_hashed), set(b_hashed)))

def split_vector(signature, b:int):
    assert len(signature) % b == 0
    r = int(len(signature) / b)
    # code splitting signature in b parts
    subvecs = []
    for i in range(0, len(signature), r):
        subvecs.append(signature[i : i+r])
    return subvecs

band_a = split_vector(a_hashed, 10)
band_b = split_vector(b_hashed, 10)
band_c = split_vector(c_hashed, 10)
print('band b:',band_b)

# now let's roll 
# https://www.pinecone.io/learn/series/faiss/locality-sensitive-hashing/