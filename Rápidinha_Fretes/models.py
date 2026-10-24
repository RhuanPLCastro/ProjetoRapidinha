from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.


class Login(models.Model):
    id_login = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=50, unique=True)
    cargo = models.CharField(max_length=50)
    senha = models.CharField(max_length=255)

    class Meta:
        db_table = "login"

    def __str__(self):
        return self.usuario


class Veiculo(models.Model):
    id_veiculo = models.AutoField(primary_key=True)
    placa = models.CharField(max_length=8, unique=True)
    numero_frota = models.CharField(max_length=10, unique=True)
    tipo = models.CharField(max_length=10)
    modelo = models.CharField(max_length=50)
    combustivel = models.CharField(max_length=10)
    status = models.CharField(max_length=20, default="Ativo")

    class Meta:
        db_table = "veiculo"

    def __str__(self):
        return f"{self.placa} - {self.modelo}"


class Motorista(models.Model):
    id_motorista = models.AutoField(primary_key=True)
    cnh = models.CharField(max_length=20, unique=True)
    categoria_cnh = models.CharField(max_length=3)
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    id_login = models.OneToOneField(
        Login, 
        on_delete=models.CASCADE, 
        db_column="id_login"
    )
    id_veiculo = models.ForeignKey(
        Veiculo, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        db_column="id_veiculo"
    )

    class Meta:
        db_table = "motorista"

    def __str__(self):
        return self.nome


class Manutencao(models.Model):
    id_manutencao = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=10)
    local = models.CharField(max_length=100, null=True, blank=True)
    descricao = models.CharField(max_length=500, null=True, blank=True)
    custo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_entrada = models.DateField()
    data_saida = models.DateField(null=True, blank=True)
    id_veiculo = models.ForeignKey(
        Veiculo, 
        on_delete=models.CASCADE, 
        db_column="id_veiculo"
    )

    class Meta:
        db_table = "manutencao"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(data_saida__isnull=True) | models.Q(data_saida__gte=models.F('data_entrada')),
                name="check_data_saida"
            )
        ]

    def __str__(self):
        return f"{self.tipo} - {self.id_veiculo}"
