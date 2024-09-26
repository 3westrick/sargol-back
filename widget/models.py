from django.db import models
from rest_framework.exceptions import ValidationError
from attribute.models import Attribute
from attribute.serial import AttributeSerial
from category.models import Category
from category.serial import CategorySerial

# Create your models here.
class Widgetgroup(models.Model):
    title = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)

    def create_attribute(self, attribut_id, title, display, ):
        self.widgets.create(option='attribute', value=attribut_id, main=True)
        self.widgets.create(option=f'attribute-{attribut_id}-display', value=display, main=False)
        self.widgets.create(option=f'attribute-{attribut_id}-title', value=title, main=False)

    def create_category(self, title, display):
        if not self.widgets.filter(option__in=['category-display', 'category-title']).exists():
            self.widgets.create(option='category-display', value=display, main=False)
            self.widgets.create(option='category-title', value=title, main=True)  
        else:
            raise ValidationError({'detail': 'Already have category'})

    def create_price(self, title, apply_filter, type):
        if not self.widgets.filter(option__in=['price-title', 'price-apply-filter', 'price-type']).exists():
            self.widgets.create(option='price-title', value=title, main=True)
            self.widgets.create(option='price-apply-filter', value=apply_filter, main=False)
            self.widgets.create(option='price-type', value=type, main=False)
        else:
            raise ValidationError({'detail': 'Already have price'})

    def create_rating(self, title):
        if not self.widgets.filter(option='rating-title').exists():
            self.widgets.create(option='rating-title', value=title, main=True)
        else:
            raise ValidationError({'detail': 'Already have rating'})

    def get_attribute(self,widgets,widget):
        if widgets is None: widgets = self.widgets.all()
        
        return {
            'attributes': AttributeSerial(instance=Attribute.objects.get(pk=widget.value)).data,
            'title': widgets.get(option=f'attribute-{widget.value}-title').value,
            'display': widgets.get(option=f'attribute-{widget.value}-display').value,
            'type': 'attribute',
            'id': widget.id,
        }

    def get_category(self, widgets, widget):
        if widgets is None: widgets = self.widgets.all()
        try:
            return {
                'title':  widget.value,
                'display':  widgets.get(option='category-display').value,
                'categories': CategorySerial(Category.objects.all(), many=True).data,
                'type': 'category',
                'id': widget.id,
            }
        except:
            return None
        
    def get_price(self, widgets, widget):
        if widgets is None: widgets = self.widgets.all()
        try:
            return {
                'price-title':  widgets.get(option='price-title').value,
                'price-apply-filter':  widgets.get(option='price-apply-filter').value,
                'price-type': widgets.get(option='price-type').value,
                'type': 'price',
                'id': widget.id,
            }
        except:
            return None
    
    def get_rating(self, widgets, widget):
        if widgets is None: widgets = self.widgets.all()
        try:
            return {
                'rating-title':  widgets.get(option='rating-title').value,
                'type': 'rating',
                'id': widget.id,
            }
        except:
            return None
    
    def widget_switch(self, widget):
        widgets = self.widgets.all()
        switcher = {
            'attribute': lambda: self.get_attribute(widgets, widget),
            'category-title': lambda:self.get_category(widgets,widget),
            'price-title': lambda:self.get_price(widgets, widget),
            'rating-title': lambda:self.get_rating(widgets, widget),
        }

        return switcher.get(widget.option)()

    def get_widgets(self):
        widgets = self.widgets.filter(main=True)
        temp = []
        for widget in widgets:
            w = self.widget_switch(widget)
            if w is not None:
                temp.append(w)

        return temp
        

            

class Widget(models.Model):
    group = models.ForeignKey(Widgetgroup, on_delete=models.CASCADE, related_name='widgets')
    option = models.CharField(max_length=50)
    value = models.CharField(max_length=50, null=True, blank=True)
    main = models.BooleanField()