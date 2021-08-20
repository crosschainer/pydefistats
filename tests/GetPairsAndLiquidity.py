from pydefistats.chains.bsc import ChainInfo as BSCInfo 
from pydefistats.dex_stats import getPairs

pairs = getPairs(BSCInfo().network, "Pancake v2", "0x64d5baf5ac030e2b7c435add967f787ae94d0205")
print(pairs)
