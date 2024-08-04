from rest_framework.authentication import TokenAuthentication
from user.models import Token  # Import your custom Token model

class CustomTokenAuthentication(TokenAuthentication):
    model = Token  # Specify your custom Token model
