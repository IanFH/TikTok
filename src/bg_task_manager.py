from apscheduler.schedulers.background import BackgroundScheduler
from transaction_accumulator import TransactionAccumulator, FailsafeAccumulator
from database_handler import DatabaseHandler


class BgTaskManager:

    def __init__(self, 
                 transaction_accumulator: TransactionAccumulator, 
                 failsafe_accumulator: FailsafeAccumulator,
                 database_handler: DatabaseHandler):
        self.background_scheduler = BackgroundScheduler()
        self.transaction_accumulator = transaction_accumulator
        self.failsafe_accumulator = failsafe_accumulator
        self.database_handler = database_handler
        self.add_bulk_update_transaction_job()
        self.add_update_used_transaction_session_id_job()
        self.add_failsafe_job()

    def start(self):
        self.background_scheduler.start()

    def stop(self):
        self.background_scheduler.shutdown()

    def _add_job(self, func, trigger, seconds, args):
        self.background_scheduler.add_job(func, trigger, seconds=seconds, args=args)

    def add_bulk_update_transaction_job(self, ):
        self._add_job(self.transaction_accumulator.process_transaction_tasks,
                      'interval',
                      seconds=60,
                      args=(self.database_handler, self.failsafe_accumulator))
        
    def add_update_used_transaction_session_id_job(self):
        self._add_job(self.transaction_accumulator.clear_used_transaction_session_ids,
                      'interval',
                      seconds=300,
                      args=())
        
    def add_failsafe_job(self):
        self._add_job(self.failsafe_accumulator.process_transaction_tasks_seq,
                      'interval',
                      seconds=300,
                      args=(self.database_handler, ))
        
    def add_registration_check_job(self):
        # TODO: Implement this (Joseph)
        pass