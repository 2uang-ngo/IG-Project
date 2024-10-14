
import access
import requests

def create_story_media(image_url, access_token, instagram_account_id):
    media_url = f"https://graph.facebook.com/v17.0/{instagram_account_id}/media"
    params = {
        'image_url': image_url,
        'access_token': access_token,
        'media_product_type': 'STORIES'
    }
    response = requests.post(media_url, params=params)
    if response.status_code == 200:
        return response.json()['id']
    else:
        print(f"Error creating Story media: {response.text}")
        return None

def publish_story(media_id, access_token, instagram_account_id):
    publish_url = f"https://graph.facebook.com/v17.0/{instagram_account_id}/media_publish"
    params = {
        'creation_id': media_id,
        'access_token': access_token
    }
    response = requests.post(publish_url, params=params)
    if response.status_code == 200:
        print("Story published successfully!")
        return response.json()
    else:
        print(f"Error publishing Story: {response.text}")
        return None


image_url = "your url"
access_token = access.access_token
instagram_account_id = access.instagram_account_id

media_id = create_story_media(image_url, access_token, instagram_account_id)
if media_id:
    publish_story(media_id, access_token, instagram_account_id)