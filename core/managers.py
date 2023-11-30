from django.core.exceptions import ObjectDoesNotExist
from django.db import models, transaction
from django.db.models import QuerySet
from django.utils import timezone
from rest_framework.exceptions import NotFound


class SoftDeleteQuerySet(QuerySet):
    def hard_delete(self):
        return super().delete()

    def delete(self, *args, **kwargs):
        # 삭제되기 전의 객체 리스트를 저장합니다.
        deleted = list(self)

        # 트랜잭션 블록 시작
        with transaction.atomic():
            # 현재 QuerySet 내의 모든 객체들에 대해 연관된 객체들을 찾아내기
            for obj in self:
                # 모든 관련 객체 필드를 순회
                for rel in obj._meta.get_fields():
                    # 외래 키 역관계에 대해서만 처리
                    if rel.one_to_many or rel.one_to_one and not rel.auto_created:
                        # related_name을 통해 연결된 QuerySet을 가져옵니다.
                        related_query_set = getattr(obj, rel.get_accessor_name()).all()
                        # 연관된 객체들을 소프트 삭제합니다.
                        related_query_set.update(deleted_at=timezone.now())

            # 현재 QuerySet의 객체들을 소프트 삭제
            self.update(deleted_at=timezone.now())

        # 삭제된 객체 리스트와 함께 deactivate 메소드의 결과(True)를 반환합니다.
        return deleted, True

    def deactivate(self):
        # 이 메소드는 각 객체의 상태를 비활성화 상태로 변경합니다.
        # 이 부분은 update()를 호출하여 일괄 처리합니다.
        return self.update(deleted_at=timezone.now())

    def active(self):
        # 삭제되지 않은 객체만 필터링
        return self.filter(deleted_at__isnull=True)


class RestoreQuerySet(QuerySet):
    def hard_delete(self):
        return self.delete()

    def restore(self):
        restored = list(self)
        return restored, self.activate()

    def activate(self):
        return self.update(deleted_at=None)

    def deleted(self):
        return self.filter(deleted_at__isnull=False)

    def active(self):
        # 삭제되지 않은 객체만 필터링
        return self.filter(deleted_at__isnull=True)


class BaseManager(models.Manager):
    def get_queryset(self):
        return RestoreQuerySet(model=self.model, using=self._db, hints=self._hints)

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    def get_or_raise_not_found(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist as e:
            raise NotFound() from e


class ActiveManager(BaseManager):
    def get_queryset(self):
        return SoftDeleteQuerySet(
            model=self.model, using=self._db, hints=self._hints
        ).active()
