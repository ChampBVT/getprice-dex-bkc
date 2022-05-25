import json
from constants import addresses
from web3 import Web3
import os

# TODO: Make function generalized
def getPrice(chain, factory, pair):

    #####################################################################
    #####################################################################

    AMM = addresses.module['AMM'][chain][factory]['Factory']

    token_names = pair.split('/')
    token1_address = addresses.module['Tokens'][chain][token_names[0]]
    token2_address = addresses.module['Tokens'][chain][token_names[1]]

    # Init Web3
    web3 = Web3(Web3.HTTPProvider(addresses.module['Chain'][chain]))
    token1_address = web3.toChecksumAddress(token1_address)
    token2_address = web3.toChecksumAddress(token2_address)
    factory_address = web3.toChecksumAddress(AMM)

    # ABI Contract factory
    with open(os.getcwd() + '/ABIs/factory.json', 'r') as abi_definition:
        abi = json.load(abi_definition)

    # ABI Contract Pancake Pair
    with open(os.getcwd() + '/ABIs/token.json', 'r') as abi_definition:
        parsed_pair = json.load(abi_definition)

    #####################################################################
    #####################################################################

    contract = web3.eth.contract(address=factory_address, abi=abi)

    pair_address = contract.functions.getPair(
        token1_address, token2_address).call()
    pair = web3.eth.contract(abi=parsed_pair, address=pair_address)

    reserves = pair.functions.getReserves().call()
    reserve_token1 = reserves[0]
    reserve_token2 = reserves[1]

    token1 = web3.eth.contract(address=token1_address, abi=parsed_pair)
    token2 = web3.eth.contract(address=token2_address, abi=parsed_pair)

    token1_decimals = token1.functions.decimals().call()
    token2_decimals = token2.functions.decimals().call()

    token_decimal_diff = abs(token1_decimals - token2_decimals)

    # In case 2 tokens has different decimals value
    if token1_decimals < token2_decimals:
        reserve_token1 = reserve_token1 * \
            (10 ** token_decimal_diff)
    elif token1_decimals > token2_decimals:
        reserve_token2 = reserve_token2 * \
            (10 ** token_decimal_diff)

    return {
        token_names[0]: "{:.6f}".format(reserve_token2/reserve_token1),
        token_names[1]: "{:.6f}".format(reserve_token1/reserve_token2)
    }

    #####################################################################
    #####################################################################
