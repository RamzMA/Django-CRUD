from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderItemSerializer, OrderSerializer, UserSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import date
from django.contrib.auth.models import User,Group
from rest_framework.decorators import api_view, permission_classes

"""
    Generics: allows for prebuilt GET,POST,EDIT,DELETE with LIST,CREATE,UPDATE,DELETE view
    IsAdmin: Built in function to check if user is user.staff
    IsAuthenticated: Built in function to check if user is logged in
    Queryset: Tells view what data to work with, for instance Category.objects.all() is all fields of category. Used for GET response.
    Serializer_class: Tells view what serializer to use to convert data to and from json
"""
class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
#MenuItem View
"""
    Ordering_fields: Ensures order is able to be sorted by price (e.g. /api/menu-items?ordering=price)
    search_fields: Ensures order is able to be searched (e.g. /api/menu-items?search=pizza)
"""
class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price']
    search_fields = ['title']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsAuthenticated()]

#SingleItem View
"""
    RetrieveUpdateDestroyAPIView: Gets, updates and deletes
"""
class SingleItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAdminUser()]

#Cart View
"""
    permission_classes: As we only need user to be logged in to get their cart and delete from their cart
    get_queryset: As instead of Cart.objects.all() which gets all carts which is a security risk
        - We filter for user=self.request.user which is the current user making the request
    delete: This filters for the user making the request and deletes the cart
        -returns response and status code
"""
class CartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    def delete(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response({'Message': 'Cart Cleared'}, status=200)
    
#Helpers for orders
"""
    is_manager: Filters user groups on django to see if manager group is on user
    is_delivery_crew: Filters user groups on django to see if deliver crew group is on user
"""
def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_delivery_crew(user):
    return user.groups.filter(name='Delivery Crew').exists()

#Orders classes
"""
    get_queryset: Gets user then
        -Checks if user is superuser created by django or is manager determined by helper
            -returns all orders if either one
        -Checks if delivery crew
            -If they are return all orders assigned to them
        -Otherwise return orders for user
    serializer: Converts order using OrderSerializer which is then use to return response with seralizer.data
"""
class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or is_manager(user):
            return Order.objects.all()
        if is_delivery_crew(user):
            return Order.objects.filter(delivery_crew=user)
        return Order.objects.filter(user=user)
    
    def create(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({'message': 'Cart is empty'}, status=400)
        
        total = sum(item.price for item in cart_items)
        order = Order.objects.create(
            user=request.user,
            total=total,
            date=date.today(),
            status=False
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                menuitem = item.menuitem,
                quantity = item.quantity,
                unit_price = item.unit_price,
                price = item.price
            )

        cart_items.delete()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=201)

#SingleOrder View
"""
    get_queryset: Same as OrderView, filters what each role can see
        - Admins and managers see all orders
        - Delivery crew only see orders assigned to them
        - Customers only see their own orders
        This prevents customers accessing other peoples orders

    update: Different roles can update different things
        - is_delivery_crew: Can only update status to mark as delivered
            - request.data.get('status', order.status) gets status from request
              if not provided falls back to current status so it doesnt get wiped
        - is_manager or superuser: Can assign delivery crew and update status
            - get_object_or_404 fetches the delivery crew user by their ID
            - if delivery crew id provided assign them to the order
        - Anyone else (customer): Gets 403 Forbidden

    delete: Only managers and admins can delete orders
        - Checks if user is superuser or manager
        - If neither returns 403 Forbidden
        - If allowed calls super().delete() which is the parent class delete method
          passing *args and **kwargs along with it

    get_object(): Built in DRF method that fetches single object based on pk in URL
        - Uses get_queryset so customers cant access other peoples orders
        - Returns 404 if object not found in queryset
"""
class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or is_manager(user):
            return Order.objects.all()
        if is_delivery_crew(user):
            return Order.objects.filter(delivery_crew=user)
        return Order.objects.filter(user=user)
    
    def update(self, request, *args, **kwargs):
        order = self.get_object()
        user = request.user

        if is_delivery_crew(user):
            order.status = request.data.get('status', order.status)
            order.save()
            return Response({'message': 'Order status updated'})
        
        if is_manager(user) or user.is_superuser:
            delivery_crew_id = request.data.get('delivery_crew')
            if delivery_crew_id:
                crew = get_object_or_404(User, pk=delivery_crew_id)
                order.delivery_crew = crew
            order.status = request.data.get('status', order.status)
            order.save()
            serializer = OrderSerializer(order)
            return Response(serializer.data)

        return Response({'message': 'Forbidden'}, status=403) 
    
    def delete(self, request, *args, **kwargs):
        if not request.user.is_superuser and not is_manager(request.user):
            return Response({'message': 'Forbidden'}, status=403)
        return super().delete(request, *args, **kwargs)

#Adding managers and delivery crew
"""
    managers: Handles GET and POST for manager group
        - GET: Returns list of all managers (admin only)
        - POST: Adds a user to the manager group by username (admin only)
        - get_object_or_404: If user doesnt exist returns 404 automatically
        - group.user_set.add(user): Django's built in way to add user to a group

    manager_detail: Handles DELETE for manager group
        - Removes a user from the manager group by their ID
        - group.user_set.remove(user): Django's built in way to remove user from group
"""
@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def managers(request):
    manager_group = Group.objects.get(name='Manager')

    if request.method == 'GET':
        managers = User.objects.filter(groups=manager_group)
        serializer = UserSerializer(managers, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        manager_group.user_set.add(user)
        return Response({'message': f'{username} added to Manager group'}, status=201)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def manager_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    manager_group = Group.objects.get(name='Manager')
    manager_group.user_set.remove(user)
    return Response({'message': f'{user.username} removed from Manager group'}, status=200)

"""
    delivery_crew: Handles GET and POST for delivery crew group
        - Checks if user is manager or superuser first, if not returns 403
        - GET: Returns list of all delivery crew
        - POST: Adds a user to the delivery crew group by username

    delivery_crew_detail: Handles DELETE for delivery crew group
        - Checks if user is manager or superuser first, if not returns 403
        - Removes a user from the delivery crew group by their ID
"""
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def delivery_crew(request):
    if not is_manager(request.user) and not request.user.is_superuser:
        return Response({'message': 'Forbidden'}, status=403)

    delivery_group = Group.objects.get(name='Delivery crew')

    if request.method == 'GET':
        crew = User.objects.filter(groups=delivery_group)
        serializer = UserSerializer(crew, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        delivery_group.user_set.add(user)
        return Response({'message': f'{username} added to Delivery crew'}, status=201)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delivery_crew_detail(request, pk):
    if not is_manager(request.user) and not request.user.is_superuser:
        return Response({'message': 'Forbidden'}, status=403)

    user = get_object_or_404(User, pk=pk)
    delivery_group = Group.objects.get(name='Delivery crew')
    delivery_group.user_set.remove(user)
    return Response({'message': f'{user.username} removed from Delivery crew'}, status=200)