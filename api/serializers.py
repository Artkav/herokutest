from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.utils.translation import gettext_lazy as _
from users.utils import send_email_for_verify
from rest_framework import serializers
from app.models import Task
from datetime import date as dt

User = get_user_model()

'''Custom serializer for authenticate user in DRF, verify email and blocked user'''


class CustomAuthTokenSerializer(AuthTokenSerializer):
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            elif not user.email_verify:
                send_email_for_verify(self.context.get('request'), user)
                msg = _('Check your email, and verify it!')
                raise serializers.ValidationError(msg, code='authorization')
            elif user.blocked:
                msg = _('You are blocked')
                raise serializers.ValidationError(msg, code='login_blocked')

        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('name', 'short_text', 'status', 'deadline_date', 'full_text')
        read_only_fields = ('status',)
        extra_kwargs = {"full_text": {"write_only": True}}

    @staticmethod
    def validate_deadline_date(value):
        if value < dt.today():
            raise serializers.ValidationError("Deadline must be later than today")
        return value


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'position_in_company', 'email',)
