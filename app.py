from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from preprocessing import load_mri_image, normalize_image, denoise_image, skull_strip, resize_image, augment_image, visualize_image, compute_histogram

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')
ALLOWED_EXTENSIONS = {'nii', 'jpg', 'jpeg', 'png'}  # You can allow other file types as needed
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        # Save the uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Process the file based on its type
        if filename.endswith('.nii'):
            # Process MRI file with nibabel and perform preprocessing steps
            mri_data = load_mri_image(file_path)
            normalized_mri = normalize_image(mri_data)
            denoised_mri = denoise_image(normalized_mri)
            skull_stripped_mri = skull_strip(denoised_mri)
            resized_mri = resize_image(skull_stripped_mri, (128, 128, 128))
            augmented_mri = augment_image(resized_mri)

            # Visualize or save the results
            visualize_image(mri_data, title="Original MRI Image")
            visualize_image(augmented_mri, title="Augmented MRI Image")

            flash(f"'{filename}' successfully processed as an MRI file.")
        
        else:
            # Handle regular image file (jpg, png, etc.)
            flash(f"'{filename}' uploaded but only MRI (.nii) processing is supported.")
        
        return redirect(url_for('home'))

    flash('Invalid file type. Please upload a .nii, .jpg, .jpeg, or .png file.')
    return redirect(request.url)

if __name__ == "__main__":
    app.run(debug=True)