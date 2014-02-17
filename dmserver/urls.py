from django.conf.urls import patterns, url

from dmserver import views
from dmserver import textsearch
from dmserver import ParamsFilter

urlpatterns = patterns('',
    url(r'^categories/', views.categoriesDoPost, name='categories'),
    url(r'^detailproduct/', views.DetailProdByPidPost, name='detailProd'),
    url(r'^homepage/', views.DetailProdByPidPost, name='homepage'),
    url(r'^textsearch/', textsearch.debugTextSearch, name='textsearch'),
    url(r'^debugisleaf/', ParamsFilter.debugIsLeaf, name='debugIsLeaf'),
    url(r'^debugparamsfilter', ParamsFilter.doFilter, name='debugParamsFilter')
)
