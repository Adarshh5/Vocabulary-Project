from django.shortcuts import render, redirect
from .models import Word, UserSessionData, UserApiMode, UserApiPlan, UserIdentity,OfflineCoaching
from django.core.paginator import Paginator
from django.core.paginator import Paginator
from django.views import View
from .forms import registrationFrom, FilterForm, OfflineCoachingForm, CoachingFilterForm
from django.contrib import messages
from django.contrib.auth import login
from .forms import LoginForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
import requests
import json
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import random
from django.shortcuts import get_object_or_404
import string

class registration(View):
    def get(self, request):
        form  = registrationFrom()
        return render(request, 'vocabulary/registration.html', {'form':form})
    def post(self, request):
        form  = registrationFrom(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Successfully.')
            form.save()
        return render(request, 'vocabulary/registration.html', {'form':form})


    
def home(request):
   
    l = []
    word = Word.objects.all().order_by('id')
    part_of_speech = request.GET.get('part_of_speech')
    level = request.GET.get('level')
   

    if part_of_speech: 
        if part_of_speech == "Verb":
           word = word.filter(part_of_speech="Verb").order_by('id')
        elif part_of_speech == "Phrasal Verb":
            word = word.filter(part_of_speech="Phrasal Verb").order_by('id')
        elif  part_of_speech == "Noun":
            word = word.filter(part_of_speech="Noun").order_by('id')
        elif part_of_speech == "Adjective":
            word = word.filter(part_of_speech="Adjective").order_by('id')
        elif part_of_speech == "Adverb":
            word = word.filter(part_of_speech="Adverb").order_by('id')


    if level :
        if level == "Basic":
           word =word.filter(level="Basic").order_by('id')
        elif level == "Intermediate":
           word = word.filter(level="Intermediate").order_by('id')
        elif level == "Advanced":
           word = word.filter(level="Advanced").order_by('id')
       
    paginator = Paginator(word, 6, orphans=1)
    page_number = request.GET.get('page',1)
    page_obj = paginator.get_page(page_number)
    form = FilterForm(request.GET or None)
    return render(request, "vocabulary/home.html", {'page_obj': page_obj, 'total': word.count(), 'form': form})


def full_page(request, pk):
    word = Word.objects.get(id=pk)
    if request.user.is_authenticated :
        containers = list(request.session['Vocab_Container'].keys())
        if containers:
           return render(request, "vocabulary/full_page.html", {'word': word, 'containers': containers})
        else:
            return render(request, 'vocabulary/full_page.html', {'word':word})
    else:
        return render(request, 'vocabulary/full_page.html', {'word':word})


def search(request):
    query = request.GET.get('query', None)
    mydata = None
    if query is not None:
        if len(query) == 1:
          mydata = Word.objects.filter(word_name__startswith=query)
        if len(query) >= 2:
          mydata = Word.objects.filter(word_name=query) | Word.objects.filter(Synonyms__icontains=query) | Word.objects.filter(word_name__icontains=query)
        return render(request, 'vocabulary/basic.html',{'words':mydata})

def basic(request):
   words = Word.objects.filter(level="basic")
   return render(request, 'vocabulary/basic.html', {'words':words} )

def intermediate(request):
   words = Word.objects.filter(level="intermediate")
   return render(request, 'vocabulary/basic.html', {'words':words} )


def advanced(request):
   words = Word.objects.filter(level="advanced")
   return render(request, 'vocabulary/basic.html', {'words':words} )
  

    

@login_required
def SaveItems(request):
  if 'Vocab_Container' not in request.session:
        request.session['Vocab_Container'] = {}

  container = request.GET.get('container_name')
 
  if container:
    if container not in request.session['Vocab_Container']:
        request.session['Vocab_Container'][container] = []
        request.session.modified = True

  containers = list(request.session['Vocab_Container'].keys())


  return render(request, 'vocabulary/SaveItems.html', {'containers': containers})


def DeleteContainer(request):
    if request.method == "POST":
        container_name = request.POST.get('container_name')
        if 'Vocab_Container' in request.session:
            request.session['Vocab_Container'].pop(container_name, None)
            request.session.modified = True
   
    return redirect('SaveItems')

@login_required
def SaveWord(request):
    if request.method== 'POST':
       box =  request.POST.get('box')
       WordId = request.POST.get('WordId')
       WordId = int(WordId)
       if box and WordId:
        if WordId not in request.session['Vocab_Container'][box]:
            request.session['Vocab_Container'][box].append(WordId)
            request.session.modified = True
    
    return redirect(f'/full_page/{WordId}/')


@login_required
def onebox(request, container):
    if request.method == 'GET':
      items = request.session['Vocab_Container'][container]
      SelectedWord = Word.objects.filter(id__in=items)
        
      return render(request, 'vocabulary/onebox.html', {"SelectedWord": SelectedWord, 'container_name': container})
      
      
    
@login_required
def DeleteWordFormContainer(request, container_name, pk):
    if container_name and pk:
        word_list = request.session.get('Vocab_Container')
        if container_name in word_list:
            word_list[container_name].remove(pk) 
            request.session.modified = True
        return redirect(f'/onebox/{container_name}/')
    else:
        return redirect('/')  




def login_view(request):
    if request.user.is_authenticated:
        return redirect('SaveItems')

    if request.method == "GET":
        form = LoginForm()
        return render(request, 'vocabulary/login.html', {'form': form})

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()  
            login(request, user) 
            try:
                session_data = UserSessionData.objects.get(user=user)
                request.session['Vocab_Container'] = session_data.data
                request.session.modified = True
            except UserSessionData.DoesNotExist:
                request.session['Vocab_Container'] = {}

            return redirect('SaveItems')
        else:
            messages.error(request, "Invalid Username or Passowrd")

    return render(request, 'vocabulary/login.html', {'form': form})



def custom_logout(request):
    if request.user.is_authenticated:
       
        vocab_container = request.session.get('Vocab_Container', {})
        if vocab_container:
            session_data, created = UserSessionData.objects.get_or_create(user=request.user)
            session_data.data = vocab_container
            session_data.save()

    request.session.flush()
    logout(request)
    return redirect('login')




class APISection(View):
    def get(self, request):
         usr = request.user
         try:
            api_mode_obj = UserApiMode.objects.get(user=usr)
            api_plan_obj = UserApiPlan.objects.filter(user=usr).last()
            if api_plan_obj and api_plan_obj.is_expired():
                api_mode_obj.api_mode = UserApiMode.DEACTIVE
                api_mode_obj.save()

            if api_mode_obj.api_mode == UserApiMode.DEACTIVE:
                return redirect('ApiPlan')

            return render(request, 'vocabulary/APISection.html')

         except UserApiMode.DoesNotExist:
            return redirect('ApiPlan')
        
    def post(self, request):
        user = request.user
        context = {}
        if request.method == "POST" and "generate_tokens" in request.POST:
            refresh = RefreshToken.for_user(user)
            context["access_token"] = str(refresh.access_token)
            context["refresh_token"] = str(refresh)
            access_lifetime = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]
            context["access_expiry"] = access_lifetime.total_seconds() // 60
            context["created_at"] = refresh.current_time.strftime("%Y-%m-%d %H:%M:%S")
        if request.method == "POST" and "refresh_token" in request.POST:
            submitted_refresh_token = request.POST.get("refresh_token")
            try:
                refresh = RefreshToken(submitted_refresh_token)
                context["access_token"] = str(refresh.access_token)
                context["refresh_token"] = str(refresh)  
                access_lifetime = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]
                context["access_expiry"] = access_lifetime.total_seconds() // 60
                context["message"] = "Tokens refreshed successfully!"
            except TokenError:
                context["error"] = "Invalid or expired refresh token."

        return render(request, "vocabulary/APISection.html", context)
    

