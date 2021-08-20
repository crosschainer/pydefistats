from pydefistats.chains.bsc import ChainInfo as BSCInfo 
from pydefistats.dex_stats import getPrice

price = getPrice(BSCInfo().network, "Pancake v2", "0x64d5baf5ac030e2b7c435add967f787ae94d0205", "0xbe2c760aE00CbE6A5857cda719E74715edC22279")
print(price)
