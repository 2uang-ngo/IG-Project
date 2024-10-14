import access
import requests
import InstagramUpload_Playwright
import os

def upload_image_to_imgur(image_path, client_id):
    url = "https://api.imgur.com/3/upload"
    
    headers = {
        "Authorization": f"Client-ID {client_id}"
    }
    
    with open(image_path, 'rb') as img:
        image_data = img.read()
    
    data = {
        'image': image_data,
        'type': 'file'
    }
    
    response = requests.post(url, headers=headers, files={'image': image_data})
    
    if response.status_code == 200:
        response_data = response.json()
        image_url = response_data['data']['link']
        print("Image uploaded successfully. Image URL:", image_url)
        return image_url
    else:
        print(f"Failed to upload image. Status code: {response.status_code}, Response: {response.text}")
        return None

def create_media_object(image_url, access_token, instagram_account_id):
    media_url = f"https://graph.facebook.com/v17.0/{instagram_account_id}/media"
    params = {
        'image_url': image_url,
        'access_token': access_token
    }
    response = requests.post(media_url, params=params)
    if response.status_code == 200:
        return response.json()['id']
    else:
        print(f"Error creating media object: {response.text}")
        return None

def create_carousel(media_ids, caption, access_token, instagram_account_id):
    carousel_url = f"https://graph.facebook.com/v17.0/{instagram_account_id}/media"
    params = {
        'access_token': access_token,
        'media_type': 'CAROUSEL',
        'children': ','.join(media_ids),
        'caption': caption
    }
    response = requests.post(carousel_url, params=params)
    if response.status_code == 200:
        return response.json()['id']
    else:
        print(f"Error creating carousel: {response.text}")
        return None

def publish_carousel(creation_id, access_token, instagram_account_id):
    publish_url = f"https://graph.facebook.com/v17.0/{instagram_account_id}/media_publish"
    params = {
        'access_token': access_token,
        'creation_id': creation_id
    }
    response = requests.post(publish_url, params=params)
    if response.status_code == 200:
        print("Carousel post published successfully!")
        return response.json()
    else:
        print(f"Error publishing carousel post: {response.text}")
        return None

def upload_carousel_post(image_urls, caption, access_token, instagram_account_id):
    media_ids = []

    for image_url in image_urls:
        media_id = create_media_object(image_url, access_token, instagram_account_id)
        if media_id:
            media_ids.append(media_id)
        else:
            print(f"Failed to create media for {image_url}")

    if len(media_ids) == len(image_urls):
        creation_id = create_carousel(media_ids, caption, access_token, instagram_account_id)
        if creation_id:
            publish_carousel(creation_id, access_token, instagram_account_id)
        else:
            print("Failed to create carousel post")
    else:
        print("Error: Not all media objects were created successfully")

def Instagram_Upload(root_folder,caption_file,hashtag_file, access_token, instagram_account_id,imgur_clientID,so_anh=3):
    random_images, folder_name = InstagramUpload_Playwright.get_random_images_from_random_folder(root_folder, so_anh)
    print(f"Photos selected for upload: {random_images}")
    print(f"The name of the folder containing the photo: {folder_name}")
    random_caption = InstagramUpload_Playwright.get_random_caption(caption_file)
    print(f"Selected caption: {random_caption}")
    random_hashtags = InstagramUpload_Playwright.get_random_hashtags(hashtag_file, 10)
    hashtag_string = " ".join(random_hashtags)
    print(f"Selected hashtags: {hashtag_string}")
    new_caption = f"{random_caption}"
    print(f"Final caption: {new_caption}")

    image_urls = []

    for image_path in random_images:
        url = upload_image_to_imgur(image_path, imgur_clientID)
        if url:
            image_urls.append(url)

    upload_carousel_post(image_urls, new_caption, access_token, instagram_account_id)
    for image in random_images:
            os.remove(image)
            print(f"Deleted: {image}")



if __name__ == "__main__":
    # Input details
    ig_download_folder = os.path.join(os.path.dirname(os.getcwd()), "IG download")
    caption_file = os.path.join(os.getcwd(), "caption.txt")
    hashtag_file = os.path.join(os.getcwd(), "hashtag.txt")
    access_token = access.access_token
    instagram_account_id = access.instagram_account_id 
    imgur_clientID = access.imgur_client_id

    Instagram_Upload(ig_download_folder, caption_file,hashtag_file, access_token, instagram_account_id,imgur_clientID)
