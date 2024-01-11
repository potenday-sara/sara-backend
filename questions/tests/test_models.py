from django.test import TestCase

from answers.models import Answer
from answers.tests.factories import AnswerFactory
from questions.models import AI, Question, QuestionFeedback
from questions.tests.factories import AIFactory, QuestionFactory


class QuestionFeedbackModelTest(TestCase):
    question: Question
    answer: Answer
    ai: AI
    question_feedback: QuestionFeedback

    @classmethod
    def setUpTestData(cls):
        cls.url = "/questions/"
        cls.question = QuestionFactory(type="sara")
        AnswerFactory(question=cls.question, checked=True)
        cls.ai = AIFactory(type="sara")

        cls.question_feedback = QuestionFeedback.objects.create(
            question=cls.question, feedback=1
        )

    def test_str_함수_호출_시(self):
        self.assertEqual(
            self.question_feedback.__str__(), QuestionFeedback.FeedbackType.GOOD.label
        )
