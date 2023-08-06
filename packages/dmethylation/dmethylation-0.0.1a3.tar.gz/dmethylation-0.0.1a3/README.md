
# dmethylation

Dgenome is a Django app which handle the genome coordinates 

Quick start
-----------

1. Add "dgenome" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'dgenome',
        'dmethylation',
    ]

2. Include the dgenome URLconf in your project urls.py like this::

    url(r'^dmethylation/', include((dmethylation.urls, 'dmethylation'), namespace='dmethylation')),

3. Run `python manage.py migrate` to create the dmethylation models.

4. Insert the Illiumina HumanMethylation450 CSV file and the script: bin/load_annotation_HumanMethylation450.py

5. See available API endpoints:

   /dmethylation/api/

