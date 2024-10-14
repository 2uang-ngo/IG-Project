import instaloader
import os
from datetime import datetime, timedelta
import shutil

def download_all_photos(profile_name, target_folder):
    # Initialize Instaloader with the specified folder
    L = instaloader.Instaloader(dirname_pattern=os.path.join(target_folder, '{target}'))
    try:
        # Get profile information
        profile = instaloader.Profile.from_username(L.context, profile_name)
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Profile '{profile_name}' does not exist.")
        return
    except instaloader.exceptions.ConnectionException as e:
        print(f"Connection error: {e}")
        return

    print(f"Downloading all posts from profile: {profile_name} to {target_folder}")

    for post in profile.get_posts():
        try:
            print(f"Downloading post from {post.date}...")
            L.download_post(post, target=profile.username)
        except Exception as e:
            print(f"Failed to download post from {post.date}: {e}")

    print("Download complete.")

def download_recent_posts(profile_name, target_folder, days=30):
    # Initialize Instaloader with the specified folder
    L = instaloader.Instaloader(dirname_pattern=os.path.join(target_folder, '{target}'))

    try:
        # Get profile information
        profile = instaloader.Profile.from_username(L.context, profile_name)
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Profile '{profile_name}' does not exist.")
        return
    except instaloader.exceptions.ConnectionException as e:
        print(f"Connection error: {e}")
        return

    print(f"Downloading posts from the last {days} days from profile: {profile_name} to {target_folder}")

    # Calculate the cut-off date from now to the "days" period (e.g. 30 days ago)
    time_limit = datetime.now() - timedelta(days=days)

    for post in profile.get_posts():
        # Only download posts within the next 30 days
        if post.date >= time_limit:
            try:
                print(f"Downloading post from {post.date}...")
                L.download_post(post, target=profile.username)
            except Exception as e:
                print(f"Failed to download post from {post.date}: {e}")
        else:
            # Stop if the post is older than the cut-off date, as subsequent posts will also be older
            print(f"Post from {post.date} is older than {days} days. Stopping download.")
            break

    print("Download complete.")

def rut_gon_folder(folder_path):
    # Inspect all files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and not (filename.lower().endswith('.jpg') or filename.lower().endswith('.mp4')):
            os.remove(file_path)
            print(f"Đã xóa: {filename}")

    print("Deleted all non-.jpg files.")

def chuyen_file_video(folder_a,folder_b):
    if not os.path.exists(folder_b):
        os.makedirs(folder_b)

    for filename in os.listdir(folder_a):
        if filename.endswith('.mp4'):
            source = os.path.join(folder_a, filename)
            destination = os.path.join(folder_b, filename)
            shutil.move(source, destination)
    print("Successfully migrated all .mp4 files.")

def update_anh():
    target_folder = os.path.join(os.path.dirname(os.getcwd()), "IG download")
    target_folder_Video = os.path.join(os.path.dirname(os.getcwd()), "IG download Video")
    folders = [folder for folder in os.listdir(target_folder) if os.path.isdir(os.path.join(target_folder, folder))]
    for profile_name in folders:

        rut_gon_folder(os.path.join(target_folder, profile_name))
        chuyen_file_video(os.path.join(target_folder, profile_name),os.path.join(target_folder_Video, profile_name))


def tim_new_Model(profile_names):
    target_folder = os.path.join(os.path.dirname(os.getcwd()), "IG download")
    target_folder_Video = os.path.join(os.path.dirname(os.getcwd()), "IG download Video")
    
    for profile_name in profile_names: 
        download_all_photos(profile_name, target_folder)
    
        rut_gon_folder(os.path.join(target_folder, profile_name))
        chuyen_file_video(os.path.join(target_folder, profile_name),os.path.join(target_folder_Video, profile_name))

if __name__ == "__main__":
    target_folder = os.path.join(os.path.dirname(os.getcwd()), "IG download")
    download_recent_posts("abc", target_folder, days=1)