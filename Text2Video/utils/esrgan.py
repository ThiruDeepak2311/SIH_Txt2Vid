import os
import requests
from base64 import b64encode
from PIL import Image
from io import BytesIO
import shutil

def toB64(imgUrl):
    return str(b64encode(requests.get(imgUrl).content))[2:-1]

def enhance(image_url,count, scale,):
    url = os.environ["ESRGAN_ENDPOINT"]
    api_key=os.environ['ESRGAN_API']

    # Request payload
    data = {
        "image": toB64(image_url['image_url']),
        "scale": scale
    }
    image_name = 'enhanced_image_'+str(count)+'.jpg'
    try:
        response = requests.post(url, json=data, headers={'x-api-key': api_key})

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Create a folder named "enhanced_images" if it doesn't exist
            if not os.path.exists('enhanced_images'):
                os.makedirs('enhanced_images')

            # Extract image content from the response
            image_content = response.content

            # Save the enhanced image content to a file in the "enhanced_images" folder
            
            enhanced_image_path = os.path.join('enhanced_images', image_name)
            with open(enhanced_image_path, 'wb') as file:
                file.write(image_content)

            print(f"Enhanced image saved at: {enhanced_image_path}")

        else:
            print(f"Error enhancing image: {response.status_code}")
            print(response.text)
            copy_image_on_error(image_url['image_path'],image_name, 'enhanced_images')

    except Exception as e:
        print(f"Error enhancing image: {str(e)}")
        copy_image_on_error(image_url['image_path'],image_name ,'enhanced_images')

def copy_image_on_error(image_url, image_name, destination_folder):
    try:

        original_image_path = image_url
        destination_path = os.path.join(destination_folder, image_name)

        shutil.copy(original_image_path, destination_path)

        print(f"Original image copied to: {destination_path}")

    except Exception as e:
        print(f"Error copying original image: {str(e)}")

# Example usage

# image_list = [{'image_path': 'images\\downloaded_image_8.jpg', 'image_url': 'https://jeremykarnowski.files.wordpress.com/2015/07/alexnet2.png'}, {'image_path': 'images\\downloaded_image_9.jpg', 'image_url': 'https://slideplayer.com/slide/14080019/86/images/23/Zeiler-Fergus+Architecture+%281+tower%29.jpg'}] 
def enchance_images(image_list):
    count=1
    for image in image_list:
        enhance(image,count,scale="2")
        count+=1
