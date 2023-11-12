import uuid

from django.db import models
from django.utils import timezone

from core.managers import ActiveManager, BaseManager


class CommonModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = ActiveManager()
    all_objects = BaseManager()

    class Meta:
        abstract = True
        default_manager_name = "objects"

    def delete(self, using=None, keep_parents=False):
        """
        Soft Delete. deleted_at 레코드를 현재시각으로 변경
        """
        del keep_parents
        self.deleted_at = timezone.now()
        self.save(using=using)

    def hard_delete(self, using=None, keep_parents=False):
        """
        Hard Delete. Row 자체를 삭제함.
        """
        super().delete(using=using, keep_parents=keep_parents)

    def restore(self, using=None):
        """
        Restore. deleted_at 을 None 으로 변경하여 soft delete 되었던 row 를 복원함
        """
        self.deleted_at = None
        self.save(using=using)
