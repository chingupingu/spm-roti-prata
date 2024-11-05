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
    
    def get_by_other_id(self, field: str, value: int):
        query = self.db.collection(self.collection_name).where(field, "==", value).limit(1)
        results = query.stream()
        for doc in results:
            return {"doc_id": doc.id, **doc.to_dict()}  # Include doc_id in the result
        return None
    
    def update(self, id, data):
        self.db.collection(self.collection_name).document(id).update(data)

    def update_by_other_id(self, field: str, value: int, data: dict):
        query = self.db.collection(self.collection_name).where(field, "==", value).limit(1)
        results = query.stream()
        for doc in results:
            self.db.collection(self.collection_name).document(doc.id).update(data)  # {{ edit_1 }}
            return True
        return False

    def delete(self, id):
        self.db.collection(self.collection_name).document(id).delete()

    def get_all(self):
        docs = self.db.collection(self.collection_name).stream()
        # return [doc.to_dict() for doc in docs]
        return [{"doc_id": doc.id, **doc.to_dict()} for doc in docs]
    
    # def validate(self, data):
    #     return self.db.collection(self.collection_name).where( '==', data.Email).get()
