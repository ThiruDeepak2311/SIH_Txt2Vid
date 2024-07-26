import os
import requests
import wget
# Assuming you have an empty list initialized elsewhere in your code
image_list = []

def is_valid_image(img_url):
    valid_extensions = {".jpg", ".jpeg", ".png"}
    _, ext = os.path.splitext(img_url)
    return ext.lower() in valid_extensions

def generate_images(img_prompt, count, video_id):
    serpapi_endpoint = os.environ['SERP_ENDPOINT']
    serpapi_api_key = os.environ['SERP_API']

    search_url = f"{serpapi_endpoint}&q={img_prompt}&api_key={serpapi_api_key}&gl=in&ijn=1"
    response = requests.get(search_url)
    data = response.json()

    for img_result in data.get("images_results", []):
        if is_valid_image(img_result.get("original", "")):
            image_url = img_result["original"]

            save_directory = "images"

            if not os.path.exists(save_directory):
                os.makedirs(save_directory)

            file_name = f"downloaded_image_{count}.jpg"
            file_path = os.path.join(save_directory, file_name)

            try:
                img_download_data = requests.get(image_url, stream=True)

                if img_download_data.status_code == 200:
                    with open(file_path, "wb") as file:
                        for chunk in img_download_data.iter_content(chunk_size=1024):
                            file.write(chunk)
                    print(f"Image downloaded to {file_path}")

                    image_list.append({"image_path": file_path, "image_url": image_url})
                    
                    break  # Stop loop if image is successfully downloaded
            except Exception as e:
                print(f"Error downloading image: {e}")
                # Continue to the next image if an error occurs

    return image_list

print(image_list)