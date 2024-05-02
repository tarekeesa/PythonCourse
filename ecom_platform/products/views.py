from django.shortcuts import render
from django.views.generic import ListView,DetailView
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

from .models import Category, Product
# Create your views here.

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    print('product lists ')
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
        return queryset.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        categories = Category.objects.filter(products__isnull=False).distinct()
        context['categories'] = categories
        return context


def product_list_view(request):
    product_list = Product.objects.filter(active=True).order_by('-id')  # Assuming you might want to order by id or any other field
    paginator = Paginator(product_list, 10)  # Show 10 products per page

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    featured_products = Product.objects.filter(active=True, featured=True).order_by('-id')[:5]
    categories = Category.objects.filter(products__isnull=False).distinct()

    context = {
        'products': products,
        'featured_products':featured_products,
        'categories': categories,
    }
    return render(request, 'products/product_list.html', context)


from django.db.models import Count

def filter_products(request):
    category_ids = request.GET.getlist('categories')
    print('category_ids',category_ids)
    category_ids = [int(id) for id in category_ids if id.isdigit()]  # Convert to integers
    price_min = request.GET.get('price_min', 0)
    price_max = request.GET.get('price_max', 500)
    sort_by = request.GET.get('sort_by', 'id')
    print('category_ids',category_ids)
    keyword = request.GET.get('keyword', '')

    products = Product.objects.all()
    if keyword:
        products = products.filter(title__icontains=keyword)  # Or any other field relevant to your search
    if category_ids:
        products = products.filter(category_id__in=category_ids)
        print('products',products)
    if price_min and price_max:
        products = products.filter(price__gte=price_min, price__lte=price_max)

    # Handling sorting
    if sort_by:
        # Assume 'popularity' might be sorted by a 'likes' count or similar field, adjust as needed
        if sort_by == 'popularity':
            products = products.annotate(likes_count=Count('likes')).order_by('-likes_count')
        elif sort_by == 'price':
            products = products.order_by('price')
        elif sort_by == '-price':
            products = products.order_by('-price')

    # Prepare data for JSON response
    products_data = []
    for product in products:
        product_data = {
            'id': product.id,
            'title': product.title,
            'price': product.price,
            'unit': product.unit,
            'image': request.build_absolute_uri(product.image.url) if product.image else '',
            'category': product.category.name if product.category else '',
        }
        products_data.append(product_data)

    data = {'products': products_data}
    return JsonResponse(data)

