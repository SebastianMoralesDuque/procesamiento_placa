from rest_framework import viewsets
from .serializer import TaskSerializer
from .models import Task
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

class YourView(APIView):
    def post(self, request, format=None):
        texto_ingresado = request.POST.get('texto_ingresado')

        # Realizar las operaciones necesarias para generar el texto deseado
        texto_generado = "Texto generado"  # Reemplazar con la lógica de generación de texto que corresponda

        # Guardar el texto ingresado y el texto generado en tu modelo de Django
        objeto = Task(texto_ingresado=texto_ingresado, texto_generado=texto_generado)
        objeto.save()
        print("hola")
        return Response(status=200)



