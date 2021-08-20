from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

def getLastExchanges(network, exchange, contract: str, limit, pairAddress):
    transport = AIOHTTPTransport(url="https://graphql.bitquery.io")
    client = Client(transport=transport, fetch_schema_from_transport=True)
    query = gql(
    """
    query getLastExchanges ($network: EthereumNetwork, $contract: String!, $exchange: String!, $limit: Int, $pairAddress: String!){
      ethereum(network: $network) {
        dexTrades(
          options: {limit: $limit, desc: "timeInterval.second"}
          exchangeName: {is: $exchange}
          baseCurrency: {is: $contract}
          smartContractAddress: {is: $pairAddress}
        ) {
          transaction {
            hash
          }
          date {
            date
          }
          block {
            height
          }
          buyAmount
          buyAmountInUsd: buyAmount(in: USD)
          buyCurrency {
            symbol
            address
          }
          sellAmount
          sellAmountInUsd: sellAmount(in: USD)
          sellCurrency {
            symbol
            address
          }
          sellAmountInUsd: sellAmount(in: USD)
          tradeAmount(in: USD)
          transaction {
            gasValue
            gasPrice
            gas
          }
          timeInterval {
            second
          }
        }
      }
    }

    """
    )

    params = {
        "network": network,
        "contract": contract,
        "exchange": exchange,
        "limit": limit,
        "pairAddress": pairAddress
    }
    result = client.execute(query, variable_values=params)
    return(result["ethereum"]["dexTrades"])

def getPairs(network, exchange, contract: str):
    transport = AIOHTTPTransport(url="https://graphql.bitquery.io")
    client = Client(transport=transport, fetch_schema_from_transport=True)
    query = gql(
    """
    query getPairs ($network: EthereumNetwork, $contract: String!, $exchange: String!){
      ethereum(network: $network) {
        dexTrades(
          exchangeName: {is: $exchange}
          baseCurrency: {is: $contract}
          options: {desc: "trades"}
        ) {
          quoteCurrency: quoteCurrency {
            symbol
            address
          }
          baseCurrency {
            symbol
            address
          }
          poolToken: smartContract {
            address {
              address
            }
          }
          trades: count
        }
      }
    }


    """
    )

    params = {
        "network": network,
        "contract": contract,
        "exchange": exchange
    }
    result = client.execute(query, variable_values=params)
    dex_trades = (result["ethereum"]["dexTrades"])
    pool_addresses = []
    quote_currencies = []
    for x in dex_trades:
        pool_addresses.append(x["poolToken"]["address"]["address"])
    for x in dex_trades:
        quote_currencies.append(x["quoteCurrency"]["address"])
    transport = AIOHTTPTransport(url="https://graphql.bitquery.io")
    client = Client(transport=transport, fetch_schema_from_transport=True)
    query = gql(
    """
    query getPairLiquidity ($network: EthereumNetwork, $pool_addresses: [String!]){
      ethereum(network: $network) {
        address(address: {in: $pool_addresses}) {
          balances {
            currency {
              address
              name
            }
            value
          }
          address
        }
      }
    }



    """
    )

    params = {
        "network": network,
        "pool_addresses": pool_addresses
    }
    result = client.execute(query, variable_values=params)
    balances = (result["ethereum"]["address"])
    pools=[]
    for x in balances:
      for y in x["balances"]:
        if(y["currency"]["address"] in quote_currencies or y["currency"]["address"] == contract):
          pools.append([x["address"], y["currency"]["name"], y["value"]])
    return list(zip(pools,pools[1:]))

def getPrice(network, exchange, contract: str, pairAddress):
    transport = AIOHTTPTransport(url="https://graphql.bitquery.io")
    client = Client(transport=transport, fetch_schema_from_transport=True)
    query = gql(
    """
    query getLastExchanges ($network: EthereumNetwork, $contract: String!, $exchange: String!, $pairAddress: String!){
      ethereum(network: $network) {
        dexTrades(
          options: {limit: 1, desc: "timeInterval.second"}
          exchangeName: {is: $exchange}
          baseCurrency: {is: $contract}
          smartContractAddress: {is: $pairAddress}
        ) {
          transaction {
            hash
          }
          date {
            date
          }
          block {
            height
          }
          buyAmount
          buyAmountInUsd: buyAmount(in: USD)
          buyCurrency {
            symbol
            address
          }
          sellAmount
          sellAmountInUsd: sellAmount(in: USD)
          sellCurrency {
            symbol
            address
          }
          sellAmountInUsd: sellAmount(in: USD)
          tradeAmount(in: USD)
          transaction {
            gasValue
            gasPrice
            gas
          }
          timeInterval {
            second
          }
        }
      }
    }

    """
    )

    params = {
        "network": network,
        "contract": contract,
        "exchange": exchange,
        "pairAddress": pairAddress
    }
    result = client.execute(query, variable_values=params)
    #print(result["ethereum"]["dexTrades"][0]["buyAmountInUsd"])
    #print(result["ethereum"]["dexTrades"][0]["sellAmount"])
    return(result["ethereum"]["dexTrades"][0]["buyAmountInUsd"] / result["ethereum"]["dexTrades"][0]["sellAmount"])