import os

from flask import Flask, send_file, request, jsonify, redirect, Response, make_response
from werkzeug.utils import secure_filename

from controllers import db_utils
from controllers import analyze_directory

app = Flask(__name__)


@app.route('/')
def hello():
    return send_file("static/pages/index.html")


@app.route('/login', methods=['POST'])
def login_clicked():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    is_valid, _id = db_utils.login(username, password)
    if is_valid:
        data = db_utils.get_user_data_by_id(_id)
        return jsonify({"success": True, "data": data})
    else:
        return jsonify({"success": False, "data": None})


@app.route('/join')
def join():
    return send_file("static/pages/register.html")


@app.route('/join', methods=['POST'])
def join_post():
    data = request.get_json()
    firstName = data.get("firstName")
    lastName = data.get('lastName')
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    photo = data.get('pfp')
    print(f"firstName: {firstName} \t lastName: {lastName} \t email: {email} \t username: {username}"
          f"\t password: {password} \t photo: {photo}")


@app.route('/register', methods=['POST'])
def register_clicked():
    data = request.get_json()
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    profile_picture = request.files['pfp']

    if profile_picture:
        profile_picture_path = os.path.join('db', 'profile_pictures', profile_picture.filename)
        profile_picture.save(profile_picture_path)
        
    is_valid, _id = db_utils.register(firstName, lastName, email, username, password)

    if is_valid:
        data = db_utils.get_user_data_by_id(_id)
        return jsonify({"success": True, "data": data})
    else:
        return jsonify({"success": False, "data": None})


@app.route('/profile', methods=['GET'])
def load_profile_page():
    return send_file("static/pages/profile.html")


@app.route('/gallery', methods=['GET'])
def load_gallery_page():
    return send_file("static/pages/gallery.html")


@app.route('/contribute', methods=['GET'])
def ingest_collaboration_data():
    return send_file("static/pages/contribute.html")


@app.route('/contribute', methods=['POST'])
def load_collaborate_page():
    if 'file' not in request.files:
        return redirect(request.url)
    files = request.files

    title = request.form.get('title')
    date = request.form.get('date')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    address = request.form.get('address')

    for key in files.keys():
        values = files.getlist(key)
        for value in values:
            if value and allowed_file(value.filename):
                filename = secure_filename(value.filename)
                base_address = "controllers/data_to_test/"
                img_path = os.path.join(base_address, filename)
                value.save(img_path)
                db_utils.insert_img_mapping(img_path, latitude, longitude, address, date)
                analyze_directory.identify_user_in_images(img_path)
    return send_file("static/pages/contribute.html")


@app.route('/map', methods=['GET'])
def load_map_page():
    user_id = request.args.get("user_id")
    data = db_utils.get_user_data_by_id(user_id)
    # username = data["username"]
    # data = db_utils.get_map_data(user_id, username)
    response = make_response(send_file("static/pages/map.html"))
    # response.headers["data"] = data
    return response


@app.route('/login', methods=['GET'])
def login():
    return send_file("static/pages/login.html")


# Configure the upload directory and allowed extensions
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    files = request.files

    for key in files.keys():
        values = files.getlist(key)
        for value in values:
            if value and allowed_file(value.filename):
                filename = secure_filename(value.filename)
                value.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return 'File uploaded successfully.'


def read_images_from_disk(image_folder):
    import base64
    images = []
    f = open(image_folder, "rb")
    image_data = f.read()
    images.append(base64.b64encode(image_data).decode("utf-8"))
    return images


@app.route("/get_user_images", methods=["GET"])
def get_images():
    id = request.args.get("user_id")
    image_paths = db_utils.get_user_mapping(id)
    images = []
    print(f"Image paths: {image_paths}")
    for path in image_paths:
        images.append(read_images_from_disk(path))

    response = {
        "status": "success",
        "images": images
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(port=8000)
