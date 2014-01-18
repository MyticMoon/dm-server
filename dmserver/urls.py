from django.conf.urls import patterns, url

from dmserver import views

urlpatterns = patterns('',
    url(r'^categories/', views.categoriesDoPost, name='homepage'),
    url(r'^detailproduct/', views.DetailProdByPidPost, name='detailProd'),
)
