from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import QuestionMessage, AnswerMessage, FilteredQuestion


class AnswerInline(admin.TabularInline):
    model = AnswerMessage
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'date', 'user_id', 'username', 'first_name', 'last_name', 'text')
    inlines = [AnswerInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        FilteredQuestion.objects.update_or_create(
            original_message_id=obj.message_id,
            defaults={
                'date': obj.date,
                'user_id': obj.user_id,
                'username': obj.username,
                'first_name': obj.first_name,
                'last_name': obj.last_name,
                'text': obj.text,
            }
        )


class FilteredQuestionAdmin(admin.ModelAdmin):
    list_display = ('original_message_id', 'date', 'user_id', 'username', 'first_name', 'last_name', 'text')
    search_fields = ('text', 'username', 'first_name', 'last_name')
    readonly_fields = ('answers_list',)

    def answers_list(self, obj):
        try:
            question = QuestionMessage.objects.get(message_id=obj.original_message_id)
            answers = question.answers.all()
            answers_html = ''.join([
                f'<div style="margin-bottom: 10px;">'
                f'<strong>ID:</strong> {answer.message_id}<br>'
                f'<strong>Date:</strong> {answer.date}<br>'
                f'<strong>User ID:</strong> {answer.user_id}<br>'
                f'<strong>Username:</strong> {answer.username}<br>'
                f'<strong>First Name:</strong> {answer.first_name}<br>'
                f'<strong>Last Name:</strong> {answer.last_name}<br>'
                f'<strong>Text:</strong> {answer.text}<br>'
                f'</div>'
                for answer in answers
            ])
            return mark_safe(answers_html)
        except QuestionMessage.DoesNotExist:
            return "No related question found"

    answers_list.short_description = 'Answers'


admin.site.register(QuestionMessage, QuestionAdmin)
admin.site.register(AnswerMessage)
admin.site.register(FilteredQuestion, FilteredQuestionAdmin)