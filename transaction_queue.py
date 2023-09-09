from transaction_task import TransactionTask


class Node:
    def __init__(self, val: TransactionTask, next):
        self.val = val
        self.next = next

    def attachNext(self, node):
        self.next = node

    def getNext(self):
        return self.next

    def getVal(self):
        return self.val


class TransactionQueue:
    def __init__(self):
        self.curr = None
        self.last = None
        self.limit = 10  # limit of transaction tasks in the queue

    def enqueue(self, transaction_task: TransactionTask):
        if (self.curr == None):
            self.curr = Node(transaction_task, None)
            self.last = self.curr
        else:
            newNode = Node(transaction_task, None)
            self.last.attachNext(newNode)
            self.last = newNode

    def dequeue(self):
        if (self.curr == None):
            print("Queue is empty")
        else:
            result = self.curr.getVal()
            self.curr = self.curr.getNext()
            return result
