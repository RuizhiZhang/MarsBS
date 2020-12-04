from django.shortcuts import render
import requests
import json
from base64 import b64encode, b64decode
from detectionApp.settings import MEDIA_ROOT

# Create your views here.
# from detectionApp.models import cal
from django.http import HttpResponse

def prepage(request):
    return render(request, 'predict.html')

def predict(request):
    if request.POST:
        img = request.FILES['img']

        save_path = "%s/detection/%s" % (MEDIA_ROOT, img.name)

        with open(save_path, 'wb') as f:
            for content in img.chunks():
                f.write(content)

        with open(save_path, 'rb') as f:
            data = f.read()
        postdata = {'image': b64encode(data).decode()}
        res = requests.post('http://20.208.112.203:8500/inpect_sfittings/', data=json.dumps(postdata))
        result = b64decode(res.content)

        return render(request, 'result.html', context={'data': result})
    else:
        return HttpResponse('Please visit us with POST')