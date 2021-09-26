import json
from typing import Optional
from dataclasses import dataclass, asdict
from hashlib import sha256
from time import time

@dataclass
class Transaction:
    sender: str
    recipient: str
    amount: float

@dataclass
class Block:
    index: int
    timestamp: float
    transactions: list[Transaction]
    proof_of_work: int
    prev_block_hash: str

class Blockchain:
    def __init__(self):
        self.chain: list[Block] = []
        self.current_transactions: list[Transaction] = []
        self.new_block(0, '0')

    def new_block(
        self, 
        proof_of_work,
        prev_block_hash=None
    ) -> None:
        '''Creates a new block and add it to the chain.'''
        # create new block and reset current transactions
        block = Block(
            index=len(self.chain) + 1,
            timestamp=time(),
            transactions=self.current_transactions,
            proof_of_work=proof_of_work,
            prev_block_hash=prev_block_hash or self.hash(self.last_block)
        )
        self.current_transactions = []

        # append new block to chain and return it
        self.chain.append(block)
        return block

    def new_transaction(self, transaction: Transaction) -> int:
        '''
        Add a new transction to list of current transactions.
        Returns index of block that will hold this transaction.
        '''
        self.current_transactions.append(transaction)
        return len(self.chain) + 1

    
    def hash(self, block: Block) -> str:
        '''Get SHA256 hash of a block.'''
        serialized:str  = json.dumps(
            asdict(block),
            sort_keys=True
        )
        return sha256(serialized).hexdigest()

    @property
    def last_block(self) -> Block:
        '''Returns last block in the chain.'''
        # there will always be at least 1 block (genesis block)
        return self.chain[-1]

    def proof_of_work(self) -> int:
        '''
        Proof of work algorithm which finds a value x such that
        hash(prev_hash + previous_proof + x) starts with 3 0s
        '''
        last_proof = self.last_block.proof_of_work
        prev_hash = self.hash(self.last_block)
        proof = 0

        # brute force search for valid proof of work
        while not self.is_valid_proof(proof, last_proof, prev_hash):
            proof += 1
        return proof

    def is_valid_proof(
        self, 
        proof: int, 
        last_proof: int, 
        prev_hash: str
    ) -> bool:
        '''
        Validates the proof of work:
        
        hash(prev_block_hash + last_block_proof + curr_block_proof)

        must start with 3 0s
        '''
        guess_str = f'{prev_hash}{last_proof}{proof}'.encode()
        guess_hash = sha256(guess_str).hexdigest()
        return guess_hash[:3] == '000'
        
        