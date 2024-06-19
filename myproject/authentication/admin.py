from django.contrib import admin 
from .models import Question, Option, CodeSnippet
 
class OptionInline(admin.TabularInline): 
    model = Option 
    extra = 3  # Show 3 option fields by default 
 
class QuestionAdmin(admin.ModelAdmin): 
    inlines = [OptionInline] 

@admin.register(CodeSnippet)
class CodeSnippetAdmin(admin.ModelAdmin):
    list_display = ('language', 'code')
 
admin.site.register(Question, QuestionAdmin)