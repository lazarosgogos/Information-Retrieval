# import json
import os
import django
import pickle
import csv
from similarities import libsim, mtree

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IRProject.settings")
django.setup()



from IRWebApp.models import SimilarSpeeches

def hamming_distance(a: int, b:int):
    """
    This function returns the hamming distance between two integers.
    The hamming distance is defined as the total number of 1s, after
    the XOR operation between two binary numbers
    """
    return int.bit_count(a ^ b) # requires python 3.10
def import_pkl_data(csv_file_path):
    # with open('speeches_signatures.pkl', 'rb') as pkl_file:
    #     speeches_signatures = pickle.load(pkl_file) # a dictionary
    #     # key: the index of the speech
    #     # value: the signature of the speech
    # with open('speeches_inv_signatures.pkl', 'rb') as fo:
    #     speeches_inv_signatures = pickle.load(fo) # dictionary
    #     # key: the signature of some speech
    #     # value: a LIST of which speeches have this signature
    # with open('sim_tree.pkl', 'rb') as pkl_file:
    #     mtree = pickle.load(pkl_file) # the M-Tree
    #     # where the speeches are grouped together
    #     # and searches can take place
    #     # to find similar ones!
    # import time
    # for index, signature in speeches_signatures.items():
    #     if (index % 10000 == 0):
    #         print(index, time.localtime())
    #     res = list(mtree.search(signature, 3)) # for the given signature, find 3 similar speeches
        
    #     similar_signature_1 = res[0] # get the signature of a similar speech (this returns a list!)
    #     similar_signature_2 = res[1] # same 
    #     similar_signature_3 = res[2] # same

    #     # minor inconvenience: IF a signature is the same for two or more speeches
    #     # we ignore them and only deal with the first one
    #     # get the speech id 
    #     speech1 = speeches_inv_signatures[similar_signature_1][0] # no check needed, there's at least 1 similar speech in the m
    #     speech2 = speeches_inv_signatures[similar_signature_2][0] if len(speeches_inv_signatures[similar_signature_2]) > 0 else -1
    #     speech3 = speeches_inv_signatures[similar_signature_3][0] if len(speeches_inv_signatures[similar_signature_3]) > 0 else -1
        
    #     SimilarSpeeches.objects.create(
    #         speech_index =  index,
    #         speech_similar_1_index = speech1,
    #         speech_similar_2_index = speech2,
    #         speech_similar_3_index = speech3
    #     )

    from tqdm import tqdm
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for index, row in tqdm(enumerate(reader)):
            # if (index % 10000 == 0):
            #     print(index)
            SimilarSpeeches.objects.create(
                speech = row['speech'],
                speech_id = index
            )


# Execute the function
csv_file_path = '../processedspeechfinal.csv'
import_pkl_data(csv_file_path)