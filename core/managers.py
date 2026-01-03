from django.db.models.query import QuerySet
from django.db.models import Manager
from django.utils import timezone

class SoftDeleteQueryset(QuerySet):
    def only_deleted(self):
        return self.filter(is_deleted=True)
    
    def not_deleted(self):
        return self.filter(is_deleted=False)
    
    def soft_delete(self):
        return self.update(is_deleted=True, deleted_date=timezone.now())
    
    def restore(self):
        return self.update(is_delete=False, deleted_date=None)
    
class SoftDeleteOnlyQuerySet(SoftDeleteQueryset):
    def delete(self):
        return self.update(is_delete=True, deleted_date=timezone.now())


class SoftDeleteManager(Manager):
    queryset = SoftDeleteQueryset

    def get_queryset(self):
        return self.queryset(self.model, using=self._db).not_deleted()
    
    def only_deleted(self):
        return self.queryset(self.model, using=self._db).only_deleted()

    def with_deleted(self): 
        return self.queryset(self.model, using=self._db)
    
class SoftDeleteOnlyManager(SoftDeleteManager):
    queryset=SoftDeleteOnlyQuerySet
