from django.http import HttpResponse
import models
import textsearch
import Filters
import NewFilter
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json
from django.utils.encoding import smart_str

filterMap = ['brand', 'price', 'color', 'merchant', 'gender', 'style']
sortMap = ['price', 'name']
catCache = "select c.cid, count(p.product_id) from categories as c left join products as p on c.cid=p.cid group by c.cid"


def isLeaf(catStr):
    # is leaf function is to check if the category is leaf category or not
    # by querying from database and check if the catStr is in the list or not
    catID = long(catStr)
    catQuerySet = models.Categories.objects.filter(cid__in=(models.Products.objects.all().values_list('cid'))).values_list('cid')
    if (catID,) in catQuerySet:
        return True
    return False

@csrf_exempt
def doFilter(request):
    response = None
    catID = request.GET.get('catid', None)
    topCategory = request.GET.get('topcategory', None)  # primKey always store pid value
    category = request.GET.get('category', None)  # secKey stores value for sort field, must be null if there is no sorting
    gender = request.GET.get('gender', None)  # only allow single sort
    brandName = request.GET.get('productFilter', None)  # allow multiple filters
    primKey = request.GET.get('primKey', None)
    secKey = request.GET.get('secKey', None)
    sortParam = request.GET.get('sort', None)
    filterString = request.GET.get('filter', None)
    environment = request.GET.get('env', None)
    #request.GET['env'] = environment
    page = int(request.GET.get('page', None))
    text = request.GET.get('text', None)

    whereClause1 = ""  # clause for next pages
    whereClause2 = ""  # clause for previous pages
    sortClause1 = ""  # clause for next pages
    sortClause2 = ""  # clause for previous pages

    filterSelection = []

    if primKey is None and secKey is not None:
        return HttpResponse("BAD REQUEST")

    if primKey is not None and ((sortParam is not None and secKey is None) or (secKey is not None and sortParam is None)):
        return HttpResponse("BAD REQUEST")

    if catID is not None:
        if isLeaf(catID):
            whereClause1 += "p.cid = " + catID
        else:
            #request.GET["catid"] = catID
            # is catID is leaf, dispatch from here and do not perform computation after this
            # originally the request is dispatched to msm4
            return HttpResponse("No category found")
        filterSelection = ["gender", "style", "brand"]
    elif brandName is not None:
        whereClause1 += "p.brand='" + brandName + "'"
        filterSelection = ["gender", "style", "category"]
    elif topCategory is not None:
        whereClause1 += "p.topcategory = '" + topCategory + "'"
        filterSelection = ["gender", "style", "brand", "category"]
    elif category is not None:
        whereClause1 += "p.category = '" + category + "'"
        filterSelection = ["gender", "style", "brand"]
    elif gender is not None:
        whereClause1 += "p.gender='" + gender + "'"
        filterSelection = ["category", "style", "brand"]
    elif text is not None:
        start = str(100*page-100)
        hash = textsearch.getPIDFromText(text, start, "100")
        if hash is not None:
            productIDs = str(",".join(list(hash.values())))
            whereClause1 += ("p.product_id in (" + productIDs + ")")
        else:
            # bad request
            return HttpResponse("Bad request")
        filterSelection = ["category", "style", "brand", "gender"]
    else:
        # bad request
        return HttpResponse("Bad request")

    whereClause2 += whereClause1

    # If there's no sort and is searching 1st page, no need to append anything
    # If there's no sort and is searching non-1st page using primKey, append the following whereClause using only primKey
    # If there's sorting and is searching 1st page, only need to append sortClause
    # If there's sorting and is searching non-1st page using primKey & secKey, append sortClause and whereClause using both keys
    if sortParam is None:
        if primKey is not None:
            whereClause1 += " and p.product_id>=" + primKey
            whereClause2 += " and p.product_id<" + primKey
    else:
        sort = sortParam.split(":")
        if len(sort) == 2 and sort[0] in sortMap:
            #request.GET["sortField"] = sort[0]
            if "desc" == sort[1]:
                sortClause1 += sort[0] + " desc, "
                sortClause2 += sort[0] + " asc, "
                if primKey is not None:
                    whereClause1 += " and (" + sort[0] + "=" + secKey + " and p.product_id>=" + primKey + " or " + sort[0] + "<" + secKey + ")"
                    whereClause2 += " and (" + sort[0] + "=" + secKey + " and p.product_id<" + primKey + " or " + sort[0] + ">" + secKey + ")"
            else:
                sortClause1 += sort[0] + " asc, "
                sortClause2 += sort[0] + " desc, "
                if primKey is not None:
                    whereClause1 += " and (" + sort[0] + "=" + secKey + " and p.product_id>=" + primKey + " or " + sort[0] + ">" + secKey + ")"
                    whereClause2 += " and (" + sort[0] + "=" + secKey + " and p.product_id<" + primKey + " or " + sort[0] + "<" + secKey + ")"
        else:
            return HttpResponse("This is bad request")

    filters = NewFilter.NewFilter()

    filters.SetFilterQuery(filterString, filterSelection, page)
    #TODO need to check this part
    filterSelection = filters.filterSelectionSet
    if filters.error:
        return HttpResponse("Bad request")
    #request.GET["filterSelection"] = filterSelection
    if filters.whereClause is not None:
        whereClause1 += unicode(filters.whereClause)
        whereClause2 += unicode(filters.whereClause)
    if filters.sortClause is not None:
        sortClause1 += filters.sortClause
        sortClause2 += filters.sortClause

    sortClause1 = sortClause1[:0] + " order by " + sortClause1[0:]
    sortClause1 += "p.product_id asc"

    #request.GET["whereClause1"] = whereClause1
    #request.GET["sortClause1"] = sortClause1

    if primKey is not None:
        request.GET["whereClause2"] = whereClause2
        sortClause2.insert(0, " order by ")
        sortClause2 += ("p.product_id desc")
        request.GET["sortClause2"] = sortClause2

    #TODO there is a "limit ?" in proQuery but I can't find the usage of it
    proQuery = "select p.product_id, p.name, p.price, p.cid, i.pic_url, i.img_id from products as p left join images as i on p.product_id=i.product_id where %s and i.img_type like 'P' %s limit 100" % (smart_str(whereClause1), smart_str(sortClause1))

    cursor1 = connection.cursor()
    cursor1.execute(proQuery)
    prod_result = cursor1.fetchall()
    result_json = formatParamsFilterJson(prod_result)

    # print "finish execution, debug"


    # print result_json

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

