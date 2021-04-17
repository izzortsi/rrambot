class ATrader:

    def __init__(strategy, init_btc, symbol, timeframe):

        self.strategy = strategy
        self.init_btc = init_btc
        self.symbol = symbol
        self.timeframe = timeframe
        self.state = False

        self.entrydates = []
        self.exitdates = []
        self.entryprices = []
        self.exitprices = []

        self.log = []
        self.profits = []

    def trade(self, i, dates, prices, indicators):

        price = prices.iloc[i]
        time = dates[i]
        t0, buy_price = self.Entry

        if (self.S and self.X(i, self.stoploss, buy_price, prices, indicators, self.speriod)):
            #ordem de venda
            #aqui vai ser order = ...
            #e if (order["status"] == "FILLED") return (order["orderId"], order["transactTime"], order["price"])
            #else tem que ver issae
            sell_price = float(price)
            eXit = [time, sell_price]
            profit = (sell_price - buy_price)
            percentual_profit = ((sell_price - buy_price)/buy_price)*100
            self.profits.append(percentual_profit)
            res_time = str(time - t0)
            print(f"vendeu a {sell_price} em {time}. Diferença absoluta de: {profit}; Diferença percentual: {percentual_profit}%. Tempo de resolução: {res_time} ")
            
            self.log[self.opscount].append(f"({self.opscount}) vendeu a {sell_price} em {time}. Diferença absoluta de: {profit}; Diferença percentual: {percentual_profit}%. Tempo de resolução: {res_time}.\n")
            self.trades[-1].append(time)
            self.opscount += 1

            self.exitdates.append(time)
            self.exitprices.append(price)

            self.S = not(self.S)

            return self.Entry, self.eXit, profit, res_time, self.S #tem que ver melhor que que precisa retornar

        elif (not(self.S) and self.E(i, prices, indicators, self.bperiod)):

            self.Entry = [time, price]
            print(f"comprou a {price} em {time}")
            self.log.append([f"({self.opscount}) comprou a {price} em {time}.\n"])

            self.entrydates.append(time)
            self.entryprices.append(price)

            self.trades.append([time])
            self.S = not(self.S)

            return None

        else:
            if self.S and self.stoploss_check(i, self.stoploss, buy_price, prices, indicators):
                sell_price = float(price)
                eXit = [time, sell_price]
                profit = (sell_price - buy_price)
                percentual_profit = ((sell_price - buy_price)/buy_price)*100
                #self.profits.append(percentual_profit)
                global stoploss_parameter
                self.profits.append(stoploss_parameter)
                res_time = str(time - t0)
                print(f"Stop-loss: vendeu a {sell_price} em {time}. Diferença absoluta de: {profit}; Diferença percentual: {percentual_profit}%. Tempo de resolução: {res_time} ")

                self.log[self.opscount].append(f"({self.opscount}) STOP-LOSS: Vendeu a {sell_price} em {time}. Diferença absoluta de: {profit}; Diferença percentual: {percentual_profit}%. Tempo de resolução: {res_time}.\n")
                self.trades[-1].append(time)
                self.opscount += 1
                
                self.exitdates.append(time)
                self.exitprices.append(price)
                
                self.S = not(self.S)
                return self.Entry, self.eXit, profit, res_time, self.S

    def backtest(self):

        prices = self.df["close"]
        indicators = self.df.loc[:, self.df.columns != "close"]
        dates = prices.index

        dataset_size = len(dates)
        i = 26 + max(self.bperiod, self.speriod) #26 é o maior número de Nans nas dataframes

        while (i <= dataset_size - 1):
            #print(self.S)
            action = self.strategy(i, dates, prices, indicators)

            if action != None:
                self.Ops.append(action[:-1])

            i += 1

        total_profit = 0
        for profit in self.profits:
            total_profit += profit

        print(f"Lucro percentual aproximado: {total_profit}")
        with open(f"{filename}", "w") as log:
            for i, trade in enumerate(self.log):

                log.writelines(trade)

        log = open(f"{filename}", "a")
        log.write(f"Lucro percentual total: {total_profit}%.")
        log.close()            

        csv_data = []
        for (a, b, c, d, e) in zip(self.entrydates, self.entryprices, self.exitdates, self.exitprices, self.profits):
            csv_data.append([a, b, c, d, e])
            
        csv_name = filename.replace(".txt", ".csv")
        dftrades = pd.DataFrame(data = csv_data, columns = ["entry_date", "entry_price", "exit_date", "exit_price", "profit"])
        dftrades.to_csv(f'{csv_name}', index = False)

        return total_profit, self.trades
