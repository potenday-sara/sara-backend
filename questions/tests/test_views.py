from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from answers.models import Answer
from answers.tests.factories import AnswerFactory
from questions.consts import QUESTION_LIST_MAX_LENGTH
from questions.models import Comment, Feedback, Like, Question, QuestionFeedback
from questions.tests.factories import AIFactory, QuestionFactory


class QuestionsView_테스트(TestCase):
    client_class = APIClient

    @classmethod
    def setUpTestData(cls):
        cls.url = "/questions/"
        cls.question_list: list[Question] = QuestionFactory.create_batch(
            50, type="sara"
        )
        for question in cls.question_list:
            AnswerFactory(question=question, checked=True)
        cls.ai = AIFactory(type="sara")

    def test_questions_조회_요청_성공_시(self):
        self.question_list[0].hidden = True
        self.question_list[0].save()

        response = self.client.get(self.url)
        response_data = response.json()

        with self.subTest("status code 200이 리턴된다."):
            self.assertEqual(response.status_code, 200)
        with self.subTest("질문 목록이 리턴된다."):
            self.assertTrue(len(self.question_list) >= 1)
        with self.subTest("히든 처리된 질문은 제외된다."):
            self.assertNotIn(
                self.question_list[0].id,
                map(lambda x: x["id"], response_data["results"]),
            )
        with self.subTest("답변이 체크된 질문만 리턴된다."):
            self.assertTrue(
                all(
                    map(
                        lambda x: Answer.objects.get(question_id=x["id"]).checked,
                        response_data["results"],
                    )
                )
            )
        with self.subTest("전달한 order에 따라 정렬된다."):
            self.question_list[-1].like_count = 100
            self.question_list[-1].save()
            response = self.client.get(self.url, data={"order": "like"})
            response_data = response.json()
            most_popular_question_like_count = (
                max(map(lambda x: x["like_count"], response_data["results"])),
            )[0]
            self.assertEqual(
                response_data["results"][0]["like_count"],
                most_popular_question_like_count,
            )

            response = self.client.get(self.url, data={"order": "time"})
            response_data = response.json()
            last_created_question_date = (
                max(map(lambda x: x["created_at"], response_data["results"])),
            )[0]
            self.assertEqual(
                response_data["results"][0]["created_at"],
                last_created_question_date,
            )

        with self.subTest("전달한 AI type에 따라 필터링된다."):
            response = self.client.get(self.url, data={"type": self.ai.type})
            response_data = response.json()
            self.assertTrue(
                all(
                    map(
                        lambda x: x["type"] == self.ai.type,
                        response_data["results"],
                    )
                )
            )

            response = self.client.get(self.url, data={"type": "mara"})
            response_data = response.json()
            self.assertEqual(len(response_data["results"]), 0)

    def test_questions_random_조회_요청_성공_시(self):
        self.question_list[0].hidden = True
        self.question_list[0].save()

        response = self.client.get(self.url + "random/")

        with self.subTest("status code 200이 리턴된다."):
            self.assertEqual(response.status_code, 200)
        with self.subTest("질문 목록이 리턴된다."):
            self.assertTrue(len(self.question_list) >= 1)
        with self.subTest("히든 처리된 질문은 제외된다."):
            self.assertNotIn(
                self.question_list[0].id, map(lambda x: x["id"], response.data)
            )
        with self.subTest("답변이 체크된 질문만 리턴된다."):
            self.assertTrue(
                all(
                    map(
                        lambda x: Answer.objects.get(question_id=x["id"]).checked,
                        response.data,
                    )
                )
            )
        with self.subTest("설정된 최대 개수를 넘지 않는다."):
            self.assertTrue(len(response.data) <= QUESTION_LIST_MAX_LENGTH)

    @patch("questions.views.task_get_answer")
    def test_question_등록_요청_성공_시(self, mock_producer):
        mock_producer.return_value.produce.return_value = None
        data = {
            "type": "sara",
            "product": "테스트 상품",
            "content": "테스트 질문",
        }
        response = self.client.post(self.url, data=data)

        with self.subTest("status code 201이 리턴된다."):
            self.assertEqual(response.status_code, 201)
        with self.subTest("질문이 생성된다."):
            self.assertEqual(response.data["product"], data["product"])
            self.assertEqual(response.data["content"], data["content"])
            self.assertEqual(response.data["type"], data["type"])

    def test_questions_feedback_요청_성공_시(self):
        response = self.client.post(
            self.url + f"{self.question_list[0].id}" + "/feedback/",
            data={"feedback": "1", "question": self.question_list[0].id},
        )
        with self.subTest("status code 201이 리턴된다."):
            self.assertEqual(response.status_code, 201)
        with self.subTest("questions feedback 데이터가 생성된다"):
            QuestionFeedback.objects.get(question=self.question_list[0], feedback="1")

    def test_question_cs_요청_성공_시(self):
        response = self.client.post(
            self.url + f"{self.question_list[0].id}" + "/cs/",
            data={"content": "test", "question": self.question_list[0].id},
        )
        with self.subTest("status code 201이 리턴된다."):
            self.assertEqual(response.status_code, 201)

        with self.subTest("feedback 데이터가 생성된다"):
            self.assertEqual(Feedback.objects.count(), 1)

    def test_comments_조회_요청_성공_시(self):
        Comment.objects.create(
            question=self.question_list[0], content="test", nickname="test"
        )

        response = self.client.get(
            self.url + f"{self.question_list[0].id}" + "/comments/"
        )
        with self.subTest("status code 200이 리턴된다."):
            self.assertEqual(response.status_code, 200)
        with self.subTest("comments 데이터가 리턴된다"):
            self.assertTrue(len(response.data) >= 1)

    def test_comments_등록_요청_성공_시(self):
        response = self.client.post(
            self.url + f"{self.question_list[0].id}" + "/comments/",
            data={
                "content": "test",
                "nickname": "test",
            },
        )
        with self.subTest("status code 201이 리턴된다."):
            self.assertEqual(response.status_code, 201)
        with self.subTest("comments 데이터가 생성된다"):
            self.assertEqual(
                Comment.objects.filter(question=self.question_list[0]).count(), 1
            )

    def test_like_요청_성공_시(self):
        response = self.client.post(self.url + f"{self.question_list[0].id}" + "/like/")
        with self.subTest("status code 201이 리턴된다."):
            self.assertEqual(response.status_code, 201)
        with self.subTest("like 데이터가 생성된다"):
            self.assertEqual(
                Like.objects.filter(question=self.question_list[0]).count(), 1
            )

    def test_like_제거_요청_성공_시(self):
        Like.objects.create(question=self.question_list[0])

        response = self.client.delete(
            self.url + f"{self.question_list[0].id}" + "/like/",
            data={"question": self.question_list[0].id},
        )
        with self.subTest("status code 204가 리턴된다."):
            self.assertEqual(response.status_code, 204)
        with self.subTest("like 데이터가 제거된다"):
            self.assertEqual(
                Like.objects.filter(question=self.question_list[0]).count(), 0
            )
