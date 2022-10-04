import pickle
routesdoc = open("routes.pkl","rb")
routes = pickle.load(routesdoc)
for x in routes:
  print(x["airline"])