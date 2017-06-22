from django.conf.urls import url
from perfis import views

urlpatterns = [
    url(r'^recomendacaofilmeusuario.html', views.recomendacaofilmeusuario, name=''),
    url(r'^recomendacaofilmeusuarioresposta.html/(?P<perfil_id>\d+)$',views.recomendacaofilmeusuarioresposta,name=''),
    url(r'^bemvindo.html', views.index, name=''),
    url(r'^$', views.index, name=''),
    url(r'^usuariofilme.html', views.usuariofilme, name=''),
    url(r'^perfilusufilme.html', views.perfilusufilme, name=''),
    url(r'^perfilusufilmeresposta.html/(?P<perfil_id>\d+)$',views.perfilusufilmeresposta,name='')
]