import re
from playwright.sync_api import Playwright, sync_playwright, expect
import time
import os
import random

def get_random_images_from_random_folder(root_folder, num_images=3):
    all_folders = [subdir for subdir, _, files in os.walk(root_folder) if files]
    
    if not all_folders:
        raise ValueError("No folders containing images.")
    
    random_folder = random.choice(all_folders)
    
    jpg_files = [os.path.join(random_folder, file) for file in os.listdir(random_folder) if file.lower().endswith('.jpg')]
    
    if len(jpg_files) < num_images:
        raise ValueError(f"{random_folder} folder doesn't have enough {num_images} images.")
    
    random_images = random.sample(jpg_files, num_images)

    folder_name = os.path.basename(random_folder)
    
    return random_images, folder_name

def get_random_Video_from_random_folder(root_folder, num_images=3):
    all_folders = [subdir for subdir, _, files in os.walk(root_folder) if files]
    
    if not all_folders:
        raise ValueError("No folders containing images.")
    
    random_folder = random.choice(all_folders)
    
    jpg_files = [os.path.join(random_folder, file) for file in os.listdir(random_folder) if file.lower().endswith('.mp4')]
    
    if len(jpg_files) < num_images:
        raise ValueError(f"{random_folder} folder doesn't have enough {num_images} images.")
    
    random_images = random.sample(jpg_files, num_images)

    folder_name = os.path.basename(random_folder)
    
    return random_images, folder_name

def get_random_caption(caption_file_path):
    with open(caption_file_path, 'r', encoding='utf-8') as file:
        captions = file.readlines()
    
    captions = [caption.strip() for caption in captions if caption.strip()]

    if not captions:
        raise ValueError("No captions found in the file.")

    random_caption = random.choice(captions)
    formatted_caption = random_caption.replace('\\n', '\n')
    return formatted_caption

def get_random_hashtags(hashtag_file_path, num_hashtags=10):
    with open(hashtag_file_path, 'r', encoding='utf-8') as file:
        hashtags = file.readlines()
    
    hashtags = [hashtag.strip() for hashtag in hashtags if hashtag.strip()]

    if len(hashtags) < num_hashtags:
        num_hashtags = len(hashtags)
    
    random_hashtags = random.sample(hashtags, num_hashtags)
    return random_hashtags
