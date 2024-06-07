import lzma
import dill as pickle
import pandas as pd
import numpy as np

def load_pickle(path):
    with lzma.open(path,"rb") as fp:
        file = pickle.load(fp)
    return file

def save_pickle(path,obj):
    with lzma.open(path, "wb") as fp:
        pickle.dump(obj, fp)


class Alpha():
    def __init__(self, insts, dfs, start, end):
        self.insts = insts
        self.dfs = dfs
        self.start = start
        self.end = end

    def init_portfolio_settings(self,trade_range):
        portfolio_df = pd.DataFrame(index=trade_range)\
            .reset_index()\
            .rename(columns={"index":"datetime"})
        portfolio_df.loc[0, "capital"] = 10000
        return portfolio_df


    def compute_meta_info(self, trade_range):
        for inst in self.insts:
            
            df = pd.DataFrame(index=trade_range)
            self.dfs[inst] = df.join(self.dfs[inst]).fillna(method="ffill").fillna(method="bfill")
            self.dfs[inst]['ret'] = -1 + self.dfs[inst]["close"]/self.dfs[inst]["close"].shift(1)
            sampled = self.dfs[inst]["close"] != self.dfs[inst]["close"].shift(1).fillna(method="bfill")
            eligible = sampled.rolling(5).apply(lambda x: int(np.any(x))).fillna(0)
            self.dfs[inst]["eligible"] = eligible.astype(int) & (self.dfs[inst]["close"] > 0).astype(int)
            # input(self.dfs[inst])
        return
            
            
            
            

    def run_simulation(self):
        print("running_backtest")
        date_range = pd.date_range(start=self.start, end=self.end, freq="D")
        self.compute_meta_info(trade_range=date_range)
        portfolio_df = self.init_portfolio_settings(trade_range=date_range)
        for i in portfolio_df.index:
            date = portfolio_df.loc[i, "datetime"]
            eligibles = [inst for inst in self.insts if self.dfs[inst].loc[date, "eligible"]]
            non_eligibles = [inst for inst in self.insts if inst not in eligibles ]
            if i != 0:
                #compute pnl
                pass
            # compute alpha signal
            alpha_scores = {}
            import random
            for inst in eligibles:
                alpha_scores[inst] = random.uniform(0,1)
            alpha_scores = {k:v for k,v in sorted (alpha_scores.items(), key=lambda pair: pair[1])}
            alpha_long = list(alpha_scores.keys())[-int(len(eligibles)/4):]
            alpha_short = list(alpha_scores.keys())[:int(len(eligibles)/4)]

            
            for inst in non_eligibles:
                portfolio_df.loc[i, "{} w".format(inst)] = 0
                portfolio_df.loc[i, "{} units".format(inst)] = 0
            
            for inst in eligibles:
                forecast = 1 if inst in alpha_long else (-1 if inst in alpha_short else 0)
                dollar_allocation = portfolio_df.loc[i, "capital"] / (len(alpha_long) + len(alpha_short))
                

            # compute positions and other information



