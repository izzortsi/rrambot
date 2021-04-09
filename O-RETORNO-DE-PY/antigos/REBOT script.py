# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
#%matplotlib inline
#%config InlineBackend.figure_format = 'svg'

from sklearn import manifold
from binance.client import Client

import ta as ta
import numpy as np
import pandas as pd
import sklearn.preprocessing as sklp

import plotly as ply
import plotly.graph_objs as go
from plotly import tools

#from plotly import offline
#offline.init_notebook_mode();


# %%
#symbol = "BTCUSDT"
#interval = Client.KLINE_INTERVAL_1DAY
#fromdate = "25 Jan, 2017"
#todate = "25 Jan, 2019"

symbol = "ETHUSDT"
interval = Client.KLINE_INTERVAL_1HOUR
fromdate = "1 week ago"
todate = "now"

client = Client("api key", "api secret")
klines = client.get_historical_klines(symbol, interval, fromdate, todate)

def format_klines(klines):
    OHLCV = []
    for k in klines:
        ohlcv = [float(k[1]), float(k[2]), float(k[3]), float(k[4]), float(k[5])]
        OHLCV.append(ohlcv)

#    return OHLCV

    O = pd.Series([k[0] for k in OHLCV], name = "OPEN")
    H = pd.Series([k[1] for k in OHLCV], name = "HIGH")
    L = pd.Series([k[2] for k in OHLCV], name = "LOW")
    C = pd.Series([k[3] for k in OHLCV], name = "CLOSE")
    V = pd.Series([k[4] for k in OHLCV], name = "VOLUME")

    OHLCV = pd.DataFrame([O,H,L,C,V]).T

    OHLCV.to_csv( "{0}-{1}-{2}-{3}.csv".format(symbol, interval, fromdate, todate) )

    obv = ta.volume.on_balance_volume(C, V)
    #obv
    macd = ta.trend.macd(C, fillna=True)
    #macd
    macddiff = ta.trend.macd_diff(C, fillna=True)
    #macddiff
    macdsign = ta.trend.macd_signal(C, fillna=True)
    #macdsign
    neg_vol = ta.volume.negative_volume_index(C, V, fillna=True)
    #neg_vol
    DF = pd.DataFrame([O, H, L, C, V, obv, macd, macddiff, macdsign, neg_vol])

    #X = [np.array(O), np.array(H), np.array(L), np.array(C), np.array(V), np.array(obv), np.array(macd), np.array(macddiff), np.array(macdsign), np.array(neg_vol)]

    X=np.array([O.values, H.values, L.values, C.values, V.values, obv.values, macd.values, macddiff.values, macdsign.values, neg_vol.values])
    X_ = X.transpose()

    return X_, O, H, L, C, V, DF


X_, O, H, L, C, V, DF = format_klines(klines)
#####SCALERS E TRANSFORMERS

#sklp.MinMaxScaler()
#sklp.MaxAbsScaler()
#sklp.PowerTransformer()
#sklp.QuantileTransformer()

#sklp.RobustScaler()
#sklp.StandardScaler()

scalers = [sklp.MinMaxScaler(), sklp.MaxAbsScaler(), sklp.PowerTransformer(), sklp.QuantileTransformer(), sklp.RobustScaler(), sklp.StandardScaler()]


# %%
def fit_all(xscalers, X):
    yscalers = []
    for xscaler in xscalers:
        yscalers.append(xscaler.fit(X))

    return yscalers

def transform_all(xscalers, X):
    tX = []
    for xscaler in xscalers:
        tX.append(xscaler.transform(X))

    return tX


scalers = fit_all(scalers, X_)
scalers
tXs = transform_all(scalers, X_)

specemb = manifold.SpectralEmbedding(n_components=3)


def embed_all(specemb, tXs):
    embedded = []
    for tX in tXs:
        embedded.append(specemb.fit_transform(tX))

    return embedded

embedded_data = embed_all(specemb, tXs)

#closesplot = ply.offline.iplot([{"y": C}]);

#normsplot = ply.offline.iplot([{"y": norms}]);


# %%
def plot_data(embedd_data, closes):
    pltdt = []
    for ed in embedd_data:
        pltdt1 = []
        for i, x in enumerate(ed):
            nx= list(x.T) + list([closes.values[i]])
            #print(nx)
            pltdt1.append(nx)
        pltdt.append(pltdt1)
    return pltdt


pltdt= plot_data(embedded_data, C);

#EXEMPLO DE CALL DE ARRAY: np.array(pltdt)[0,0:-1, 0]


#pltdt = np.array([[1]])

#pltdt2 = np.array([[4]])
#pltdt2[0]
#np.concatenate((pltdt, pltdt2), axis=1)

#plot_data(embedded_data, C)

