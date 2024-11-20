from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionSerializer
from django.shortcuts import get_object_or_404

# Create a new transaction (POST)
class TransactionCreateView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

# List transactions for a specific user (GET)
class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if not user_id:
            return Transaction.objects.none()  # Return an empty queryset if no user_id is provided
        return Transaction.objects.filter(user_id=user_id)

    def list(self, request, *args, **kwargs):
        user_id = self.request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "user_id query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        return super().list(request, *args, **kwargs)

# Retrieve or update a specific transaction (GET, PUT)
class TransactionDetailView(generics.RetrieveUpdateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def update(self, request, *args, **kwargs):
        transaction = self.get_object()
        status_value = request.data.get('status')

        # Validate status
        if status_value not in ['COMPLETED', 'FAILED']:
            return Response({"error": "Invalid status value"}, status=status.HTTP_400_BAD_REQUEST)

        # Update and save transaction status
        transaction.status = status_value
        transaction.save()

        serializer = self.get_serializer(transaction)
        return Response(serializer.data, status=status.HTTP_200_OK)