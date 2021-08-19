from pydefistats.chains.bsc import ChainInfo 
from pydefistats.chain_stats import getTotalSupply

TotalSupply = getTotalSupply(ChainInfo().network, "0x64d5baf5ac030e2b7c435add967f787ae94d0205")
print(TotalSupply)