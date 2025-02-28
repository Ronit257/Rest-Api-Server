# Media Collection Manager

This project is a full-stack application that includes a REST API server and a Streamlit frontend for managing a media collection. It allows users to perform CRUD operations (Create, Read, Update, Delete) on media items such as books and movies.

## Features

- REST API server built with Flask
- MongoDB integration for data storage
- Streamlit web interface for easy interaction
- Full CRUD functionality:
  - View all media items
  - Add new media items
  - Update existing media items
  - Delete media items

## Requirements

- Python 3.7 or higher
- MongoDB installed and running locally
- All required Python packages listed in requirements.txt

## Setup Instructions

1. Clone the repository:
```
git clone <repository-url>
cd media-collection-manager
```

2. Install the required packages:
```
pip install -r requirements.txt
```

3. Make sure MongoDB is running on your local machine:
```
# Start MongoDB (commands may vary based on your OS and installation)
mongod
```

4. Start the Flask API server:
```
python app.py
```

5. In a new terminal, start the Streamlit app:
```
streamlit run streamlit_app.py
```

6. Open your browser and go to http://localhost:8501 to access the Streamlit interface.

## API Endpoints

- GET `/api/media` - Retrieve all media items
- GET `/api/media/<id>` - Retrieve a specific media item by ID
- POST `/api/media` - Create a new media item
- PUT `/api/media/<id>` - Update an existing media item
- DELETE `/api/media/<id>` - Delete a media item

## Data Structure

Each media item has the following structure:
```json
{
  "name": "Title of the media",
  "img": "URL to the image",
  "summary": "Description of the media"
}
```