from django.shortcuts import render
from product.models import Product
from adminpanel.product.serial import ProductSerial, ProductSingleSerial,ProductGallery,VariantSerial

from base.mixins import ModelPermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics, mixins, permissions, authentication
from base.mixins import CheckPermission
import time
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes

# Create your views here.

class ProductListView(CheckPermission, generics.ListAPIView):
    queryset = Product.objects.filter(parent=None)
    serializer_class = ProductSerial


    
class ProductRetriveView(CheckPermission, generics.RetrieveAPIView):
    queryset = Product.objects.filter(parent=None)
    serializer_class = ProductSingleSerial
    lookup_field = 'pk'


class ProductCreateView(CheckPermission, generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerial


    def perform_create(self, serializer):
        product = serializer.save()
        data = self.request.data

        gallery = data.getlist('gallery')
        attrbiutes = data.getlist('attributes')
        visibleAttributes = data.getlist('visibleAttributes')
        variantAttributes = data.getlist('variantAttributes')
        for image in gallery:
            product.gallery.create(image=image)
        
        for attribute in attrbiutes:
            visible = False
            variant = False
            if attribute in visibleAttributes:
                visible = True
            if attribute in variantAttributes:
                variant = True
            product.attributes.create(attribute_id=attribute,visible=visible, variant=variant)

        
class VariantCreateView(CheckPermission, generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = VariantSerial     

    def perform_create(self, serializer):
        product = serializer.save()
        product.slug = product.id
        product.save()
        data = self.request.data
        
        parent_attrbiutes = product.parent.attributes.filter(variant=True)
        for p_a in parent_attrbiutes:
            product.attributes.create(attribute=p_a.attribute, visible=p_a.visible, variant=True)

        gallery = data.getlist('gallery')
        for image in gallery:
            product.gallery.create(image=image)

class VariantEditView(CheckPermission, generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = VariantSerial 
    lookup_field = 'pk'

    def perform_update(self, serializer):
        data = self.request.data
        product = serializer.save()
        product.attributes.all().delete()

        parent_attrbiutes = product.parent.attributes.filter(variant=True)
        for p_a in parent_attrbiutes:
            product.attributes.create(attribute=p_a.attribute, visible=p_a.visible, variant=True)
        
        gallery = data.getlist('gallery')
        product_gallery = product.gallery.all().values_list('id', flat=True)

        old_images_ids = [ int(x) for x in gallery if type(x) == str]
        new_images = [ x for x in gallery if type(x) != str]
        
        for i in product_gallery:
            if not i in old_images_ids:
                product.gallery.get(id=i).delete()

        for image in new_images:
            product.gallery.create(image=image)



class ProductUpdateView(CheckPermission, generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerial
    lookup_field = 'pk'
    

    def perform_update(self, serializer):
        data = self.request.data
        variants_id= [int(x) for x in data.getlist('variants')]
        product = serializer.save()
        
        print(variants_id)
        variants = product.variants.all().values_list('id', flat=True)
        for variant in variants:
            if not variant in variants_id:
                product.variants.get(id=variant).delete()

        product.attributes.all().delete()
        attrbiutes = data.getlist('attributes')
        visibleAttributes = data.getlist('visibleAttributes')
        variantAttributes = data.getlist('variantAttributes')
        for attribute in attrbiutes:
            visible = False
            variant = False
            if attribute in visibleAttributes:
                visible = True
            if attribute in variantAttributes:
                variant = True
            product.attributes.create(attribute_id=attribute,visible=visible, variant=variant)

        
        gallery = data.getlist('gallery')
        product_gallery = product.gallery.all().values_list('id', flat=True)

        old_images_ids = [ int(x) for x in gallery if type(x) == str]
        new_images = [ x for x in gallery if type(x) != str]
        
        for i in product_gallery:
            if not i in old_images_ids:
                product.gallery.get(id=i).delete()

        for image in new_images:
            product.gallery.create(image=image)
            
        return super().perform_update(serializer)


class ProductDeleteView(CheckPermission, generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerial
    lookup_field = 'pk'
    def perform_destroy(self, instance):
        instance.delete()


class ProductGalleryDeleteView(CheckPermission, generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductGallery
    lookup_field = 'pk'