# def formatProDetailJson(query_results, recommend_result):
#     #profield = ProductID,ProductName,ProductPrice,ProductDesc,ProductURL,ProductBrand,ProductMerchant,ProductColor,CatID,CatName
#     delete = 'this'
#     prod_json = [{'ProductID': query_results[0][0],
#                 'ProductName': query_results[0][1],
#                 'ProductPrice': str(query_results[0][2]),
#                 'ProductDesc': query_results[0][3],
#                 'ProductURL': query_results[0][4],
#                 'ProductBrand': query_results[0][5],
#                 'ProductMerchant': query_results[0][6],
#                 'ProductColor': query_results[0][7],
#                 'CatID': query_results[0][8],
#                 'CatName': query_results[0][9]}]
#
#     new_image_json = []
#     for index in range(len(query_results)):
#         if index == 0:
#             new_image_json.extend([{'PrimaryImage': query_results[index][10]+str(query_results[index][11])}])
#         else:
#             new_image_json.extend([{'VariantImage': query_results[index][10]+str(query_results[index][11])}])
#
#
#
#     json_file = json.dumps([{'Result': {'ResultType': 'productdetails'},
#                              'Output': {'Product': prod_json,
#                                         'ProductImage': new_image_json,
#                                         'Recommendation': recommend_result},
#                              }])
#     return json_file


def debugIsLeaf(request):
    isLeaf(10300)
    return HttpResponse("This is debug function")

