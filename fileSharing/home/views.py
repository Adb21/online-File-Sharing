from telnetlib import STATUS
from django.shortcuts import render
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from home.serializer import FileListSerializer
from django.views import View
 
# Create your views here.

class FileUpload(APIView):
    parser_classes = [MultiPartParser]
    def post(self,request):
        try :
            data = request.data
            serializer = FileListSerializer(data=data)    
            if serializer.is_valid():
                serializer.save()

                return Response(
                    {
                        'message':"Files Uploaded Successfully",
                        'data':serializer.data
                    },status=status.HTTP_200_OK
                )
            return Response({"Error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)

class HomePageView(View):

    def get(self,request):
        return render(request,'home.html')

class DownloadPageView(View):

    def get(self,request,uid):
        return render(request,'download.html',context={"uid":uid})