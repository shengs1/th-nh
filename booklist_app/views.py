import sys
sys.setrecursionlimit(2000)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
from rest_framework import viewsets

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'All Books': '/books/',
        'Search by Category': '/books/?category=category_name',
        'Search by Subcategory': '/books/?subcategory=category_name',
        'Add Book': '/books/create/',
        'Update Book': '/books/update/id/',
        'Delete Book': '/books/id/delete/',
    }
    return Response(api_urls)
    
@api_view(['GET'])
def view_book(request):
    # Check if there are query parameters
    if request.query_params:
        filtered_books = Book.objects.filter(**request.query_params.dict())
    else:
        # No query parameters, get all books
        filtered_books = Book.objects.all()

    if filtered_books:
        serializer = BookSerializer(filtered_books, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


from rest_framework import status
 

@api_view(['POST'])
def add_book(request):
    # Deserialize the incoming JSON data
    book_serializer = BookSerializer(data=request.data)

    # Validate the data
    if book_serializer.is_valid():
        # Check if a book with the same title already exists
        existing_book = Book.objects.filter(title=request.data['title']).first()
        if existing_book:
            return Response({"error": "A book with this title already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new book if it doesn't exist
        book_serializer.save()
        return Response(book_serializer.data, status=status.HTTP_201_CREATED)

    # Return validation errors if the data is invalid
    return Response(book_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_book(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
@api_view(['DELETE'])
def delete_book(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        book.delete()
        return Response({"message": "Book deleted successfully"}, status=status.HTTP_204_NO_CONTENT)