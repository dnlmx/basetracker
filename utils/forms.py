#-*- coding: utf-8 -*-

from django import forms
from django.utils.html import conditional_escape, mark_safe
from django.utils.encoding import smart_text
from django.core.validators import EMPTY_VALUES

class NestedModelChoiceField(forms.ModelChoiceField):
    """A ModelChoiceField that groups parents and childrens"""
    def __init__(self, related_name, parent_field, label_field, empty_label, *args, **kwargs):
        """
        @related_name: related_name or "FOO_set"
        @parent_field: ForeignKey('self') field, use 'name_id' to save some queries
        @label_field: field for obj representation

        ie: 
        class MyModel(models.Model):
            parent = models.ForeignKey('self', null=True, blank=True)
            title = models.CharField()
        
        field = NestedModelChoiceField(queryset=MyModel.objects.all(),
                                       related_name='mymodel_set',
                                       parent_field='parent_id',
                                       label_field='title')
        """
        super(NestedModelChoiceField, self).__init__(*args, **kwargs)
        self.related_name = related_name
        self.parent_field = parent_field
        self.label_field = label_field
        self.empty_label = empty_label
        self._populate_choices()

    def _populate_choices(self):
        # This is *hackish* but simpler than subclassing ModelChoiceIterator
        choices = []
        kwargs = {self.parent_field: None, }
        queryset = self.queryset.filter(**kwargs)\
            .prefetch_related(self.related_name)
        
        if getattr(self, 'empty_label'):
            choices.append((0, self.empty_label))
        for parent in queryset:
            choices.append((self.prepare_value(parent), self.label_from_instance(parent)))
            choices.extend([(self.prepare_value(children), self.label_from_instance(children))
                            for children in getattr(parent, self.related_name).all()])

        self.choices = choices

    def label_from_instance(self, obj):
        level_indicator = ""
        if getattr(obj, self.parent_field):
            level_indicator = "--- "

        return mark_safe(level_indicator + conditional_escape(smart_text(getattr(obj, self.label_field))))

    #def validate(self, value):
    #    return Field.validate(self, value)        
    def to_python(self, value):
        if value in EMPTY_VALUES:
            return []