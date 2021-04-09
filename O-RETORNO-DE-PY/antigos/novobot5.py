#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 05:28:42 2018

@author: igor
"""
import csv
import math
from drawnow import drawnow
import matplotlib.pyplot as plt
import numpy as np
from binance.client import Client
import time

api_key = "bcKDGNhRoFKgdRbKSnIlCOKBvB5eDlecUY7kRcZV2r0a1P35H5WbcLIugcybzdIV"
api_secret = "xZrZ9TxbMDtdFGzJ5ugNUCkac1Ps0jtdRqzoYUNHEwTGlxaJkFbP2rTkGi0opeTd"


coin = "LTCBTC"
coin_ = "LTC"

securper1=6
securper2 = 0.2
S=10
realmoney = False
client = Client(api_key, api_secret)
tick = client.get_ticker(symbol=coin)
initbtc = 0.0021

interval = Client.KLINE_INTERVAL_1MINUTE

drawgraph = True

s=client.get_symbol_info(coin)['filters'][0]['tickSize']
s=s[s.find("."):s.find("1")]
ticksize = len(s)-1
s=client.get_symbol_info(coin)['filters'][1]['stepSize']
s=s[s.find("."):s.find("1")]
stepsize = len(s)

#btcp = float(client.get_symbol_ticker(symbol='BTC')['price'])

#print(client.get_symbol_info(coin)['filters'][1]['stepSize'],stepsize, client.get_symbol_info(coin)['filters'][0]['tickSize'],ticksize)

high=(float(tick['highPrice']))
low=(float(tick['lowPrice']))



Times=[float(tick['closeTime']), float(tick['closeTime'])]
AcTimes=[float(tick['closeTime'])]



if Times[-1]-Times[-2] != 0:
    dt = (Times[-1]-Times[-2])
else:
    dt=1000
    

    
    
agg_trades = client.get_aggregate_trades(symbol=coin, limit=4)
P=0
N=0
mass=0
    
for agg in agg_trades:
    if bool(agg['m'])==False:
        P+=(float(agg['q']))*(float(agg['p']))
    else:
        N+=(float(agg['q']))*(float(agg['p']))
        P=P/dt**2
        N=N/dt**2
        mass += float(agg['q'])


global c

i=0
ii=0
iii=0
iv=0
c = 0
C =[c]
x, y, z, w, dw = [P], [float(tick['lastPrice'])], [N], [P-N], []
Volumes = [float(tick['volume'])]
Highs =[high]
Lows=[low]
Perchanges =[float(tick['priceChangePercent'])]
Mass =[mass]
Momentum = [(y[-1])/dt]
dw.append(w[c-1])
DT = [dt]
thresh = 0
#BTC = [btcp]

    
kline = client.get_klines(symbol=coin,interval=interval)
meanprice = (float(kline[-1][1]) + float(kline[-1][4]))/2    
V = float(float(tick['volume']))
perchange = float(tick['priceChangePercent'])
Volumes.append(V), Perchanges.append(perchange)

Es = math.exp(-((float(kline[-1][2])-high)*10**(stepsize) + perchange/100))*(Volumes[-1]/Volumes[-2])
Ei = math.exp(-((-float(kline[-1][3])+low)*10**(stepsize) + perchange/100))*(Volumes[-2]/Volumes[-1])


Crs = math.sqrt((float(kline[-1][2])**2 + meanprice**2)/2)
Cri = math.sqrt((float(kline[-1][3])**2 + meanprice**2)/2)

mi = math.sqrt((((Cri+Crs)/2 - meanprice)**2)/2)

lims = Crs + mi*(1+Es)
limi = Cri - mi*(1+Ei)


lms, lmi = [lims],[limi]


csvfile = "/Users/igor/Dropbox/DATAtesta.txt"


plt.ion()
fig=plt.figure(1)
plt.locator_params(axis ='y', nticks=15)

def makeFig():
    momentum_ = np.array(Momentum[1:])
    lms_ = np.array(lms[1:])
    lmi_ = np.array(lmi[1:])
    x_,y_,z_,C_ = np.array(x[1:]),np.array(y[1:]),np.array(z[1:]),np.array(C[1:]) 
    w_=np.array(w[1:])

    
    
    ax1= plt.subplot(411)
    ax1.grid(alpha=0.5)
    ax1.plot(C_, lms_, 'g--', lw=0.8)
    ax1.plot(C_, y_,'b-', lw=1.5)
    ax1.plot(C_, lmi_, 'r--', lw=0.8)
    
    ax2= plt.subplot(412)
    ax2.grid(alpha=0.5)
    ax2.plot(C_, x_, 'g--', lw=1 )
    ax2.plot(C_, z_, 'r--', lw=1 ) 
    
    ax3 = plt.subplot(413)
    ax3.grid(alpha=0.5)
    ax3.plot(C_, w_, 'c', lw=1) 
    
    
    ax4 = plt.subplot(414)
    ax4.grid(alpha=0.5)
    ax4.plot(C_, momentum_, 'm', lw=1) 

def att():
    global c
    tick = client.get_ticker(symbol=coin)
    kline = client.get_klines(symbol=coin,interval=interval, limit=4)
    #meanprice = (float(kline[-1][1]) + float(kline[-1][4]))/2 
    meanprice = (((float(kline[-1][4])+float(kline[-1][1]))/2)*float(kline[-1][5]) +
                 ((float(kline[-2][4])+float(kline[-2][1]))/2)*float(kline[-2][5]))/(float(kline[-2][5])+float(kline[-1][5]))
    
    high = float(tick['highPrice'])
    low = float(tick['lowPrice'])
    V = float(float(tick['volume']))
    perchange = float(tick['priceChangePercent'])
#    BTC.append(btcp)
    Volumes.append(V), Highs.append(high), Lows.append(low), Perchanges.append(perchange), Times.append(float(tick['closeTime']))
    AcTimes.append(Times[-1] + AcTimes[-1])
    if Times[-1]-Times[-2] != 0:
        dt = (Times[-1]-Times[-2])
    else:
        dt=1000
    DT.append(dt)
    Es = math.exp(-((float(kline[-1][2])-high)*10**(stepsize) + (perchange/100)*(Volumes[-1]/Volumes[-2])))
    Ei = math.exp(((-float(kline[-1][3])+low)*10**(stepsize) + (perchange/100)*(Volumes[-1]/Volumes[-2])))

#    print(Es, Ei)

#    print(kline)
    Crs = math.sqrt((float(kline[-1][2])**2 + meanprice**2)/2)
    Cri = math.sqrt((float(kline[-1][3])**2 + meanprice**2)/2)
#           Crs = (float(kline[-1][2]) + meanprice)/2
#           Cri = (float(kline[-1][3]) + meanprice)/2
 

         
    mi = math.sqrt((((Cri+Crs)/2 - meanprice)**2)/2)
    
    agg_trades = client.get_aggregate_trades(symbol=coin, limit=1)
    
    y.append(float(kline[-1][4]))
#    lims = Cr + 2*mi*(1/math.log(2)) + (2*10**(-ticksize+1))*y[-1]
#    limi = Cr - 2*mi*(1/math.log(2)) + (2*10**(-ticksize+1))*y[-1]
#    lims = Cr + 2*mi*(1/math.log(2)) + (2*10**(-ticksize+1))*y[-1]
#    limi = Cr - 2*mi*(1/math.log(2)) - (2*10**(-ticksize+1))*y[-1]
 
    lims = Crs + mi*(1+Es)
    limi = Cri - mi*(1+Ei)
    
    
    lms.append(lims), lmi.append(limi)
    
    P=0
    N=0
    mass = 0
    for agg in agg_trades:
        if bool(agg['m'])==False:
            P+=(float(agg['q']))*(float(agg['p']))
        else:
            N+=(float(agg['q']))*(float(agg['p']))
        P=P/dt**2
        N=N/dt**2
        mass += float(agg['q'])
            
    c+=1
    x.append(P), z.append(N), C.append(c)
   
    w.append((x[-1]-z[-1])), Mass.append(mass)
    Momentum.append(10*(abs(Mass[-1]-Mass[-2]))*(y[-1] - y[-2])/dt)

    if c <3:
        dw.append(w[c-1])
    else:
        dw.append((w[-1]-w[-2])/dt)
#    print(Momentum[-1], mi*Es, mi*Ei)
    
    termo1 = ((float(kline[-1][4])-float(kline[-1][1]))*float(kline[-1][5])*2 + (float(kline[-2][4])-float(kline[-2][1]))*float(kline[-2][5]))/(float(kline[-2][5])+float(kline[-1][5])*2)
#    termo2 = ((float(kline[-3][4])-float(kline[-3][1]))*float(kline[-3][5]) + (float(kline[-4][4])-float(kline[-4][1]))*float(kline[-4][5]))/(float(kline[-4][5])+float(kline[-3][5]))

    thresh = termo1 
    
    if drawgraph == True:    
        drawnow(makeFig)
        plt.pause(0.01)
    return thresh

while True:

    thresh = att()
#    print(thresh)

    if c>=S:
#        print(w[-1]-w[-2], Momentum[-1]- Momentum[-2], Momentum[-2]-Momentum[-3])
#        print(-math.sqrt(((high-meanprice)**2 + (meanprice-low)**2)/2)*(Perchanges[-1]-Perchanges[-4])  <= y[-1] - y[4] <= (1.002)*math.sqrt(((high-meanprice)**2 + (meanprice-low)**2)/2)*abs(Perchanges[-1]-Perchanges[-4]) and y[-1] - y[-2] >=0)
        if (thresh > 0 and (
        Perchanges[-1]-Perchanges[-2] >= -securper1) and
        (Perchanges[-2]-Perchanges[-3] >= -securper1) and 
        (Perchanges[-S]-Perchanges[-1] >= -securper2)):
            
    

            if ( w[-1] - w[-2] > 0 and w[-2] - w[-3] >= 0 and
                 Momentum[-1]-Momentum[-2] >=0):


#            if w[-1] > 0 and w[-2] > 0 and Momentum[-1] <= 0 and Momentum[-2] <= 0:
                i = 1
                
            price = float(client.get_symbol_ticker(symbol=coin)['price'])
            
            if True:
                ii=1
    
            if (y[-1]-y[-S]) >= 0:
                iii=1
    
#            if -2*10**(-ticksize+1) <= y[-1] - y[-4] <= 2*10**(-ticksize+1) and y[-1] - y[-2] >=0: #o ideal aqui seria y-1 - y-4 positivo, mas não muito positivo

#            if -math.sqrt(((high-meanprice)**2 + (meanprice-low)**2)/2)*(Perchanges[-1]-Perchanges[-4])  <= y[-1] - y[4] <= (1.002)*math.sqrt(((high-meanprice)**2 + (meanprice-low)**2)/2)*abs(Perchanges[-1]-Perchanges[-4]) and y[-1] - y[-2] >=0: #o ideal aqui seria y-1 - y-4 positivo, mas não muito positivo
            if True:
                iv=1
#            print(-math.sqrt(((high-meanprice)**2 + (meanprice-low)**2)/2)*(Perchanges[-1]-Perchanges[-2]), y[-1] - y[4], (1.002)*math.sqrt(((high-meanprice)**2 + (meanprice-low)**2)/2)*abs(Perchanges[-1]-Perchanges[-2]))        
            if i*ii*iii*iv == 1:
                if realmoney == False:
                    print('buy', y[-1])
                    i, ii, iii, iv = 0, 0, 0, 0
                    fill = False
                    count = 0
                    while fill == False:
                        count += 1
                        price = float(client.get_symbol_ticker(symbol=coin)['price'])
                        att()
                        if price >= y[-1]*1.0025:
                            print('sold', y[-1]*1.0025, time.ctime() )
                            fill = True
                            W= 'Win'
                            dic = {'buy price': y[-1], 'sell price': y[-1]*1.0025, 'profit': 100*(y[-1]*1.0025 - (y[-1]*1.0025)*0.0005 -y[-1]*0.0005), 'time': time.ctime(), 'real money?': 'False', 'Trade quality': W }
                            fieldnames=['buy price', 'sell price', 'profit', 'time', 'real money?', 'Trade quality']
                            with open(csvfile, 'a') as file:
                                writer = csv.DictWriter(file, fieldnames=fieldnames)
                                writer.writerow(dic)
                        elif price <= y[-1]*0.98 and count >= 200:
                            print('sold', y[-1]*1.0025, time.ctime() )
                            fill = True
                            W= 'Loss'
                            dic = {'buy price': y[-1], 'sell price': y[-1]*1.0025, 'profit': 100*(y[-1]*1.0025 - (y[-1]*1.0025)*0.0005 -y[-1]*0.0005), 'time': time.ctime(), 'real money?': 'False', 'Trade quality': W }
                            fieldnames=['buy price', 'sell price', 'profit', 'time', 'real money?', 'Trade quality' ]
                            realmoney = False
                            with open(csvfile, 'a') as file:
                                writer = csv.DictWriter(file, fieldnames=fieldnames)
                                writer.writerow(dic)
                                
                                
                if realmoney == True:
                    qv=(initbtc)/y[-1]
                    qb2f = "{:0.0{}f}".format(qv, stepsize)

                    order = client.order_market_buy(
                        symbol=coin,
                        quantity=qb2f,
                        newOrderRespType=Client.ORDER_RESP_TYPE_FULL,
                        recvWindow=180)
                    if order['status']=='FILLED' or order['status']=='PARTIALLY_FILLED':
                        preco = float(order['fills'][0]['price'])
                        qtd = float(order['executedQty'])                        
                        sellprice = preco*1.0025
                        qb2f = "{:0.0{}f}".format(qtd, stepsize)
                        sellprice = "{:0.0{}f}".format(sellprice, ticksize)
                    
                        order = client.order_limit_sell(
                            symbol=coin,
                            quantity=qb2f, price=sellprice,
                            newOrderRespType=Client.ORDER_RESP_TYPE_FULL,
                            recvWindow=400)
                        
                        print('buy', preco)
                        i, ii, iii, iv = 0, 0, 0, 0
                        fill = False
                        count = 0
                        oid = order['orderId']
                        while fill == False:
                            price = float(client.get_symbol_ticker(symbol=coin)['price'])
                            count += 1
                            order = client.get_order(symbol=coin, orderId=oid)
                            att()
                            if order['origQty']==order['executedQty']:
                                fill=True
                                venda = float(order['price'])
                                W = 'Win'
                            elif order['executedQty']==0 and price <= 0.98*preco and count >= 200:
                                client.cancel_order(symbol=coin, orderId=oid)
                                order = client.order_market_sell(
                                        symbol=coin,
                                        quantity=qb2f)
                                venda = float(order['price'])
                                fill = True
                                W='Loss'
                                realmoney = False
                                
                                
                                
                        initbtc = venda*float(order['executedQty'])
                        
                        print('sold', venda, time.ctime() )
                        order = False
                        dic = {'buy price': preco, 'sell price': venda, 'profit': 100*(venda - venda*0.0005 -price*0.0005), 'time': time.ctime(), 'real money?': 'True', 'Trade quality': W }
                        fieldnames=['buy price', 'sell price', 'profit', 'time', 'real money?', 'Trade quality']

                        with open(csvfile, 'a') as file:
                            writer = csv.DictWriter(file, fieldnames=fieldnames)
                            writer.writerow(dic)
                            
                        



