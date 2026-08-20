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
    installment_options_list = serializers.SerializerMethodField()
    discount_percentage = serializers.ReadOnlyField()
    is_offer_active = serializers.ReadOnlyField()
    price = serializers.DecimalField(max_digits=15, decimal_places=2)
    installment_interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    sale_price = serializers.DecimalField(max_digits=15, decimal_places=2, allow_null=True, required=False)

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'category_name', 'brand', 'model', 'price', 'sale_price',
                  'installment_interest_rate', 'installment_options', 'installment_options_list', 'stock_quantity', 'is_active', 'is_on_sale', 'discount_percentage', 'is_offer_active', 'offer_start_date', 'offer_end_date', 'first_image')

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

    def get_installment_options_list(self, obj):
        return obj.get_installment_options_list()


class ProductDetailSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    first_image = serializers.SerializerMethodField()
    installment_options_list = serializers.SerializerMethodField()
    discount_percentage = serializers.ReadOnlyField()
    is_offer_active = serializers.ReadOnlyField()
    price = serializers.DecimalField(max_digits=15, decimal_places=2)
    installment_interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    sale_price = serializers.DecimalField(max_digits=15, decimal_places=2, allow_null=True, required=False)

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'brand', 'model', 'description',
                  'price', 'sale_price', 'installment_interest_rate', 'installment_options',
                  'installment_options_list', 'stock_quantity', 'min_stock_quantity',
                  'is_active', 'is_on_sale', 'discount_percentage', 'is_offer_active', 'offer_start_date', 'offer_end_date', 'is_low_stock', 'images', 'first_image', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at', 'is_low_stock')

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

    def get_installment_options_list(self, obj):
        return obj.get_installment_options_list()
