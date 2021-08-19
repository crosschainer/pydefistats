from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


def getTotalSupply(network, contract: str):
    transport = AIOHTTPTransport(url="https://graphql.bitquery.io")
    client = Client(transport=transport, fetch_schema_from_transport=True)
    query = gql(
    """
    query getTotalSupply ($contract: String!, $network: EthereumNetwork) {
    ethereum(network: $network) {
        transactions {
        gasValue
        }
        transfers(
        currency: {is: $contract}
        sender: {is: "0x0000000000000000000000000000000000000000"}
        ) {
        amount
        }
    }
    }
    """
    )

    params = {
        "network": network,
        "contract": contract
    }
    result = client.execute(query, variable_values=params)
    total_supply = result["ethereum"]["transfers"][0]["amount"]
    
    # Sometimes tokens burn so we also need to calculate this
    
    transport = AIOHTTPTransport(url="https://graphql.bitquery.io")
    client = Client(transport=transport, fetch_schema_from_transport=True)
    query = gql(
    """
    query getTotalSupply ($contract: String!, $network: EthereumNetwork) {
    ethereum(network: $network) {
        transactions {
        gasValue
        }
        transfers(
        currency: {is: $contract}
        receiver: {is: "0x0000000000000000000000000000000000000000"}
        ) {
        amount
        }
    }
    }
    """
    )

    params = {
        "network": network,
        "contract": contract
    }
    result = client.execute(query, variable_values=params)
    if(result["ethereum"]["transfers"][0]["amount"] != None):
        total_supply = round(float(total_supply) - float(result["ethereum"]["transfers"][0]["amount"]),8)
        return total_supply
    else:
        return total_supply