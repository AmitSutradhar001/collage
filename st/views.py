from django.shortcuts import render
from .form import StForm, DecodeForm
from .steganography import encode_image, decode_image

def encode_view(request):
    if request.method == 'POST':
        # Pass both POST data and FILES to the form
        form = StForm(request.POST, request.FILES)
        if form.is_valid():
            # Access the validated data
            message = form.cleaned_data['message']
            img = form.cleaned_data['img']
            # Encode the image and upload to Cloudinary
            img_url = encode_image(img=img, text=message)
            # Assuming img_url is returned from the encode_image function
            download_url = img_url.replace("https://res.cloudinary.com/dzely4n74/image/upload","https://res.cloudinary.com/dzely4n74/image/upload/fl_attachment")
            # Clear the form by reinitializing it
            form = StForm()
            # Render the page with the image URL
            return render(request, 'st/encode.html', {'form': form, 'success': True, 'image_url': img_url, "download_url":download_url})
    else:
        form = StForm()
    
    return render(request, 'st/encode.html', {'form': form, 'success': False})



def decode_view(request):
    if request.method == 'POST':
        form = DecodeForm(request.POST, request.FILES)
        if form.is_valid():
            # Access the uploaded image file
            img = form.cleaned_data['img']

            # Decode the message directly from the uploaded image
            message = decode_image(encoded_image=img)

            # Render the template with the decoded message
            return render(request, 'st/decode.html', {'form': form, 'message': message, 'success': True})
    else:
        form = DecodeForm()

    return render(request, 'st/decode.html', {'form': form, 'success': False})
