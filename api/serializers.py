from rest_framework import serializers
from vocabulary.models import Word

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['word_name', 'definition', 'part_of_speech', 'hindi_meaning']




class GameSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()  
    class Meta:
        model = Word
        fields = ['id', 'word_name', 'definition']



class GameSerializer1(serializers.ModelSerializer):
    id = serializers.IntegerField()  
    class Meta:
        model = Word
        fields = ['id', 'word_name']

class PaymentSerializer(serializers.Serializer):
    PojectIdentity = serializers.CharField(max_length=10)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    IdentityOfUser = serializers.CharField()