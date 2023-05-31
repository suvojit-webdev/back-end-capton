from django.urls import reverse
from django.contrib.auth.models import User, Group
from rest_framework.test import APITestCase
from rest_framework import status
from .models import MenuItem, Category, Cart, Order, OrderItem, UserProfile
from .serializers import MenuItemSerializer, CategorySerializer, CartSerializer, OrderSerializer

class MenuItemTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Category 1')
        self.menuitem = MenuItem.objects.create(title='Item 1', price='10.00', category=self.category)
        self.url = reverse('menuitem-list')

    def test_get_menu_items(self):
        response = self.client.get(self.url)
        menuitems = MenuItem.objects.all()
        serializer = MenuItemSerializer(menuitems, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_menu_item(self):
        data = {
            'title': 'New Item',
            'price': '15.00',
            'category': self.category.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MenuItem.objects.count(), 2)

class CartTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.menuitem = MenuItem.objects.create(title='Item 1', price='10.00', category=Category.objects.create(title='Category 1'))
        self.cart_url = reverse('cart-list')

    def test_add_to_cart(self):
        data = {
            'menuitem': self.menuitem.id,
            'quantity': 2
        }
        response = self.client.post(self.cart_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cart.objects.count(), 1)

    def test_get_cart_items(self):
        Cart.objects.create(user=self.user, menuitem=self.menuitem, quantity=2)
        response = self.client.get(self.cart_url)
        cart_items = Cart.objects.filter(user=self.user)
        serializer = CartSerializer(cart_items, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

class OrderTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.menuitem = MenuItem.objects.create(title='Item 1', price='10.00', category=Category.objects.create(title='Category 1'))
        self.order_url = reverse('order-list')

    def test_place_order(self):
        Cart.objects.create(user=self.user, menuitem=self.menuitem, quantity=2)
        data = {'total': '20.00'}
        response = self.client.post(self.order_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

    def test_get_orders(self):
        Order.objects.create(user=self.user, total='20.00')
        response = self.client.get(self.order_url)
        orders = Order.objects.filter(user=self.user)
        serializer = OrderSerializer(orders, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

class UserProfileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.userprofile_url = reverse('userprofile-detail', args=[self.user.id])

    def test_update_userprofile(self):
        data = {'address': '123 Test Street'}
        response = self.client.patch(self.userprofile_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserProfile.objects.get(user=self.user).address, '123 Test Street')
