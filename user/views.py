from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
# from user.api_permissions import CustomTokenAuthentication
# from rest_framework import TokenAuthentication
from .models import Token, Userprofile
# from project.utils import utc_today, validate_password
import json
from django.views.decorators.csrf import csrf_exempt

class UserLoginapi(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = tuple()

    def get(self, request):
        response_dict = {"status": False}
        response_dict["logged_in"] = bool(request.user.is_authenticated)
        response_dict["status"] = True
        return Response(response_dict, HTTP_200_OK)

    def post(self, request):
        response_dict = {"status": False, "token": None, "redirect": False}
        password = request.data.get("password")
        username = request.data.get("username")

        try:
            t_user = Userprofile.objects.get(username=username)
        except Userprofile.DoesNotExist:
            response_dict["reason"] = "No account found for this username. Please signup."
            return Response(response_dict, HTTP_200_OK)

        # blocked_msg = "This account has been blocked. Please contact admin."
        # today = utc_today()
        authenticated = authenticate(username=t_user.username, password=password)
        if not authenticated:
            response_dict["reason"] = "Invalid credentials."
            return Response(response_dict, HTTP_200_OK)

        user = t_user


        session_dict = {"real_user": authenticated.id}
        token, _ = Token.objects.get_or_create(
            user=user, defaults={"session_dict": json.dumps(session_dict)}
        )
        login(request, user, "django.contrib.auth.backends.ModelBackend")
        response_dict["session_data"] = {
            "user_id": user.id,
            "user_type": user.user_type,
            "token": token.key,
            "username": user.username,
            "name": user.first_name,
            "status": user.status,
        }
        response_dict["token"] = token.key
        response_dict["status"] = True
        return Response(response_dict, HTTP_200_OK)


from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class UserLogoutAPI(APIView):
    permission_classes = (IsAuthenticated,)
    @csrf_exempt
    def post(self, request):
        response_dict = {"status": False}
        
        try:
            # Get the user's token and delete it
            token = Token.objects.get(user=request.user)
            token.delete()
            
            # Log the user out
            logout(request)
            
            response_dict["status"] = True
            response_dict["message"] = "Successfully logged out."
            return Response(response_dict, HTTP_200_OK)
        except Token.DoesNotExist:
            response_dict["message"] = "Token does not exist or already deleted."
            return Response(response_dict, HTTP_400_BAD_REQUEST)