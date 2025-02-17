# VocabValt

## Project Overview
VocabValt is a vocabulary-building web application designed for students. Users can search for words and view comprehensive details, including:
- Word name
- Hindi meaning
- Part of speech
- Example sentences
- Definitions
- Difficulty level
- An illustrative image representing the word's meaning

### Additional Features:
- Filters to search words by **part of speech** and **difficulty level**
- Save difficult words into personal containers (session-based storage)
- Pagination for better word browsing experience
- Offline coaching centers can advertise their courses and update details
- Students can find nearby offline coaching centers with filters based on **city, fees, and duration**
- Public API to create **word guessing games** and fetch word definitions within an IDE

## Features
- Built-in Django authentication
- Save difficult words using custom containers
- Comprehensive word details with images
- Advertise and list offline coaching centers
- Find coaching centers based on location, fees, and duration
- API for word-guessing game creation
- Advanced filtering options

## Installation & Setup
### Virtual Environment
VocabValt uses a **virtual environment (venv)** for package management. Make sure to activate it before running the project.

### Setup Commands:
```sh
# Clone the repository
git clone <repo-url>
cd VocabValt

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver 5555
```

## Technologies Used
- **Django 5** (Backend framework)
- **MySQL** (Database)
- **HTML, CSS, Bootstrap, JavaScript** (Frontend)
- **Git** (Version control)

## Usage
Run the project using:
```sh
python manage.py runserver 5555
```

## API Documentation
VocabValt offers an API that allows developers to:
- Fetch word definitions
- Create custom word-guessing games

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository
2. Create a new branch (`feature-branch`)
3. Make your changes and commit them
4. Open a pull request

## Deployment
Currently, the project is running locally. Deployment plans include:
- Hosting on **Heroku, AWS, or DigitalOcean**
- Setting up proper **CI/CD pipelines**




### Future Enhancements:
- Deploying the project online
- Adding more word-related interactive features
- Improving UI/UX for better student experience

