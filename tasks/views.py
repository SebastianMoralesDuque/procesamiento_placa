import cv2
import pytesseract
from fuzzywuzzy import fuzz
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import TaskSerializer
from .models import Task
import os

os.environ['TESSDATA_PREFIX'] = 'tesseract-ocr/tessdata'


from django.db.models import Q

def get_similarity(string1, string2):
    similarity_ratio = fuzz.partial_ratio(string1.lower(), string2.lower())
    return similarity_ratio


def process_image(texto_ingresado, imagen_nombre):
    # Obtener la ruta absoluta de la imagen
    image_path = os.path.join(os.getcwd(), 'images', imagen_nombre)
    # Cargar la imagen de la placa
    img = cv2.imread(image_path)

    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicar un filtro Gaussiano para suavizar la imagen
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # Aplicar la binarización adaptativa para resaltar los bordes de la placa
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 2)

    # Encontrar los contornos de la placa
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Seleccionar el contorno más grande (que debería ser la placa)
    if contours:
        contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
        largest_contour = max(contour_sizes, key=lambda x: x[0])[1]

        # Dibujar un rectángulo alrededor de la placa
        x, y, w, h = cv2.boundingRect(largest_contour)
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Recortar la imagen de la placa
        plate_img = gray[y:y+h, x:x+w]

        # Obtener el texto de la placa utilizando Tesseract OCR
        text = pytesseract.image_to_string(plate_img, lang='spa', config='--psm 8 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ -c tessedit_font_size=12 --oem 1').strip()

        precision = get_similarity(text, texto_ingresado)

    return text, precision



class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def create(self, request, *args, **kwargs):
        imagen = request.FILES.get('imagen')
        imagen_nombre = str(imagen.name)
        texto_ingresado = request.data.get('texto_ingresado')
        texto_ingresado = texto_ingresado.upper()
        # Guarda los datos iniciales en tu modelo de Django
        objeto = Task(imagen=imagen, texto_generado="", texto_ingresado=texto_ingresado, precision=0)
        objeto.save()

        text, precision = process_image(texto_ingresado, imagen_nombre)

        # Obtén los nuevos datos que deseas actualizar
        nuevo_texto_generado = text
        nueva_precision = precision

        # Actualiza los campos del objeto
        objeto.texto_generado = nuevo_texto_generado
        objeto.precision = nueva_precision

        # Guarda el objeto actualizado en la base de datos
        objeto.save()

        serializer = self.get_serializer(objeto)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        imagen = request.FILES.get('imagen')
        imagen_nombre = str(imagen.name)
        texto_ingresado = request.data.get('texto_ingresado')
        texto_ingresado = texto_ingresado.upper()

        # Obtener el objeto existente
        instance = self.get_object()

        # Actualizar los campos del objeto
        instance.texto_ingresado = texto_ingresado
        instance.imagen = imagen

        # Guardar el objeto en la base de datos
        instance.save()

        # Procesar la imagen y actualizar los campos adicionales
        instance.texto_generado, instance.precision = process_image(texto_ingresado, imagen_nombre)
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
