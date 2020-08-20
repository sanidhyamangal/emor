from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from .models import (User, Education, Experience, ProfileSkills, UserProject,
                     PriceAvailablity, DeveloperProfile, Notification)
from .serializers import (UserSerializer, EducationSerializer,
                          ExperienceSerializer, ProfileSkillsSerializer,
                          UserProjectSerializer, PriceAvailablitySerializer,
                          DeveloperProfileSerializer, NotificationSerializer,
                          DeveloperProfileSerializerRead)
from .permissions import (IsOwnerOrReadOnly, IsSuperAdminOrStaff,
                          IsOwnerAttributes)

from rest_framework_simplejwt.tokens import RefreshToken
from django.http import Http404
from rest_framework.exceptions import ValidationError


class DetailsAPI(APIView):
    """
    Retrieve, update or delete a objects instance instance.
    """
    model_class = None
    serializer_class = None
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    instance_name = None

    def get_object(self, pk):
        try:
            return self.model_class.objects.get(pk=pk)
        except self.model_class.DoesNotExist:
            raise ValidationError({
                'status': False,
                'message': f"failed to find {self.instance_name}",
                "data": {}
            })

    def get(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = self.serializer_class(obj)
        return Response(
            data={
                "status": True,
                "message": f"{self.instance_name} reterived sucessfully",
                "data": serializer.data
            })

    def put(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = self.serializer_class(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={
                    "status": True,
                    "message": f"{self.instance_name} updated sucessfully",
                    "data": serializer.data
                })
        return Response(data={
            "status": False,
            "message": f"{self.instance_name} update failed",
            "data": serializer.errors
        },
                        status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = self.serializer_class(obj,
                                           data=request.data,
                                           partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={
                    "status": True,
                    "message": f"{self.instance_name} updated sucessfully",
                    "data": serializer.data
                })
        return Response(data={
            "status": False,
            "message": f"{self.instance_name} update failed",
            "data": serializer.errors
        },
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response(data={
            "status": True,
            "message": f"{self.instance_name} deleted sucessfully",
            "data": {}
        },
                        status=status.HTTP_200_OK)


class UserAttributeList(APIView):
    """
    A Base API class for listing attributes based on user
    """
    model_class = None
    serializer_class = None
    instance_name = None
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, userid, format=None):
        if self.model_class.objects.filter(user__uid=userid).exists():
            obj = self.model_class.objects.filter(user__uid=userid)
            serializer = self.serializer_class(obj, many=True)
            response_data = {
                'status': True,
                'message': f'{self.instance_name} reterieved sucessfully',
                'data': serializer.data
            }
            return Response(response_data)
        else:
            response_data = {
                'status': False,
                'message': 'error in user key',
                'data': {}
            }
            return Response(response_data)


class CreateAttribute(APIView):
    """
    custom class to save data
    """

    model_class = None
    serializer_class = None
    instance_name = None
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "status": True,
                'message': f'{self.instance_name} created',
                'data': serializer.data
            }
            return Response(data=response_data)
        response_data = {
            'status': False,
            'message': f'error creating {self.instance_name}',
            'data': serializer.errors
        }
        return Response(data=response_data, status=404)


class UserList(APIView):
    """
    A custom class to signup users
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'message': 'signup successfully',
                'data': {
                    "uid": serializer.data['uid']
                }
            }
            return Response(data=response_data)
        response_data = {
            'message': 'user with this email already exist',
            'data': {}
        }
        return Response(data=response_data, status=404)


# class UserList(generics.ListCreateAPIView):
#     """
#     A custom user model views to create and list all the users
#     """

#     serializer_class = UserSerializer
#     queryset = User.objects.all()

#     def get_permissions(self):
#         if self.request.method == "GET":
#             permission_classes = [
#                 IsSuperAdminOrStaff, permissions.IsAuthenticated
#             ]
#         else:
#             permission_classes = []
#         return [permission() for permission in permission_classes]


class UserDetails(DetailsAPI):
    """
    Retrieve, update or delete a User instance.
    """
    # permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    model_class = User
    serializer_class = UserSerializer
    instance_name = "user"


class DeveloperProfileList(CreateAttribute):
    """
    """

    model_class = DeveloperProfile
    serializer_class = DeveloperProfileSerializer
    instance_name = "developer profile"

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [
                permissions.IsAuthenticated, IsOwnerAttributes
            ]
        else:
            permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]


class DeveloperProfileDetails(DetailsAPI):
    model_class = DeveloperProfile
    serializer_class = DeveloperProfileSerializer
    instance_name = "developer profile"

    def get_object(self, pk):
        try:
            return self.model_class.objects.get(user__uid=pk)
        except self.model_class.DoesNotExist:
            raise ValidationError({
                'status': False,
                'message': f"failed to find {self.instance_name}",
                "data": {}
            })

    def get(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = DeveloperProfileSerializerRead(obj)
        return Response(
            data={
                "status": True,
                "message": f"{self.instance_name} reterived sucessfully",
                "data": serializer.data
            })

    def put(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = self.serializer_class(obj, data=request.data)

        user_data = {}
        if request.data.get("first_name"):
            user_data["first_name"] = request.data.get("first_name")
        if request.data.get("last_name"):
            user_data["last_name"] = request.data.get("last_name")

        if User.objects.filter(pk=pk).exists():
            user_obj = User.objects.get(pk=pk)
            user_serializer = UserSerializer(user_obj,
                                             data=user_data,
                                             partial=True)

            if user_serializer.is_valid():
                user_serializer.save()

        if serializer.is_valid():
            serializer.save()
            return Response(
                data={
                    "status": True,
                    "message": f"{self.instance_name} updated sucessfully",
                    "data": serializer.data
                })
        return Response(data={
            "status": False,
            "message": f"{self.instance_name} update failed",
            "data": serializer.errors
        },
                        status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = self.serializer_class(obj,
                                           data=request.data,
                                           partial=True)

        user_data = {}
        if request.data.get("first_name"):
            user_data["first_name"] = request.data.get("first_name")
        if request.data.get("last_name"):
            user_data["last_name"] = request.data.get("last_name")

        if User.objects.filter(pk=pk).exists():
            user_obj = User.objects.get(pk=pk)
            user_serializer = UserSerializer(user_obj,
                                             data=user_data,
                                             partial=True)

            if user_serializer.is_valid():
                user_serializer.save()

        if serializer.is_valid():
            serializer.save()
            return Response(
                data={
                    "status": True,
                    "message": f"{self.instance_name} updated sucessfully",
                    "data": serializer.data
                })
        return Response(data={
            "status": False,
            "message": f"{self.instance_name} update failed",
            "data": serializer.errors
        },
                        status=status.HTTP_400_BAD_REQUEST)


class EducationCreate(CreateAttribute):
    """
    """
    model_class = Education
    serializer_class = EducationSerializer
    instance_name = "education"


class UserEductionList(UserAttributeList):
    """
    Custom user list view for the education
    """
    model_class = Education
    serializer_class = EducationSerializer
    instance_name = "education"


class EducationDetails(DetailsAPI):
    """
    Retrieve, update or delete a Eduction instance.
    """
    model_class = Education
    serializer_class = EducationSerializer
    instance_name = "education"
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class ExperienceCreate(CreateAttribute):
    """
    A Generic View class for creating experience
    """

    model_class = Experience
    serializer_class = ExperienceSerializer
    instance_name = "experience"


class UserExperienceList(UserAttributeList):
    """
    Custom user list view for the experience
    """

    model_class = Experience
    serializer_class = ExperienceSerializer
    instance_name = "experience"


class ExperienceDetail(DetailsAPI):
    """
    """

    model_class = Experience
    serializer_class = ExperienceSerializer
    instance_name = "experience"


class ProfileSkillsCreate(CreateAttribute):
    """
    A Generic View class for creating ProfileSkills
    """

    model_class = ProfileSkills
    serializer_class = ProfileSkillsSerializer
    instance_name = "profile skills"


class UserProfileSkillsList(UserAttributeList):
    """
    Custom user list view for the ProfileSkills
    """

    model_class = ProfileSkills
    serializer_class = ProfileSkillsSerializer
    instance_name = "profile skills"


class ProfileSkillsDetail(DetailsAPI):
    """
    """
    model_class = ProfileSkills
    serializer_class = ProfileSkillsSerializer
    instance_name = "profile skills"


class UserProjectCreate(CreateAttribute):
    """
    A Generic View class for creating UserProject
    """

    model_class = UserProject
    serializer_class = UserProjectSerializer
    instance_name = "user project"


class UserProjectList(UserAttributeList):
    """
    Custom user list view for the UserProject
    """

    model_class = UserProject
    serializer_class = UserProjectSerializer
    instance_name = "user projects"


class UserProjectDetail(DetailsAPI):
    """
    """

    model_class = UserProject
    serializer_class = UserProjectSerializer
    instance_name = "profile skills"


class PriceAvailablityCreate(CreateAttribute):
    """
    A Generic View class for creating PriceAvailablity
    """

    model_class = PriceAvailablity
    serializer_class = PriceAvailablitySerializer
    instance_name = "price availablity"


class UserPriceAvailablityList(UserAttributeList):
    """
    Custom user list view for the PriceAvailablity
    """

    model_class = PriceAvailablity
    serializer_class = PriceAvailablitySerializer
    instance_name = "price availablity"


class PriceAvailablityDetail(DetailsAPI):
    """
    """

    model_class = PriceAvailablity
    serializer_class = PriceAvailablitySerializer
    instance_name = "price availablity"


class AuthorizeUser(APIView):
    def post(self, request):
        if User.objects.filter(email=request.data.get('email')).exists():
            user = User.objects.get(email=request.data.get('email'))

            if user.check_password(request.data.get('password')):
                token = RefreshToken.for_user(user)
                user = UserSerializer(user)

                self.__populate_notification_data(user, request)

                response_data = {
                    'message': 'login sucessfull',
                    'data': {
                        'user': user.data,
                        'token': str(token.access_token)
                    }
                }
                return Response(data=response_data)
            else:
                response_data = {'message': 'password is invalid', 'data': {}}
                return Response(data=response_data, status=404)

        else:
            response_data = {'message': 'email id is invalid', 'data': {}}
            return Response(data=response_data, status=404)

    def __populate_notification_data(self, user: dict, request) -> None:

        # get user data for notification type
        notification = Notification.objects.filter(
            user__uid=user.data['uid']).filter(
                userType=request.data.get('userType'))

        request.data['user'] = user.data['uid']

        if notification.exists():
            notification = Notification.objects.get(
                pk=notification.values('uid')[0]['uid'])
            serializer = NotificationSerializer(notification,
                                                data=request.data)
        else:
            serializer = NotificationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()


class CustomerFeed(APIView):

    # get developers
    def get(self, request, search_term="", format=None):

        try:
            user_ids = []
            for user in ProfileSkills.objects.filter(title__icontains=str(
                    search_term).strip().replace('-', ' ')).values('user'):

                user_ids.append(user['user'])

            return Response(
                data={
                    "status": True,
                    "message": "users list reterived sucessfully",
                    "data": user_ids
                })
        except Exception:
            return Response(data={
                "status": False,
                "message": "users list reterived failed",
                "data": {}
            },
                            status=status.HTTP_400_BAD_REQUEST)
