import numpy as np
from itertools import combinations
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import gc

sentences = ["this is some speech related to animal rights", #0
            "yet some other speech about human rights", #1
            "blue shark in the ocean waters", #2
            'this is some other speech about human species', #3
            'waters found in the ocean are always blue', #4
            'some speech related to rights only', #5
            'another speech regarding human rights',] #6
class LSH:
    buckets = [] # will this variable become huge?
    bucket = defaultdict(set)
    candidate_pairs = list()
    def __init__(self, sentences, b=5, size_of_hash_functions=20):
        self.sentences = sentences
        self.b = b
        self.size_of_hash_functions = size_of_hash_functions
        for _ in range(b):
            self.buckets.append({}) # append an empty set in each bucket

    def build_shingles(self, sentence: str, k=8):
        """Take a sentence and tokenize/create shingles of size k out of it. """
        shingles = []
        tokens = sentence.split(' ')
        # for i in range(len(sentence) - k):
        #     shingles.append(sentence[i:i+k])
        return set(tokens)
        return set(shingles) # shingles on such a big file should be illegal

    def build_vocab(self, shingle_sets: list):
        """Take all the shingles available and create a vocabulary (a dictionary) out of them.
        Vocabulary is of the following like
        {'this': 0, 'is': 1, 'a': 2, 'library': 3, ... , 'waters': 53}"""
        # convert list of shingle sets into single set
        full_set = {item for shingle_set in shingle_sets for item in shingle_set}
        vocab = {}
        for i, shingle in enumerate(list(full_set)):
            vocab[shingle] = i
        return vocab

    def one_hot(self, shingles: set, vocab: dict):
        """Given a vocab and a shingle set, create an array of zeros,
        and put one whereever a shingle appears in the vocab.
        
        A vector of the sorts is returned:
        onehotvector = [1 1 0 0 1 0 ... 0 1] where each index is correlated to the position of the key (word)
        in the vocabulary."""
        vec = np.zeros(len(vocab), dtype=np.uint64)
        for shingle in shingles:
            idx = vocab[shingle]
            vec[idx] = 1
        return vec

    def _create_hash(self, vocab: dict):
        """Create a random permutation of the elements' indices, essentially.
        For a vocabulary of size 6, something like this would be created:
        [5 3 4 2 6 1]"""
        length = len(vocab.keys())
        # permutation = np.random.permutation(length)
        return np.random.permutation(length) + 1

    def build_hashes(self, vocab: dict, n_hash_functions:int):
        """
        NOTE: The following matrix should be Transposed! it works the same this way though
        Create a 2D array of hash values (random permutations of arrays) like so:
        Say we have a vocabulary of size 5 and we want 2 hash functions
        [[3 2]
         [1 3]
         [5 1]
         [2 4]
         [4 5]]"""
        length = len(vocab.keys())
        
        # create a 2D array where each row is a number coming from the random permutation
        # and each column is a different hash function
        hashes = np.empty((length ,n_hash_functions), dtype=np.uint64)
        for j in range(n_hash_functions):
            hashes[: , j] = self._create_hash(vocab) 
        # print(hashes)
        return hashes

    def get_signature(self, hashes, token_vector):
        """For the given token/shingle onehot vector, get only the positions that have a 1
        and find the minimum value in the hashed value, that simultaneously has a 1 in the token vector. 
        For example: for the given 
        hash values
        [[3 2]      and the following   [[1]
         [1 3]      token vector         [0]
         [5 1]                           [0]
         [2 4]                           [1]
         [4 5]]                          [0]]
        we would get
        [2 2]
        """
        non_zero_indices = np.nonzero(token_vector)[0].tolist()
        # based on these indices, which point only to 1s in the shingle/token vector
        # take the values from the hash value that also have 1s in the token vector
        relevant_shingles = hashes[non_zero_indices, : ]
        # now, the signature 
        signature = np.min(relevant_shingles, axis=0)
        return signature.tolist()
        return self.vec_to_int(signature)


    def jaccard(self, a: set, b: set):
        return len(a.intersection(b)) / len(a.union(b))

    def vec_to_int(self, vec):
        return sum(digit * 10 ** i for i, digit in enumerate(vec))

    def make_subvectors(self, signature):
        length = len(signature)
        # print('len:',length)
        # the signature must be divisible by the number of buckets we want to have
        assert length % self.b == 0
        r = int(length / self.b) # the number of rows is directly related to the number of buckets we have
        subvectors = []
        for i in range(0, length, r):
            # work directly with integers as they're more memory efficient
            # and we NEED MEMORY
            subvectors.append(vec_to_int(signature[i:i+r]))
        return np.stack(subvectors)

    def _make_subvector(self, signature, current_bucket: int):
        length = len(signature)
        # print('len:',length)
        # the signature must be divisible by the number of buckets we want to have
        assert length % self.b == 0
        r = int(length / self.b) 
        i = r*current_bucket # for slicing
        return self.vec_to_int(signature[i:i+r])

    def add_hash(self, signature, current_bucket: int, sentence_index: int):
        """For the given signature, split it into parts
        and take into account only the bucket we're currently working with!
        This should theorically save up some memory for us"""
        subsig = self._make_subvector(signature, current_bucket)
        self.bucket[subsig].add(sentence_index) # add this signature to the bucket
        # remember, we must clear the bucket once we're done with it before we move to the next one!
    
    def check_candidate_pairs(self):
        for key in self.bucket.keys():
            if len(self.bucket[key]) > 1:
                combs = self.bucket[key]
                self.candidate_pairs.extend(combinations(combs, 2))
    
    def perform_LSH(self):
        shingles_set = [self.build_shingles(sentence) for sentence in self.sentences]
        vocab = self.build_vocab(shingles_set)
        onehots = [self.one_hot(shingle, vocab) for shingle in shingles_set]
        
        hashes = self.build_hashes(vocab, self.size_of_hash_functions)

        signatures = [self.get_signature(hashes, onehots[i]) for i in range(len(onehots))]
        print(signatures)
        return
        del shingles_set, vocab, onehots, hashes
        gc.collect()
        for i in range(self.b):
            # for each bucket, run simsearch, find candidates and forget the bucket
            self.bucket = defaultdict(set)
            for sentence_index in range(len(self.sentences)):
                self.add_hash(signatures[sentence_index], i, sentence_index)
            # after we're done adding all the subsignatures into this bucket
            # let's check for candidate pairs
            self.check_candidate_pairs() # this automatically adds 
            # the candidate pairs to the set

            del self.bucket
            gc.collect()
            
        # print(set(self.candidate_pairs))

