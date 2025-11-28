from django.contrib import admin
from .models import Reclamation, ReclamationComment

@admin.register(Reclamation)
class ReclamationAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_submitter', 'type_de_reclamation', 'priorite', 'status', 'date_creation', 'date_resolution')
    list_filter = ('priorite', 'status', 'date_creation')
    search_fields = ('client__first_name', 'client__last_name', 'type_de_reclamation', 'description')

    def get_submitter(self, obj):
        return obj.submitter_name()
    get_submitter.short_description = 'Client'

@admin.register(ReclamationComment)
class ReclamationCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'reclamation', 'get_submitter', 'date_added')
    search_fields = ('description', 'user__first_name', 'user__last_name')

    def get_submitter(self, obj):
        return obj.submitter_name()
    get_submitter.short_description = 'Utilisateur'
