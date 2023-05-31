from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import MenuItem, Category, Cart, Order, OrderItem, UserProfile
from .serializers import MenuItemSerializer, CategorySerializer, CartSerializer, OrderSerializer, UserProfileSerializer
from .permissions import IsManager, IsDeliveryCrew
from django.contrib.auth.models import Group

class MenuItemListView(generics.ListAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    pagination_class = MenuItemPagination
    filterset_fields = ['category']
    ordering_fields = ['price']

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)

class AssignUserToManagerGroup(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = UserProfile.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        group = Group.objects.get(name='Manager')
        instance.user.groups.add(group)
        return Response({'message': 'User assigned to Manager group'}, status=status.HTTP_200_OK)
