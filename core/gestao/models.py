from django.db import models

# Create your models here.

NATUREZA = [
    ('DESPESA','DESPESA'),
    ('RECEITA','RECEITA')
]

TIPO_CATEGORIA = [
    ('ANALITICA','ANALITICA'),
    ('SINTETICA','SINTETICA')
]



class Balancete(models.Model):
    codigo = models.CharField(max_length=10)
    nome = models.CharField(max_length=100)
    nivel = models.CharField(max_length=100, null=True, blank=True)
    calculo = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return self.nivel
    
    def save(self, *args, **kwargs):
        self.nivel = self.codigo +' - '+ self.nome
        super(Balancete, self).save(*args,**kwargs)
        
    
    
class Conta(models.Model):
    codigo  = models.CharField(max_length=30, unique=True)  # Código único para cada conta
    nome    = models.CharField(max_length=100)
    cd_varejo = models.IntegerField(null=True, blank=True)
    pai = models.IntegerField(null=True, blank=True)
    inativa = models.IntegerField(default=0)
    posicao = models.IntegerField(null=True, blank=True)
    natureza = models.CharField(max_length=30, choices=NATUREZA, null=True, blank=True)
    tipo = models.CharField(max_length=30, choices=TIPO_CATEGORIA, null=True, blank=True)
    hierarquia   = models.IntegerField(null=True, blank=True)
    balancete     = models.ForeignKey(Balancete, on_delete=models.SET_NULL, null=True, blank=True) # Nivel hierárquico da conta (0 para o topo)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.codigo) +' - '+ self.nome

            
