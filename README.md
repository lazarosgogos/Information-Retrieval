# IRProject

This project aims to extract useful information from speeches taken from the Greek Parliament in the period of 1989-2020.

# How to run

You'll need to create a conda environment and install the necessary requirements, included in this github repository.
To do so run the following command:  
`conda create --name <env> --file requirements.txt`

Then navigate to the project folder, for example `~/anacoda/IRProject/` and place all the files included in this github repo.

Make sure you have also downloaded the `db.sqlite3` database file and placed it into the PROJECT_DIR/WebApp directory, if you don't want to build the database from scratch (which would take hours).

## Building the database from scratch

Firstly, grab the files from the following links.
https://drive.google.com/file/d/1za9X4IN6Wmq9Y8JGGrOymGy0MCnWGT4D/view?usp=drive_link  
https://drive.google.com/file/d/1w0akuQEmv4B78nWVePTCZX8JH_O5PUXD/view?usp=drive_link  
https://drive.google.com/file/d/1hCXb_xMyYW79IGC5pGmNSZ6KivuDoYlg/view?usp=drive_link  
https://drive.google.com/file/d/1fHJaMZLjgpphr4-9qjqfYD3Zy0i1SJhT/view?usp=drive_link  
https://drive.google.com/file/d/1r7pto0PQI2LnQdQqXOn_LQGtIUk7VD46/view?usp=sharing  
SQLite database: https://drive.google.com/file/d/1kLTZKV3YJu2LKedzii3Qrmao4_oYIDCW/view?usp=sharing  

These files must be placed in the WebApp directory.
You will need to run the following python commands in order to create the objects for Django to run.  
`cd ./WebApp` if not already in the WebApp directory  
`python inverted_catalog.py`  
`python import_keywords_members.py`  
`python import_keywords_party.py`  
`python import_similarities.py`  
`python import_speeches.py`  
`python import_sim_speeches_mtree.py`  
(this following command may even be omitted, as the objects created by it are not used anymore) `python import_SVD.py`  

This might take several hours.


Then migrate data into the database using 
`python manage.py migrate`

## Running the server

Import all the files from this github repo and navigate into the WebApp directory. 
Then run:  
`python manage.py runserver`

## WebApp

The home page can be visited via a browser at [localhost](http://127.0.0.1:8000/)  

URLs:  
```
http://127.0.0.1:8000/quicksearch/  
http://127.0.0.1:8000/search/  
http://127.0.0.1:8000/similarities/  
http://127.0.0.1:8000/keywords_member/  
http://127.0.0.1:8000/keywords_party/  
http://127.0.0.1:8000/similar_speeches/  
http://127.0.0.1:8000/similar_speeches_minhash/  
http://127.0.0.1:8000/svd/  
http://127.0.0.1:8000/summarizer/  
```