import yfinance as yf
import numpy as np
from sklearn.linear_model import LinearRegression

#test the models with K-fold cross validation
def test_models(all_data, all_results, k=10):
    global history

    accuracies = []
    models = []

    for b in range(len(all_results)):

        items_per_fold = int(len(all_results[b]) / k)
        extra = len(all_results[b]) % k

        for f in range(k):

            test = all_data[b][f*items_per_fold:(f+1)*items_per_fold]
            test_results = all_results[b][f*items_per_fold:(f+1)*items_per_fold]

            data_array = all_data[0:f*items_per_fold]
            data_array.extend(all_data[(f+1)*items_per_fold:])
            results_array = all_results[0:f*items_per_fold]
            results_array.extend(all_data[(f+1)*items_per_fold:])

            for i in range(len(results_array)):

                models.append(LinearRegression())
                models[-1].fit(data, results)

                predicated_results = []
                for d in range(len(test)):
                    predicated_results.append(models[b].predict([test[d]]))
                    # print(predicated_results[-1])
                percentage_inaccuracy = []
                for p in range(len(predicated_results)):
                    percentage_inaccuracy.append(abs(1-(predicated_results[p]/test_results[p])))
                # print(percentage_inaccuracy)
                accuracies.append(np.mean(percentage_inaccuracy))
    
    print(np.mean(accuracies))


if __name__ == "__main__":

    num_train = 100

    stock = yf.Ticker("BAC")
    history = stock.history(period='max')[["High", "Low"]].to_numpy()

    all_data = []
    all_results = []

    #build models
    for b in range(0,2):

        data = []
        results = []

        for i in range(len(history)):
            data.append([history[i][b]])
            if i > num_train:
                results.append(history[i][b])
            for j in range(2, min(len(data)+1, num_train)):
                data[-j].append(history[i][b])

        if len(data) == len(results):
            data = data[:-num_train]
            results = results[:-num_train]
        else:
            data = data[:-1][:len(results)]

        all_data.append(data)
        all_results.append(results)
        
    test_models(all_data, all_results)

