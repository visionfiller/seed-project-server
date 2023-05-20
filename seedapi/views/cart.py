from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from seedapi.models import Cart
from rest_framework.decorators import action




class CartView(ViewSet):
    """Level up game types view"""
  
    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
       
        """
        carts = Cart.objects.all()
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)

    

    def destroy(self, request, pk):
        cart = Cart.objects.get(pk=pk)
        cart.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


    @action(methods=['get'], detail=False)
    def current(self, request):
        """Get the user's current order"""
        try:
            cart = Cart.objects.get(
                completed_on=None, customer=request.auth.user)
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        except Cart.DoesNotExist:
            return Response({
                'message': 'You do not have a current order. Add a product to the cart to get started'},
                status=status.HTTP_404_NOT_FOUND
                )

        
  


class CartSerializer(serializers.ModelSerializer):
    """JSON serializer for Products
    """
   
    class Meta:
        model = Cart
        fields = ('id', 'payment_type', 'created_on', 'completed_on', 'customer', 'products')
       
        
        
        