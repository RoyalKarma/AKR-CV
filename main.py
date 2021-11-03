from hashlib import sha256
import time
import json


def is_chain_valid():
    for block in blockchain:

        if block.hash != block.hash_func:
            print("not match")
            return False
        else:
            print("match")
            return True


class Wallet:
    def __init__(self, name):
        self.name: str = name
        self.UTXOs: list = []

    def send_funds(self, recipient, value: float):
        blockchain.append(
            Block(Transaction(self, recipient, value), "0" if len(blockchain) == 0 else blockchain[-1].hash))

    @property
    def total(self) -> float:
        total: float = 0
        for i in range(len(self.UTXOs)):
            total += self.UTXOs[i].value

        return total


class Transaction:
    outputs: list = []

    def __init__(self, sender, recipient, value: float):
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.inputs = sender.UTXOs
        self.id = self.calculate_hash

        self.process_transaction()

    def calculate_hash(self):
        return str(sha256((self.sender + self.recipient + self.value).encode('utf-8')).hexdigest())

    def process_transaction(self) -> bool:
        if self.value > self.sender.total:
            return False

        total: float = 0
        while True:
            total += self.inputs.pop().value

            if total >= self.value:
                break

        leftover: float = total - self.value

        self.sender.UTXOs.append(TransactionOutput(self.sender, leftover, str(self.id)))
        self.recipient.UTXOs.append(TransactionOutput(self.recipient, self.value, str(self.id)))

        return True


class TransactionOutput:
    def __init__(self, sender: Wallet, value: float, parentTransactionId: str):
        self.sender = sender
        self.value = value
        self.parentTransactionId = parentTransactionId
        self.id = self.calculate_hash

    @property
    def calculate_hash(self):
        return str(
            sha256((self.sender.name + str(self.value) + str(self.parentTransactionId)).encode('utf-8')).hexdigest())


class TransactionInput:
    UTXO: TransactionOutput = None

    def __init__(self, transactionOutputId: str, ):
        self.transactionOutputId = transactionOutputId


class Block:

    @property
    def hash_func(self):
        return str(
            sha256((str(self.transaction.value) + self.previousHash + self.timestamp).encode('utf-8')).hexdigest())

    def hash_func_nonce(self, nonce):
        return str(sha256((str(self.transaction.value) + self.previousHash + self.timestamp + str(nonce)).encode(
            'utf-8')).hexdigest())

    def __init__(self, transaction, previousHash):
        self.previousHash: str = previousHash
        self.transaction: Transaction = transaction
        self.timestamp: str = time.asctime()
        self.hash: str = self.mine_block()

    def mine_block(self):
        difficulty = 4
        nonce = 0
        num_of_zeros = difficulty * "0"

        while True:
            hash_with_nonce = self.hash_func_nonce(nonce)

            if not hash_with_nonce.startswith(num_of_zeros):
                nonce += 1
            else:
                print(hash_with_nonce)

                return hash_with_nonce

    def changeBlock(self):
        self.transaction = "new transaction."
        return self


if __name__ == '__main__':
    change = False

    blockchain = []

    walletA = Wallet("alice")
    walletB = Wallet("bob")

    walletA.UTXOs.append(TransactionOutput(walletA, 1000, "Gift from God"))

    print(f'Současná bilance: {walletA.total}')
    print(f'Současná bilance: {walletB.total}')

    walletA.send_funds(walletB, 10)

    print(f'Současná bilance: {walletA.total}')
    print(f'Současná bilance: {walletB.total}')

    """blockchain.append(Block("blok jedna", "0"))
    print("vytezen 1")
    if change:
        blockchain.append(Block("blok dva.", blockchain[0].hash).changeBlock())
        is_chain_valid()
    else:
        blockchain.append(Block("blok dva.", blockchain[0].hash))
    print("vytezen 2")
    blockchain.append(Block("blok 3", blockchain[1].hash))
    print("vytezen 3")
"""
    for block in blockchain:
        with open("data.json", "w") as outfile:
            json.dump([block.__dict__ for block in blockchain], fp=outfile, default=lambda o: "object-non-serializable",
                      indent=4)
