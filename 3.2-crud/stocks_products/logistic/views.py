from rest_framework.viewsets import ModelViewSet

from logistic.models import Product, Stock, StockProduct
from logistic.serializers import ProductSerializer, StockSerializer

from rest_framework.filters import SearchFilter
from django.db.models import Prefetch
# from rest_framework.pagination import PageNumberPagination


# class StandardResultsSetPagination(PageNumberPagination):
#     page_size = 10
#     page_size_query_param = 'page_size'
#     max_page_size = 100


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter]
    search_fields = ["title", "description"]


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.none()
    serializer_class = StockSerializer
    # pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter]
    search_fields = ["positions__product__title", "positions__product__description"]

    def get_queryset(self):
        product_id = self.request.query_params.get('products')

        if product_id:
            filtered_positions = StockProduct.objects.filter(product_id=product_id)
            
            return Stock.objects.filter(
                positions__product_id=product_id
            ).prefetch_related(
                Prefetch('positions', queryset=filtered_positions)
            ).distinct()

        return Stock.objects.all()