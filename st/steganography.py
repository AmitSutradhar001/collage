import cloudinary
import cloudinary.uploader
from PIL import Image
import io
import os

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),  # Add your API secret here
    secure=True
)


def encode_image(img, text):
    # Open the uploaded image file
    image = Image.open(img)
    encoded = image.convert("RGB")  # Ensure it's in RGB mode
    width, height = encoded.size

    # Add a delimiter to the text (to signal the end of the message)
    text += "\0"
    index = 0

    for row in range(height):
        for col in range(width):
            pixel = encoded.getpixel((col, row))

            if len(pixel) == 4:  # If RGBA, handle the alpha channel
                r, g, b, a = pixel
            else:  # For RGB
                r, g, b = pixel

            if index < len(text):
                # Store the ASCII value of the character in the blue channel
                ascii_code = ord(text[index])
                if len(pixel) == 4:  # If RGBA, keep alpha channel unchanged
                    encoded.putpixel((col, row), (r, g, ascii_code, a))
                else:  # For RGB
                    encoded.putpixel((col, row), (r, g, ascii_code))
                index += 1
            else:
                # Keep original pixel values once all text has been encoded
                if len(pixel) == 4:  # If RGBA
                    encoded.putpixel((col, row), (r, g, b, a))
                else:  # For RGB
                    encoded.putpixel((col, row), (r, g, b))

    # Save the encoded image to an in-memory buffer
    buffer = io.BytesIO()
    encoded.save(buffer, format=encoded.format if encoded.format else "PNG")
    buffer.seek(0)

    # Upload the image to Cloudinary directly from memory
    upload_result = cloudinary.uploader.upload(
        buffer,
        folder="encoded_images",
        public_id=f"encoded_{img.name.split('.')[0]}",  # Optional: Set a public ID based on original file name
        resource_type="image"
    )
    return upload_result["secure_url"]

def decode_image(encoded_image):
    # Open the uploaded image file
    image = Image.open(encoded_image)
    width, height = image.size
    decoded_text = ""

    for row in range(height):
        for col in range(width):
            # Get the pixel values
            pixel = image.getpixel((col, row))

            if len(pixel) == 4:  # If RGBA, handle the alpha channel
                r, g, b, a = pixel
            else:  # For RGB
                r, g, b = pixel

            # Stop decoding when the delimiter (ASCII code 0) is encountered
            if b == 0:
                return decoded_text

            # Convert blue channel value to corresponding character
            decoded_text += chr(b)

    return decoded_text  # Return decoded text even if no delimiter was found


# # 08071176059
# academic@onlineuu.in