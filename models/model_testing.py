import yfinance as yf
import numpy as np
from sklearn.linear_model import LinearRegression

#test the models
def test_models(models):
    global history

    for b in range(0, 2):
        data = []
        results = [] 
        for i in range(len(history)-3000, len(history)):
            data.append([history[i][b]])
            if i > 3:
                results.append(history[i][b])
            for j in range(2, min(len(data)+1, 5)):
                data[-j].append(history[i][b]) 

        if len(data) == len(results):
            data = data[:-3]
            results = results[:-3]
        else:
            data = data[:len(results)]

        predicated_results = []
        for d in range(len(data)):
            predicated_results.append(models[b].predict([data[d]]))
        percentage_inaccuracy = []
        for p in range(len(predicated_results)):
            percentage_inaccuracy.append(abs(1-(predicated_results[p]/results[p])))
        print(np.mean(percentage_inaccuracy))


if __name__ == "__main__":

    stock = yf.Ticker("BAC")
    history = stock.history(period='max')[["High", "Low"]].to_numpy()

    models = []

    #build models
    for b in range(0,2):

        data = []
        results = []

        for i in range(len(history)-3000):
            data.append([history[i][b]])
            if i > 3:
                results.append(history[i][b])
            for j in range(2, min(len(data)+1, 5)):
                data[-j].append(history[i][b])

        if len(data) == len(results):
            data = data[:-3]
            results = results[:-3]
        else:
            data = data[:-1][:len(results)]

        models.append(LinearRegression())
        models[-1].fit(data, results)
        
    test_models(models)

