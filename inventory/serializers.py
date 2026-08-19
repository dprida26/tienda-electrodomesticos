from rest_framework import serializers
from .models import Product, ProductCategory, ProductImage


class ProductCategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = ProductCategory
        fields = ('id', 'code', 'name', 'description', 'order', 'is_active', 'product_count')

    def get_product_count(self, obj):
        return obj.products.filter(is_active=True).count()


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'image_url', 'order')

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            url = obj.image.url
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return None


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    first_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'category_name', 'brand', 'model', 'price',
                  'stock_quantity', 'is_active', 'first_image')

    def get_first_image(self, obj):
        first_image = obj.images.first()
        if first_image:
            request = self.context.get('request')
            if first_image.image and hasattr(first_image.image, 'url'):
                url = first_image.image.url
                if request is not None:
                    return request.build_absolute_uri(url)
                return url
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    price_display = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'brand', 'model', 'description',
                  'price', 'price_display', 'stock_quantity', 'min_stock_quantity',
                  'is_active', 'is_low_stock', 'images', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at', 'is_low_stock')

    def get_price_display(self, obj):
        return f"Gs. {obj.price:,.2f}".replace(',', '.')
