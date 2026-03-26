from django.contrib import admin
from .models  import Balancete, Conta
from django.utils.translation import gettext_lazy as _
# Register your models here.

# Personalizando o título e o cabeçalho
admin.site.site_header = _('VilaBox')
admin.site.site_title = _('VilaBox')
admin.site.index_title = _('Administração')

class filterNivel1Balancete(admin.SimpleListFilter):
    title = 'Balancete'
    parameter_name = 'balancete_id'
    
    def lookups(self, request, model_admin):
        lista = Conta.objects.raw("select distinct d.id, d.nivel from gestao_conta c join gestao_balancete d on d.id = c.balancete_id ") 
        return [(x.id, x.nivel) for x in lista]
    
    def queryset(self, request, queryset):
        if self.value():   
            return queryset.filter(balancete=self.value())
        
        return queryset            

class filterNivel1Conta(admin.SimpleListFilter):
    title = 'Conta Nível 1'
    parameter_name = 'conta_nivel'
    
    def lookups(self, request, model_admin):
        lista = Conta.objects.raw("select codigo id, codigo+' - '+nome nome from Gestao_conta where hierarquia = 1") 
        return [(x.id, x.nome ) for x in lista]
    
    def queryset(self, request, queryset):
        if self.value():   
            print('O valor é: '+ self.value()   )
            return  queryset.filter(codigo__startswith=self.value())
        
        return queryset     


@admin.register(Balancete)
class BalanceteAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'nivel', 'calculo')


@admin.register(Conta)
class ContaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'cd_varejo','hierarquia','balancete', 'pai', 'inativa', 'posicao', 'natureza', 'tipo')
    list_filter = ('tipo','natureza',filterNivel1Balancete, filterNivel1Conta)  
    search_fields = ('nome',)