import hashlib
from datetime import datetime

# ブロック単体のクラス
class Block:
    def __init__(self, account, amount, previousHash):
        self.previousHash = previousHash
        self.account = account
        self.amount = amount
        self.date = datetime.now()
        self.hash = self.calcHash()

    # ハッシュ値を計算する
    def calcHash(self):
        return hashlib.sha256((str(self.previousHash) 
        + str(self.account)
        + str(self.amount)
        + str(self.date)).encode('utf-8')).hexdigest()

    # ブロックの内容をリストに変換する
    def encodeList(self):
        return ["previousHash : " + str(self.previousHash), 
        "account : " + str(self.account),
        "amount : " + str(self.amount),
        "date : " + str(self.date),
        "Hash : "+str(self.hash) ]

# ブロックチェーンのクラス
class BlockChain:
    def __init__(self):
        self.chain = []
        self.chain.append(Block("GenesisBlock", "GenesisBlock", "GenesisBlock"))

    # 取引を追加する
    def addTrade(self, account, amount):
        self.chain.append(Block(account, amount, self.getLatestHash()))

    # 最新のブロックを取得する
    def getLatestHash(self):
        return self.chain[-1].hash

    # ブロックチェーンの内容を表示する
    def printBlockChain(self):
        for i, b in enumerate(self.chain):
            print("Block No." + str(i))
            print(b.encodeList())

if __name__ == "__main__":
    # インスタンス生成
    blockChain = BlockChain()

    # 取引を追加
    while True:
        account = input("input account : ")
        if account == 'quit' or account == '':
            break

        amount = input("input amount : ")
        if amount == 'quit' or amount == '':
            break
        
        print('Add Block!')
        print('')

        blockChain.addTrade(account, amount)

    # ブロック一覧を表示
    print('')
    blockChain.printBlockChain()