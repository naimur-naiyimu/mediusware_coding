# from django.views import generic

# from product.models import Variant


# class CreateProductView(generic.TemplateView):
#     template_name = 'products/list.html'

#     def get_context_data(self, **kwargs):
#         context = super(CreateProductView, self).get_context_data(**kwargs)
#         variants = Variant.objects.filter(active=True).values('id', 'title')
#         context['product'] = True
#         context['variants'] = list(variants.all())
#         return context

from django.core.paginator import Paginator
from django.shortcuts import render
from product.models import Product, ProductVariant, Variant, ProductVariantPrice
from django.db.models import Q


def product_list(request):
    products = Product.objects.all()
    paginator = Paginator(products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    variants = Variant.objects.all()
    prices = ProductVariantPrice.objects.all()

    # Filter products based on the request parameters
    title = request.GET.get('title')
    variant = request.GET.get('variant')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    date = request.GET.get('date')

    if title:
        page_obj = products.filter(title__icontains=title)

    if variant:
        page_obj = products.filter(Q(productvariant__variant_title__icontains=variant) | Q(
            productvariant__variant__title__icontains=variant))

    if price_from and price_to:
        variant_prices = ProductVariantPrice.objects.filter(
            price__gte=price_from, price__lte=price_to)
        variant_ids = variant_prices.values_list(
            'product_variant_one_id', 'product_variant_two_id', 'product_variant_three_id')
        variant_ids = set(
            [item for sublist in variant_ids for item in sublist if item])
        page_obj = products.filter(
            Q(productvariant__id__in=variant_ids) | Q(productvariant__isnull=True))

    if date:
       page_obj = products.filter(created_at__date=date)




    # varianti = {}
    # for product in page_obj:
    #     try:
    #         variant = ProductVariant.objects.filter(product=product).first()
    #         varianti[product.id] = variant.variant_title if variant else ''
    #     except ProductVariant.DoesNotExist:
    #         varianti[product.id] = ''

    context = {
        'page_obj': page_obj,
        # 'varianti': varianti,
        'variants': variants,
        'prices': prices
    }

    return render(request, 'products/product_list.html', context)
