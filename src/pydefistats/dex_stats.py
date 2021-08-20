from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

def getLastExchanges(network, exchange, contract: str, limit):
    transport = AIOHTTPTransport(url="https://graphql.bitquery.io")
    client = Client(transport=transport, fetch_schema_from_transport=True)
    query = gql(
    """
    query getLastExchanges ($network: EthereumNetwork, $contract: String!, $exchange: String!, $limit: Int){
      ethereum(network: $network) {
        dexTrades(
          options: {limit: $limit, desc: "timeInterval.second"}
          exchangeName: {is: $exchange}
          baseCurrency: {is: $contract}
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
        "limit": limit
    }
    result = client.execute(query, variable_values=params)
    return(result["ethereum"]["dexTrades"])
