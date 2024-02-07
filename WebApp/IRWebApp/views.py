from django.shortcuts import render
from IRWebApp.models import PartyKeywords, SimilarMembers, MemberKeywords, Speech, InvertedCatalog, SVD, SimilarSpeeches
import pandas as pd
from .forms import SearchForm
from .search import query_copy
from .similar_speeches import tree_search, tree_create

# Create your views here.

def home(request):
    return render(request, 'IRWebApp/home.html')

def keywords_party(request):
    data = PartyKeywords.objects.all()

    #data = data.filter(year = 2001)
    #print(type(data))
    #df_data = pd.DataFrame(data.values())
    # Retrieve data from the database
    # Perform data manipulation if needed
    return render(request, 'IRWebApp/keywords_per_party.html', {'data': data})

def keywords_member(request):
    data = MemberKeywords.objects.all()

    #data = data.filter(member_name = 'καστανιδης γεωργιου χαραλαμπος')

    return render(request, 'IRWebApp/keywords_per_member.html', {'data': data})


def similarities_members(request):
    data = SimilarMembers.objects.all()

    return render(request, 'IRWebApp/similarities.html', {'data': data})

def search_speeches(request):
    processed_speeches = Speech.objects.all().values_list('processed_speech', flat=True)
    processed_speeches = list(processed_speeches)
    
    indices = []
    if request.method == "POST":
        search_query = request.POST.get('query')
        indices = query_copy.search2(search_query, processed_speeches)
        indices = [i+1 for i in indices] # +1 because the indexes differ
    
    # Get the entries of the queryset with pk = the indices of the search sorted.
    results = Speech.objects.all().filter(pk__in = indices)
    results_list = list(results)
    ordered_results = sorted(results_list, key=lambda x: indices.index(x.pk))

    
    return render(request, 'IRWebApp/search.html', {'results': ordered_results})

def quick_search_speeches(request):
    ordered_results = []
    search_indices = []
    filtered_speeches = []
    if request.method == "POST":
        search_query = request.POST.get('query')
        search_query = query_copy.mod_query(search_query)
        # check the indexed catalog to get the indices of the relevant speeches
        search_query_list = search_query.split(' ')
        print(search_query)
        
        retrieved_list = []
        for words in search_query_list:
            

            wordlist = list(InvertedCatalog.objects.filter(word = words).values_list('speech_indices', flat=True))
            try:
                retrieved_list.extend(wordlist[0].replace('[', '').replace(']', '').split(', '))
            except:
                print('not in list')            
        
        indices = list(map(int,retrieved_list))
        indices = [i+1 for i in indices]
        
        filtered_speeches = Speech.objects.all().filter(pk__in = indices)
        list_filtered_processed_speeches = filtered_speeches.values_list('processed_speech', 'pk')
        list_processed_speeches = [t[0] for t in list_filtered_processed_speeches]        
       
        search_indices = query_copy.search2(search_query, list_processed_speeches)
        
        final_search_indices = [list_filtered_processed_speeches[i][1] for i in search_indices]
        
        results = filtered_speeches.filter(pk__in = final_search_indices)
        results_list = list(results)
        ordered_results = sorted(results_list, key=lambda x: final_search_indices.index(x.pk))
    
    return render(request, 'IRWebApp/quicksearch.html', {'results': ordered_results})


def svd(request):
    data = SVD.objects.all()

    return render(request, 'IRWebApp/svd.html', {'data': data})

def similar_speeches(request):
    # data = SimilarSpeeches.objects.all()
    # speeches = SimilarSpeeches.objects.all().values_list('speech', flat=True)
    # speeches = list(speeches)
    
    indices = []
    if request.method == "POST":
        if ('create_m_tree' in request.POST):
            print('Loading processed speeches only..')
            processed_speeches = Speech.objects.all().values_list('processed_speech', flat=True)
            processed_speeches = list(processed_speeches)
            print('Done loading processed speeches. Proceeding to create the M-Tree')
            tree_create.create_M_Tree(processed_speeches)
            
        else:
            requested_speech_id = int(request.POST.get('requested_speech_id')) 
            k = int(request.POST.get('k'))
            # search_query = request.POST.get('query')
            indices = tree_search.get_similar_speeches(requested_speech_id, k)
            indices.insert(0, requested_speech_id)
            indices = [i+1 for i in indices] # +1 because the indexes differ 
    # print(len(indices))
    # Get the entries of the queryset with pk = the indices of the search sorted.
    data = Speech.objects.all().filter(pk__in = indices)
    data_list = list(data)

    
    # return render(request, 'IRWebApp/search.html', {'results': ordered_results})
    return render(request, 'IRWebApp/similar_speeches.html', {'data': data_list})
