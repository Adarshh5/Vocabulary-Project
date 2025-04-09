from rest_framework.views import APIView
from rest_framework.response import Response
from vocabulary.models import Word, UserApiMode, UserApiPlan, UserIdentity
from .serializers import WordSerializer, GameSerializer, GameSerializer1, PaymentSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import TokenAuthentication

class WordLookupAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, word_name):
        words = Word.objects.filter(word_name__iexact=word_name)  
        if not words.exists():
            return Response({'error': 'Word not found'}, status=404)
        serializer = WordSerializer(words, many=True)
        return Response(serializer.data)


class GameAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
       
        word = Word.objects.order_by('?').first()
        if not word:
            return Response({"error": "No words available in the database"}, status=404)

        serializer = GameSerializer(word)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = GameSerializer1(data=request.data)
        if serializer.is_valid():
            id = serializer.validated_data['id']
            word_name = serializer.validated_data['word_name']
            word = get_object_or_404(Word, id=id)
            if word_name.lower() == word.word_name.lower():
                return Response({'msg': 'Word Correct'})
            else:
                return Response({'msg': 'Word Not Correct', 'correct_word': f'{word.word_name}'})
        else:
            return Response(serializer.errors, status=400)


class PaymentDoneViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def create(self, request, format=None):
        print(f"User: {request.user}")
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            IdentityOfUser = serializer.validated_data['IdentityOfUser']
            amount = serializer.validated_data['amount']
            try:
                user = UserIdentity.objects.get(identity=IdentityOfUser)
                activation = UserApiMode.objects.get(user=user.user)
                activation.api_mode = 'Active'
                activation.save()
                UserApiPlan.objects.create(
                    user=user.user,
                    api_plan='primium',
                    duration_in_days=1,
                    amount=amount
                )
                return Response({'msg': 'Account is activated'},status=200)
            except ObjectDoesNotExist as e:
                return Response({'msg': 'something error. Please contact support.', 'error': str(e)}, status=404)
            except Exception as e:
                return Response({'msg': 'An error occurred. Please try again later.', 'error': str(e)}, status=500)
        return Response({'msg': 'Data is not valid.', 'errors': serializer.errors}, status=400)