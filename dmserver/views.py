from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import math
import random
from dmserver.models import Categories, Products
import json
from django.db import connection
import pycurl
# Create your views here.


def viewHomePage(request):
    return render(request, 'homepage.html')

def apiOverviewSubCategories(request):
    return render(request, 'subcategories.html')

def apiOverview(request):
    return render(request, 'apioverview.html')

def apiOverviewCategoriesListing(request):
    return render(request, 'categorylisting.html')

def apiOverviewDetailProduct(request):
    return render(request, 'detailproduct.html')

def apiOverviewImageSearch(request):
    return render(request, 'imagesearch.html')

def apiOverviewParamsSearch(request):
    return render(request, 'parametersearch.html')

@csrf_exempt
def categoriesDoPost(request):
    if request.method == "POST":
        catID = request.POST['catid']
    else:
        catID = request.GET['catid']
    cat_result = None
    json_result = None
    cat_json = None

    if catID is not None:
        cat_filter_results = list(Categories.objects.filter(parent_cid=catID))
        cat_json = formatCategoryJson(cat_filter_results)
    return HttpResponse(cat_json)


def formatCategoryJson(query_results):
    #catXml = CatID, CatName
    #TODO prepare a config file
    cat_json = [{'CatID': result.cid,
                 'CatName': result.name} for result in query_results]
    json_file = json.dumps([{'Result': {'ResultType': 'categorydetails'},
                 'Output': cat_json
                }])
    return json_file


@csrf_exempt
def DetailProdByPidPost(request):
    proID = None;
    if request.method == "POST":
        proID = request.POST.get('pid',None)
    else:
        proID = request.GET.get('pid',None)
    if proID == None:
        return HttpResponse("Invalid request, pid is missing")
    prod_query = "select p.product_id, p.name, p.price, p.description, p.product_url, p.brand, p.merchant, p.color, c.cid, c.name, i.pic_url, i.img_id from (products as p left join categories as c on p.cid=c.cid) left join images as i on p.product_id=i.product_id where p.product_id = %s order by i.img_type asc" % (str(proID))
    cursor1 = connection.cursor()
    cursor1.execute(prod_query)
    prod_result = cursor1.fetchall()

    if len(prod_result) >= 1:
        catID = prod_result[0][8]
        prod_results = list(Products.objects.filter(cid=catID))
        rowsNum = len(prod_results)
        offset = 0

        if rowsNum > 4:
            offset = int(math.floor(random.random()*(rowsNum-4)))

        recommended_query = "select p.product_id, p.name, p.price, p.cid, i.pic_url, i.img_id from products as p left join images as i on p.product_id=i.product_id where p.product_id!= %s and p.cid = %s and i.img_type='P' limit %s, 4"
        cursor2 = connection.cursor()
        query_string = 'select p.product_id, p.name, p.price, p.cid, i.pic_url, i.img_id from products as p left join images as i on p.product_id=i.product_id where p.product_id!= %s and p.cid = %s and i.img_type="P" limit %s, 4' % (str(proID), str(catID), str(offset))
        cursor2.execute(query_string)
        recommend_result = cursor2.fetchall()
        recommend_result_formatted_dict = formatRecommendJson(recommend_result)

    prod_json_result = formatProDetailJson(prod_result, recommend_result_formatted_dict)

    return HttpResponse(prod_json_result)


def formatProDetailJson(query_results, recommend_result):
    #profield = ProductID,ProductName,ProductPrice,ProductDesc,ProductURL,ProductBrand,ProductMerchant,ProductColor,CatID,CatName
    delete = 'this'
    prod_json = [{'ProductID': query_results[0][0],
                'ProductName': query_results[0][1],
                'ProductPrice': str(query_results[0][2]),
                'ProductDesc': query_results[0][3],
                'ProductURL': query_results[0][4],
                'ProductBrand': query_results[0][5],
                'ProductMerchant': query_results[0][6],
                'ProductColor': query_results[0][7],
                'CatID': query_results[0][8],
                'CatName': query_results[0][9]}]

    new_image_json = []
    for index in range(len(query_results)):
        if index == 0:
            new_image_json.extend([{'PrimaryImage': query_results[index][10]+str(query_results[index][11])}])
        else:
            new_image_json.extend([{'VariantImage': query_results[index][10]+str(query_results[index][11])}])



    json_file = json.dumps([{'Result': {'ResultType': 'productdetails'},
                             'Output': {'Product': prod_json,
                                        'ProductImage': new_image_json,
                                        'Recommendation': recommend_result},
                             }])
    return json_file


def formatRecommendJson(query_results):
    #recommendXML = ProductID,ProductName,ProductPrice,CatID,ProductImage,ProductImageID
    recommend_product = [{'ProductID': result[0],
                          'ProductName': result[1],
                          'ProductPrice': str(result[2]),
                          'CatID': result[3],
                          'ProductImage': result[4],
                          'ProductImageID':result[5]} for result in query_results]

    #recommend_json = [{'Recommendation': recommend_product}]

    return recommend_product


@csrf_exempt
def categoriesListing(request):
    # if request.method != 'POST':
    #     return HttpResponse('Bad Http Request')
    categoriesListingQuery = "select cid, name, parent_cid, is_parent from categories"
    cursor2 = connection.cursor()
    cursor2.execute(categoriesListingQuery)
    category_result = cursor2.fetchall()
    formattedJsonResult = formatCategoryListing(category_result)
    return HttpResponse(formattedJsonResult)


def formatCategoryListing(category_results):
    # jsonCategoryResult = [{'CategoryID': result[0],
    #                        'Name': result[1],
    #                        'Parent_CID': result[2],
    #                        'Is_Parent': result[3]} for result in category_results]
    jsonCategoryResult = []
    jsonSubCategory = []
    tempParentCid = str(category_results[0][2])
    for result in category_results:
        if str(result[2]) != tempParentCid:
            jsonCategoryResult.append({'ParentID': tempParentCid,
                                       'Categories': jsonSubCategory})
            jsonSubCategory = []
            tempParentCid = str(result[2])
        jsonSubCategory.append({'CategoryID': result[0],
                           'Name': result[1],
                           'Parent_CID': result[2],
                           'Is_Parent': result[3]})

    formattedJsonResult = json.dumps([{'Result': {'ResultType': 'category_listing'},
                                       'Output': jsonCategoryResult}])
    return formattedJsonResult

@csrf_exempt
def returnImageList(request):
    categoriesListingQuery = "select substring(pic_url, 24) from images limit 300"
    cursor2 = connection.cursor()
    cursor2.execute(categoriesListingQuery)
    category_result = cursor2.fetchall()
    returnValue = ""
    for result in category_result:
        returnValue += "," + result[0]
    return HttpResponse(returnValue)