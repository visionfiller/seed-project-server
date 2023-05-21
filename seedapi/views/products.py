from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from seedapi.models import Product
from seedapi.models import Category, Cart
from django.contrib.auth.models import User
from rest_framework.decorators import action




class ProductView(ViewSet):
    """Level up game types view"""
  
    def retrieve(self, request, pk):
        """Handle GET requests for single game type
        
        Returns:
            Response -- JSON serialized game type
        """
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

   
    def list(self, request):
       
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
       
        """
        products = Product.objects.all()
        category_id = request.query_params.get('category', None)
        if category_id is not None:
            category = Category.objects.get(pk=category_id)
            products = products.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle ProducT operations

        Returns
            Response -- JSON serialized game instance
        """
        category = Category.objects.get(pk=request.data['category'])
        product = Product.objects.create(
                name=request.data['name'],
                description = request.data['description'],
                price=request.data['price'],
                quantity=request.data['quantity'],
                category=category,
                image_path = request.data['image_path'],
                seller = request.auth.user
            )
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
       

    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        category = Category.objects.get(pk=request.data['category'])

        try:
            product = Product.objects.get(
                pk=pk, seller=request.auth.user)
            product.name = request.data['name']
            product.description = request.data['description']
            product.price = request.data['price']
            product.quantity = request.data['quantity']
            product.image_path = request.data['image_path']
            product.category = category
            product.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

       
    def destroy(self, request, pk):
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def add_to_cart(self, request, pk):
        """Add a product to the current users open order"""
        try:
            product = Product.objects.get(pk=pk)
            cart, _ = Cart.objects.get_or_create(
                customer=request.auth.user, completed_on=None, payment_type=None)
            cart.products.add(product)
            return Response({'message': 'product added'}, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    @action(methods=['delete'], detail=True)
    def remove_from_cart(self, request, pk):
            """Remove a product from the users open order"""
            try:
                product = Product.objects.get(pk=pk)
                cart = Cart.objects.get(
                    customer=request.auth.user, completed_on=None)
                cart.products.remove(product)
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            except (Product.DoesNotExist, Cart.DoesNotExist) as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)




    
        
class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'seller','price' 'description', 'quantity','image_path', 'category', 'favorited_by']



class ProductSerializer(serializers.ModelSerializer):
    """JSON serializer for Products
    """
   
    class Meta:
        model = Product
        fields = ('id', 'name', 'seller','price', 'description', 'quantity','image_path', 'category', 'favorited_by' )
        
        
        