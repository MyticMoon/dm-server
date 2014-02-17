from django.http import HttpResponse


def doFilter(request):
    response = None

    filterMap = ['brand', 'price', 'color', 'merchant', 'gender', 'style']
    sortMap = ['price', 'name']

    imgID = request.GET['data']
    primKey = request.GET['primeKey']  # primKey always store pid value
    secKey = request.GET['secKey']  # secKey stores value for sort field, must be null if there is no sorting
    sortParam = request.GET['sort']  # only allow single sort
    filterParam = request.GET['filter']  # allow multiple filters

    whereClause1 = None  # clause for next pages
    whereClause2 = None  # clause for previous pages
    sortClause1 = None  # clause for next pages
    sortClause2 = None  # clause for previous pages

    #	Truth table for passing primKey, secKey, sort parameters
	#	 *  -----------------------------------
	#	 *  | primKey | secKey | sort | pass? |
	#	 * 	-----------------------------------
	#	 *  |    0    |    0   |   0  |   1   |
	#	 *  |    0    |    0   |   1  |   1   |
	#	 *  |    0    |    1   |   0  |   0   |
	#	 *  |    0    |    1   |   1  |   0   |
	#	 *  |    1    |    0   |   0  |   1   |
	#	 *  |    1    |    0   |   1  |   0   |
	#	 *  |    1    |    1   |   0  |   0   |
	#	 *  |    1    |    1   |   1  |   1   |
	#	 *  -----------------------------------
	#	 */

    if primKey is None and secKey is None:
        return HttpResponse('Bad Request')

    if primKey is not None and ((sortParam is not None and secKey is None) or (secKey is not None and sortParam is None)):
        return HttpResponse('Bad Request')

    if imgID is not None:
        whereClause1 += "i.img_id in (" + imgID + ")"
        whereClause2 += "i.img_id in (" + imgID + ")"
    else: #if it's not a catID, pID or brand search, it's invalid
        return HttpResponse('Bad Request')

    # If there's no sort and is searching 1st page, no need to append anything
	# If there's no sort and is searching non-1st page using primKey, append the following whereClause using only primKey
	# If there's sorting and is searching 1st page, only need to append sortClause
	# If there's sorting and is searching non-1st page using primKey & secKey, append sortClause and whereClause using both keys
    if sortParam is not None:
        sort = sortParam.split(':')
        #if it's an array of 2 strings and sort field is valid
        if len(sort) == 2 and sortMap.__contains__(sort[0]):
            response = [{"sort field": sort[0]}]
            if sort[1] == "desc":
                sortClause1 += sort[0] + " desc, "
                sortClause2 += sort[0] + " desc, "
                if primKey is not None:
                    whereClause1 += " and (" + sort[0] + "=" + secKey + " and i.img_id>=" + primKey + " or " + sort[0] + "<" + secKey + ")"
                    whereClause2 += " and (" + sort[0] + "=" + secKey + " and i.img_id>=" + primKey + " or " + sort[0] + "<" + secKey + ")"
            else:
                sortClause1 += sort[0] + " asc, "
                sortClause2 += sort[0] + " desc, "
                if primKey is not None:
                    whereClause1 += " and (" + sort[0] + "=" + secKey + " and i.img_id>=" + primKey + " or " + sort[0] + ">" + secKey + ")"
                    whereClause2 += " and (" + sort[0] + "=" + secKey + " and i.img_id<" + primKey + " or " + sort[0] + "<" + secKey + ")"
        else:
            return HttpResponse("Bad Request")

    if filterParam is not None:
        for items in filterParam:
            filter = items.split(':')
            if len(filter) == 2 and filterMap.__contains__(filter[0]):
                whereClause1 += " and " + filter[0] + " like '%" + filter[1] +"%'"
                whereClause2 += " and " + filter[0] + " like '%" + filter[1] +"%'"

    sortClause1.insert(0, " order by ")
    sortClause1 += "i.img_id asc"

    response["whereClause1"] = whereClause1
    response["sortClause1"] = sortClause1

    if primKey is not None:
        response["whereClause2"] = whereClause2
        sortClause2.insert(0, " order by ")
        sortClause2.insert("i.img_id desc")
        response["sortClause2"] = sortClause2

    #do filter here

    return None
