import pickle


def get_speech_keys(filename='minhash.pkl'):
    """
    This function returns speech indices, which can then be taken
    and used to find which speeches are similar
    """
    with open(filename, 'rb') as pkl_file:
        minhash_dict = pickle.load(pkl_file) # a dictionary
        # key: the index of the speech
        # value: the speech IDs similar
    return list(minhash_dict.keys())

def get_similar_speeches(speechID, filename='minhash.pkl'):
    """
    This function returns speech indices, which can then be taken
    and used to find which speeches are similar
    """
    with open(filename, 'rb') as pkl_file:
        minhash_dict = pickle.load(pkl_file) # a dictionary
        # key: the index of the speech
        # value: the speech IDs similar to this speech
    
    if speechID not in minhash_dict.keys():
        return None

    similar_speeches = list(minhash_dict[speechID])
    # del minhash_dict
    return similar_speeches