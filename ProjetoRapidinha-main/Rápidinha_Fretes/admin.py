from django.contrib import admin
from .models import Login, Veiculo, Motorista, Manutencao

# Register your models here.


admin.site.register(Login)
admin.site.register(Veiculo)
admin.site.register(Motorista)
admin.site.register(Manutencao)
