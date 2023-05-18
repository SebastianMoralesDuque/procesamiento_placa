import cv2
import pytesseract
from fuzzywuzzy import fuzz
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializer import TaskSerializer
from .models import Task
import os
from fuzzywuzzy import fuzz
os.environ['TESSDATA_PREFIX'] = 'tesseract-ocr/tessdata'

from pytesseract import pytesseract

def get_similarity(string1, string2):
    similarity_ratio = fuzz.ratio(string1.lower(), string2.lower()) / 100
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
        # Obtener el resultado correcto del usuario y calcular la precisión
        print(text)
        print(texto_ingresado)

        precision = get_similarity(text,texto_ingresado);

    return text, precision



class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def create(self, request, *args, **kwargs):
        imagen = request.FILES.get('imagen')
        imagen_nombre = str(imagen.name)
        texto_ingresado = request.data.get('texto_ingresado')
        text, precision = process_image(texto_ingresado,imagen_nombre)

        # Guarda los datos en tu modelo de Django
        objeto = Task(imagen=imagen, texto_generado=text, texto_ingresado=texto_ingresado, precision=precision)
        objeto.save()

        serializer = self.get_serializer(objeto)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)





