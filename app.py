import os
from flask import Flask, request, send_file, render_template
from cryptography.fernet import Fernet

app = Flask(__name__)

# Load encryption key from environment variable
key = os.getenv("SECRET_KEY").encode()
cipher = Fernet(key)

UPLOAD_FOLDER = "uploads"
ENCRYPTED_FOLDER = "encrypted"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            with open(filepath, "rb") as f:
                encrypted_data = cipher.encrypt(f.read())

            encrypted_path = os.path.join(ENCRYPTED_FOLDER, file.filename)
            with open(encrypted_path, "wb") as f:
                f.write(encrypted_data)

            return "File uploaded and encrypted successfully"

    return render_template("index.html")

@app.route("/download/<filename>")
def download(filename):
    encrypted_path = os.path.join(ENCRYPTED_FOLDER, filename)

    with open(encrypted_path, "rb") as f:
        decrypted_data = cipher.decrypt(f.read())

    decrypted_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(decrypted_path, "wb") as f:
        f.write(decrypted_data)

    return send_file(decrypted_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
