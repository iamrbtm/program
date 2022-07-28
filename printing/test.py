import csv, json

with open("filaments.csv", mode="r") as inp:
    reader = csv.reader(inp)
    
    outerdict = []
    
    for rows in reader:
        innerdict = []
        innerdict.append(rows[0])
        innerdict.append(rows[1])
        innerdict.append(rows[2])
        innerdict.append(rows[3])
        innerdict.append(rows[4])
        innerdict.append(rows[5])
        innerdict.append(rows[6])
        
        outerdict.append(innerdict)
    

print(outerdict)

with open('filament.json', 'w') as file:
    file.write(json.dumps(outerdict))