from django.contrib import admin
from .models import facture

@admin.register(facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ('num', 'datefact', 'total', 'compte', 'categ')  # Customize as needed
    search_fields = ('num', 'compte', 'categ')
    list_filter = ('datefact', 'categ')

# Alternatively, simple registration without customization:
# admin.site.register(facture)
