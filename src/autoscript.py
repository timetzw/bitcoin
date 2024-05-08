import subprocess
import sys
import hashlib
import json
import time


def double_sha256(hex_input):
    # First SHA256 hash
    input_bytes = bytes.fromhex(hex_input)

    # First SHA256 hash
    first_hash = hashlib.sha256(input_bytes).digest()

    # Second SHA256 hash
    second_hash = hashlib.sha256(first_hash).digest()

    return second_hash.hex()


def execute_command(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, check=True)
        return result.stdout.decode().strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return None


def main():
    # Check if correct number of arguments are provided
    if len(sys.argv) != 3:
        print("Usage: {} <txId> <amount>".format(sys.argv[0]))
        sys.exit(1)

    txId = sys.argv[1]
    amount = sys.argv[2]

    node4 = "./bitcoin-cli -regtest  -datadir=../../data/nodeM -rpcport=1227"

    amount1 = str(float(amount) - 0.003)
    rawTx1 = execute_command(
        f"{node4} createrawtransaction '[{{\"txid\":\"{txId}\",\"vout\":0}}]' '{{\"bcrt1qjcn96zgy5t44mkmv0n6p48s4y74xkwyc0n6m5g\":{amount1}}}'")
    signedTx1 = execute_command(f"{node4} signrawtransactionwithwallet {rawTx1} | awk -F'\"' '/hex/{{print $4}}'")

    amount2 = str(float(amount) - 0.003)
    rawTx2 = execute_command(
        f"{node4} createrawtransaction '[{{\"txid\":\"{txId}\",\"vout\":0}}]' '{{\"bcrt1q37a75pxn09hqpp8nxrewur9xkhrw967axsqqc0\":{amount2}}}'")
    signedTx2 = execute_command(f"{node4} signrawtransactionwithwallet {rawTx2} | awk -F'\"' '/hex/{{print $4}}'")

    amount3 = str(float(amount) - 0.003)
    rawTx3 = execute_command(
        f"{node4} createrawtransaction '[{{\"txid\":\"{txId}\",\"vout\":0}}]' '{{\"n1tZMEDX4LMQavpBKR7CQvpKAq8hpoBiRf\":{amount3}}}'")
    signedTx3 = execute_command(f"{node4} signrawtransactionwithwallet {rawTx3} | awk -F'\"' '/hex/{{print $4}}'")

    print(signedTx1)
    print(signedTx2)
    print(signedTx3)

    invPrefix = "05000000"
    wtx1 = invPrefix + double_sha256(signedTx1)
    wtx2 = invPrefix + double_sha256(signedTx2)
    wtx3 = invPrefix + double_sha256(signedTx3)
    inv_tx1 = invPrefix + double_sha256(signedTx1)
    inv_tx2 = invPrefix + double_sha256(signedTx2)
    inv_tx3 = invPrefix + double_sha256(signedTx3)

    inv_node1 = "02" + wtx2 + wtx3
    inv_node2 = "02" + wtx1 + wtx3
    inv_node3 = "02" + wtx1 + wtx2

    print(inv_tx1)
    print(inv_tx2)
    print(inv_tx3)

    input("Press Enter to send inv tx1-3...")

    tempRes = execute_command(f"{node4} sendmsgtopeer 0 \"inv\" \"{inv_node1}\"")
    print("inv msg send to node1 " + ("success" if tempRes == "{\n}" else "fail"))
    time.sleep(0.5)

    tempRes = execute_command(f"{node4} sendmsgtopeer 1 \"inv\" \"{inv_node2}\"")
    print("inv msg send to node2 " + ("success" if tempRes == "{\n}" else "fail"))
    time.sleep(0.5)

    tempRes = execute_command(f"{node4} sendmsgtopeer 2 \"inv\" \"{inv_node3}\"")
    print("inv msg send to node3 " + ("success" if tempRes == "{\n}" else "fail"))
    time.sleep(0.5)

    # tempRes=execute_command(f"{node4} sendmsgtopeer 1 \"inv\" \"{inv_tx1}\"")
    # print("inv_tx1 send to node1 " + ("success" if tempRes == "{\n}" else "fail"))
    # tempRes=execute_command(f"{node4} sendmsgtopeer 2 \"inv\" \"{inv_tx1}\"")
    # print("inv_tx1 send to node2 " + ("success" if tempRes == "{\n}" else "fail"))

    # tempRes=execute_command(f"{node4} sendmsgtopeer 0 \"inv\" \"{inv_tx2}\"")
    # print("inv_tx2 send to node0 " + ("success" if tempRes == "{\n}" else "fail"))
    # tempRes=execute_command(f"{node4} sendmsgtopeer 2 \"inv\" \"{inv_tx2}\"")
    # print("inv_tx2 send to node2 " + ("success" if tempRes == "{\n}" else "fail"))

    # tempRes=execute_command(f"{node4} sendmsgtopeer 0 \"inv\" \"{inv_tx3}\"")
    # print("inv_tx3 send to node0 " + ("success" if tempRes == "{\n}" else "fail"))
    # tempRes=execute_command(f"{node4} sendmsgtopeer 1 \"inv\" \"{inv_tx3}\"")
    # print("inv_tx3 send to node1 " + ("success" if tempRes == "{\n}" else "fail"))

    input("Press Enter to send txP1-3 to node1-3")

    tempRes = execute_command(f"{node4} sendmsgtopeer 0 \"tx\" \"{signedTx1}\"")
    print("tx1 send to node1 " + ("success" if tempRes == "{\n}" else "fail"))
    time.sleep(0.5)

    tempRes = execute_command(f"{node4} sendmsgtopeer 1 \"tx\" \"{signedTx2}\"")
    print("tx2 send to node2 " + ("success" if tempRes == "{\n}" else "fail"))
    time.sleep(0.5)

    tempRes = execute_command(f"{node4} sendmsgtopeer 2 \"tx\" \"{signedTx3}\"")
    print("tx3 send to node3 " + ("success" if tempRes == "{\n}" else "fail"))
    time.sleep(0.5)

    print("Choose one node to mine next block...")

    tempRes = execute_command(f"{node4} decoderawtransaction {signedTx1}")
    txId1 = json.loads(tempRes)['txid']
    print("txId1=", txId1)
    tempRes = execute_command(f"{node4} decoderawtransaction {signedTx2}")
    txId2 = json.loads(tempRes)['txid']
    print("txId2=", txId2)
    tempRes = execute_command(f"{node4} decoderawtransaction {signedTx3}")
    txId3 = json.loads(tempRes)['txid']
    print("txId3=", txId3)

    tx_Ip_dict = {}
    tx_Ip_dict[txId1] = "127.0.0.1:1111"
    tx_Ip_dict[txId2] = "127.0.0.1:1112"
    tx_Ip_dict[txId3] = "127.0.0.1:1113"

    currentHeight = execute_command(f"{node4} getblockcount ")

    while currentHeight == execute_command(f"{node4} getblockcount "):
        time.sleep(2)

    currentHeight = execute_command(f"{node4} getblockcount ")
    tempRes = execute_command(f"{node4} getblockstats {currentHeight}")
    blockHash = json.loads(tempRes)["blockhash"]
    tempRes = execute_command(f"{node4} getblock \"{blockHash}\" 2")
    blockInfo = json.loads(tempRes)

    coinbase = []

    for tx in blockInfo["tx"]:
        for vin in tx["vin"]:
            if "coinbase" in vin:
                for vout in tx["vout"]:
                    if "address" in vout["scriptPubKey"]:
                        coinbase.append(vout["scriptPubKey"]["address"])
        if tx["txid"] in tx_Ip_dict:
            print("Miner:", coinbase, "is mapping to", tx_Ip_dict[tx["txid"]])


    # tempRes=execute_command(f"{node4} sendmsgtopeer 1 \"tx\" \"{signedTx2}\"")
    # tempRes=execute_command(f"{node4} sendmsgtopeer 2 \"tx\" \"{signedTx3}\"")

    # txDs1 = execute_command(f"{node4} sendrawtransaction {signedTx1}")
    # txDs2 = execute_command(f"{node2} sendrawtransaction {signedTx2}")
    # txDs3 = execute_command(f"{node3} sendrawtransaction {signedTx3}")

    # print(f"txDs1={txDs1}")
    # print(f"txDs2={txDs2}")
    # print(f"txDs3={txDs3}")

    # input("Press Enter to check txPs in node1 pool...")
    # res1_1 = execute_command(f"{node1} getmempoolentry {txDs1}")
    # res1_2 = execute_command(f"{node1} getmempoolentry {txDs2}")
    # res1_3 = execute_command(f"{node1} getmempoolentry {txDs3}")
    # print("txP1 in node1:\n", res1_1)
    # print("txP2 in node1:\n", res1_2)
    # print("txP2 in node1:\n", res1_3)

    # input("Press Enter to check txPs in node2 pool...")
    # res2_1 = execute_command(f"{node2} getmempoolentry {txDs1}")
    # res2_2 = execute_command(f"{node2} getmempoolentry {txDs2}")
    # res2_3 = execute_command(f"{node2} getmempoolentry {txDs3}")
    # print("txP1 in node2:\n", res2_1)
    # print("txP2 in node2:\n", res2_2)
    # print("txP3 in node2:\n", res2_3)

    # input("Press Enter to check txPs in node3 pool...")
    # res3_1 = execute_command(f"{node3} getmempoolentry {txDs1}")
    # res3_2 = execute_command(f"{node3} getmempoolentry {txDs2}")
    # res3_3 = execute_command(f"{node3} getmempoolentry {txDs3}")
    # print("txP1 in node3:\n", res3_1)
    # print("txP2 in node3:\n", res3_2)
    # print("txP3 in node3:\n", res3_3)


#     input("Press Enter to send txM...")
#     sumTxM = str(float(amount) - 0.006)
#     rawTxM = execute_command(
#         f"{node1} createrawtransaction '[{{\"txid\":\"{txDs1}\",\"vout\":0}}]' '{{\"bcrt1qjcn96zgy5t44mkmv0n6p48s4y74xkwyc0n6m5g\":{sumTxM}}}'")
#     signedTxM = execute_command(f"{node1} signrawtransactionwithwallet {rawTxM} | awk -F'\"' '/hex/{{print $4}}'")
#     print("signedTxM=", signedTxM)
#     txDsM = execute_command(f"{node1} sendrawtransaction {signedTxM}")
#     print("txDsM=", txDsM)


if __name__ == "__main__":
    main()
