from rest_framework import serializers
# from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from base.models import User, Post, Review

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    # phone_number = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id','_id','username','email','name','isAdmin', 'phone_number']
        
    def get__id(self, obj):
        return obj.id
    def get_isAdmin(self, obj): 
        return obj.is_staff
    def get_name(self, obj):
        name = obj.first_name
        if name == ' ':
            name = obj.email
        return name


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin', 'phone_number','token']

    def get_token(self, obj):
        if hasattr(obj, 'id'):
            token = RefreshToken.for_user(obj)
            return str(token.access_token)
        return None
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__' 
        
class PostSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = '__all__'

#ID/비밀번호 찾기
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# from rest_framework_jwt.serializers import RefreshJSONWebTokenSerializer, VerifyJSONWebTokenSerializer
# from rest_framework_jwt.views import RefreshJSONWebToken, VerifyJSONWebToken
# #jwt 인증 관련 시리얼라이저 오버라이딩
# RefreshJSONWebTokenSerializer._declared_fields.pop('token')
# VerifyJSONWebTokenSerializer._declared_fields.pop('token')

# class VerifyJSONWebTokenSerializerCookieBased(VerifyJSONWebTokenSerializer):
#     def validate(self, data):
#         data['token'] = JSONWebTokenAuthentication().get_jwt_value(self.context['request'])
#         return super(VerifyJSONWebTokenSerializerCookieBased, self).validate(data)

# class RefreshJSONWebTokenSerializerCookieBased(RefreshJSONWebTokenSerializer):
#     def validate(self, data):
#         data['token'] = JSONWebTokenAuthentication().get_jwt_value(self.context['request'])
#         return super(RefreshJSONWebTokenSerializerCookieBased, self).validate(data)

# VerifyJSONWebToken.serializer_class = RefreshJSONWebTokenSerializerCookieBased
# RefreshJSONWebToken.serializer_class = RefreshJSONWebTokenSerializerCookieBased

# class FindIDPasswordSerializer(serializers.Serializer):
#     IDorPassword=serializers.RegexField(regex=r"id|password")
#     username=serializers.CharField(min_length=8, max_length=15, allow_blank=True)
#     email=serializers.EmailField()
