ReelAdvisor - Movie Recommendation System
<img width="1893" height="862" alt="image" src="https://github.com/user-attachments/assets/2fa74e79-a1b6-4a18-8e4a-29ab124ffa80" />
<img width="1892" height="866" alt="image" src="https://github.com/user-attachments/assets/db753308-6bd6-428b-8409-e1a57cb60b1a" />
ReelAdvisor is an intelligent movie recommendation system that helps you discover your next favorite film. Built with Python and Django, it uses advanced machine learning algorithms to analyze your preferences and suggest movies you'll love.

Key Features
🎬 Smart Recommendations: Content-based filtering using TF-IDF and cosine similarity

🌓 Dual Theme: Beautiful dark and light mode options

🔍 Instant Search: Autocomplete functionality for quick movie discovery

📱 Responsive Design: Works seamlessly on all devices

🎨 Modern UI: Sleek, aesthetic interface with smooth animations

🧠 AI-Powered: Learns from thousands of movies to find perfect matches

Technologies Used
Backend
Python 3.8+

Django 4.2

Pandas

Scikit-learn

SQLite

Frontend
HTML5, CSS3

JavaScript

Bootstrap 5

Font Awesome

Installation Guide
Prerequisites
Python 3.8 or higher

pip package manager

Setup Instructions
Clone the repository:

bash:

git clone https://github.com/yourusername/ReelAdvisor.git
cd ReelAdvisor

Create and activate virtual environment:

bash:

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

Install dependencies:

bash:
pip install -r requirements.txt

Download dataset:

Place tmdb_5000_movies.csv in the data/ directory

Run migrations:

bash:

python manage.py makemigrations

python manage.py migrate

Import movie data:

bash:

python manage.py import_movies

Start the development server:

bash:

python manage.py runserver

Access the application at:

text
http://localhost:8000


Usage Guide
Search for a Movie: Enter a movie you like in the search box

Get Recommendations: Click "Recommend" to see 10 personalized suggestions

Explore Details: Click on movie cards to view more information

Switch Themes: Toggle between dark and light mode using the moon/sun icon

Try Suggestions: Click on popular movie badges for quick searches



Project Structure
text
ReelAdvisor/
├── data/                   # Dataset directory
├── reel_advisor/           # Django project configuration
├── recommender/            # Main application
│   ├── management/         # Custom management commands
│   ├── migrations/         # Database migrations
│   ├── static/             # Static files (CSS, JS, images)
│   ├── templates/          # HTML templates
│   ├── admin.py            # Admin configuration
│   ├── apps.py             # App configuration
│   ├── models.py           # Database models
│   ├── tests.py            # Unit tests
│   ├── urls.py             # URL routing
│   ├── utils.py            # Recommendation algorithm
│   └── views.py            # Application views
├── .gitignore              # Files to ignore in version control
├── manage.py               # Django management script
├── README.md               # Project documentation
└── requirements.txt        # Python dependencies




Customization
To customize ReelAdvisor:

Update Styles: Modify recommender/static/css/style.css

Change Algorithm: Edit recommender/utils.py

Add Features: Extend recommender/views.py

Modify UI: Adjust templates in recommender/templates/



Contributing
We welcome contributions! Please follow these steps:

Fork the repository

Create a new branch (git checkout -b feature/your-feature)

Commit your changes (git commit -am 'Add some feature')

Push to the branch (git push origin feature/your-feature)

Discover your next favorite movie with ReelAdvisor! 🍿🎬
