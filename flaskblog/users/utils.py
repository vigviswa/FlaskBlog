import os
import secrets
from PIL import Image
from flaskblog import app
from flask_mail import Message
from flaskblog import mail
from flask import url_for, current_app
import oci

config = {
    "user": "ocid1.user.oc1..aaaaaaaaxkpb5pjfaf4432pd4fb7vsjzbprdghzyfxog56w6xg4lcio6qhga",
    "fingerprint": "63:bf:5a:b6:34:e1:f7:c3:41:d1:f4:a8:0c:b8:73:a4",
    "tenancy": "ocid1.tenancy.oc1..aaaaaaaary5pyagidupdq63x5fyeo4oenxt7tvtjtrpp6sljbmxslz56liza",
    "region": "us-phoenix-1",
    "key_file": "/home/ubuntu/FlaskBlog/keyfiles/vigviswa.pem",
}


def save_picture(form_picture):
    obj = oci.object_storage.ObjectStorageClient(config)
    namespace = obj.get_namespace().data
    bucket_name = "flask-demo-bucket"
    _, f_ext = os.path.splitext(form_picture.filename)
    random_hex = secrets.token_hex(8)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    with open(picture_path, mode="rb") as file:
        data = file.read()
    obj.put_object(namespace, bucket_name, picture_fn, data)
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        "Password Reset Request",
        sender="vigviswa@cloudmazingblog.com",
        recipients=[user.email],
    )
    msg.body = f"""To reset your password, visit the following link:
    {url_for('users.reset_token', token=token, _external=True)}
    
    If you did not make this request then simply ignore this email and no changes required
    """
    mail.send(msg)
