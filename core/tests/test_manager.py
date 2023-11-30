from django.test import TestCase
from rest_framework.exceptions import NotFound

from questions.models import Question
from questions.tests.factories import QuestionFactory


class SoftDeleteQuerySet_테스트(TestCase):
    def setUp(self):
        self.obj1 = QuestionFactory()
        self.obj2 = QuestionFactory()

    def test_soft_delete(self):
        Question.objects.all().delete()
        self.assertEqual(Question.all_objects.all().deleted().count(), 2)
        self.assertEqual(Question.all_objects.all().active().count(), 0)

    def test_hard_delete(self):
        Question.objects.all().hard_delete()
        self.assertEqual(Question.all_objects.all().deleted().count(), 0)

    def test_deactivate(self):
        Question.objects.all().deactivate()
        self.assertEqual(Question.all_objects.all().active().count(), 0)

    def test_active(self):
        self.assertEqual(Question.objects.all().active().count(), 2)


class RestoreQuerySet_테스트(TestCase):
    def setUp(self):
        self.obj1 = QuestionFactory()
        self.obj2 = QuestionFactory()
        Question.objects.all().delete()

    def test_hard_delete(self):
        Question.all_objects.all().hard_delete()
        self.assertEqual(Question.all_objects.all().deleted().count(), 0)

    def test_restore(self):
        Question.all_objects.all().deleted().restore()
        self.assertEqual(Question.all_objects.all().active().count(), 2)

    def test_activate(self):
        Question.all_objects.all().deleted().activate()
        self.assertEqual(Question.all_objects.all().active().count(), 2)

    def test_deleted(self):
        self.assertEqual(Question.all_objects.all().deleted().count(), 2)


class BaseManager_테스트(TestCase):
    def test_get_or_none(self):
        self.assertIsNotNone(Question.all_objects.get_or_none(pk=QuestionFactory().pk))
        self.assertIsNone(Question.all_objects.get_or_none(pk=9999))

    def test_get_or_raise_not_found(self):
        with self.assertRaises(NotFound):
            Question.all_objects.get_or_raise_not_found(pk=9999)


class ActiveManager_테스트(TestCase):
    def setUp(self):
        self.obj1 = QuestionFactory()
        self.obj2 = QuestionFactory()
        Question.objects.all().delete()

    def test_active_queryset(self):
        self.assertEqual(Question.objects.all().count(), 0)
