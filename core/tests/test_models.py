from django.test import TestCase

from questions.models import Question
from questions.tests.factories import QuestionFactory


class CommonModel_테스트(TestCase):
    def setUp(self):
        self.obj1 = QuestionFactory()
        self.obj2 = QuestionFactory()

    def test_soft_delete(self):
        self.obj1.delete()
        self.assertIsNotNone(self.obj1.deleted_at)
        self.assertFalse(Question.objects.filter(pk=self.obj1.pk).exists())

    def test_hard_delete(self):
        obj_id = self.obj2.id
        self.obj2.hard_delete()
        self.assertFalse(Question.objects.all().filter(id=obj_id).exists())
        self.assertFalse(Question.all_objects.all().active().filter(id=obj_id).exists())

    def test_restore(self):
        self.obj1.restore()
        self.assertIsNone(self.obj1.deleted_at)
        self.assertTrue(
            Question.objects.all().active().filter(id=self.obj1.id).exists()
        )
