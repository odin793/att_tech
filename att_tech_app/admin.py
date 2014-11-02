# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline
from att_tech_app.models import *

def copy_object(queryset):
    for art in queryset:
        art_copy = ArticleWithDocuments(
            title = art.title,
            text = art.text,
            location = art.location
        )
        art_copy.save()

        for f in art.files_list.all():
            f_copy = Document(
                content_object = art_copy,
                name = f.name,
                url = f.url,
            )
            f_copy.save()


class PictureInline(GenericTabularInline):
    model = Picture


class DocumentInline(GenericTabularInline):
    model = Document


class DisciplineInline(admin.TabularInline):
    model = Discipline

    
class BasicArticleAdmin(admin.ModelAdmin):
    inlines = (PictureInline,)
    actions = ('copy_article',)

    def copy_article(self, request, queryset):
        for art in queryset:
            art_copy = BasicArticle(
                title = art.title,
                text = art.text,
                location = art.location
            )
            art_copy.save()
        
            for f in art.files_list.all():
                f_copy = Picture(
                    content_object = art_copy,
                    name = f.name,
                    url = f.url,
                    thumbnail_url = f.thumbnail_url,
                )
                f_copy.save()
    copy_article.short_description = u'Копировать выбранные статьи'


class ArticleWithDocumentsAdmin(admin.ModelAdmin):
    inlines = (DocumentInline,)
    actions = ('copy_article',)
    
    def copy_article(self, request, queryset):
        copy_object(queryset)
    copy_article.short_description = u'Копировать выбранные статьи'


class DocumentAdmin(admin.ModelAdmin):
    pass
    

class NewAdmin(admin.ModelAdmin):
    inlines = (PictureInline,)
    actions = ('copy_new', )
    list_display = ('title', 'is_event',)
    list_editable = ('is_event',)
    
    def copy_new(self, request, queryset):
        for new in queryset:
            n = New(
                title = new.title,
                short_text = new.short_text,
                full_text = new.full_text,
                main_photo = new.main_photo,
                date_added = new.date_added,
                is_event = new.is_event,
            )
            n.save()
            
            for ph in new.pictures_list.all():
                p = Picture(
                    content_object = n,
                    name = ph.name,
                    url = ph.url,
                    thumbnail_url = ph.thumbnail_url,
                )
                p.save()
    copy_new.short_description = u'Копировать выбранные новости'


class PersonAdmin(admin.ModelAdmin):
    inlines = (DisciplineInline,)


class ContactsAdmin(admin.ModelAdmin):
    pass
    

class DisciplineAdmin(admin.ModelAdmin):
    pass


class DisciplineTypeAdmin(admin.ModelAdmin):
    pass


class ProfessionAdmin(admin.ModelAdmin):
    pass


class NewCounterAdmin(admin.ModelAdmin):
    pass


class IndexPictureAdmin(admin.ModelAdmin):
    list_display = ('name', 'descr', 'position',)
    list_editable = ('position',)
    

class IndexTextBlockAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'position',)
    list_editable = ('position',)


class EmployeesInfoBlockAdmin(admin.ModelAdmin):
    pass

admin.site.register(BasicArticle, BasicArticleAdmin)
admin.site.register(ArticleWithDocuments, ArticleWithDocumentsAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(New, NewAdmin)
admin.site.register(DisciplineType, DisciplineTypeAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Discipline, DisciplineAdmin)
admin.site.register(Profession, ProfessionAdmin)
admin.site.register(Contacts, ContactsAdmin)
admin.site.register(NewCounter, NewCounterAdmin)
admin.site.register(IndexPicture, IndexPictureAdmin)
admin.site.register(IndexTextBlock, IndexTextBlockAdmin)
admin.site.register(EmployeesInfoBlock, EmployeesInfoBlockAdmin)