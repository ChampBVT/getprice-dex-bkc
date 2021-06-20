import json
import addresses
import math
from web3 import Web3


def getPrice(chain, factory, pair, decimal="18/18"):

    #####################################################################
    #####################################################################

    AMM = addresses.module['AMM'][chain][factory]['Factory']
    x = pair.split('/')
    Tokens1 = addresses.module['Tokens'][chain][x[0]]
    Tokens2 = addresses.module['Tokens'][chain][x[1]]

    web3 = Web3(Web3.HTTPProvider(addresses.module['Chain'][chain]))
    Tokens1 = web3.toChecksumAddress(Tokens1)
    Tokens2 = web3.toChecksumAddress(Tokens2)
    Factory_Address = web3.toChecksumAddress(AMM)

    # ABI Contract factory
    with open('src/factory.json', 'r') as abi_definition:
        abi = json.load(abi_definition)

    # ABI Contract Pancake Pair
    with open('src/pair.json', 'r') as abi_definition:
        parsed_pair = json.load(abi_definition)

    #####################################################################
    #####################################################################

    contract = web3.eth.contract(address=Factory_Address, abi=abi)
    GDR = web3.eth.contract(address=Tokens2, abi=parsed_pair)
    print(GDR.functions.decimals().call())
    pair_address = contract.functions.getPair(Tokens1, Tokens2).call()
    pair1 = web3.eth.contract(abi=parsed_pair, address=pair_address)

    reserves = pair1.functions.getReserves().call()
    reserve0 = float(reserves[0])
    reserve1 = float(reserves[1])

    d = decimal.split('/')
    decimal_diff = int(d[0]) - int(d[1])
    if decimal_diff > 0:
        reserve1 = reserve1 * 10 ** decimal_diff
    elif decimal_diff < 0:
        reserve0 = reserve0 * 10 ** decimal_diff

    print(
        f'The current {pair} price on {factory} is : {"{:.20f}".format(reserve1/reserve0)}')
    print(f'Inverse: {"{:.20f}".format(reserve0/reserve1)}')
    print(f'Reserve 0: {"{:.20f}".format(reserve0)}')
    print(f'Reserve 1: {"{:.20f}".format(reserve1)}')

    #####################################################################
    #####################################################################


getPrice(chain="BKC", factory="TukTuk", pair="WKUB/GDR", decimal="18/8")
# getPrice(chain="BKC", factory="TukTuk", pair="WKUB/TUK")
# getPrice(chain="BKC", factory="TukTuk", pair="GDR/TUK")
# getPrice(chain="BKC", factory="TukTuk", pair="WKUB/kBNB")
# getPrice(chain="BSC", factory="Pancake", pair="DOP/BUSD")