"""Generate a random token with special characters."""

def generate_token(length=10):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    token = ''.join(random.choices(characters, k=length))
    return token

BASE_URL = "http://127.0.0.1:8000"
class ApiPlan(View):
    def get(self, request):
        usr = request.user
        try:
            IdentityToken = UserIdentity.objects.get(user=usr)
            mode = UserApiMode.objects.get(user=usr)
        except ObjectDoesNotExist:
            indentity = generate_token()
            UserIdentity.objects.create(user=usr, identity= indentity)
            UserApiMode.objects.create(user=usr, api_mode='Deactive')
        finally:
            return render(request, 'vocabulary/ApiPlan.html')
    
    def post(self, request):
        upi_id = request.POST.get('upiId')
        PojectIdentity = 'I*#k=b&tG'
        amount = 500.00
        name = 'VocabVault'
        usr = request.user
        IdentityToken = UserIdentity.objects.get(user=usr)
        IdentityOfUser = IdentityToken.identity
        data = {
            'upi_id': upi_id,
            'PojectIdentity': PojectIdentity,
            'amount': amount,
            'name': name,
            'IdentityOfUser': IdentityOfUser,
        }
        json_data = json.dumps(data)
        token = "d568ab9c9cc68325617770596741637bb063eb05"
        URL = "http://127.0.0.1:8000/PaybuddyAPI/"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Token {token}',
        }
        try:
            r = requests.post(url=URL, headers=headers, data=json_data)

            if r.status_code == 200:
                print(r.status_code)
                messages.success(request, f"{r.json().get('msg')}")
                return redirect('ApiPlan')  
            else:
                error_msg = r.json().get('error')
                messages.error(request, f"Payment failed: {r.json().get('msg')}")
                return redirect('ApiPlan')  
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            messages.error(request, "An HTTP error occurred while processing your request.")
        except requests.exceptions.JSONDecodeError:
            print(f"Invalid JSON response: {r.text}")
            messages.error(request, "Received an invalid response from the server.")
        except Exception as e:
            print(f"An error occurred: {e}")
            messages.error(request, "An unexpected error occurred.")
        return redirect('ApiPlan')  
    







