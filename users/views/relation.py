from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.serializers import FollowUserSerializer
from users.models import FollowUser
from users.models import Person


class FollowUserView(generics.ListCreateAPIView):
    '''
    View for  user

    '''
    permission_classes = [IsAuthenticated]
    serializer_class = FollowUserSerializer
    queryset = FollowUser.objects.all()

    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            print(serializer.erros)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()(queryset, many=True)
        for i in serializer.data:
            print(Person.objects.get(pk=i["follower"]))
        return Response(serializer.data)


class FollowersView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowUserSerializer
    queryset = FollowUser.objects.all()

    def get(self, request, pk):
        queryset = self.get_queryset().filter(
            following=Person.objects.get(pk=pk))
        serializer = self.get_serializer_class()(queryset, many=True)
        return Response(serializer.data)


class FollowingView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowUserSerializer
    queryset = FollowUser.objects.all()

    def get(self, request, pk):
        queryset = self.get_queryset().filter(
            follower=Person.objects.get(pk=pk))
        serializer = self.get_serializer_class()(queryset, many=True)
        return Response(serializer.data)


class DeleteFollow(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowUserSerializer
    queryset = FollowUser.objects.all()

    def get(self, request, id1, id2):
        queryset = self.get_queryset().filter(
            follower=Person.objects.get(pk=id1),
            following=Person.objects.get(pk=id2))
        serializer = self.get_serializer_class()(queryset, many=True)
        return Response(serializer.data)

    def delete(self, request, id1, id2):
        return Response(status=status.HTTP_204_NO_CONTENT)
