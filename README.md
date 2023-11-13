# GitHub Analytics Dashboard

## Project Overview
The GitHub Analytics Dashboard is a web-based tool designed to provide developers and teams with in-depth analysis of their GitHub repositories. It offers key insights into metrics such as commit frequency, pull request trends, issue resolution times, and contributor activities.

## Features
- **User Authentication**: Secure user authentication implemented with GitHub OAuth.
- **Repository Selection**: Users can choose one or multiple GitHub repositories for analysis.
- **Data Visualization**: Charts and statistics displaying commit activities, PR trends, and issue resolution times.
- **Customizable Dashboard**: Users can customize the data and format displayed according to their needs.
- **Responsive Design**: Adapted for different devices and screen sizes to ensure a great experience on both mobile and desktop.

## Quick Start
Here are brief instructions on how to run the GitHub Analytics Dashboard locally:

1. Clone the repository:
git clone https://github.com/ELF-Conan/Github-Analytics-Dashboard.git

2. Install dependencies:
pip install -r requirements.txt

3. Run migrations to create database tables:
python manage.py migrate

4. Start the Django development server:
python manage.py runserver

5. Access `http://localhost:8000` in your browser.

## Technologies Used
- Backend: Django, Django REST Framework
- Frontend: JS, Chart.js
- Authentication: OAuth 2.0 (with Django integration)
- Data: GitHub API

## Contribution Guidelines
We welcome all forms of contributions, including code contributions, issue reporting, or feature suggestions. Please contact us through Pull Requests or Issues.