from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import math
import random
from dmserver.models import Categories, Products
import json
from django.db import connection

@csrf_exempt
def categoriesDoPost(request):
    catID = request.POST['catid']
    

    return HttpResponse(None)