def make_traces(pltdt):
    traces = []
    series = []
    pltdt = np.array(pltdt)
    for embdt in pltdt:
        #print(embdt[0:-1][0])
        Y1 = pd.Series(embdt[0:-1, 0])
        #Y1 = pd.Series(Y[0:-1,0])
        trace1 = go.Scatter(x = Y1.index, y=Y1)

        Y2 = pd.Series(embdt[0:-1, 1])
        #Y2 = pd.Series(Y[0:-1,1])
        trace2 = go.Scatter(x = Y2.index, y=Y2)

        Y3 = pd.Series(embdt[0:-1, 2])
        #Y3 = pd.Series(Y[0:-1,2])
        trace3 = go.Scatter(x = Y3.index, y=Y3)

        Y4 = pd.Series(embdt[0:-1, 3])
        #Y3 = pd.Series(Y[0:-1,2])
        trace4 = go.Scatter(x = Y4.index, y=Y4)



        #Y5 = pd.Series(embdt[0:-1, 4])
        #Y3 = pd.Series(Y[0:-1,2])
        #trace5 = go.Scatter(x = Y5.index, y=Y5)

        #traces.append([trace1, trace2, trace3, trace4, trace5])
        traces.append([trace1, trace2, trace3, trace4])
        #series.append([Y1, Y2, Y3, Y4, Y5])
        series.append([Y1, Y2, Y3, Y4])

    return traces, series


traces, series = make_traces(pltdt)




def make_plots(traces, H=1000, W=1000):
    plots = []
    for tr in traces:
        fig = tools.make_subplots(rows=4, cols=1, subplot_titles=( 'closes', 'reducao_dim_0', 'reducao_dim_1', 'reducao_dim_2'));

        fig.append_trace(tr[0], 2, 1);
        fig.append_trace(tr[1], 3, 1);
        fig.append_trace(tr[2], 4, 1);
        fig.append_trace(tr[3], 1, 1);
        fig['layout'].update(height=H, width=W, title='i <3 annotations and subplots');

        plots.append(fig)
    return plots

#fig['layout'].update(height=1800, width=1200, title='i <3 annotations and subplots')

plots = make_plots(traces)


# %%
from sklearn.cluster import SpectralClustering
from sklearn.neural_network import BernoulliRBM

def apply_rbm(embedd_data, n_components=2):
    extracted_features = []
    rbms = []
    for data in embedd_data:
        model = BernoulliRBM(n_components=n_components)
        tX = model.fit_transform(data)
        extracted_features.append(tX)
        rbms.append(model)
    return extracted_features, rbms

def apply_specl(embedd_data):
    clusters = []
    models = []
    for data in embedd_data:
        model = SpectralClustering(n_clusters=3, assign_labels="discretize", random_state=0)
        tX = model.fit_predict(data)
        clusters.append(tX)
        models.append(model)
    return clusters, models


exft, rbms = apply_rbm(embedded_data)
clusters, clusterers = apply_specl(embedded_data)

def rbm_traces(exft, n_components=2):
        traces = []
        series = []
        for feats in exft:
            Y1 = pd.Series([f[0] for f in feats])
            #Y1 = pd.Series(Y[0:-1,0])


            Y=Y1**2
            for i in range(n_components-1):
                Y += pd.Series([f[i+1] for f in feats])**2

            Y =np.sqrt(Y)

            trace1 = go.Scatter(x = Y.index, y=Y)
            global C
            trace2 = go.Scatter(x = C.index, y=C)
            traces.append([trace2, trace1])
            series.append([C, Y])

        return traces, series

def specl_traces(clusters):
        traces = []
        series = []
        for labels in clusters:
            #Y1 = pd.Series([l[0] for l in labels])
            Y1 = pd.Series(labels)
            trace1 = go.Scatter(x = Y1.index, y=Y1)
            global C
            print(C)
            trace2 = go.Scatter(x = C.index, y=C)
            traces.append([trace2, trace1])
            series.append([C, Y1])

        return traces, series


#exft[1]

#Y1 = pd.Series([f[0] for f in exft[1]])

#Y1

rbmtraces, rbmseries = rbm_traces(exft);
specltraces, speclseries = specl_traces(clusters);




def make_plots2(traces, H=1000, W=1000, rows=4):
    plots = []
    for tr in traces:
        fig = tools.make_subplots(rows=rows, cols=1)#, subplot_titles=( 'closes', 'transformer_0', 'transformer_1', 'transformer_2', 'transformer_3', 'transformer_4', 'transformer_5'));
        for x in range(1,rows+1):
            print(x)
            fig.append_trace(tr[x-1], x, 1);
            #fig.append_trace(tr[x-1], x, 1);

        fig['layout'].update(height=H, width=W, title='i <3 annotations and subplots');

        plots.append(fig)
    return plots

speclplots2 = make_plots2(specltraces, H=600, W=1200, rows=2);
rbmplots2 = make_plots2(rbmtraces, H=600, W=1200, rows=2);


# %%
ply.offline.iplot(rbmplots2[3], filename="rbmplt")


# %%
ply.offline.iplot(speclplots2[3], filename="rbmplt")


# %%




# %%

# %%

# %%
