from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .serializers import *
from .models import Trip
from api.models import *
from api.serializers import *
from review.models import Review
import datetime

from rest_framework import viewsets

# Create your views here.
@api_view(['GET'])
def trip_list(request):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y%m%d')
    trips = Trip.objects.filter(user=user, date__gte=int(nowDate)).order_by('date')
    serializer = TripListSerializer(trips, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def checkID(request, name):
    User = get_user_model()
    user = User.objects.filter(username=name)
    minFlag = maxFlag = numFlag = False
    if len(name) < 5:
        minFlag = True
    if len(name) >= 16:
        maxFlag = True
    try:
        int(name)
        numFlag = True
    except:
        pass
    
    if user:
        return HttpResponse('이미 있는 아이디입니다.')
    elif minFlag:
        return HttpResponse('아이디가 너무 짧습니다.')
    elif maxFlag:
        return HttpResponse('아이디가 너무 깁니다.')
    elif numFlag:
        return HttpResponse('아이디는 숫자로만 이루어질 수 없습니다.')
    else:
        return HttpResponse('사용 할 수 있는 아이디입니다.')

@api_view(['POST'])
def idealtag(request):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    tags = request.data['tags']
    print('tag')
    user.done_cup = 1
    user.save()
    for i in tags:
        tag = TagModel.objects.create(name=i, user=user, count=1)
    return HttpResponse('잘됨')

@api_view(['POST'])
def idealcategory(request):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    tags = request.data['tags']
    print('category')
    for i in tags:
        tag = CategoryUser.objects.create(name=i, user=user, count=1)
    return HttpResponse('잘됨')
    

# @api_view(['POST'])
# def create_trip(request):
#     serializer = TripSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         serializer.save(user=request.user)
#         return Response(serializer.data)

# @api_view(['GET'])
# def trip_detail(request, trip_pk):
#     trip = get_object_or_404(Trip, pk=trip_pk)
#     serializer = TripSerializer(trip)
#     return Response(serializer.data)

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.pk)

@api_view(['GET'])
def store_detail(request, store_pk):
    store = get_object_or_404(Store, pk=store_pk)
    serializer = StoreSerializer(store)
    return Response(serializer.data)

@api_view(['GET'])
def trip_today(request):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y%m%d')
    trip = get_object_or_404(Trip, user=user, date=int(nowDate))
    serializer = TripListSerializer(trip)
    tplan = trip.plan
    plan_id = []
    chk = 0
    num = ''
    for i in tplan:
        if i == 'R' or i == 'C':
            chk = 1
        elif i == 'S' or i == 'A':
            chk = 0
            plan_id.append(-1)
        elif i == '-':
            plan_id.append(num)
            num = ''
            chk = 0
        elif chk == 1:
            num += i
    if chk:
        plan_id.append(num)
    res = [0]*len(plan_id)
    for i in range(len(res)):
        if plan_id[i] == -1:
            continue
        elif plan_id[i] == '':
            continue
        else:
            tchk = Store.objects.get(id=plan_id[i])
            tstore = Review.objects.filter(user=user, store_id=tchk)
            if tstore.exists():
                res[i] = 1
    result = [serializer.data, res]
    return Response(result)

@api_view(['DELETE'])
def delete_trip(request, trip_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    trip = get_object_or_404(Trip, id=trip_pk)
    if trip.user == user:
        trip.delete()
        return HttpResponse('잘 지워짐')
    return HttpResponse('니 글 아님 ㅅㄱ')

@api_view(['POST'])
def date_chk(request):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    trip = Trip.objects.filter(user=user, date=request.data['date'])
    if trip.exists():
        return HttpResponse('1')
    else:
        return HttpResponse('0')
    
@api_view(['POST'])
def delete_date_chk(request):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    trip = Trip.objects.filter(user=user, date=request.data['date'])
    if trip[0].user == user:
        trip[0].delete()
        return HttpResponse('잘 지워짐')
    return HttpResponse('error')