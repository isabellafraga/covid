from datetime import datetime, timedelta

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.timezone import localdate
from django.views.defaults import bad_request, server_error
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated


from app1.forms import EventForm, CommentForm, FormCadastro
from app1.models import Event, Comment, Cadastro
from .serializers import CommentSerializer, EventSerializer
from .services import split_str_date

ITEMS_PER_PAGE = 5
FIRST_PAGE = 1


# PÁGINA PRINCIPAL INDEX
# ----------------------------------------------
def indexx(request):
    return render(request, 'app3/index.html')

# ----------------------------------------------
def noticia(request):
    return render(request, 'app3/noticia.html')

def manutencao(request):
    return render(request, 'app3/manutencao.html')

def cadastro(request):
    if request.method == 'POST':
        form = FormCadastro(request.POST)
        if form.is_valid():
            usuario = User()
            usuario.first_name = form.cleaned_data['first_name']
            usuario.email = form.cleaned_data['email']
            usuario.username = form.cleaned_data['username']
            usuario.password = form.cleaned_data['password']

            usuario.save()
            usuario.set_password(usuario.password)
            usuario.save()

            cad = Cadastro()
            cad.CPF = form.cleaned_data['CPF']
            cad.nascimento = form.cleaned_data['nascimento']
            cad.telefone = form.cleaned_data['telefone']
            cad.endereco = form.cleaned_data['endereco']
            cad.complemento = form.cleaned_data['complemento']
            cad.numero = form.cleaned_data['numero']
            cad.bairro = form.cleaned_data['bairro']
            cad.CEP = form.cleaned_data['CEP']
            cad.grupo = form.cleaned_data['grupo']
            cad.sexo = form.cleaned_data['sexo']

            cad.usuario = usuario
            cad.save()
            return HttpResponseRedirect(reverse('app1:lista_cadastro'))
    else:
        form = FormCadastro()

    return render(request, 'app3/cadastrar.html', {'form': form})

# PÁGINA PRINCIPAL FUNCIONARIO
# ----------------------------------------------

class IndexCadastroTemplateView(TemplateView):
    template_name = "app3/principal.html"

# LISTA DE FUNCIONÁRIOS
# ----------------------------------------------

class CadastroListView(ListView):
    template_name = "app3/lista.html"
    model = Cadastro
    context_object_name = "cadastrado"


# ATUALIZAÇÃO DE FUNCIONÁRIOS
# ----------------------------------------------

class CadastroUpdateView(UpdateView):
    template_name = "app3/confirmar.html"
    model = Cadastro
    fields = '__all__'
    context_object_name = 'cadastro'
    success_url = reverse_lazy("app1:lista_cadastro")


# EXCLUSÃO DE FUNCIONÁRIOS
# ----------------------------------------------

class CadastroDeleteView(DeleteView):
    template_name = "app3/index.html"
    model = Cadastro
    context_object_name = 'cadastro'
    success_url = reverse_lazy("app1:lista_cadastro")

# PÁGINA PRINCIPAL LOGIN
# ----------------------------------------------
def loginn(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        user = authenticate(username=usuario, password=senha)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('app1:indexx'))
            else:
                return HttpResponse("Sua Conta Não Esta Ativa.")
        else:
            print("Alguém Tentou Fazer Login e Falhou")
            print("Foi Usado userName: {} e senha: {}".format(usuario, senha))
            return HttpResponse("O Login ou Senha Está Incorreto.")

    else:
        return render(request, 'app3/login.html', {})

# PÁGINA PRINCIPAL LOGOUT
# ----------------------------------------------
@login_required
def logoutt(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

class EventViewSet(viewsets.ModelViewSet):
    """
    Disponibiliza os eventos da agenda como uma API REST.
    """

    queryset = Event.objects.all()
    serializer_class = EventSerializer

    permission_classes = (IsAuthenticated,)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Disponibiliza os eventos da agenda como uma API REST.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("event__id",)

    permission_classes = (IsAuthenticated,)

# PÁGINA PRINCIPAL AGENDA
# ----------------------------------------------
@login_required
def agenda(request):
    """
    Exibe a página principal da aplicaão.
    """
    context = {
        "hide_new_button": True,
        "priorities": Event.priorities_list,
        "today": localdate(),
    }

    return render(request, "app3/agenda/agenda.html", context)


@login_required
def all(request):
    """
    Exibe todas os eventos consolidados em uma única página, recebe o
    número da página a ser visualizada via GET.
    """

    page = request.GET.get("page", FIRST_PAGE)
    paginator = Paginator(Event.objects.all(), ITEMS_PER_PAGE)
    total = paginator.count

    try:
        events = paginator.page(page)
    except InvalidPage:
        events = paginator.page(FIRST_PAGE)

    context = {
        "events": events,
        "total": total,
        "priorities": Event.priorities_list,
        "today": localdate(),
    }

    return render(request, "app3/agenda/events.html", context)


@login_required
def day(request, year: int, month: int, day: int):
    """
    Visualização dos eventos de um determinado dia, recebe a data em
    formato ano/mês/dia como parâmtro.
    """


    day = datetime(year, month, day)
    filted_events = Event.objects.filter(
        date="{:%Y-%m-%d}".format(day)
    ).order_by("-priority", "event")

    context = {
        "today": localdate(),
        "day": day,
        "events": filted_events,
        "next": day + timedelta(days=1),
        "previous": day - timedelta(days=1),
        "priorities": Event.priorities_list,
    }

    return render(request, "app3/agenda/day.html", context)


@login_required
def delete(request, id: int):
    """
    Apaga um evento específico, se o evento não existir resultará em
    erro 404, se algo errado ocorrer retornará a página de erro.
    """
    event = get_object_or_404(Event, id=id)
    (year, month, day) = split_str_date("{:%Y-%m-%d}".format(event.date))

    if event.delete():
        return redirect("app1:agenda-events-day", year=year, month=month, day=day)
    else:
        return server_error(request, "ops_500.html")


@login_required
def edit(request):
    """
    Edita o conteúdo de um evento, recebendo os dados enviados pelo
    formulário, validando e populando em um evento já existente.
    """
    form = EventForm(request.POST)

    if form.is_valid():
        event = get_object_or_404(Event, id=request.POST["id"])
        event.date = form.cleaned_data["date"]
        event.event = form.cleaned_data["event"]
        event.priority = form.cleaned_data["priority"]
        event.save()
        (year, month, day) = split_str_date("{:%Y-%m-%d}".format(event.date))
        return redirect("app1:agenda-events-day", year=year, month=month, day=day)
    else:
        return bad_request(request, None, "ops_400.html")


@login_required
def new(request):
    """
    Recebe os dados de um novo evento via POST, faz a validação dos dados
    e aí insere na base de dados.
    """
    form = EventForm(request.POST)

    if form.is_valid():
        form.save(commit=True)
        # e uso a data enviada pelo formulário para o redirecionamento.
        year, month, day = split_str_date(request.POST["date"])

        return redirect("app1:agenda-events-day", year=year, month=month, day=day)
    else:
        return bad_request(request, None, "ops_400.html")


def show(request, id: int):
    """
    Visualização de um determinado evento e de seus comentários, recebe
    o 'id' do evento. Caso seja acessado via POST insere um novo comentário.
    """
    event = get_object_or_404(Event, id=id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect("app1:agenda-events-show", id=id)

    context = {
        "event": event,
        "comments": Comment.objects.filter(event=id).order_by("-commented"),
        "hide_new_button": True,
        "priorities": Event.priorities_list,
        "today": localdate(),
    }

    return render(request, "app3/agenda/show.html", context)