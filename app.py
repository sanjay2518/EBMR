from flask import Flask, render_template, request, flash, redirect, url_for
from deepface import DeepFace
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import cv2
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key"

# Spotify credentials
client_id = '2a7dcbf8deeb49abac534747e4eff598'
client_secret = '50495fb1a1974a5b89917c4258ce0be1'

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret))

# Check if image is blurry
def is_image_blurry(image_path, threshold=100):
    try:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return True
        laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()
        return laplacian_var < threshold
    except Exception as e:
        print(f"Error in blur detection: {e}")
        return True

# Check if image is black
def is_image_black(image_path):
    try:
        img = cv2.imread(image_path)
        if img is None:
            return True
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return not cv2.countNonZero(gray)
    except Exception as e:
        print(f"Error in black image detection: {e}")
        return True

# Detect emotion
def detect_emotion(image):
    image_path = 'temp_image.jpg'
    try:
        image.save(image_path)
        
        if is_image_black(image_path):
            return "black_image"
        
        if is_image_blurry(image_path):
            return "blurry_image"
        
        results = DeepFace.analyze(img_path=image_path, actions=['emotion'], enforce_detection=False)

        if isinstance(results, list) and len(results) == 0:
            return "no_face"
        if isinstance(results, list) and len(results) > 1:
            return "multiple_faces"

        # Consistently extract the dominant emotion
        dominant_emotion = results[0]['dominant_emotion'] if isinstance(results, list) else results['dominant_emotion']
        return dominant_emotion

    except ValueError as e:
        if "Face could not be detected" in str(e):
            return "no_face"
        raise e
    except Exception as e:
        print(f"Error in emotion detection: {e}")
        return "error"
    finally:
        if os.path.exists(image_path):
            os.remove(image_path)


# Recommend music based on emotion
def recommend_music(emotion):
    emotion_to_genre = {
        'happy': 'pop',
        'sad': 'blues',
        'angry': 'rock',
        'calm': 'classical',
        'neutral': 'jazz',
        'surprise': 'electronic',
        'fear': 'ambient',
        'disgust': 'heavy-metal'
    }
    genre = emotion_to_genre.get(emotion, 'pop')

    try:
        results = sp.search(q=f'genre:{genre} Tamil', type='track', limit=20, market='IN')
        track_urls = [track['external_urls']['spotify'] for track in results['tracks']['items']]
        random.shuffle(track_urls)
        return track_urls[:4]
    except Exception as e:
        print(f"Error in music recommendation: {e}")
        return []

# Routes
@app.route("/")
def login():
    return render_template("login.html")

@app.route("/home", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'image' not in request.files:
            flash("No file part in the request", "danger")
            return redirect(request.url)
        
        image = request.files['image']
        if image.filename == '':
            flash("No image selected for uploading", "danger")
            return redirect(request.url)
        
        emotion = detect_emotion(image)
        
        if emotion == "multiple_faces":
            flash("Multiple faces detected. Please upload an image with only one face.", "danger")
        elif emotion == "blurry_image":
            flash("The image is too blurry. Please upload a clear image.", "danger")
        elif emotion == "black_image":
            flash("Uploaded image appears to be completely black. Please upload a valid image.", "danger")
        elif emotion == "no_face":
            flash("No face detected in the image. Please upload an image with a clear human face.", "danger")
        elif emotion == "error":
            flash("Error processing the image. Please try again.", "danger")
        else:
            tracks = recommend_music(emotion)
            if tracks:
                flash(f"Detected Emotion: {emotion.capitalize()}", "success")
                return render_template("index.html", tracks=tracks, emotion=emotion)
            else:
                flash("Could not fetch music recommendations. Please try again.", "warning")
                return render_template("index.html", tracks=None, emotion=emotion)

    return render_template("index.html", tracks=None, emotion=None)

if __name__ == "__main__":
    app.run(debug=True)
