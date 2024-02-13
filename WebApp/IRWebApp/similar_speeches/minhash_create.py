from similarities import minhash

b = 12
k = 6 # shingle size
k = None # use tokens instead of k-shingles
n_of_hash_functions = 204

# if we have 204 permutations and 12 buckets, the rows are 17 
# and the threshold for similar documents is about 85%. good enough
def create_minhash(speeches, b, n_of_hash_functions, k=None):
    lsh = minhash.LSH(speeches, b, n_of_hash_functions, k)
    lsh.create_minhash()