from django.shortcuts import render,redirect
import cloudinary.uploader
from .forms import ImageForm
import cloudinary
from decouple import config 
from django.contrib import messages
# Configuration       
cloudinary.config( 
    cloud_name = "dgpcfijvz", 
    api_key = "954922678679494", 
    api_secret = "PJt30un2scOy7-xYS4f3azBUgCU", # Click 'View API Keys' above to copy your API secret
    secure=True
)
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
                    response = cloudinary.uploader.upload(uploaded_image, public_id=image_name)
                    url = response["secure_url"]
                    print(response["public_id"])

                    # Clear the session data
                    del request.session["uploaded_image"]
                    del request.session["image_name"]
                    return redirect(url)
                except Exception as e:
                    messages.error(request,"There is a problem with the API limits. Please try again leter.")
                    return redirect("cloud:home")

    form = ImageForm()
    return render(request,"cloud/home.html",context={"form":form})


def ai_task(request,url,img_id):
    return render(request,"cloud/ai.html")