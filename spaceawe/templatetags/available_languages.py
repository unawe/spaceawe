from django import template

register = template.Library()


@register.inclusion_tag('booklet_languages_snippet.html')
def item_languages(item, actual_language):
    choices = [(item_language.language_code, item_language.get_language_code_display()) for item_language in item.translations.all()]
    return {'choices': choices, 'actual_language': actual_language}
