from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Details
import kairos_face
import sys
import os
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
kairos_face.settings.app_id = "51b5544c"
kairos_face.settings.app_key = "f33ff7569a1a23e32d24f2818c1922e9"

def signup(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST) 
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      raw_password = form.cleaned_data.get('password1')
      user = authenticate(username=username, password=raw_password)
      login(request, user)
      return redirect('index')
  else:
    form = UserCreationForm()
  return render(request, 'signup.html', {'form': form})


def index(request):
  return render(request,'index.html')

def enroll(request):
  captured=False
  while not captured:
    try:
      if request.method == 'POST' and request.FILES['image']:
        myfile = request.FILES['image']
        fs = FileSystemStorage()
        filename=fs.save(myfile.name, myfile)
#        print(filename)
        name     = request.POST.get('name')
        description     = request.POST.get('description')
        location     = request.POST.get('location')
        date=request.POST.get('date')
        x=(""+filename+"")
        detail_obj = Details(name=name,description=description,location=location,date=date,image=fs.url(x))
        print(x)
        detail_obj.save()
        kairos_face.enroll_face(file=BASE_DIR+"/media/"+fs.url(filename), subject_id=str(detail_obj.id), gallery_name='a-gallery')
        captured=True
        messages.add_message(request, messages.SUCCESS, 'Successfully enrolled!')
      return render(request,'enroll.html')
    except kairos_face.exceptions.ServiceRequestError:
      messages.add_message(request, messages.ERROR, 'Error! No face found in the image',extra_tags='safe')
      return render(request,'enroll.html')
      

# Create your views here.
def recognize(request):
  rec=''
  path=''
  can_name=''
  can_loc=''
  can_des=''
  can_date=''
  captured=False
  while not captured:
    try:
      if request.method == 'POST' and request.FILES['image']:
        myfile = request.FILES['image']
        fs = FileSystemStorage()
        filename=fs.save(myfile.name, myfile)
        global recognized_faces
        recognized_faces = kairos_face.recognize_face(file=BASE_DIR+"/media/"+fs.url(filename), gallery_name='a-gallery')
        captured=True
        sub_id=recognized_faces['images'][0]['candidates'][0]['subject_id']
        obj=Details.objects.get(pk=sub_id)
        path=str(obj.image)
        can_name=obj.name
        can_loc=obj.location
        can_des=obj.description
        can_date=obj.date
        rec=recognized_faces['images'][0]['candidates'][0]['confidence']*100
        os.remove("media/"+fs.url(filename))
      return render(request,'recognize.html',{'rec': rec,'path':path,'name':can_name,'loc':can_loc,'des':can_des,'date':can_date})
    except kairos_face.exceptions.ServiceRequestError:
      messages.add_message(request, messages.ERROR, 'Error occurred')
      os.remove("media/"+fs.url(filename))
      return render(request,'recognize.html')
    except FileNotFoundError:
      messages.add_message(request, messages.ERROR, 'Please enter the correct file type')
      os.remove("media/"+fs.url(filename))
      return render(request,'recognize.html')
    except MultiValueDictKeyError:
      messages.add_message(request, messages.ERROR, 'No data present in database')
      os.remove("media/"+fs.url(filename))
      return render(request,'recognize.html')
    except KeyError:
      messages.add_message(request, messages.ERROR, 'No matching details found')
      os.remove("media/"+fs.url(filename))
      return render(request,'recognize.html')

def delete(request):
  captured=False
  while not captured:
    try:      
      if request.method == 'POST':
        if request.POST.get('id'):
          enrolled_id = request.POST.get('id')
          obj=Details.objects.get(pk=enrolled_id)
          os.remove("media/"+str(obj.image))
          obj.delete()
          kairos_face.remove_face(subject_id=str(enrolled_id), gallery_name='a-gallery')
          messages.add_message(request, messages.SUCCESS, 'Successfully deleted!')
        if request.POST.get('delete'):
          global remove_gallery_1
          remove_gallery_1 = kairos_face.remove_gallery('a-gallery')
          Details.objects.all().delete()
          messages.add_message(request, messages.SUCCESS, 'Gallery deleted!')
        captured=True
      return render(request,'delete.html')
    except kairos_face.exceptions.ServiceRequestError:
      messages.add_message(request, messages.ERROR, 'Database is empty! Please enroll details')
      return render(request,'delete.html')
    except ValueError:
      messages.add_message(request, messages.ERROR, 'Please enter a valid ID')
      return render(request,'delete.html')
    except ObjectDoesNotExist:
      messages.add_message(request, messages.ERROR, 'Error occured. Either DB is empty or the ID does not exist')
      return render(request,'delete.html')
    
def list_all(request):
  captured=False
  while not captured:
    try:
      gallery_obj=[]
      gallery_subjects = kairos_face.get_gallery('a-gallery')
      gallery=gallery_subjects['subject_ids']
      for candidate in gallery:
        obj=Details.objects.get(pk=candidate)
        gallery_obj.append(obj)
      captured=True
      return render(request,'gallery_subjects.html',{'gallery':gallery_obj})
    except kairos_face.exceptions.ServiceRequestError:
      messages.add_message(request, messages.ERROR, 'Database is empty! Please enroll details')
      return render(request,'gallery_subjects.html')