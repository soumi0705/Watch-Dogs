import dill as pickle

with open('./maid_monitoring.pkl', 'rb') as fin:
    model = pickle.load(fin)
