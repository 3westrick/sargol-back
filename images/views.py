from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serial import ImageSerializer

class ImageUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)