import json
from faker import Faker
import random

NUMBER_OF_DATA = 30  # Number of data elements to be generated.
REQUIRED_BIAS = .7  # Posibility of not required fields to be filled.

fake = Faker()

model_file = open('../backend/db/fields.json')
data_model = json.load(model_file)

print("Template succesfully loaded. Generating",NUMBER_OF_DATA,"sample(s).")

output = []


def populateObject(model):
    object = {}
    for field in model:
        print(field)
        if (not field['required'] and random.uniform(0, 1) >= REQUIRED_BIAS):
            object[field['name']] = {}
        else: 
            object[field['name']] = populateField(field)
    return object


def populateField(field):
    if (field['type'] == 'int'):
        return random.randint(field['min'], field['max'])
    elif (field['type'] == 'object'):
        return populateObject(field['fields'])
    elif (field['type'] == 'name'):
        return fake.name()
    elif (field['type'] == 'array'):
        array = []
        length = random.randint(1, field['max-length'])
        for i in range(0, length):
            element = populateField(field['element'])
            array.append(element)
        return array
    elif (field['type'] == 'float'):
        return round(random.uniform(field['min'], field['max']), 2)
    elif (field['type'] == 'date'):
        return fake.date_time_this_decade().isoformat()
    elif (field['type'] == 'string'):
        return fake.bothify(field['pattern'])
    elif(field['type'] == 'text'):
        return fake.text(max_nb_chars=field['max-length'])
    elif(field['type'] == 'email'):
        return fake.ascii_email()


for i in range(0, NUMBER_OF_DATA):
    element = populateObject(data_model)
    output.append(element)

with open('../backend/db/db.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=4)

print("Samples dumped in db.json")

'''
with open('./backend/db/db.json', 'w', encoding='utf-8') as f:
    json.dump(x, f, ensure_ascii=False, indent=4)
'''
model_file.close()
