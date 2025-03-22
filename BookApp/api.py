from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import BookModel
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookModel
        fields = '__all__'

    def validate(self, data):
        price = data['price']
        if price < 0:
            raise serializers.ValidationError('Price cannot be negative')
        return data

# @api_view(['GET'])
# def BookListApi(request):
#     #fetch from database

#     books = BookModel.objects.all()

#      #send response

#     serializer = BookModelSerializer(books, many = True)

#     return Response(serializer.data)

# @api_view(['POST'])
# def BookCreateApi(request):
#     data = request.data

#     serializer = BookModelSerializer(data = data)

#     if serializer.is_valid():
#         serializer.save()

#         return Response({
#             'message': 'Book created'
#         })
    
#     return Response(serializer.errors)

# @api_view(['PUT'])
# def BookUpdateAPi(request, id):

#     data = request.data

#     book = BookModel.objects.get(id = id)

#     serializer = BookModelSerializer(instance = book, data = data)

#     if serializer.is_valid():
#         serializer.save()

#         return Response(
#             {
#                 'message': 'Book updated'
#             }
#         )
#     return Response(serializer.errors)

# @api_view(['DELETE'])
# def BookDeleteApi(request, id):

#     book = BookModel.objects.get(id = id)

#     book.delete()

#     return Response({
#         'message': 'Book Deleted'
#     })

from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class CustomPagination(CursorPagination):
    # #query parameters: limit and offset
    # # ?limit = 2 & offset = 2
    # limit_query_param ='limit'
    # offset_query_param = 'offset'
    page_size = 2
    ordering = 'price'
    

class BookViewSet(ModelViewSet):
    queryset = BookModel.objects.all()
    serializer_class = BookModelSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def list(self, request):
        #GET
        #gets the user
        user = request.user
        #gets the books of current login user
        books = BookModel.objects.filter(author = user)
        page = self.paginate_queryset(books)
        #serialize the books to json
        serializer = self.get_serializer(page, many = True)

        return self.get_paginated_response(serializer.data)


    def create(self, request):
        #POST
        # data here is to get the name, price
        data = request.data

        #author
        user = request.user

        serializer = self.get_serializer(data = data)

        if serializer.is_valid():
            serializer.save(author = user)
        return Response({
            'message': 'Book Created'
        })
        

    def update(self, request, pk):
        #PUT
        #get the existing book
        book = BookModel.objects.get(id = pk)
        if book.author == request.user:
            #the data that needs to be replaced with the existing book
            data = request.data

            serializer = self.get_serializer(instance=book, data=data)

            if serializer.is_valid():
                serializer.save()
            
            return Response({
                'message': 'Book Updated'
            })
        return Response({
            'message': 'You are not the author of this book'
        })
      
    def destroy(self, request, pk):
        #DELETE
        book = BookModel.objects.get(id = pk)

        if book.author == request.user:

            book.delete()

            return Response({
                'message': "Book Deleted"
            })
        
        return Response({
            'message': 'You are not the author of this book'
        })
