from abc import ABC


class BaseService(ABC):
    def __init__(self, db):
        self.db = db
