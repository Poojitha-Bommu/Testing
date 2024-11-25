{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "9c7aa7c8-c669-4a75-a357-578dda849ba3",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: flask in /opt/anaconda3/lib/python3.12/site-packages (3.0.3)\n",
      "Requirement already satisfied: pillow in /opt/anaconda3/lib/python3.12/site-packages (10.4.0)\n",
      "Requirement already satisfied: Werkzeug>=3.0.0 in /opt/anaconda3/lib/python3.12/site-packages (from flask) (3.0.3)\n",
      "Requirement already satisfied: Jinja2>=3.1.2 in /opt/anaconda3/lib/python3.12/site-packages (from flask) (3.1.4)\n",
      "Requirement already satisfied: itsdangerous>=2.1.2 in /opt/anaconda3/lib/python3.12/site-packages (from flask) (2.2.0)\n",
      "Requirement already satisfied: click>=8.1.3 in /opt/anaconda3/lib/python3.12/site-packages (from flask) (8.1.7)\n",
      "Requirement already satisfied: blinker>=1.6.2 in /opt/anaconda3/lib/python3.12/site-packages (from flask) (1.6.2)\n",
      "Requirement already satisfied: MarkupSafe>=2.0 in /opt/anaconda3/lib/python3.12/site-packages (from Jinja2>=3.1.2->flask) (2.1.3)\n"
     ]
    }
   ],
   "source": [
    "!pip install flask pillow"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "a8942ec4-d435-494d-acf3-baf0575cd9f9",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app '__main__'\n",
      " * Debug mode: off\n"
     ]
    }
   ],
   "source": [
    "from flask import Flask, render_template, request\n",
    "from werkzeug.utils import secure_filename\n",
    "import os\n",
    "from PIL import Image, ImageOps\n",
    "\n",
    "# Setup Flask\n",
    "app = Flask(__name__)\n",
    "\n",
    "# Configuration\n",
    "UPLOAD_FOLDER = 'static/uploads'\n",
    "os.makedirs(UPLOAD_FOLDER, exist_ok=True)\n",
    "app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER\n",
    "app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB\n",
    "\n",
    "@app.route('/', methods=['GET', 'POST'])\n",
    "def index():\n",
    "    if request.method == 'POST':\n",
    "        if 'image' not in request.files:\n",
    "            return \"No file uploaded\", 400\n",
    "        file = request.files['image']\n",
    "        if file.filename == '':\n",
    "            return \"No file selected\", 400\n",
    "        if file:\n",
    "            filename = secure_filename(file.filename)\n",
    "            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)\n",
    "            file.save(input_path)\n",
    "\n",
    "            # Process Image: Example Grayscale and Flipped Versions\n",
    "            output_filenames = []\n",
    "            with Image.open(input_path) as img:\n",
    "                # Grayscale version\n",
    "                grayscale_filename = f'grayscale_{filename}'\n",
    "                grayscale_path = os.path.join(app.config['UPLOAD_FOLDER'], grayscale_filename)\n",
    "                grayscale_img = ImageOps.grayscale(img)\n",
    "                grayscale_img.save(grayscale_path)\n",
    "                output_filenames.append(grayscale_filename)\n",
    "\n",
    "                # Flipped version\n",
    "                flipped_filename = f'flipped_{filename}'\n",
    "                flipped_path = os.path.join(app.config['UPLOAD_FOLDER'], flipped_filename)\n",
    "                flipped_img = ImageOps.mirror(img)\n",
    "                flipped_img.save(flipped_path)\n",
    "                output_filenames.append(flipped_filename)\n",
    "\n",
    "            return {\n",
    "                \"input_image\": filename,\n",
    "                \"output_images\": output_filenames,\n",
    "            }\n",
    "    return \"Flask is running. Send a POST request with an image.\"\n",
    "\n",
    "# Run Flask in a thread (use run with debug=False for notebooks)\n",
    "import threading\n",
    "def run_app():\n",
    "    app.run(debug=False, use_reloader=False, port=5000)\n",
    "\n",
    "thread = threading.Thread(target=run_app)\n",
    "thread.start()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "14746d78-3f5a-42c2-8873-792d6c9dffd8",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
