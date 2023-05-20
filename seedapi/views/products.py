from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from seedapi.models import Product
from django.contrib.auth.models import User



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
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle ProducT operations

        Returns
            Response -- JSON serialized game instance
        """
        user = User.objects.get(pk=request.auth.user)
        serializer = CreateProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(seller=user)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    # def update(self, request, pk):
    #     """Handle PUT requests for a game

    #     Returns:
    #         Response -- Empty body with 204 status code
    #     """

    #     Product = Product.objects.get(pk=pk)
    #     Product.title = request.data["title"]
    #     Product.publication_date = request.data["publication_date"]
    #     Product.content = request.data["content"]
    #     Product.approved = request.data["approved"]
    #     print(request.data)
    #     category = Category.objects.get(pk=request.data["category"])
    #     Product.category = category

    #     all_tags = []
    #     tags = request.data["tags"]
    #     for tag in tags:
    #         Product_tag = Tag.objects.get(pk=tag)
    #         all_tags.append(Product_tag)
    #     Product.tags.set(all_tags)
    #     user = RareUser.objects.get(pk=request.data['user'])
    #     Product.user = user
    #     Product.save()

    #     return Response(None, status=status.HTTP_204_NO_CONTENT)
    def destroy(self, request, pk):
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)



    
        
class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'user', 'category', 'title', 'publication_date', 'image_url', 'content','approved', 'tags')



class ProductSerializer(serializers.ModelSerializer):
    """JSON serializer for Products
    """
   
    class Meta:
        model = Product
        fields = ('id', 'name', 'seller', 'description', 'quantity','image_path', 'category', 'favorited_by' )
        
        
        