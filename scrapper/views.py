from .serializers import ScrapperSerializer
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ScrapperSerializer
from django.shortcuts import render
from django.views.generic import TemplateView
from .selenium_manager import task_queue, start_worker
from .utils import search_by_cpf
import json, threading


class ScrapperView(APIView):
    serializer_class = ScrapperSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        cpf = serializer.validated_data["cpf"]

        # garante que o worker está rodando
        start_worker()

        event = threading.Event()
        response_holder = {}

        def callback(resultado, erro):
            response_holder["resultado"] = resultado
            response_holder["erro"] = erro
            event.set()

        # envia para a fila
        task_queue.put((cpf, callback))

        # aguarda o worker finalizar
        event.wait()

        if response_holder.get("erro"):
            return Response(
                {"erro": str(response_holder["erro"])},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            data=response_holder["resultado"],
            status=status.HTTP_200_OK
        )



class ScrapperTemplateView(TemplateView):
    template_name = "scrapper.html"

