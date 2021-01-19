from django.db.models import query
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.utils import serializer_helpers
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RoomSerializer, CreateRoomSerializer
from .models import Room


class RoomView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class CreateRoomView(APIView):
    # queryset = Room.objects.all()
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.guest_can_pause
            votes_to_skip = serializer.data.votes_skip
            host = self.request.session.session_key
            queryset = Room.objects.filter(host=host)

            # performs update action if already in the db
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
            else:
                room = Room(host=host, guest_can_pause=guest_can_pause,
                            votes_skip=votes_to_skip)
                room.save()

            return Response(RoomSerializer(room).data, status=status.status.HTTP_202_ACCEPTED)
