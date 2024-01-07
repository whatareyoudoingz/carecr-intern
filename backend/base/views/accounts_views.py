from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from base.models import User
from base.serializers import UserSerializer, UserSerializerWithToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from rest_framework import generics, status, permissions
from django.http import JsonResponse
from rest_framework.permissions import AllowAny

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k,v in serializer.items():
            data[k]=v
        return data
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def registerUser(request):
    data = request.data
    message = {"여기 통과함"}
    try:
        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            phone_number=data['phone_number'],
            password=make_password(data['password'])
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': '해당 이메일의 사용자가 이미 존재합니다.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request,pk):
    user=User.objects.get(id=pk)
    serializer=UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteUser(request, pk):
    userForDeletion=User.objects.get(id=pk)
    userForDeletion.delete()
    return Response('User was deleted')


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)

    data = request.data
    user.first_name = data['name']
    # user.username = data['email']
    user.phone_number = data['phone_number']

    if data['password'] != '':
        user.password = make_password(data['password'])
    user.save()
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

# 임시
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token

# @api_view(['POST'])
# # @authentication_classes([])
# @permission_classes([AllowAny])
# def find_user_id(request):
#     phone_number = request.POST.get('phone_number','')
#     print(phone_number)
#     print('실행되나??')
#     try:
#         user = User.objects.get(phone_number = phone_number)
#         return Response({'username':user.username})
#     except User.DoesNotExist:
#         return Response({'error':'입력하신 번호로 가입된 이메일을 찾을 수 없습니다.'})

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_password(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)

    data = request.data
    if (user.username == data['email'])&(user.phone_number == data['phone_number']):
        if data['password'] != '':
            user.password = make_password(data['password'])
        user.save()
    return Response(serializer.data)


# 다른 방식
class find_user_id(generics.CreateAPIView):
    print(generics.CreateAPIView)
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')

        try:
            user = User.objects.get(phone_number=phone_number)


            return JsonResponse({'e-mail': user.email}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)



# 로그인이랑 비슷한 방식 
# class MyTokenObtainWithEmailView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer

#     def post(self, request):
#         print('호출은 되냐?')
#         phone_number = request.data.get('phone_number', None)

#         if phone_number:
#             try:
#                 user = User.objects.get(phone_number=phone_number)

#                 serializer = UserSerializerWithToken(user)
#                 user_data = serializer.data
#                 return Response({'email': user_data['email']})
#             except User.DoesNotExist:
#                 return Response({'error': '해당 사용자를 찾을 수 없습니다.'}, status=400)
            
#         return Response({'error': '전화번호를 입력해주세요.'}, status=400)