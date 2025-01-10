#!bin/python3

import os
import json
from decimal import Decimal

print()

f = open("export_pretty.json", "r")
data = json.load(f)
f.close()

export_json = data['hits']['hits']

#for media in export_json:
    #if 'blog_name' not in media['_source']:
    #    print("blog_name missing for " + media['_source']['path'])

print("String to json")
tags_str = "italy,face,echinacea,bee,tuscany,2010,276"
tag_list = list(tags_str.split(","))
tags = json.dumps(tag_list)
print(tags)

print()


print("JSON list to {}")
#tags_list = ["apple","orange","banana"]
#tags = list(tags_list.split(','))


tags_list = ["apple","orange","banana"]
#tags = "{"+','.join(tags_list)+"}"
#tags = "{"+str(tags_list)+"}"
tags = json.dumps(tags_list)

print(tags)


print(Decimal("38.743741"))
print(Decimal("-109.499178"))


print();quit()