def AddCoaching(request):
    if request.method == "GET":
        user = request.user
        try:
           OfflineCoaching.objects.get(user=user)
        except ObjectDoesNotExist:
            form = OfflineCoachingForm()
            return render(request, 'vocabulary/AddCoaching.html', {'form': form})
            
        else:
            return redirect("UpdateCoachingData")
            
            
        
    if request.method =="POST":
        user = request.user
        form = OfflineCoachingForm(request.POST, request.FILES)
        if form.is_valid():
            Coaching = form.save(commit=False)
            Coaching.user = user
            Coaching.save()
            messages.info(request, "Coaching institude has been added call us to active you Coaching")
            return redirect('home')
        messages.error(request, "data is not valid")
        return render(request, 'vocabulary/AddCoaching.html', {'form': form})
       
    




def Coaching(request):
    
    Coachings =  OfflineCoaching.objects.filter(status='Active')
    city = request.GET.get('city')
    duration = request.GET.get('duration')
    fees = request.GET.get('fees')

    if city:
        Coachings = Coachings.filter(city=city)
    if duration:
        Coachings = Coachings.filter(duration=duration)
    if fees:
        Coachings = Coachings.filter(fees=fees)


    form = CoachingFilterForm()
    return render(request, 'vocabulary/Coaching.html', {"Coachings": Coachings, 'form': form})


def UpdateCoachingData(request):
    if request.method == "GET":
        Coaching = get_object_or_404(OfflineCoaching, user=request.user)
        form = OfflineCoachingForm(instance=Coaching)
        return render(request, 'vocabulary/UpdateCoachingData.html', {'form':form})
    if request.method == "POST":
        Coaching = get_object_or_404(OfflineCoaching, user=request.user)
        form =  OfflineCoachingForm(request.POST, instance=Coaching)
        if form.is_valid():
            UpdateCoaching = form.save(commit=False)
            UpdateCoaching.status = "Active"
            UpdateCoaching.save()
            messages.success(request, "Coaching details updated successfully!")
            return render(request, 'vocabulary/UpdateCoachingData.html', {'form':form})
        messages.error(request, "Please correct the errors below")

            

