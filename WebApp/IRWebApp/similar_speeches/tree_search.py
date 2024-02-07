import pickle 

def hamming_distance(a: int, b:int):
        """
        This function returns the hamming distance between two integers.
        The hamming distance is defined as the total number of 1s, after
        the XOR operation between two binary numbers
        """
        return int.bit_count(a ^ b) # requires python 3.10

def get_similar_speeches(speechID, k=4):
    with open('sim_tree_2.pkl','rb') as fo:
        tree = pickle.load(fo) # the M-Tree
            # where the speeches are grouped together
            # and searches can take place
            # to find similar ones!
    with open('speeches_inv_signatures_2.pkl', 'rb') as fo:
        speeches_inv_signatures = pickle.load(fo) # dictionary
        # key: the signature of some speech
        # value: a LIST of which speeches have this signature
    with open('speeches_signatures_2.pkl', 'rb') as pkl_file:
        speeches_signatures = pickle.load(pkl_file) # a dictionary
        # key: the index of the speech
        # value: the signature of the speech
    """
    This function returns k speech indices, which can then be taken
    and used to find which speeches are similar
    """
    signature = speeches_signatures[speechID]
    res = tree.search(signature, k)
    res = list(res) # convert map to list
    similar_speeches = []

    for i in range(k):
        similar_speech_index = speeches_inv_signatures[res[i]][0] if len(speeches_inv_signatures[res[i]]) > 0 else 0
        # print(similar_speech_index)
        similar_speeches.append(similar_speech_index) # this index could be a list actually
        # and we might need to iterate over it later on!

    del tree, speeches_inv_signatures, speeches_signatures
    return similar_speeches



# use this if memory reaches max
# import gc
# gc.collect()