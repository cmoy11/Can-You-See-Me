import os
from controllers import db_utils
from controllers import recognizerx


def get_tagged_ids(img_dir_to_test):
    known_face_names, known_face_encodings = recognizerx.get_face_encodings()

    for dirpath, dirnames, filenames in os.walk(img_dir_to_test):
        for file in filenames:
            path = dirpath + "/" + file
            ids = recognizerx.get_tagged_ids(path, known_face_names, known_face_encodings )
            print(f"For file: {file} \t ids: {str(ids)}")
            for id in ids:
                db_utils.insert_user_mapping(id, path)


def identify_user_in_images(path):
    known_face_names, known_face_encodings = recognizerx.get_face_encodings()
    ids = recognizerx.get_tagged_ids(path, known_face_names, known_face_encodings)
    for id in ids:
        db_utils.insert_user_mapping(id, path)
