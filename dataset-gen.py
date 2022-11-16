import json

from faker import Faker
import random
fake = Faker()

f = open('params.json')
data = json.load(f)

x = {}

for i in range(0,150):
    o = {}
    for field in data['fields']:
        if(field['required'] or random.uniform(0,1) <= 0.7):
            if(field['type'] == 'string'):
                o[field['name']] = '#'+fake.bothify('?-####')
            elif(field['type'] == 'number'):
                o[field['name']] = random.randint(1,150)
    key = fake.hexify('^^^^^^^^^')
    x[key] = o;

fields = []
for field in data['fields']:
    fields.append(field['name'])
print(fields)

obj = {"fields" : fields}

with open('./backend/db/params.json', 'w', encoding='utf-8') as f:
    json.dump(obj, f, indent=4)

with open('./backend/db/db.json', 'w', encoding='utf-8') as f:
    json.dump(x, f, ensure_ascii=False, indent=4)

f.close()
