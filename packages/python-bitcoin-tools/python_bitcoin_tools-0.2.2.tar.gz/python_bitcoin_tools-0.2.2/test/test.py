
from bitcoin_tools.analysis.status.utils import get_utxo, decode_utxo, display_decoded_utxo
from bitcoin_tools.utils import change_endianness

txid_genesis = change_endianness('0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098')
index = 0

outpoint_genesis, genesis_utxo = get_utxo(txid_genesis, index)
decoded_genesis = decode_utxo(genesis_utxo, outpoint_genesis)

print(decoded_genesis)

