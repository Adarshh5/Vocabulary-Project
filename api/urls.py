
from django.urls import path
from .views import WordLookupAPIView, GameAPIView,PaymentDoneViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView,  TokenVerifyView

urlpatterns = [
    path('word-lookup/<str:word_name>/', WordLookupAPIView.as_view(), name='word-lookup'),
    path('Game/', GameAPIView.as_view(), name='Game'),
    path('PaymentDone/', PaymentDoneViewSet.as_view({'post': 'create'}), name='PaymentDone'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verifytoken/', TokenVerifyView.as_view(), name='token_verify'),
]
