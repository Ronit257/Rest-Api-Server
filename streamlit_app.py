import streamlit as st
import requests
import json
from PIL import Image
from io import BytesIO

# API URL
API_URL = "http://localhost:5000/api/media"

# Set page title
st.set_page_config(page_title="Media Collection Manager", layout="wide")
st.title("Media Collection Manager")

# Function to load image from URL
def load_image(url):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img
    except:
        return None

# Function to fetch all media from API
def fetch_all_media():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            st.error(f"Failed to fetch media: {response.text}")
            return []
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return []

# Function to add a new media item
def add_media(name, img_url, summary):
    try:
        data = {
            "name": name,
            "img": img_url,
            "summary": summary
        }
        response = requests.post(API_URL, json=data)
        if response.status_code == 201:
            st.success("Media added successfully!")
            return True
        else:
            st.error(f"Failed to add media: {response.text}")
            return False
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return False

# Function to update a media item
def update_media(id, name, img_url, summary):
    try:
        data = {
            "name": name,
            "img": img_url,
            "summary": summary
        }
        response = requests.put(f"{API_URL}/{id}", json=data)
        if response.status_code == 200:
            st.success("Media updated successfully!")
            return True
        else:
            st.error(f"Failed to update media: {response.text}")
            return False
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return False

# Function to delete a media item
def delete_media(id):
    try:
        response = requests.delete(f"{API_URL}/{id}")
        if response.status_code == 200:
            st.success("Media deleted successfully!")
            return True
        else:
            st.error(f"Failed to delete media: {response.text}")
            return False
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return False

# Create sidebar for operations
st.sidebar.title("Operations")
operation = st.sidebar.radio("Select Operation", ["View All", "Add New", "Update", "Delete"])

# Display based on operation
if operation == "View All":
    st.header("Media Collection")
    media_items = fetch_all_media()
    
    if media_items:
        for i, item in enumerate(media_items):
            col1, col2 = st.columns([1, 3])
            with col1:
                img = load_image(item['img'])
                if img:
                    st.image(img, width=200)
                else:
                    st.error("Image could not be loaded")
            with col2:
                st.subheader(item['name'])
                st.write(item['summary'])
            st.divider()
    else:
        st.info("No media items found")

elif operation == "Add New":
    st.header("Add New Media Item")
    
    name = st.text_input("Title")
    img_url = st.text_input("Image URL")
    summary = st.text_area("Summary")
    
    if st.button("Add Media"):
        if name and img_url and summary:
            success = add_media(name, img_url, summary)
            if success:
                st.experimental_rerun()
        else:
            st.warning("Please fill all fields")

elif operation == "Update":
    st.header("Update Media Item")
    
    media_items = fetch_all_media()
    if media_items:
        media_names = [item['name'] for item in media_items]
        selected_name = st.selectbox("Select Media to Update", media_names)
        
        # Find selected media
        selected_media = None
        for item in media_items:
            if item['name'] == selected_name:
                selected_media = item
                break
        
        if selected_media:
            name = st.text_input("Title", value=selected_media['name'])
            img_url = st.text_input("Image URL", value=selected_media['img'])
            summary = st.text_area("Summary", value=selected_media['summary'])
            
            if st.button("Update Media"):
                if name and img_url and summary:
                    success = update_media(selected_media['_id'], name, img_url, summary)
                    if success:
                        st.experimental_rerun()
                else:
                    st.warning("Please fill all fields")
    else:
        st.info("No media items found to update")

elif operation == "Delete":
    st.header("Delete Media Item")
    
    media_items = fetch_all_media()
    if media_items:
        media_names = [item['name'] for item in media_items]
        selected_name = st.selectbox("Select Media to Delete", media_names)
        
        # Find selected media
        selected_media = None
        for item in media_items:
            if item['name'] == selected_name:
                selected_media = item
                break
        
        if selected_media:
            col1, col2 = st.columns([1, 3])
            with col1:
                img = load_image(selected_media['img'])
                if img:
                    st.image(img, width=200)
            with col2:
                st.subheader(selected_media['name'])
                st.write(selected_media['summary'])
            
            st.warning("Are you sure you want to delete this media?")
            if st.button("Delete Media"):
                success = delete_media(selected_media['_id'])
                if success:
                    st.experimental_rerun()
    else:
        st.info("No media items found to delete")