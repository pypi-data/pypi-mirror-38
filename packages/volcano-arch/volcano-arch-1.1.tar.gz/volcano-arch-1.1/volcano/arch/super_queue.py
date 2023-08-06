import threading


class SuperQueue:
    capacity = 1000
    tsh_no_priority = 0.7
    tsh_priority = 0.95

    def __init__(self):
        self.queue_ = [None] * self.capacity
        self.size_ = 0
        self.lock_ = threading.Lock()

    def push_one(self, msg, priority: bool) -> bool:
        tsh_pct = self.tsh_priority if priority else self.tsh_no_priority
        tsh_int = int(self.capacity * tsh_pct)

        self.lock_.acquire()
        try:
            if self.size_ >= tsh_int:
                return False
            self.queue_[self.size_] = msg
            self.size_ += 1
        finally:
            self.lock_.release()

    def pop_many(self, max_nb: int = None) -> (tuple, None):
        self.lock_.acquire()
        try:
            nb = min(self.size_, max_nb) if max_nb else self.size_

            if nb == 0:
                return None

            res = tuple(self.queue_[:nb])
            for i in range(nb):
                self.queue_[i] = self.queue_[i + nb]
                self.queue_[i + nb] = None
            self.size_ -= nb

            return res
        finally:
            self.lock_.release()

