from django.urls import path
from .views import ProductListView, filter_products, product_detail_view, product_list_view, submit_comment


app_name = 'products'


urlpatterns = [
    path('class', ProductListView.as_view(), name='product_list_class'),
    path('', product_list_view, name='list'),
    path('<slug:slug>/', product_detail_view, name='product-detail'),
    path('filter_products/', filter_products, name='filter_products'),
    path('submit-comment/<int:product_id>/', submit_comment, name='submit_comment'),

    # path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]