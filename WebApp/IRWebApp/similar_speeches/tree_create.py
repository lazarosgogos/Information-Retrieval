from similarities import libsim, mtree
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
import pickle

def hamming_distance(a: int, b:int):
    """
    This function returns the hamming distance between two integers.
    The hamming distance is defined as the total number of 1s, after
    the XOR operation between two binary numbers
    """
    return int.bit_count(a ^ b) # requires python 3.10

def create_M_Tree(speeches):
    print('tfidf vectorizing')
    # print(speeches[0])
    # return
    vectorizer = TfidfVectorizer(encoding='utf-8', lowercase=False, )
    X = vectorizer.fit_transform(speeches) # Are speeches in the correct format??

    print('Creating weights for each word')
    names = vectorizer.get_feature_names_out()
    max_idf = len(names) - 1
    weights = {name: (idx/max_idf) for idx, name in enumerate(names)} # normalized weights

    print('Creating signatures for each speech')
    # The following list is an array of signatures in integer form 
    # signatures = [libsim.getSignatureOfSpeech(speech, weights) for speech in speeches]
    signatures = {idx: libsim.getSignatureOfSpeech(speech, weights) for idx, speech in enumerate(speeches)}
    # this took 14 minutes to complete
    
    print('Creating inverse signature list')
    # where did each signature come from? correlate 
    inv_signatures = defaultdict(list)
    for k, v in signatures.items():
        inv_signatures[v].append(k) # handle duplicate signatures by creating a list
    
    print('Creating M-Tree')
    # create M-Tree data structure
    tree = mtree.MTree(hamming_distance, max_node_size=10)
    tree.add_all(signatures.values())
    # should take 20 seconds to build the tree
    print('Saving.')
    # save() # save data

# def save():
    with open('sim_tree_2.pkl', 'wb') as fo:
        tree = pickle.dump(tree, fo)
        # LOAD SIGNATURES DICTIONARY

    with open('speeches_inv_signatures_2.pkl', 'wb') as fo:
        inv_signatures = pickle.dump(inv_signatures, fo) 
        # this is a dictionary of {indexOfSpeech: signatureOfSpeech}
    
    # LOAD SIGNATURES DICTIONARY
    with open('speeches_signatures_2.pkl', 'wb') as fo:
        signatures = pickle.dump(signatures, fo) 
        # this is a dictionary of {indexOfSpeech: signatureOfSpeech}
        
    print('Done creating the M-Tree')