from django.urls import path
from django.views.generic import TemplateView
from product import views

from product.views.product import product_list
from product.views.variant import VariantView, VariantCreateView, VariantEditView

app_name = "product"

urlpatterns = [
    # Variants URLs
    path('variants/', VariantView.as_view(), name='variants'),
    path('variant/create', VariantCreateView.as_view(), name='create.variant'),
    path('variant/<int:id>/edit', VariantEditView.as_view(), name='update.variant'),

    # Products URLs
    # path('create/', CreateProductView.as_view(), name='create.product'),
    # path('list/', CreateProductView.as_view(template_name='products/list.html', extra_context={
    #     'product': True
    # }), name='list.product'),
    
    path('list/', views.product.product_list, name='product_list'),
]
