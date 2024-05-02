from rest_framework import serializers

from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='get_name_display')

    class Meta:
        model = Category
        fields = ['name']


class ProductSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(many=True)
    category = serializers.SerializerMethodField()
    stock = serializers.IntegerField(min_value=0)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock', 'category']

    @staticmethod
    def get_category(obj):
        return [category.get_name_display() for category in obj.category.all()]

    def update(self, instance, validated_data):
        instance.stock = validated_data.get('stock', instance.stock)

        instance.save()
        return instance


class ProductCreationSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    stock = serializers.IntegerField(min_value=0)

    class Meta:
        model = Product
        fields = ['name', 'price', 'stock', 'category']

    @staticmethod
    def get_category(obj):
        return [category.get_name_display() for category in obj.category.all()]

    def create(self, validated_data):
        category_ids = validated_data.pop('category', [])  # Pop 'category' from validated_data
        product = Product.objects.create(**validated_data)  # Create Product instance

        # Associate Category objects with the Product
        for category_id in category_ids:
            category = Category.objects.get(pk=category_id)
            product.category.add(category)

        return product


class ProductShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']


class ProductListSerializer(serializers.ListSerializer):
    child = ProductShortSerializer()
