from io import BytesIO

from django.shortcuts import render
from django.http import HttpResponse
from robot.question import splitWord
import json
import base64
import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
from robot.models import Msg
from robot.visualdata import data_add,data_chart,data_map
from robot.pre import *

class Test(APIView):
    def get(self, request):
        a = request.GET['a']
        res = {
            'success': True,
            'data': 'a'
        }
        return Response(res)




class DATAADD(APIView):
    def get(self,request):
        jsondata=data_add.chinaDayList()
        return Response(jsondata)

class DATACHART(APIView):
    def get(self,request):
        jsondata=data_chart.datachart()
        return Response(jsondata)

class DATAMAP(APIView):
    def get(self,request):
        jsonarray={}
        provincetotal= data_map.ProvinceData()
        json1,json2,json3,json4=provincetotal.province_total_data()
        jsonarray=json.loads(json.dumps(jsonarray))
        jsonarray['data']=json1
        jsonarray['virus']=json2
        jsonarray['heal']=json3
        jsonarray['dead']=json4
        return Response(jsonarray)


class COMMENTS(APIView):
    def get(self,request):
        result = Msg.objects.all()
        comments=[]
        for one in result:
            com={}
            com['id']=one.id
            com['name']=one.name
            com['message']=one.message
            com['date']=one.date
            com['time']=one.time
            com['star']=one.star
            com['emotion']=one.emotion
            com['img']=one.photo
           # print(one.id,one.name,one.message,one.date,one.time,one.emotion)
            comments.append(com)
        return Response(comments)


@csrf_exempt
def getphoto(request):
    img = request.POST.get('data')
    print(img)
    img=img.split(',')[1]
    img = bytes(img, encoding='utf-8')
    data = base64.b64decode(img)
    filename = os.path.join(settings.STATICFILES_DIRS[0], "photo/test.jpeg")
    print(filename)
    with open(filename, 'wb') as f:
        f.write(data)
    result0,result1=predict_single_img(filename)
    result1=str(result1)
    jsondata = json.dumps({"type": result0, "pred": result1,"tips":"预测情况仅供参考，如有不适请及时就医"})
    return HttpResponse(jsondata)


@csrf_exempt
def getanswer(request):
    sentence=request.POST.get('data')
    print(sentence)
    ans=splitWord.ReturnAnswer(sentence)
    print(ans)
    return HttpResponse(ans)

@csrf_exempt
def addstar(request):
    try:
        id=request.POST.get('id')
        print(id)
        msg=Msg.objects.get(id=id)
        print(msg.star)
        msg.star=msg.star+1
        print(msg.star)
        msg.save()
        return HttpResponse(msg.star)
    except:
        return HttpResponse(-1)

@csrf_exempt
def deletestar(request):
    try:
        id=request.POST.get('id')
        print(id)
        msg=Msg.objects.get(id=id)
        print(msg.star)
        msg.star=msg.star-1
        if(msg.star<0):
            msg.star=0
        print(msg.star)
        msg.save()
        return HttpResponse(msg.star)
    except:
        return HttpResponse(-1)















