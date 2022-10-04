import csv
import pickle
files = ["cathay.csv","aa.csv","airbus.csv","austrian.csv","british.csv","china.csv","dragon.csv","europa.csv","finnair.csv","india.csv","lufthansa.csv","nz.csv","philippine.csv","qatar.csv"]


def read(filepath):
  content = []
  with open(filepath, encoding='utf-8-sig') as csvfile:
    csv_reader = csv.reader(csvfile)
    headers = next(csv_reader)

    for row in csv_reader:
      row_data = {key: value for key, value in zip(headers, row)}
      content.append(row_data)

  return content
routes = []
for x in files:
  temproutes = read(x)
  for n in temproutes:
    routes.append(n)
pickle.dump(routes, open("routes.pkl", "wb"))
