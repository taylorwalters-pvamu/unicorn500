from django.shortcuts import render
from .models import video

# Create your views here.
def demo_vid(request):
    Video= video.objects.all()
    return render(request,'demo.html',{'video':Video})