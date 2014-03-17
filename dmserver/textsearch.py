import urllib
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
import cStringIO
import pycurl
import json

@csrf_exempt
def categoriesDoPost(request):
    catID = request.POST['catid']
    return HttpResponse(None)


def processURL(address):
    res = None  # res is a string buffer
    # this is to read ID from text
    return None

#TODO remove this method


def debugTextSearch(request):
    list1 = getIDfromText("2010", "1", "20")
    list2 = getPIDFromText("2010", "1", "20")
    idsFinal = mergeIDS(list1, list2)
    return HttpResponse("This is empty function")


def getIDfromText(inputParams, start, rows):
    #this is for local environment
    #url = "http://192.168.56.101/solr/collection1/select?q="+inputParams+"&start="+start+"&rows="+rows+"&wt=json&indent=true"
    url = "http://visebuy.cloudapp.net:8983/solr/collection1/select?q="+inputParams+"&start="+start+"&rows="+rows+"&wt=json&indent=true"
    buf = cStringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(pycurl.HTTPGET, 1)
    c.setopt(c.WRITEFUNCTION, buf.write)
    c.setopt(c.CONNECTTIMEOUT, 10)
    c.perform()
    value = buf.getvalue()
    buf.close()
    json_result = json.loads(value)
    product_result = json_result['response']['docs']

    iterator = iter(range(len(product_result)))
    id_result = {}
    for i in iterator:
        id_result[i] = product_result[i]["img_id"]
    return id_result



def getPIDFromText(inputParams, start, rows):
    #this for local
    #url = "http://192.168.56.101/solr/collection1/select?q="+inputParams+"&start="+start+"&rows="+rows+"&wt=json&indent=true"
    #this for product environment
    url = "http://visebuy.cloudapp.net:8983/solr/collection1/select?q="+inputParams+"&start="+start+"&rows="+rows+"&wt=json&indent=true"
    buf = cStringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, smart_str(urllib.unquote(url).encode('utf8')))
    c.setopt(pycurl.HTTPGET, 1)
    c.setopt(pycurl.WRITEFUNCTION, buf.write)
    c.setopt(pycurl.CONNECTTIMEOUT, 10)
    c.perform()
    value = buf.getvalue()
    buf.close()
    json_result = json.loads(value)
    product_result = json_result['response']['docs']

    iterator = iter(range(len(product_result)))
    pid_result = {}
    for i in iterator:
        pid_result[i] = product_result[i]["product_id"]
    return pid_result


def mergeIDS(list1, list2):
    if list1 is None or list2 is None:
        return None
    else:
        listFinal = []
        iterator = iter(range(len(list1)))
        for i in iterator:
            if list1[i] in list2:
                listFinal.extend(list1[i])
        idsFinal = ",".join(listFinal)
        return idsFinal