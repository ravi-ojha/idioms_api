import json

from idioms.models import Idiom

# Open the data files
with open('71_to_80.json') as data_file:
    data = json.load(data_file)

# Populate db with the entries in data file
for k, v in data.iteritems():
    i = Idiom()
    i.title = v['title']
    i.meaning = v['meaning']
    i.set_examples(v['examples'])
    i.save()

