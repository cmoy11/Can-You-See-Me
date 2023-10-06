import face_recognition
import numpy as np


import os


def get_face_encodings():
    known_face_encodings = []
    known_face_names = []

    directory_path = "db/profile_pictures_directory"
    for dirpath, dirnames, filenames in os.walk(directory_path):
        if filenames:
            for file in filenames:
                img_location = dirpath + "/" + file
                image = face_recognition.load_image_file(img_location)
                face_encoding = face_recognition.face_encodings(image)[0]
                known_face_names.append(dirpath.split('/')[-1])
                known_face_encodings.append(face_encoding)
    return known_face_names, known_face_encodings


def get_tagged_ids(img_to_test, known_face_names, known_face_encodings):
    unknown_image = face_recognition.load_image_file(img_to_test)

    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    user_ids = set()

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            user_ids.add(int(name))


    return user_ids


