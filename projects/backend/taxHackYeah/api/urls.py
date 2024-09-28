from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView, TokenRefreshView

from django.urls import path

from .views import ChatViewSet, SessionViewSet, MessageViewSet, AnswersViewSet

urlpatterns = [
path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('chat/', ChatViewSet.as_view({'get': 'list'})),
    path('chat/<int:pk>/', ChatViewSet.as_view({'get': 'retrieve'})),
    path('session/', SessionViewSet.as_view({'get': 'list'})),
    path('session/<int:pk>/', SessionViewSet.as_view({'get': 'retrieve'})),
    path('message/', MessageViewSet.as_view({'get': 'list'})),
    path('message/<int:pk>/', MessageViewSet.as_view({'get': 'retrieve'})),
    path('answers/', AnswersViewSet.as_view({'get': 'list'})),
    path('answers/<int:pk>/', AnswersViewSet.as_view({'get': 'retrieve'})),

]