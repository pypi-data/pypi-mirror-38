from copy import deepcopy
import plyvel
from binascii import hexlify, unhexlify
from bitcoin_tools.analysis.status import *
from bitcoin_tools.analysis.status.plots import plots_from_samples
from bitcoin_tools.analysis.status.utils import deobfuscate_value, decode_utxo, get_serialized_size_fast, roundup_rate
import ujson
import threading

current_id = None
stop = False


def operate_values(db, o_key, prefix, reverse):
    global current_id, stop

    for key, o_value in db.iterator(prefix=prefix, reverse=reverse):
        if key == current_id:
            stop = True
        if stop:
            break
        else:
            current_id = key
            print hexlify(key), reverse
            # if o_key is not None:
            #     utxo = deobfuscate_value(o_key, hexlify(o_value))
            # else:
            #     utxo = hexlify(o_value)
            #
            # # Decode the UTXO
            # utxo = decode_utxo(utxo, key)

    return


def get_dust_ldb(fin_name=CFG.chainstate_path):
    keys = []

    # UTXO prefix
    prefix = b'C'

    # Open the LevelDB
    db = plyvel.DB(fin_name, compression=None)  # Change with path to chainstate

    # Load obfuscation key (if it exists)
    o_key = db.get((unhexlify("0e00") + "obfuscate_key"))

    # If the key exists, the leading byte indicates the length of the key (8 byte by default). If there is no key,
    # 8-byte zeros are used (since the key will be XORed with the given values).
    if o_key is not None:
        o_key = hexlify(o_key)[2:]

    t1 = threading.Thread(target=operate_values, args=[db, o_key, prefix, False])
    t2 = threading.Thread(target=operate_values, args=[db, o_key, prefix, True])

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print "end"


    # # For every UTXO (identified with a leading 'c'), the key (tx_id) and the value (encoded utxo) is displayed.
    # # UTXOs are obfuscated using the obfuscation key (o_key), in order to get them non-obfuscated, a XOR between the
    # # value and the key (concatenated until the length of the value is reached) if performed).
    # for key, o_value in db.iterator(prefix=prefix):
    #     key = hexlify(key)
    #     if o_key is not None:
    #         utxo = deobfuscate_value(o_key, hexlify(o_value))
    #     else:
    #         utxo = hexlify(o_value)
    #
    #     # Decode the UTXO
    #     utxo = decode_utxo(utxo, key)
    #
    #     # Get output size and input size to compute dust.
    #
    #     out_size = get_serialized_size_fast(utxo['out'])
    #     # prev_tx_id (32 bytes) + prev_out_index (4 bytes) + scripSig_len (1 byte) + (PUSH sig + 72-byte
    #     # sig) (73 bytes) + (PUSH pk + compressed pk) (34 bytes) + nSequence (4 bytes)
    #     in_size = 32 + 4 + 1 + 73 + 34 + 4
    #
    #     # Get dust and round it up depending on the FEE_STEP
    #     raw_dust = utxo['out']["amount"] / float(out_size + in_size)
    #     rate = roundup_rate(raw_dust, FEE_STEP)
    #
    #     # Add dust to the proper step
    #     if MIN_FEE_PER_BYTE <= rate <= MAX_FEE_PER_BYTE:
    #         dust[rate] += 1
    #         value_dust[rate] += utxo["out"]["amount"]
    #         data_len_dust[rate] += len(utxo['out']["data"]) / 2
    #
    #     # And we increase the total counters for each read utxo.
    #     total_utxo += 1
    #     total_value += utxo["out"]["amount"]
    #     total_data_len += len(utxo['out']["data"]) / 2
    #
    # db.close()
    #
    # # Store dust calculation in a file.
    # data = {"dust_utxos": dust, "dust_value": value_dust, "dust_data_len": data_len_dust,
    #         "total_utxos": total_utxo, "total_value": total_value, "total_data_len": total_data_len}
    # ujson.dumps(data, open(CFG.data_path + 'dust.json', 'w'))
    #
    # return dust, value_dust, data_len_dust, total_utxo, total_value, total_data_len


if __name__ == '__main__':
    chainstate = CFG.bitcoin_tools_dir + 'chainstate/'

    # Parse ldb to get dust data
    dust, value_dust, data_len_dust, total_utxo, total_value, total_data_len = get_dust_ldb(chainstate)
    # # Aggregate dust
    # dust, value_dust, data_len_dust = aggregate_dust(dust, value_dust, data_len_dust)
    # # Plot the charts
    # plot_dust_charts(dust, value_dust, data_len_dust, total_utxo, total_value, total_data_len)
