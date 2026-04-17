from flask import Flask, render_template, request, send_file
from PIL import Image
import os
import io
import zipfile

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/compress", methods=["POST"])
def compress():
    files = request.files.getlist("images")
    quality = int(request.form.get("quality", 70))  # default 70
    format_choice = request.form.get("format", "JPEG")  # JPEG, PNG, WEBP

    if not files:
        return "No files uploaded", 400

    # Create zip in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for file in files:
            if file.filename == "":
                continue
            img = Image.open(file)

            # Resize if width > 800px
            max_width = 800
            if img.width > max_width:
                ratio = max_width / float(img.width)
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.ANTIALIAS)

            # Save compressed image to buffer
            img_buffer = io.BytesIO()
            save_params = {}
            if format_choice.upper() in ["JPEG", "WEBP"]:
                save_params["quality"] = quality
            if format_choice.upper() == "PNG":
                save_params["optimize"] = True

            img.save(img_buffer, format=format_choice.upper(), **save_params)
            img_buffer.seek(0)

            # Add to zip
            zipf.writestr(f"compressed_{file.filename.split('.')[0]}.{format_choice.lower()}", img_buffer.read())

    zip_buffer.seek(0)
    return send_file(zip_buffer, mimetype="application/zip", as_attachment=True, download_name="compressed_images.zip")

if __name__ == "__main__":
    app.run(debug=True)