from flask import Flask, request, jsonify
from pdf_to_csv import process_pdf
import firebase_admin
from firebase_admin import credentials, storage
import os

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate('serviceAccountKey.json')  # Your Firebase Service Key
firebase_admin.initialize_app(cred, {'storageBucket': 'eduparser.appspot.com'})

# Upload CSV to Firebase Storage
def upload_to_firebase(file_path, filename):
    bucket = storage.bucket()
    blob = bucket.blob(f'csv_files/{filename}')
    blob.upload_from_filename(file_path)
    blob.make_public()
    return blob.public_url

# API Route to Handle PDF Upload & Conversion
@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    file = request.files['pdf']
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    # Save uploaded PDF
    os.makedirs('uploads', exist_ok=True)
    pdf_path = os.path.join('uploads', file.filename)
    file.save(pdf_path)

    # Process PDF to CSV
    csv_path = process_pdf(pdf_path)

    # Upload CSV to Firebase Storage
    csv_filename = os.path.basename(csv_path)
    download_url = upload_to_firebase(csv_path, csv_filename)

    return jsonify({'download_url': download_url}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
