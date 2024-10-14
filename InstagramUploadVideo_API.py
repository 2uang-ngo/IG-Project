import requests
import time
import access
import re
from playwright.sync_api import Playwright, sync_playwright, expect
import InstagramUpload_Playwright
import access
import os

def create_reels_video_object(video_url, caption, access_token, instagram_account_id):
    media_url = f"https://graph.facebook.com/v17.0/{instagram_account_id}/media"
    params = {
        'video_url': video_url,
        'caption': caption,
        'media_type': 'REELS',
        'access_token': access_token
    }
    response = requests.post(media_url, params=params)
    if response.status_code == 200:
        return response.json()['id']
    else:
        print(f"Error creating Reels video object: {response.text}")
        return None

def check_media_status(media_id, access_token):
    status_url = f"https://graph.facebook.com/v17.0/{media_id}"
    params = {
        'fields': 'status_code',
        'access_token': access_token
    }
    response = requests.get(status_url, params=params)
    if response.status_code == 200:
        return response.json()['status_code']
    else:
        print(f"Error checking media status: {response.text}")
        return None

def publish_reels_video(media_id, access_token, instagram_account_id):
    publish_url = f"https://graph.facebook.com/v17.0/{instagram_account_id}/media_publish"
    params = {
        'creation_id': media_id,
        'access_token': access_token
    }
    response = requests.post(publish_url, params=params)
    if response.status_code == 200:
        print("Reels video published successfully!")
        return response.json()
    else:
        print(f"Error publishing Reels video: {response.text}")
        return None

def upload_and_publish_reels_video(video_url, caption, access_token, instagram_account_id):
    media_id = create_reels_video_object(video_url, caption, access_token, instagram_account_id)
    
    if media_id:
        while True:
            status_code = check_media_status(media_id, access_token)
            if status_code == "FINISHED":
                print("Video is ready for publishing!")
                publish_reels_video(media_id, access_token, instagram_account_id)
                break
            elif status_code == "IN_PROGRESS":
                print("Video is still processing, waiting...")
            else:
                print(f"Error: Video status is {status_code}")
                break
    else:
        print("Failed to create media object for video.")


def upload_Video_Imgur(playwright: Playwright,video_path):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    context.grant_permissions(["clipboard-write", "clipboard-read"], origin="https://imgur.com")
        
    page = context.new_page()
    page.goto("https://imgur.com/")
    page.get_by_label("Consent", exact=True).click()
    page.get_by_role("link", name="Sign in").click()
    page.get_by_placeholder("Username or Email").click()
    page.get_by_placeholder("Username or Email").fill("your email")
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill("your password")
    page.get_by_role("button", name="Sign In").click()
    page.get_by_role("link", name="New post").click()
    page.get_by_label("Choose Photo/Video").set_input_files(video_path)
    time.sleep(2)
    page.get_by_role("button", name="Yes, keep the audio").click()
    time.sleep(60)
    page.locator(".PostContent-imageWrapper-rounded").click()
    page.get_by_role("button", name="Copy Link").click()

    link = page.evaluate('navigator.clipboard.readText()')
    link_chinh = link.replace("https://", "https://i.") + ".mp4"
    print(f"Video link: {link_chinh}")
    context.close()
    browser.close()
    return link_chinh

def upload_Video_Instagram(root_folder,caption_file,hashtag_file, access_token, instagram_account_id,so_video=1):
    random_images, folder_name = InstagramUpload_Playwright.get_random_Video_from_random_folder(root_folder, so_video)
    print(f"Videos selected for upload: {random_images}")
    print(f"The name of the folder containing the photo: {folder_name}")
    random_caption = InstagramUpload_Playwright.get_random_caption(caption_file)
    print(f"Selected caption: {random_caption}")
    random_hashtags = InstagramUpload_Playwright.get_random_hashtags(hashtag_file, 10)
    hashtag_string = " ".join(random_hashtags)
    print(f"Selected hashtags: {hashtag_string}")
    new_caption = f"{random_caption}"
    print(f"Final caption: {new_caption}")
    
    with sync_playwright() as playwright:
      video_url=upload_Video_Imgur(playwright,random_images)
      upload_and_publish_reels_video(video_url, new_caption, access_token, instagram_account_id)

if __name__=="__main__":
    # Input details
    ig_download_folder = os.path.join(os.path.dirname(os.getcwd()), "IG download Video")
    caption_file = os.path.join(os.getcwd(), "caption.txt")
    hashtag_file = os.path.join(os.getcwd(), "hashtag.txt")
    access_token = access.access_token
    instagram_account_id = access.instagram_account_id
    imgur_clientID = access.imgur_client_id

    upload_Video_Instagram(ig_download_folder,caption_file,hashtag_file, access_token, instagram_account_id,so_video=1)
