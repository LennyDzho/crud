from rest_framework import serializers
from demo.models import Product, Stock, StockProduct

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        queryset=Product.objects.all(),
        slug_field='title'
    )

    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address', 'positions']


    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for position_data in positions:
            StockProduct.objects.create(stock=stock, **position_data)
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions', [])
        stock = super().update(instance, validated_data)

        instance.positions.all().delete()
        for position_data in positions:
            StockProduct.objects.create(stock=stock, **position_data)

        return stock