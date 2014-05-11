from django.conf.urls import patterns, url

from dmserver import views
from dmserver import textsearch
from dmserver import ParamsFilter
from dmserver import indexImage

urlpatterns = patterns('',
    url(r'^categories/', views.categoriesDoPost, name='categories'),
    url(r'^detailproduct/', views.DetailProdByPidPost, name='detailProd'),
    url(r'^homepage/', views.DetailProdByPidPost, name='homepage'),
    url(r'^textsearch/', textsearch.debugTextSearch, name='textsearch'),
    url(r'^debugisleaf/', ParamsFilter.debugIsLeaf, name='debugIsLeaf'),
    url(r'^debugparamsfilter/', ParamsFilter.doFilter, name='debugParamsFilter'),
    url(r'^categorylisting/', views.categoriesListing, name='categoriesListing'),
    url(r'^imagelisting/', views.returnImageList, name='categoriesListing'),
    url(r'^indeximage/', indexImage.receiveIndexedImage, name='indexedImage'),
    url(r'^imagesearch/', indexImage.imageQueryRequest, name='imageSearch'),
    url(r'^api-overview/', views.apiOverview, name='api-overview'),
    url(r'^api-subcategories/', views.apiOverviewSubCategories, name='api-overview'),
    url(r'^api-categorylisting/', views.apiOverviewCategoriesListing, name='api-overview'),
    url(r'^api-detailproduct/', views.apiOverviewDetailProduct, name='api-overview'),
    url(r'^api-imagesearch/', views.apiOverviewImageSearch, name='api-overview'),
    url(r'^api-parametersearch/', views.apiOverviewParamsSearch, name='api-overview'),
    url(r'^productfromimgid/', ParamsFilter.getProductsFromImagesId, name='getProductFromImagesID'),
)
