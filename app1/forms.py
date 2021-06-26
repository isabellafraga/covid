from django import forms
from django.contrib.auth.models import User
from django_cpf_cnpj.fields import CPFField

from app1.models import Cadastro, Comment, Event


# Fomulario Cadastro
class FormCadastro(forms.Form):
    SEXO_CHOICES = [
        ["Feminino", "Feminino"],
        ["Masculino", "Masculino"]
    ]
    GRUPO_CHOICES = [
        ["Selecione uma Opção", "Selecione uma Opção"],
        ["Profissional de saúde", "Profissional de saúde"],
        ["Trabalhador em saúde sem conselho de classe", "Trabalhador em saúde sem conselho de classe"],
        ["Doula", "Doula"],
        ["Cuidador", "Cuidador"],
        ["Acamado com 60 anos ou mais", "Acamado com 60 anos ou mais"],
        ["Pessoa com 80 anos ou mais", "Pessoa com 80 anos ou mais"],
        ["Pessoa entre 75 e 79 anos", "Pessoa entre 75 e 79 anos"],
        ["Pessoa entre 70 e 74 anos", "Pessoa entre 70 e 74 anos"],
        ["Pessoa entre 65 e 69 anos", "Pessoa entre 65 e 69 anos"],
        ["Pessoa entre 60 e 64 anos", "Pessoa entre 60 e 64 anos"],
        ["População Geral de 45 a 59 anos", "População Geral de 45 a 59 anos"],
        ["Policial Militar", "Policial Militar"],
        ["Policial Civil", "Policial Civil"],
        ["Policial Federal", "Policial Federal"],
        ["Agente da Receita Federal", "Agente da Receita Federal"],
        ["Policial Rodoviário", "Policial Rodoviário"],
        ["Agente Penitenciário / Policial Penal", "Agente Penitenciário / Policial Penal"],
        ["Trabalhadores de Unidades Socioeducativas", "Trabalhadores de Unidades Socioeducativas"],
        ["Trabalhador do Sistema Prisional", "Trabalhador do Sistema Prisional"],
        ["Bombeiro Civil", "Bombeiro Civil"],
        ["Bombeiro Militar", "Bombeiro Militar"],
        ["Guarda Municipal", "Guarda Municipal"],
        ["Membro do Exército", "Membro do Exército"],
        ["Membro da Marinha", "Membro da Marinha"],
        ["Membro da Aeronáutica", "Membro da Aeronáutica"],
        ["Trabalhador de Transporte Aéreo", "Trabalhador de Transporte Aéreo"],
        ["Professor", "Professor"],
        ["Trabalhador da Educação", "Trabalhador da Educação"],
        ["Assistente Social", "Assistente Social"],
        ["Trabalhador da Assistência Social", "Trabalhador da Assistência Social"],
        ["População Privada de Liberdade", "População Privada de Liberdade"],
    ]
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    CPF = forms.CharField()
    first_name = forms.CharField(label='Nome Completo')
    email = forms.EmailField()
    telefone = forms.CharField()
    endereco = forms.CharField()
    numero = forms.CharField()
    complemento = forms.CharField()
    bairro = forms.CharField()
    CEP = forms.CharField()
    nascimento = forms.DateField(label='Data de Nascimento', localize=True, required=True,
                                 widget=forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}))
    sexo = forms.ChoiceField(choices=SEXO_CHOICES)
    grupo = forms.ChoiceField(choices=GRUPO_CHOICES)

    class Meta:
        model = Cadastro
        fields = '__all__'

    def __str__(self):
        return self.first_name

# Formulario Agenda de Serviços
class EventForm(forms.ModelForm):
    """Formulário utilizado para a inserção de novos eventos."""

    class Meta:
        model = Event
        fields = ["date", "event", "priority"]

    def __str__(self):
        return self.event


class CommentForm(forms.ModelForm):
    """Formulário usado para a inserção de comentários em um serviço."""

    class Meta:
        model = Comment
        fields = ["text", "author", "email", "event"]

