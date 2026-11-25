# violence Detection Web Application

## Project Overview
This Django-based web application is designed for  violence detection using video and image analysis. It leverages a pre-trained Convolutional Neural Network (CNN) model to classify video streams and images as either "Peaceful" or "Criminal Events" (violence/non-violence). The application includes user authentication, video streaming, image classification, and a database to store processed media.

## Features
- **User Authentication**: Register, login, and logout functionality.
- **Video Streaming**: Upload and stream videos with classification of criminal events.
- **Image Classification**: Upload images for violence/non-violence detection.
- **Database**: Stores uploaded videos and images with their classification results.
- **API Endpoint**: Allows external systems to upload videos with a token for processing.
- **Admin Panel**: Manage users, videos, and images via Django's admin interface.

## Prerequisites
- Python 3.8+
- Django 3.1.4
- TensorFlow/Keras (for model inference)
- OpenCV (for video processing)
- Pillow (for image processing)
- NumPy
- A pre-trained CNN model (`CustomCNN.h5`) for video classification and another (`model.h5`) for image classification

## Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd Website
   ```

2. **Set Up a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   Ensure `requirements.txt` includes:
   ```
   django==3.1.4
   tensorflow
   opencv-python
   pillow
   numpy
   ```

4. **Place Pre-trained Models**
   - Place `CustomCNN.h5` in the `Models/` directory.
   - Place `model.h5` in the `core/` directory.

5. **Apply Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a Superuser (for Admin Access)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```
   Access the application at `http://localhost:8000`.

## Project Structure
- **Website/**: Main project directory containing settings, URLs, and WSGI/ASGI configurations.
  - `settings.py`: Configures Django settings, including media paths, email backend, and model loading.
  - `urls.py`: Defines project-level URL patterns.
- **core/**: Main application directory.
  - `models.py`: Defines `DocModel` (for videos) and `UserImageModel` (for images).
  - `views.py`: Handles logic for video streaming, image classification, authentication, and API endpoints.
  - `urls.py`: Defines app-specific URL patterns.
  - `forms.py`: Contains forms for user registration and file uploads (not shown but referenced).
- **media/**: Stores uploaded videos (`documents/`) and images (`images/`).
- **static/**: Contains CSS, JavaScript, and other static assets.
- **templates/**: HTML templates for rendering pages (e.g., `home.html`, `stream.html`).

## Usage
1. **Register/Login**: Create an account or log in to access the application.
2. **Upload Video**: On the homepage, upload a video for real-time crime detection.
3. **Stream Video**: View the processed video stream with overlaid classification ("Peaceful" or "Criminal Events").
4. **Upload Image**: Use the image classification page to upload and classify images as violent or non-violent.
5. **View Database**: Access the database page to see all processed images and their labels.
6. **API**: Send POST requests to `/api/` with a video file and token to process videos programmatically.

## Key URLs
- `/`: Homepage for video upload.
- `/stream/`: View the latest video stream.
- `/streamtoken/<token>`: View a video stream by token.
- `/Deploy_8/`: Image classification page.
- `/Database/`: View stored images and labels.
- `/Register_2/`: User registration.
- `/Login_3/`: User login.
- `/Logout/`: User logout.
- `/admin/`: Django admin panel.
- `/api/`: API endpoint for video uploads.

## Notes
- The application uses a SQLite database for simplicity. For production, consider using PostgreSQL or MySQL.
- Email functionality is configured but commented out in `views.py`. Update `settings.py` with valid SMTP credentials for email alerts.
- The application assumes the pre-trained models (`CustomCNN.h5` and `model.h5`) are available and compatible with the input data.
- Video processing uses OpenCV's `VideoCapture` and may require optimization for large-scale use.
- Ensure `DEBUG = False` and update `ALLOWED_HOSTS` in `settings.py` for production deployment.

## Deployment
For production:
1. Use a WSGI server like Gunicorn (`pip install gunicorn`).
2. Configure a web server like Nginx to serve static and media files.
3. Set up a proper database and update `DATABASES` in `settings.py`.
4. Secure the application by updating `SECRET_KEY` and disabling `DEBUG`.

Example Gunicorn command:
```bash
gunicorn --workers 3 Website.wsgi:application --bind 0.0.0.0:8000
```

## Contributing
- Fork the repository.
- Create a feature branch (`git checkout -b feature-name`).
- Commit changes (`git commit -m "Add feature"`).
- Push to the branch (`git push origin feature-name`).
- Open a pull request.

## License
This project is licensed under the MIT License.