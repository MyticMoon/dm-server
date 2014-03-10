import cStringIO
import json
import os
from django.utils.encoding import smart_str
from django.db import connection, transaction
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import pycurl
from dm_server import settings
from dmserver import textsearch, Filters
from models import TmpImages



@csrf_exempt
@transaction.commit_on_success
def receiveIndexedImage(request):
    if request.method != "POST":
        return HttpResponse("Not a POST request")
    indexedResult = request.POST.get("indexedImage", None)
    listOfIndexedImg = (indexedResult).split(",")
    for img in listOfIndexedImg:
        imgAndId = img.split(":")
        imgURL = imgAndId[0]
        imgID = imgAndId[1]
        curImg = TmpImages.objects.get(pic_url__contains=str(imgURL))
        curImg.img_id_in_visebuy = int(imgID)
        curImg.save()

    return HttpResponse("No thing has been done")


@csrf_exempt
def imageSearch(request):
    uploadFullPath = settings.UPLOAD_DIR
    upload = request.FILES['file']
    while os.path.exists(os.path.join(uploadFullPath, upload.name)):
        upload.name = '_' + upload.name
    dest = open(os.path.join(uploadFullPath, upload.name), 'wb')
    for chunk in upload.chunks():
        dest.write(chunk)
    fields = [
        ('file', (pycurl.FORM_FILE, str(os.path.join(uploadFullPath, upload.name)))),
        ('api_key', settings.API_KEY),
        ('result_type', 'id')
    ]
    buff = cStringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://vise8core.cloudapp.net:8080/query/')
    c.setopt(c.HTTPPOST, fields)
    c.setopt(pycurl.WRITEFUNCTION, buff.write)
    c.perform()
    dest.close()
    value = buff.getvalue()
    buff.close()
    os.unlink(os.path.join(uploadFullPath, upload.name))
    return HttpResponse(value)


def getIDListFromImageServer(upload):
    uploadFullPath = settings.UPLOAD_DIR
    while os.path.exists(os.path.join(uploadFullPath, upload.name)):
        upload.name = '_' + upload.name
    dest = open(os.path.join(uploadFullPath, upload.name), 'wb')
    for chunk in upload.chunks():
        dest.write(chunk)
    fields = [
        ('file', (pycurl.FORM_FILE, str(os.path.join(uploadFullPath, upload.name)))),
        ('api_key', settings.API_KEY),
        ('result_type', 'id'),
        ('result_size', '50')
    ]
    buff = cStringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://vise8core.cloudapp.net:8080/query/')
    c.setopt(c.HTTPPOST, fields)
    c.setopt(pycurl.WRITEFUNCTION, buff.write)
    dest.close()
    c.perform()
    value = buff.getvalue()
    buff.close()
    os.unlink(os.path.join(uploadFullPath, upload.name))
    json_result = json.loads(value)
    #product_result = json_result['response']['docs']
    return json_result["IMAGES"]


@csrf_exempt
def imageQueryRequest(request):
    #TODO handle image_data upload here
    sortMap = ['price', 'name']
    image_data = request.FILES.get('file', None)
    page = request.POST.get('page', None)
    text = request.POST.get('text', None)
    filterString = request.POST.get('filter', None)
    env = request.POST.get('env', None)

    idList = getIDListFromImageServer(image_data)
    imageIDs = None

    if text is not None:
        page = int(page)
        start = (str)(page * 100 - 100)
        test = textsearch.mergeIDS(idList, textsearch.getIDfromText(text, start, "100"))
        if test is not None:
            imageIDs = test
        else:
            imageIDs = None

    textQuery = False
    filterParams = []
    if filterString is not None:
        filterParams = filterString.split(";")

    if filterParams is not None:
        for items in filterParams:
            filters = items.split[:]
            if(len(filters)==2 and len(items)==1 and filters[0]=="text"):
                hashID = {}
                i = 1
                for pid in idList:
                    hashID[i] = pid
                    i += 1
                start = str(page * 100 - 100)
                test = textsearch.mergeIDS(idList, textsearch.getIDfromText(text, start, "100"))
                if test is not None:
                    mergeIDs = test
                else:
                    mergeIDs = None
                textQuery = True
    if textQuery is False:
        sb = ""
        count = 0

        for id in idList:
            count = count+1
            if(count > 1):
                sb+=","
            sb+= str(id+1)
        imageIDs = str(sb)

    if filterParams is not None:
        if len(filterParams) > 1 or textQuery is False:
            whereClause1 = ""
            whereClause2 = ""
            sortClause1 = ""
            sortClause2 = ""

            sortParam = request.POST.get("sort", None)
            if sortParam is not None:
                sort = sortParam.split(":")
                if len(sort)==2 and sort[0] in sortMap:
                    if sort[1] == "desc":
                        sortClause1 = sortClause1 + sort[0] + " desc, "
                        sortClause2 = sortClause2 + sort[0] + " asc, "
                    else:
                        sortClause1 = sortClause1 + sort[0] + " asc, "
                        sortClause2 = sortClause2 + sort[0] + " desc, "
                else:
                    return HttpResponse("")

            whereClause1 = whereClause1 + "i.img_id in (" + imageIDs + ")"
            whereClause2 = whereClause2 + "i.img_id in (" + imageIDs + ")"

            filterSelection = ["gender", "style", "brand", "category"]
            filters = Filters.Filters()

            filters.SetFilterQuery(filterString, filterSelection, page)
            #TODO need to check this part
            filterSelection = filters.filterSelectionSet
            if filters.error:
                return HttpResponse("Bad request")
            #request.GET["filterSelection"] = filterSelection
            if filters.whereClause is not None:
                whereClause1 += filters.whereClause
                whereClause2 += filters.whereClause
            if filters.sortClause is not None:
                sortClause1 += filters.sortClause
                sortClause2 += filters.sortClause

            sortClause1 = sortClause1[:0] + " order by " + sortClause1[0:]
            sortClause1 += "p.product_id asc"
    proQuery = "select p.product_id, p.name, p.price, p.cid, i.pic_url, i.img_id from products as p left join images as i on p.product_id=i.product_id where %s and i.img_type like 'P' %s" % (smart_str(whereClause1), smart_str(sortClause1))
    cursor1 = connection.cursor()
    cursor1.execute(proQuery)
    prod_result = cursor1.fetchall()
    result_json = formatParamsFilterJson(prod_result)

    return HttpResponse(result_json)

def formatParamsFilterJson(query_results):
    products_json = []
    if len(query_results) > 0:
        for index in range(len(query_results)):
            products_json.extend([{
                'ProductID': query_results[index][0],
                'ProductName': query_results[index][1],
                'ProductPrice': str(query_results[index][2]),
                'CatID': query_results[index][3],
                'ProductImage': query_results[index][4],
                'ProductImageID':query_results[index][5]
            }])
    json_file = json.dumps([{'Result': {'ResultType': 'paramsfilterresult'},
                                'Output': {'Product': products_json}
                                }])
    return json_file



