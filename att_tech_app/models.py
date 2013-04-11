# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from tinymce import models as tinymce_models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

BASIC_ARTICLE_LOCATION_CHOICES = (
    ('about_tech', u'О техникуме'),
    ('tuition_by_correspondence', u'Заочное отделение'),
    ('courses', u'Подготовительные курсы'),
    ('acceptance_rules', u'Правила приема'),
)

class BasicArticle(models.Model):
    title = models.CharField(u'Заголовок', max_length=100)
    text = tinymce_models.HTMLField(u'Текст')
    location = models.CharField(u'Расположение', max_length=100,
        choices = BASIC_ARTICLE_LOCATION_CHOICES)
    files_list = generic.GenericRelation('Picture')
          
    class Meta:
        verbose_name = u'Текстовая страница (с фото)'
        verbose_name_plural = u'текстовые страницы (с фото)'
        
    def __unicode__(self):
        return self.title


ARTICLE_WITH_DOCUMENTS_LOCATION_CHOICES = (
    ('schedule', u'Расписание'),
    ('structure', u'Структура'),
    ('acceptance', u'Зачисление'),
    ('docs_samples', u'Образцы документов'),
    ('constituent_docs', u'Учредительные документы'),
)

class ArticleWithDocuments(models.Model):
    title = models.CharField(u'Заголовок', max_length=100)
    text = tinymce_models.HTMLField(u'Текст')
    location = models.CharField(u'Расположение', max_length=100,
        choices = ARTICLE_WITH_DOCUMENTS_LOCATION_CHOICES)
    files_list = generic.GenericRelation('Document')
          
    class Meta:
        verbose_name = u'Текстовая страница (c документами)'
        verbose_name_plural = u'текстовые страницы (с документами)'
        
    def __unicode__(self):
        return self.title


class New(models.Model):
    title = models.CharField(u'Заголовок', max_length=150)
    short_text = tinymce_models.HTMLField(u'Краткое содержание')
    full_text = tinymce_models.HTMLField(u'Полный текст')
    pictures_list = generic.GenericRelation('Picture')
    main_photo = models.URLField(u'Главное фото (300x200)',
        blank=True, null=True) # fixed 300 x 200 proportions
    date_added = models.DateField(u'Дата добавления')
    is_event = models.BooleanField(u'Событие студ. жизни ?', default = False)
    
    class Meta:
        ordering = ['date_added']
        verbose_name = u'Новость/Событие'
        verbose_name_plural = u'новости/события'
    
    def __unicode__(self):
        return self.title


class Profession(models.Model):
    name = models.CharField(u'Название', max_length=200)
    meta_info = models.CharField(u'Доп. информация', max_length=200)
    speciality = models.BooleanField(u'Специальность ?', default=False)
    text = tinymce_models.HTMLField(u'Описание')
    
    class Meta:
        verbose_name = u'Профессия/Специальность'
        verbose_name_plural = u'профессии/специальности'
    
    def __unicode__(self):
        return self.name


class Person(models.Model):
    full_name = models.CharField(u'ФИО', max_length=150)
    photo = models.URLField(u'Фото', blank=True, null=True) # fixed 1.5 ratio
    position = models.CharField(u'Должность', max_length=250,
        blank=True, null=True)
    contacts = models.CharField(u'Контактный телефон', max_length=50,
        blank=True, null=True)
    master_status = models.BooleanField(u'Управляющий ?', default = False)
    
    class Meta:
        verbose_name = u'Сотрудник'
        verbose_name_plural = u'сотрудники'
    
    def __unicode__(self):
        return u'%s, администрация: %s' % (self.full_name,
                                        str(self.master_status))


class Discipline(models.Model):
    name = models.CharField(u'Название дисциплины', max_length=150)
    tutor = models.ForeignKey(Person)
    discipline_type = models.ForeignKey('DisciplineType')
    
    class Meta:
        verbose_name = u'Дисциплина'
        verbose_name_plural = u'дисциплины'
    
    def __unicode__(self):
        return self.name
    

class DisciplineType(models.Model):
    discipline_type = models.CharField(u'Тип дисциплины', max_length=200)
    
    class Meta:
        verbose_name = u'Тип дисциплины'
        verbose_name_plural = u'типы дисциплин'
    
    def __unicode__(self):
        return self.discipline_type


class Contacts(models.Model):
    contacts = tinymce_models.HTMLField(u'Контакты')

    class Meta:
        verbose_name = u'Контакты'
        verbose_name_plural = u'контакты'
    
    def __unicode__(self):
        return u'Контакты'



class Document(models.Model):
    name = models.CharField(u'Название', max_length=250)
    url = models.URLField(u'ссылка')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    def natural_key(self):
        return (self.name, self.url)
    
    class Meta:
        verbose_name = u'Документ'
        verbose_name_plural = u'документы'
    
    def __unicode__(self):
        return self.name


class Picture(Document):
    thumbnail_url = models.URLField(u'ссылка на превью', blank=True, null=True)
    
    def natural_key(self):
        return (self.name, self.url, self.thumbnail_url)


    class Meta:
        verbose_name = u'Фото'
        verbose_name_plural = u'фото'
    
    def __unicode__(self):
        return self.name


class NewCounter(models.Model):
    news_number = models.PositiveIntegerField() 
    events_number = models.PositiveIntegerField()


def new_obj_changes_handling():
    new_counter, created = NewCounter.objects.get_or_create(id=0,  defaults={
        'news_number': 0,
        'events_number': 0,
    })
    new_counter.events_number = New.objects.filter(is_event=True).count()
    new_counter.news_number = New.objects.filter(is_event=False).count()
    new_counter.save()
    
@receiver(post_save, sender=New)
def new_post_save_handler(sender, **kwargs):
    new_obj_changes_handling()

@receiver(post_delete, sender=New)
def new_post_delete_handler(sender, **kwargs):
    new_obj_changes_handling()


class IndexPicture(models.Model):
    url = models.URLField(u'ссылка')
    name = models.CharField(u'Название фото', max_length=150)
    descr = models.TextField(u'Описание фото')
    position = models.SmallIntegerField(u'Порядок следования')
    
    class Meta:
        ordering = ['position',]
        verbose_name = u'Фото на главной странице'
        verbose_name_plural = u'фото на главной странице'


class IndexTextBlock(models.Model):
    title = models.CharField(u'Заголовок', max_length=100)
    text = models.TextField(u'Текст')
    position = models.SmallIntegerField(u'Порядок следования')
    
    class Meta:
        ordering = ['position',]
        verbose_name = u'Текстовый блок на главной странице'
        verbose_name_plural = u'текстовый блок на главной странице'
