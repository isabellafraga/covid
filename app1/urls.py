
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from django.urls import path, include

from . import views
from .views import CadastroListView, CadastroUpdateView, CadastroDeleteView, IndexCadastroTemplateView

router = routers.DefaultRouter()
router.register(r"events", views.EventViewSet)
router.register(r"comments", views.CommentViewSet)

app_name = 'app1'

urlpatterns = [
    path('login', views.loginn, name='login'),
    path('logout', views.logoutt, name='logout'),
    path('indexx', views.indexx, name='indexx'),
    path('noticia', views.noticia, name='noticia'),
    path('manutencao', views.manutencao, name='manutencao'),
    path('api-token-auth/', obtain_auth_token, name="api_token_auth"),
    path('cadastro/', views.cadastro, name="cadastrar"),
    path('cadastrado', CadastroListView.as_view(), name="lista_cadastro"),
    path('cadastro/<pk>', CadastroUpdateView.as_view(), name="atualiza_cadastro"),
    path('cadastro/excluir/<pk>', CadastroDeleteView.as_view(), name="deleta_cadastro"),
    path('principalcadastro/', IndexCadastroTemplateView.as_view(), name="principal_cadastro"),
    path('cpf', views.cpf, name='cpf'),
    path("api/v1/", include(router.urls)),
    path("agenda", views.agenda, name="agenda-events"),
    path("all", views.all, name="agenda-events-all"),
    path("<int:id>", views.show, name="agenda-events-show"),
    path("<int:year>/<int:month>/<int:day>", views.day, name="agenda-events-day"),
    path("new", views.new, name="agenda-events-new"),
    path("delete/<int:id>", views.delete, name="agenda-events-delete"),
    path("edit", views.edit, name="agenda-events-edit"),

]
