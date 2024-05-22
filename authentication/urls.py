from django.urls import path
from .views import UserSignUp, UserSignIn, GetMe

urlpatterns = [
	path('signup/', UserSignUp.as_view(), name='signup'),
	path('signin/', UserSignIn.as_view(), name='signin'),
	path('me/', GetMe.as_view(), name='me'),
]