# lsh = LSH(sentences, b=2, size_of_hash_functions=6)
# lsh.perform_LSH()


def build_shingles(sentence: str, k=8):
    """Take a sentence and tokenize/create shingles of size k out of it. """
    shingles = []
    tokens = sentence.split(' ')
    # for i in range(len(sentence) - k):
    #     shingles.append(sentence[i:i+k])
    return set(tokens)
    return set(shingles) # k-shingles on such a big file should be illegal

def build_vocab(shingle_sets: list):
    """Take all the shingles available and create a vocabulary (a dictionary) out of them.
    Vocabulary is of the following like
    {'this': 0, 'is': 1, 'a': 2, 'library': 3, ... , 'waters': 53}"""
    # convert list of shingle sets into single set
    full_set = {item for shingle_set in shingle_sets for item in shingle_set}
    vocab = {}
    for i, shingle in enumerate(list(full_set)):
        vocab[shingle] = i
    return vocab

def one_hot(shingles: set, vocab: dict):
    """Given a vocab and a shingle set, create an array of zeros,
    and put one whereever a shingle appears in the vocab.
    
    A vector of the sorts is returned:
    onehotvector = [1 1 0 0 1 0 ... 0 1] where each index is correlated to the position of the key (word)
    in the vocabulary."""
    vec = np.zeros(len(vocab))
    for shingle in shingles:
        idx = vocab[shingle]
        vec[idx] = 1
    return vec

