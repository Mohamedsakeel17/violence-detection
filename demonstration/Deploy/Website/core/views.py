from django.views.decorators.clickjacking import xframe_options_exempt
import numpy as np
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import DocModel
import json
from django.views.decorators import gzip
import cv2
from .forms import DocumentForm
from django.conf import settings
# from django.core.mail import send_mail


from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from . forms import UserRegisterForm


def Landing_1(request):
    return render(request, '1_Landing.html')

def HomeView(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('streamroom')

    else:
        form = DocumentForm()
        return render(request, 'home.html', {'form': form})
    

def Register_2(request):
    form = UserRegisterForm()
    if request.method =='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was successfully created. ' + user)
            return redirect('Login_3')

    context = {'form':form}
    return render(request, '2_Register.html', context)


def Login_3(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username OR Password incorrect')

    context = {}
    return render(request,'3_Login.html', context)



model = settings.MODEL

class VideoCamera(object):
    def __init__(self, url=None):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.status = True
        self.org = (50, 80)
        self.fontScale = 1.4
        self.thickness = 3
        self.SIZE = (150, 150)
        self.THRESH = 0.5
        self.url = 0 if url is None else '.' + url
        self.video = cv2.VideoCapture(self.url)
        self.skipCount = 2
        self.prev = None
        self.fcount = 0

    def __del__(self):
        self.video.release()

    def get_frame(self):
        s1 = 0
        
        ret, image = self.video.read()
        if not ret or image is None:
            self.status = False
            return b''  # Return an empty frame if there is an issue with the image

        if self.fcount % self.skipCount == 0:
            tmp = cv2.resize(image, self.SIZE)
            tmp = tmp / 255.0
            pred = model.predict(np.array([tmp]))
            string = "Criminal_Events," if pred[0][0] > self.THRESH else "Peaceful"
            string += f" {str(pred[0][0])}"
            self.prev = string
            test = self.prev.split(",")
            print('This is before if statement')
            print(test[0])
            if test[0] == 'Criminal_Events':
                print("The if successfully passed")
                self.fcount += 1
                if self.fcount >= 20:
                    print("All systems are worked")
                    # The email functionality is removed here
                    print("This is criminal events")
        else:
            string = self.prev

        color = (255, 255, 255)
        image = cv2.rectangle(image, (20, 20), (600, 100), (0, 200, 100), cv2.FILLED) if string.split(' ')[0] == 'Peaceful' else cv2.rectangle(
            image, (20, 20), (600, 100), (0, 0, 255), cv2.FILLED)
        image = cv2.putText(image, string, self.org, self.font,
                            self.fontScale, color, self.thickness, cv2.LINE_AA)
        ret, jpeg = cv2.imencode('.jpg', image)
        
        self.fcount += 1
        return jpeg.tobytes()


def gen(camera):
    while camera.status:
        frame = camera.get_frame()
        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def Stream(request):
    try:
        entry = DocModel.objects.all().last()
        return StreamingHttpResponse(gen(VideoCamera(entry.vid.url)), content_type="multipart/x-mixed-replace;boundary=frame")
    except StreamingHttpResponse.HttpResponseServerError as e:
        print("aborted")


@gzip.gzip_page
def StreamToken(request, token):
    try:
        entry = DocModel.objects.filter(stoken=token).last()
        return StreamingHttpResponse(gen(VideoCamera(entry.vid.url)), content_type="multipart/x-mixed-replace;boundary=frame")
    except StreamingHttpResponse.HttpResponseServerError as e:
        print("aborted")




def StreamView(request):
    entry = DocModel.objects.all().last()
    if entry is None:
        return JsonResponse({'message': 'No Video Files Yet!'})
    return render(request, 'stream.html')


# API End Point
def StreamTokenView(request, token):
    try:
        entry = DocModel.objects.filter(stoken=token).last()
        if entry is None:
            return JsonResponse({'message': 'Token Not Registered'})

        return render(request, 'streamtoken.html', {'token': token})

    except DocModel.DoesNotExist:
        return JsonResponse({'message': 'Token Not Registered'})


@csrf_exempt
def APIEnd(request):
    if request.method == 'POST':
        try:
            stoken = request.POST['stoken']
            vidFile = request.FILES['vid']
            DocModel(stoken=stoken, vid=vidFile).save()
            baseurl = request.build_absolute_uri(reverse('home'))
            return JsonResponse({'status': 'ok', 'message': f'Files Received from sender {stoken}', 'vidurl': baseurl+'streamtoken/'+stoken})
        except:
            return HttpResponse(status=400)

    return JsonResponse({'status': 'Wait kro bhai'})


from .models import UserImageModel
from . import forms
import numpy as np
from tensorflow import keras
from PIL import Image,ImageOps


import time


def Deploy_8(request): 
    print("HI")
    if request.method == "POST":
        form = forms.UserImageForm(files=request.FILES)
        if form.is_valid():
            print('HIFORM')
            form.save()
        obj = form.instance

        result1 = UserImageModel.objects.latest('id')
        models = keras.models.load_model('core/model.h5')
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        image = Image.open("/Users/mohamedsakeel/Downloads/ITPDL25-FINAL/ITPDL25-FINAL CODING/Deploy/Website/media/" + str(result1)).convert("RGB")
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        data[0] = normalized_image_array
        classes = ["non_violence","violence"]
        prediction = models.predict(data)
        idd = np.argmax(prediction)
        a = (classes[idd])
        if a == "non_violence":
             b ='This Image Detected non_violence'
        elif a == "violence":
            b ='This Image Detected violence'
        
        else:
            b = 'WRONG INPUT'

        data = UserImageModel.objects.latest('id')
        data.label = a
        data.save()

        

        
        

        
        return render(request, 'output.html',{'form':form,'obj':obj,'predict':b})
    else:
        
        form = forms.UserImageForm()
    return render(request, 'model.html',{'form':form})


def Database(request):
    models = UserImageModel.objects.all()
    return render(request, 'Database.html', {'models': models})

def Logout(request):
    logout(request)
    return redirect('/')






