from django.shortcuts import render,redirect,HttpResponse
from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.urls import reverse
import cloudinary.uploader
import cloudinary.api
from .forms import ImageForm
import cloudinary
import uuid
from cloudinary import CloudinaryImage
from django.contrib import messages
import datetime
from ipware import get_client_ip

# Configuration       
cloudinary.config( 
    cloud_name = "dgpcfijvz", 
    api_key = "954922678679494", 
    api_secret = "PJt30un2scOy7-xYS4f3azBUgCU", # Click 'View API Keys' above to copy your API secret
    secure=True
)



def get_ip(request):
    ip, is_routable = get_client_ip(request)
    print(is_routable)
    return ip






def home(request):
    if request.method == 'POST':
        form = ImageForm(request.POST,request.FILES)
        if form.is_valid():
            image_file = request.FILES["image"]
            request.session["uploaded_image"] = image_file.read()  # Save the binary content
            request.session["image_name"] = image_file.name 
            uploaded_image = request.session.get("uploaded_image")
            image_name = request.session.get("image_name")

            if uploaded_image and image_name:
                # Upload the image to Cloudinary
                try:
                    uid = str(uuid.uuid4())
                    response = cloudinary.uploader.upload(uploaded_image, public_id=uid)
                    img_id = uid

                    # Clear the session data
                    del request.session["uploaded_image"]
                    del request.session["image_name"]
                    return redirect(reverse("cloud:process", kwargs={"img_id": img_id}))
                except Exception as e:
                    
                    messages.error(request,"There is a problem with the API. Please try again leter.")
                    return redirect("cloud:home")

    form = ImageForm()
    
    context = {
        "form":form,
    }
    return render(request,"cloud/home.html",context=context)


def ai_task(request,img_id):
    # Get the user's IP address
    ip_address = get_ip(request)
    # Generate a unique cache key using the IP and current date
    today = datetime.date.today()
    cache_key = f"view_access_{ip_address}_{today}"
    
    # Get the current access count (default is 0)
    access_count = cache.get(cache_key, 0)
    
    if access_count >= 5:
        messages.info(request,"You have reached the maximum number of allowed accesses for today.")
        return redirect("cloud:home")
    
    # Increment the count and set it in the cache with a 24-hour timeout
    cache.set(cache_key, access_count + 1, timeout=24*3600)  # Timeout is 24 hours in seconds
    try:
        img = cloudinary.api.resource(str(img_id))
        img_url = img["secure_url"]
    except Exception as e:
        messages.error(request,"There is a problem with the API. Please try again leter.")
        return redirect("cloud:home")
    if access_count == 0:
        messages.info(request,"This was your last upload of the day.")
    messages.info(request,f"Access allowed. You have {5 - access_count - 1} accesses remaining today.")
    return render(request,"cloud/ai.html",context={"img":img_url,"pID":img_id})





def ai_upscale(request,pID):
    if request.method == 'POST':
        try:
            result = CloudinaryImage(f'{pID}').image(effect="upscale")
            url = f"{result[10:-3]}"
            return redirect(url)
        except Exception as e:
            messages.error(request,"There is a problem with the API. Please try again leter.")
            return redirect("cloud:home")


def enhance(request,pID):
    if request.method == 'POST':
        try:
            result =CloudinaryImage(f"{pID}").image(effect="enhance")
            url = f"{result[10:-3]}"
            return redirect(url)
        except Exception as e:
            messages.error(request,"There is a problem with the API. Please try again leter.")
            return redirect("cloud:home")

def genfill(request,pID):
    if request.method == 'POST':
        try:
            result =CloudinaryImage(f"{pID}").image(aspect_ratio="1:1", gravity="center", background="gen_fill", crop="pad")
            url = f"{result[10:-3]}"
            return redirect(url)
        except Exception as e:
            messages.error(request,"There is a problem with the API. Please try again leter.")
            return redirect("cloud:home")

def genreplace(request,pID):
    if request.method == "POST":
        replace_from = request.POST["from"]
        replace_to = request.POST["to"]
        try:
            result =CloudinaryImage(f"{pID}").image(effect=f"gen_replace:from_{replace_from};to_{replace_to}")
            url = f"{result[10:-3]}"
            return redirect(url)
        except Exception as e:
            messages.error(request,"There is a problem with the API. Please try again leter.")
            return redirect("cloud:home")


def bgremove(request,pID):
    if request.method == 'POST':
        try:
            result =CloudinaryImage(f"{pID}").image(effect="background_removal")
            url = f"{result[10:-3]}"
            return redirect(url)
        except Exception as e:
            messages.error(request,"There is a problem with the API. Please try again leter.")
            return redirect("cloud:home")

