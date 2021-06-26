from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django_cpf_cnpj.fields import CPFField
from libgravatar import Gravatar


class Cadastro(models.Model):
    SEXO_CHOICES = [
        ["Feminino", "Feminino"],
        ["Masculino", "Masculino"]
    ]
    GRUPO_CHOICES = [
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
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    CPF = CPFField(masked=True, unique=True)
    nascimento = models.DateField()
    telefone = models.CharField(max_length=12)
    endereco = models.CharField(max_length=150)
    numero = models.CharField(max_length=4)
    complemento = models.CharField(max_length=150)
    bairro = models.CharField(max_length=30)
    CEP = models.CharField(max_length=8)
    sexo = models.CharField(max_length=50, choices=SEXO_CHOICES)
    grupo = models.CharField(max_length=50, choices=GRUPO_CHOICES)

    objetos = models.Manager()

    def __str__(self):
        return self.usuario.first_name

# Classe Agenda
class Event(models.Model):
    """Classe contendo a agenda propriamente dito, sua data, descrição
    e também prioridade."""
    date = models.DateField(null=True)
    event = models.CharField(max_length=80, null=True)
    priorities_list = (
        ("0", "Sem prioridade"),
        ("1", "Normal"),
        ("2", "Urgente"),
        ("3", "Muito Urgente"),
    )
    priority = models.CharField(max_length=1, choices=priorities_list, null=True)

    class Meta:
        ordering = ("-date", "-priority", "event")

    def number_of_comments(self):
        """Retorna a quantidade de comentários dentro de um serviço."""
        return self.comment_event.count()

    @property
    def text_priority(self):
        """ Converte o valor da prioridade no texto correspondente. """
        for k, v in self.priorities_list:
            if k == self.priority:
                return v
        return ""

    def __str__(self):
        return self.event

# Classe Comentários de Serviços
class Comment(models.Model):
    """Comentários efetuados em um determinado serviço."""

    author = models.CharField(max_length=80, null=True)
    email = models.EmailField(null=True)
    text = models.CharField(max_length=160, null=True)
    commented = models.DateTimeField(default=timezone.now, null=True)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="comment_event", null=True
    )

    class Meta:
        ordering = ("-commented",)

    def avatar(self):
        """Retorna a partir do endereço de e-mail, um avatar
        configurado no Gravatar ou um dos avatares padrão deles."""
        g = Gravatar(self.email)
        return g.get_image(default="identicon")


    def __str__(self):
        return "'{}'\n{} em {:%c}".format(
            self.text, self.author, self.commented
        )