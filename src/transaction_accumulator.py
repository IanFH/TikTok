from transaction_task import TransactionTask
from transaction_queue import TransactionQueue
from database_handler import DatabaseHandler
import psycopg
import datetime


class TransactionAccumulator:
    def __init__(self):
        self._transaction_queue = TransactionQueue()
        self._accounts = {}
        self._transaction_history = []
        self._MAX_PER_UPDATE = 100
        self._used_transaction_session_ids = set() # generated by Stripe
        self._MAIN_POOL_ID = -1
        self._curr_tasks = []

    def _add_transaction(self, transaction_task: TransactionTask):
        self._transaction_queue.enqueue(transaction_task)

    def add_topup_task(self, uid: int, amount: float, transaction_session_id: str):
        if transaction_session_id not in self._used_transaction_session_ids:
            self._used_transaction_session_ids.add(transaction_session_id)
            curr_date = datetime.datetime.now()
            self._add_transaction(TransactionTask(self._MAIN_POOL_ID, uid, amount, curr_date))
            return True
        return False

    def add_transfer_task(self, transaction_task: TransactionTask):
        self._add_transaction(transaction_task)

    def _accumulate_transactions(self):
        cnt = 0
        while self._transaction_queue.curr is not None and cnt < self._MAX_PER_UPDATE:
            transaction_task = self._transaction_queue.dequeue()
            print(transaction_task)
            self._curr_tasks.append(transaction_task)
            sender_uid = transaction_task.get_sender_uid()

            if sender_uid != self._MAIN_POOL_ID:
                if self._accounts.get(sender_uid, None) is None:
                    # add to dict
                    self._accounts[sender_uid] = -1 * transaction_task.get_amount()
                else:
                    # update dict
                    self._accounts[sender_uid] -= transaction_task.get_amount()

            recipient_uid = transaction_task.get_recipient_uid()
            if self._accounts.get(recipient_uid, None) is None:
                # add to dict
                self._accounts[recipient_uid] = transaction_task.get_amount()
            else:
                # update dict
                self._accounts[recipient_uid] += transaction_task.get_amount()
            
            self._transaction_history.append(transaction_task.to_row())
            cnt += 1
    
    def _process_accounts(self):
        return [
            (amount, uid) for uid, amount in self._accounts.items()
        ]

    def process_transaction_tasks(self, 
                                  db_handler: DatabaseHandler, 
                                  failsafe_accumulator):
        print(f"PROCESSING TRANSACTION ACCUM")
        self._accumulate_transactions()
        if len(self._accounts) > 0:
            entries = self._process_accounts()
            try:
                db_handler.bulk_update_balance(entries)
            except psycopg.errors.Error:
                failsafe_accumulator.add_task(self._curr_tasks)
            try:
                db_handler.bulk_insert_transactions(self._transaction_history)
            except psycopg.errors.Error:
                failsafe_accumulator.add_task(self._curr_tasks)
            self._accounts = {}
            self._transaction_history = []
    
    def clear_used_transaction_session_ids(self):
        print("CLEARING USED TRANSACTION SESSION IDS")
        self._used_transaction_session_ids = set()


class FailsafeAccumulator:
    def __init__(self):
        self._transaction_queue = TransactionQueue()
        self._accounts = {}
        self._transaction_history = []
        self._MAX_PER_UPDATE = 100
        self._MAIN_POOL_ID = -1
        self._failed_tasks = []

    def add_task(self, transaction_task: TransactionTask):
        self._transaction_queue.enqueue(transaction_task)

    def process_transaction_tasks_seq(self, db_handler: DatabaseHandler):
        print("RUNNING FAILSAFE")
        cnt = 0
        while self._transaction_queue.curr is not None and cnt < self._MAX_PER_UPDATE:
            print("FOUND ISSUE, SOLVING")
            transaction_task = self._transaction_queue.dequeue()
            sender_uid = transaction_task.get_sender_uid()
            recipient_uid = transaction_task.get_recipient_uid()
            amount = transaction_task.get_amount()
            if transaction_task.get_sender_update_success():
                entry = (recipient_uid, amount)
                try:
                    db_handler.update_balance(entry)
                    transaction_task.set_recipient_update_success(True)
                except psycopg.DatabaseError:
                    self._failed_tasks.append(transaction_task)
            if transaction_task.get_recipient_update_success():
                entry = (sender_uid, -1 * amount)
                try:
                    db_handler.update_balance(entry)
                    transaction_task.set_sender_update_success(True)
                except psycopg.DatabaseError:
                    self._failed_tasks.append(transaction_task)
            if not transaction_task.get_transaction_history_update_success():
                try:
                    db_handler.insert_transaction(transaction_task.to_row())
                    transaction_task.set_transaction_history_update_success(True)
                except psycopg.DatabaseError:
                    self._failed_tasks.append(transaction_task)
            cnt += 1
        for task in self._failed_tasks:
            self._add_transaction(task)
    
    def clear_used_transaction_session_ids(self):
        self._used_transaction_session_ids = set()


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
