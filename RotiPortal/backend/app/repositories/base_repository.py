from firebase_admin import firestore
from abc import ABC, abstractmethod

class BaseRepository(ABC):
    def __init__(self):
        # self.db = firestore.Client(project="rotiprata-de9d9")
        self.db = firestore.client()
        self.collection_name = self._get_collection_name()

    @abstractmethod
    def _get_collection_name(self):
        pass
    
    def add(self, data):
        doc_ref = self.db.collection(self.collection_name).add(data)
        return doc_ref[1].id
    
    def get(self, id):
        doc = self.db.collection(self.collection_name).document(id).get()
        return doc.to_dict() if doc.exists else None
    
    def update(self, id, data):
        self.db.collection(self.collection_name).document(id).update(data)

    def delete(self, id):
        self.db.collection(self.collection_name).document(id).delete()

    def get_all(self):
        docs = self.db.collection(self.collection_name).stream()
        # return [doc.to_dict() for doc in docs]
        return [{"Staff_ID": doc.id, **doc.to_dict()} for doc in docs]