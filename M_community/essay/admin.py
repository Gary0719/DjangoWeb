from django.contrib import admin

# Register your models here.
from .models import FileReference
from .models import Essay



class FileReference_Manager(admin.ModelAdmin):
    list_display = ['file_url', 'reference_number']

admin.site.register(FileReference, FileReference_Manager)



class Essay_Manager(admin.ModelAdmin):
    list_display = ['title', 'classify', 'image', 'video', 'author', 'is_active']

admin.site.register(Essay,Essay_Manager)