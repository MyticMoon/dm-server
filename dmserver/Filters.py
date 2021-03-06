from sets import Set
from django.utils.encoding import smart_str
import textsearch


class Filters():
    filterSelectionSet = []
    error = False
    whereClause = ""
    sortClause = ""


    def __init__(self):
        self.error = False


    @staticmethod
    def SetFilterQuery(filterString, filterSelection, page):
        filterSelectionSet = Set(filterSelection)  # fitlerSelectionSet is python set
        filterParams = None  # this is an array

        if filterString is not None:
            filterParams = filterString.split(";")

        if filterParams is not None:
            for Items in filterParams:
                twoColorsSelected = False
                filter = Items.split(":")
                if len(filter) == 2:
                    if filter[0].lower() == "gender":
                        Filters.whereClause += " and gender = " + filter[1]
                    if filter[0].lower() == "color":
                        colorValues = filter[1].split(",")
                        if len(colorValues) == 4:
                            if int(colorValues[0]) != -1:
                                Filters.whereClause += " and pri_color_12 = " + colorValues[0]
                            if int(colorValues[1]) != -1:
                                Filters.whereClause += " and pri_color_128 = " + colorValues[1]
                            if int(colorValues[2]) != -1:
                                Filters.whereClause += " and sec_color_12 = " + colorValues[2]
                            if int(colorValues[3]) != -1:
                                Filters.whereClause += " and sec_color_128 = " + colorValues[3]
                        if twoColorsSelected:
                            Filters.whereClause += " and sec_color_12_value>0.2"
                        Filters.sortClause += "(0.7*pri_color_12_value+0.3*sec_color_12_value) desc, "
                    else:
                        if filter[0].lower() == "text":
                            start = str(500*page-500)
                            listFinal = []
                            hash = textsearch.getPIDFromText(smart_str(filter[1]), start, "500")  # dictionary is a hash table
                            if hash is not None:
                                # convert the dictionary to string
                                # TODO modify this part
                                productIDs = None
                                productIDs = ",".join(hash)
                                Filters.whereClause += " and p.product_id in (" + productIDs + ")"
                            else:
                                if filter[0].lower() == "style":
                                    Filters.whereClause += " and " + filter[0] + " like '%" + filter[1] + "%'"
                                else:
                                    if filter[1].contains("+"):
                                        filter[1].replace("+", " ")
                                        Filters.whereClause += " and " + filter[0] + "='" + filter[1] + "'"
                                if filter[0] in filterSelectionSet:
                                    filterSelectionSet.remove(filter[0])
                        else:
                            error = True








