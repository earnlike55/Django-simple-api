from warnings import catch_warnings
from django.http import JsonResponse
from .models import School, Student
from .serializers import SchoolSerializer, StudentPostSerializer, StudentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import uuid


@api_view(['GET','POST'])
def student_list(request):

    if request.method == 'GET': 
        student = Student.objects.all()
        serializer = StudentSerializer(student,many = True)
        return JsonResponse(serializer.data,safe = False)

    if request.method == 'POST':
       
        serializer = StudentSerializer(data=request.data)
        if(not serializer.is_valid()):
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        schoolId = serializer.validated_data['school'].id
        try: 
            school = School.objects.get(id=schoolId)
            studentCount = Student.objects.filter(school=school).count()
        
            if( studentCount < school.maxStudent):
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST,data="This school already full")

        except School.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND,data = "School not found")
        
        

@api_view(['GET','POST'])
def school_list(request):

    if request.method == 'GET':
        school = School.objects.all()
        serializer = SchoolSerializer(school,many = True)
        return JsonResponse(serializer.data,safe = False)
    
    if(request.method == 'POST'):
        serializer = SchoolSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
       
       
        
        

@api_view(['GET','PUT','DELETE'])
def  getStudentbyId(request,id):
    try:
        student = Student.objects.get(pk=id)
        
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET' :
        serializers = StudentSerializer(student)
        return JsonResponse(serializers.data,safe = False)
    elif request.method == 'PUT':
        serializers = StudentSerializer(student,data=request.data)
        if(serializers.is_valid()):
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.error, status = status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['GET','PUT','DELETE'])
def  getSchoolbyId(request,id):
    try:
        school = School.objects.get(pk=id)
    except School.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET' :
        serializers = School(school)
        return JsonResponse(serializers.data,safe = False)
    elif request.method == 'PUT':
        serializers = SchoolSerializer(school,data=request.data)
        if(serializers.is_valid()):
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.error, status = status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        school.delete()
        return Response(status=status.HTTP_200_OK)