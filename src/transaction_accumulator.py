from transaction_task import TransactionTask
from transaction_queue import TransactionQueue


class TransactionAccumulator:
    def __init__(self):
        self._transaction_queue = TransactionQueue()
        self._accounts = {}

    def addTransaction(self, transaction_task: TransactionTask):
        self._transaction_queue.enqueue(transaction_task)

    def accumulateTransactions(self):
        while (self._transaction_queue.curr != None):
            transaction_task = self._transaction_queue.dequeue()
            sender_uid = transaction_task.get_sender_uid()

            if (self._accounts.get(sender_uid, None) == None):
                # add to dict
                self._accounts[sender_uid] = -1 * transaction_task.get_amount()
            else:
                # update dict
                self._accounts[sender_uid] -= transaction_task.get_amount()

            recipient_uid = transaction_task.get_recipient_uid()
            if (self._accounts.get(recipient_uid, None) == None):
                # add to dict
                self._accounts[recipient_uid] = transaction_task.get_amount()
            else:
                # update dict
                self._accounts[recipient_uid] += transaction_task.get_amount()


if __name__ == "__main__":
    t_accumulator = TransactionAccumulator()
    task1 = TransactionTask(1, 2, 100)
    task2 = TransactionTask(1, 3, 100)
    task3 = TransactionTask(10, 1, 30)
    t_accumulator.addTransaction(task1)
    t_accumulator.addTransaction(task2)
    t_accumulator.addTransaction(task3)
    t_accumulator.addTransaction(task1)
    t_accumulator.accumulateTransactions()
    print(t_accumulator._accounts)
