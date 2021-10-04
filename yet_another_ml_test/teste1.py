 Deep Learning Intermediate Machine Learning Project Python Qlikview Sequence Modeling Structured Data Supervised Time Series Time Series Forecasting
Introduction

Predicting how the stock market will perform is one of the most difficult things to do. There are so many factors involved in the prediction – physical factors vs. psychological, rational and irrational behavior, etc. All these aspects combine to make share prices volatile and very difficult to predict with a high degree of accuracy.

Can we use machine learning as a game-changer in this domain? Using features like the latest announcements about an organization, their quarterly revenue results, etc., machine learning techniques have the potential to unearth patterns and insights we didn’t see before, and these can be used to make unerringly accurate predictions.

stock price prediction, LSTM, machine learning

In this article, we will work with historical data about the stock prices of a publicly listed company. We will implement a mix of machine learning algorithms to predict the future stock price of this company, starting with simple algorithms like averaging and linear regression, and then move on to advanced techniques like Auto ARIMA and LSTM. The above-stated machine learning algorithms can be easily learned from this ML Course online.

The core idea behind this article is to showcase how these algorithms are implemented. I will briefly describe the technique and provide relevant links to brush up on the concepts as and when necessary. In case you’re a newcomer to the world of time series, I suggest going through the following articles first:

    A comprehensive beginner’s guide to create a Time Series Forecast
    A Complete Tutorial on Time Series Modeling
    Free Course: Time Series Forecasting using Python


Project to Practice Time Series Forecasting
Problem Statement

Time Series forecasting & modeling plays an important role in data analysis. Time series analysis is a specialized branch of statistics used extensively in fields such as Econometrics & Operation Research.

Time Series is being widely used in analytics & data science. This is specifically designed time series problem for you and the challenge is to forecast traffic.

Practice Now



Are you a beginner looking for a place to start your data science journey? Presenting a comprehensive course, full of knowledge and data science learning, curated just for you! This course covers everything from basics of Machine Learning to Advanced concepts of ML, Deep Learning and Time series.

    Certified AI & ML Blackbelt+ Program

Table of Contents

        Understanding the Problem Statement
        Moving Average
        Linear Regression
        k-Nearest Neighbors
        Auto ARIMA
        Prophet
        Long Short Term Memory (LSTM)


Understanding the Problem Statement

We’ll dive into the implementation part of this article soon, but first it’s important to establish what we’re aiming to solve. Broadly, stock market analysis is divided into two parts – Fundamental Analysis and Technical Analysis.

    Fundamental Analysis involves analyzing the company’s future profitability on the basis of its current business environment and financial performance.
    Technical Analysis, on the other hand, includes reading the charts and using statistical figures to identify the trends in the stock market.

As you might have guessed, our focus will be on the technical analysis part. We’ll be using a dataset from Quandl (you can find historical data for various stocks here) and for this particular project, I have used the data for ‘Tata Global Beverages’. Time to dive in!

Note: Here is the dataset I used for the code: Download

We will first load the dataset and define the target variable for the problem:

#import packages
import pandas as pd
import numpy as np

#to plot within notebook
import matplotlib.pyplot as plt
%matplotlib inline

#setting figure size
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 20,10

#for normalizing data
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))

#read the file
df = pd.read_csv('NSE-TATAGLOBAL(1).csv')

#print the head
df.head()