def _create_hash(vocab: dict):
    """Create a random permutation of the elements' indices, essentially.
    For a vocabulary of size 6, something like this would be created:
    [5 3 4 2 6 1]"""
    length = len(vocab.keys())
    # permutation = np.random.permutation(length)
    return np.random.permutation(length) + 1

def build_hashes(vocab: dict, n_hash_functions:int):
    """Create a 2D array of hash values (random permutations of arrays) like so:
    Say we have a vocabulary of size 5 and we want 2 hash functions
    [[3 2]
     [1 3]
     [5 1]
     [2 4]
     [4 5]]"""
    length = len(vocab.keys())
    
    # create a 2D array where each row is a number coming from the random permutation
    # and each column is a different hash function
    hashes = np.empty((length ,n_hash_functions), dtype=np.uint64)
    for j in range(n_hash_functions):
        hashes[: , j] = _create_hash(vocab) 
    # print(hashes)
    return hashes

def get_signature(hashes, token_vector):
    """For the given token/shingle, get only the positions that have a 1
    and find the minimum value in the hashed value, that simultaneously has a 1 in the token vector. 
    For example: for the given hash values
    [[3 2]      and the following   [[1]
     [1 3]      token vector         [0]
     [5 1]                           [0]
     [2 4]                           [1]
     [4 5]]                          [0]]
    we would get
    [2 2]
    """
    non_zero_indices = np.nonzero(token_vector)[0].tolist()
    # based on these indices, which point only to 1s in the shingle/token vector
    # take the values from the hash value that also have 1s in the token vector
    relevant_shingles = hashes[:, non_zero_indices]
    # now, the signature 
    signature = np.min(relevant_shingles, axis=1)
    return signature


def jaccard(a: set, b: set):
    return len(a.intersection(b)) / len(a.union(b))


def create_buckets(b: int):
    buckets = []
    for _ in range(b):
        buckets.append({}) # append an empty set in each bucket
    return buckets

def vec_to_int(vec):
    return sum(digit * 10 ** i for i, digit in enumerate(vec))

def make_subvectors(signature, b: int):
    """b is the amount of buckets"""
    length = len(signature)
    # print('len:',length)
    # the signature must be divisible by the number of buckets we want to have
    assert length % b == 0
    r = int(length / b) # the number of rows is directly related to the number of buckets we have
    subvectors = []
    for i in range(0, length, r):
        # work directly with integers as they're more memory efficient
        # and we NEED MEMORY
        subvectors.append(vec_to_int(signature[i:i+r]))
    return np.stack(subvectors)

def add_hash(signature: int, buckets: list):

    return buckets
jiuice = """
shingles_set = [build_shingles(sentence) for sentence in sentences]
vocab = build_vocab(shingles_set)
onehots = [one_hot(shingle, vocab) for shingle in shingles_set]
n_hash_functions = 20
hashes = build_hashes(vocab, n_hash_functions)
non_zero_indices = [np.nonzero(onehots[i])[0].tolist() for i in range(len(onehots))]
relevant_shingles = [hashes[non_zero_indices[i], :] for i in range(len(non_zero_indices))]
signatures = [np.min(relevant_shingles[i], axis=0) for i in range(len(relevant_shingles))]
b = 5
buckets = create_buckets(b)
subvecs = [make_subvectors(signatures[i], b) for i in range(len(signatures))]
# subvecs is based on the following logic:
# each speech has been converted into a signature, right?
# well then, each signature is broken into b bands/buckets
# and each band has r rows. the total length of each signature is
# the same as the number of hash functions we have asked for
# the length must be perfectly divisible by the number of bands/buckets we have
for i, subvec in enumerate(subvecs):
    print(subvec)
    # for vec in subvec:
    #     # vec_to_int = 0
    #     # for digit in vector:
    #     #     vec_to_int = vec_to_int * 10 + digit
    #     vec_to_int = sum(digit * 10 ** i for i, digit in enumerate(vec)) # this is basically 
    #     # the same code as above, but more concise and efficient

    #     print(vec_to_int)

# permutation = np.random.permutation(10) +1
# # arr = list(range(10))
# print(permutation)
"""