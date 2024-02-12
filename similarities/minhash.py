# code found originally from 
# https://www.pinecone.io/learn/series/faiss/locality-sensitive-hashing/
# https://github.com/pinecone-io/examples/tree/master/learn/search/faiss-ebook/locality-sensitive-hashing-traditional
import numpy as np
from itertools import combinations
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

sentences = ["this is some speech related to animal rights", 
            "yet some other speech about human rights", 
            "blue shark in the ocean waters",]

def build_shingles(sentence: str, k: int):
    """Take a sentence and create shingles of size k out of it."""
    shingles = []
    tokens = sentence.split(' ')
    # for i in range(len(sentence) - k):
    #     shingles.append(sentence[i:i+k])
    return set(tokens)
    return set(shingles) # shingles on such a big file should be illegal

def build_vocab(shingle_sets: list):
    """Take all the shingles available and create a vocabulary (a dictionary) out of them"""
    # convert list of shingle sets into single set
    full_set = {item for set_ in shingle_sets for item in set_}
    vocab = {}
    for i, shingle in enumerate(list(full_set)):
        vocab[shingle] = i
    return vocab

def one_hot(shingles: set, vocab: dict):
    """Given a vocab and a shingle set, create an array of zeros,
    and put one whereever a shingle appears in the vocab."""
    vec = np.zeros(len(vocab))
    for shingle in shingles:
        idx = vocab[shingle]
        vec[idx] = 1
    return vec

def minhash_arr(vocab: dict, resolution: int):
    """Perform permutations in order to create a minhash.
    Return an integer value representing the hash."""
    length = len(vocab.keys())
    arr = np.zeros((resolution, length))
    for i in range(resolution):
        permutation = np.random.permutation(len(vocab)) + 1
        arr[i, :] = permutation.copy()
    return arr.astype(int)

def get_signature(minhash, vector):
    """Create the signature based on the minhash value.
    This is done by finding out the minimum value in each hash vector
    where the value is 1 at the same time."""
    # get index locations of every 1 value in vector
    idx = np.nonzero(vector)[0].tolist()
    # use index locations to pull only +ve positions in minhash
    shingles = minhash[:, idx]
    # find minimum value in each hash vector
    signature = np.min(shingles, axis=1)
    return signature



def jaccard(a: set, b: set):
    return len(a.intersection(b)) / len(a.union(b))

class LSH:
    buckets = []
    counter = 0
    def __init__(self, b):
        self.b = b
        for i in range(b):
            self.buckets.append({})

    def make_subvecs(self, signature):
        l = len(signature)
        assert l % self.b == 0
        r = int(l / self.b)
        # break signature into subvectors
        subvecs = []
        for i in range(0, l, r):
            subvecs.append(signature[i:i+r])
        return np.stack(subvecs)

    def add_hash(self, signature):
        subvecs = self.make_subvecs(signature).astype(str)
        for i, subvec in enumerate(subvecs):
            subvec = ','.join(subvec)
            if subvec not in self.buckets[i].keys():
                self.buckets[i][subvec] = []
            self.buckets[i][subvec].append(self.counter)
        self.counter += 1

    def check_candidates(self):
        candidates = []
        for bucket_band in self.buckets:
            keys = bucket_band.keys()
            for bucket in keys:
                hits = bucket_band[bucket]
                if len(hits) > 1:
                    candidates.extend(combinations(hits, 2))
        return set(candidates)

class MyVector:
    vec = set()
    def __init__(self, *numbers):
        self.vec = set(numbers)

def cluster_speeches(sentences, k=8, b=20, debug=False):
    """k is the shingle size"""
    # k = 8  # shingle size

    # build shingles
    shingles = []
    for sentence in sentences:
        shingles.append(build_shingles(sentence, k))

    # build vocab
    vocab = build_vocab(shingles)

    # one-hot encode our shingles
    shingles_1hot = []
    for shingle_set in shingles:
        shingles_1hot.append(one_hot(shingle_set, vocab))
    # stack into single numpy array
    shingles_1hot = np.stack(shingles_1hot)
    if debug:
        print('shingles_1hot shape:',shingles_1hot.shape)


    arr = minhash_arr(vocab, 100)

    signatures = []

    # create signatures
    for vector in shingles_1hot:
        signatures.append(get_signature(arr, vector))

    # merge signatures into single array
    signatures = np.stack(signatures)
    if debug:
        print('signatures shape:',signatures.shape)


    lsh = LSH(b)

    # create signatures and add them to LSH
    for signature in signatures:
        lsh.add_hash(signature)
    
    # if debug:
    #     print('lsh.buckets:',lsh.buckets)
    
    candidate_pairs = lsh.check_candidates()

    if debug:
        print('length of candidate_pairs', len(candidate_pairs))
        print('Peek at first 5 candidate pairs', list(candidate_pairs)[:5])

    pairs = pd.DataFrame({
        'x': [],
        'y': [],
        'jaccard': [],
        'cosine': [],
        'candidate': []
    })

    data_len = shingles_1hot.shape[0]
    chosen = set()
    # take random sample of pairs
    sample_size = 10
    for _ in range(sample_size):
        x, y = np.random.choice(data_len, 2)
        if x == y or (x, y) in chosen: continue
        chosen.add((x, y))
        vector_x = signatures[x]
        vector_y = signatures[y]
        candidate = 1 if (x, y) in candidate_pairs else 0
        cosine = cosine_similarity([vector_x], [vector_y])[0][0]
        pairs = pd.concat([pairs, pd.DataFrame([{
                'x': x,
                'y': y,
                'jaccard': jaccard(set(vector_x), set(vector_y)),
                'cosine': cosine,
                'candidate': candidate
            }])], ignore_index=True)
        # pairs = pairs.append({
        #         'x': x,
        #         'y': y,
        #         'jaccard': jaccard(set(vector_x), set(vector_y)),
        #         'cosine': cosine,
        #         'candidate': candidate
        #     }, ignore_index=True)

    # add a normalized cosine column for better alignment
    cos_min = pairs['cosine'].min()
    cos_max = pairs['cosine'].max()
    pairs['cosine_norm'] = (pairs['cosine'] - cos_min) / (cos_max - cos_min)
    if debug:
        # print(pairs.head())
        print(pairs[pairs['candidate'] != 0])
