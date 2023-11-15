from django.db import connections
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from status.exceptions import StatusCheckException


class StatusViewSet(ViewSet):
    @action(methods=["GET"], detail=False, url_path="health")
    def health_check(self, request):
        del request
        return Response(
            status=status.HTTP_200_OK,
        )

    @action(methods=["GET"], detail=False, url_path="stand-by")
    def stand_by_check(self, request):
        try:
            self._db_health_check()

        except Exception as e:  # pylint: disable=broad-except
            return Response(
                str(e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def _db_health_check():
        for alias in connections.databases.keys():
            with connections[alias].cursor() as cursor:
                cursor.execute("select 1")
                one = cursor.fetchone()[0]
                if one != 1:
                    raise StatusCheckException(f"{alias} database connection error")
