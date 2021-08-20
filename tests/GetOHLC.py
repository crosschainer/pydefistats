from pydefistats.chains.bsc import ChainInfo as BSCInfo 
from pydefistats.dex_stats import getOHLC

ohlc = getOHLC(BSCInfo().network, "Pancake v2", "0x64d5baf5ac030e2b7c435add967f787ae94d0205", "0xe9e7cea3dedca5984780bafc599bd69add087d56", 100)
print(ohlc)
