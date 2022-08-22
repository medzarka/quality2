from django.contrib import admin
from ._data_upgrade import upgrade

class upgradeAdmin(admin.ModelAdmin):
    list_display = ('upgrade_id', 'original_filename_path', 'temporary_filename_path', 'temporary_filename', 'status', 'description',)
    list_filter = ('status', )

admin.site.register(upgrade, upgradeAdmin)