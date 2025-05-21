from deepface import DeepFace

def get_emotion(image_path):
    analysis = DeepFace.analyze(image_path, actions=['emotion'], enforce_detection=False)
    dominant_emotion = analysis[0]['dominant_emotion']
    return dominant_emotion