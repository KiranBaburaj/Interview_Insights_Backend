# Interview Insights - Backend

**Interview Insights** is a job portal designed to help job seekers share their interview experiences and receive feedback from employers, even if they don't secure the job. The platform also facilitates real-time communication between job seekers and employers through chat functionality, with future plans for video calls and AI-powered features.

This repository contains the backend logic and API built using **Django** and **Django REST Framework (DRF)** for handling the job listings, user profiles, interview feedback, and chat features.

## Table of Contents
- [Project Description](#project-description)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [WebSocket Implementation](#websocket-implementation)
- [Folder Structure](#folder-structure)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## Project Description

The **Interview Insights** backend handles core functionalities like:
- User authentication and authorization.
- CRUD operations for job listings, profiles, and feedback.
- Real-time chat functionality using WebSockets and Django Channels.
- APIs that serve data to the React frontend for job searching, profile management, and messaging.

## Features

- **User Authentication**: Using Google OAuth2 and Django authentication system.
- **Job Listings**: Create, update, and search job listings.
- **Profile Management**: Job seekers can manage profiles and showcase interview feedback.
- **Real-time Chat**: Real-time communication between job seekers and employers using WebSockets.
- **Notifications**: Real-time notifications for new messages, job listings, and interview feedback.
- **Interview Scheduling**: Allow employers and job seekers to schedule interviews via the platform.
- **Interview Feedback**: Employers can provide feedback for candidates.
- **RESTful APIs**: The backend provides a set of APIs for job listings, profiles, and chat interactions.

## Tech Stack

### Backend:
- **Django**: The web framework used for rapid development and clean design.
- **Django REST Framework (DRF)**: For building the API endpoints.
- **Django Channels**: For real-time WebSocket communication.
- **PostgreSQL**: Database for storing job listings, user data, and chat messages.
- **Daphne**: ASGI server for serving Django Channels and handling WebSockets.
  
### Frontend:
This project’s frontend is built using **React.js** and can be found in a separate repository [here](https://github.com/KiranBaburaj/Interview_Insights_Frontend).

## Setup and Installation

### Prerequisites:
- **Python 3.9+**
- **PostgreSQL**
- **Node.js** (for setting up the frontend)

### Clone the repository:

```bash
git clone https://github.com/KiranBaburaj/Interview_Insights_Backend.git
cd Interview_Insights_Backend




### Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install the dependencies:

```bash
pip install -r requirements.txt
```

### Setup the environment variables:

Create a `.env` file in the root of your project and configure the following variables:

```env
SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost, 127.0.0.1
DATABASE_URL=postgres://<username>:<password>@localhost:5432/interview_insights_db
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

```

### Set up the database:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create a superuser:

```bash
python manage.py createsuperuser
```

### Start the server:

```bash
python manage.py runserver
```

For real-time chat to work, ensure that both Django Channels and Redis are properly configured and that Daphne is running:

```bash
daphne -b 0.0.0.0 -p 8001 interview_insights.asgi:application
```

## Usage

Once the backend server is running, it can handle:
- User authentication with Google OAuth2.
- API requests from the frontend for job listings, user profiles, and feedback.
- Real-time communication between users via WebSockets.

## API Endpoints

Here are some of the key API endpoints:

### Authentication
- **POST** `/api/auth/google/`: Google OAuth2 login.

### Job Listings
- **GET** `/api/jobs/`: Retrieve all job listings.
- **POST** `/api/jobs/`: Create a new job listing.
- **GET** `/api/jobs/:id/`: Retrieve details of a specific job listing.
- **PUT** `/api/jobs/:id/`: Update a job listing.
- **DELETE** `/api/jobs/:id/`: Delete a job listing.

### User Profiles
- **GET** `/api/profiles/`: Retrieve all profiles.
- **POST** `/api/profiles/`: Create a new profile.
- **GET** `/api/profiles/:id/`: Retrieve a specific user profile.

### Chat
- **GET** `/api/chat/rooms/`: Get all chat rooms.
- **POST** `/api/chat/rooms/`: Create a new chat room.
- **GET** `/api/chat/rooms/:room_id/messages/`: Retrieve all messages in a room.

## WebSocket Implementation

Real-time chat is implemented using **Django Channels** and **WebSockets**. The WebSocket server is powered by **Redis** and served via **Daphne**. Here's how the WebSocket connection works:

1. Clients connect to the WebSocket server via `/ws/chat/room_id/`.
2. Messages are sent and received in real time, with Redis managing the connection state.
3. The server broadcasts messages to all clients in the specified chat room.

## Folder Structure

The folder structure of the backend is organized as follows:

Interview_Insights_Backend/
├── Interview                  # Main interview app handling core functionalities
│   ├── ...                    # Additional files related to interviews
├── Interview_Insights         # Project directory for settings and configurations
│   ├── ...                    # Additional settings files
├── chat                       # Chat application for handling WebSocket communication
│   ├── ...                    # Chat-related files and views
├── customadmin                # Admin panel customizations
│   ├── ...                    # Custom admin-related files
├── employer                   # Employer-related functionalities
│   ├── ...                    # Additional files for employer management
├── jobs                       # Job listings and related models
│   ├── ...                    # Job-related files
├── jobseeker                  # Job seeker-related functionalities
│   ├── ...                    # Additional files for job seeker management
├── media                      # Media files
│   ├── ...                    # Uploaded media files
├── profile_photos             # Directory for storing applicant profile pictures
│   ├── ...                    # Applicant pics list
├── users                      # User management and authentication
│   ├── ...                    # User-related files
├── chat.log                   # Log file for chat-related events
├── .gitignore                 # Git ignore file to ignore sensitive files
└── manage.py                  # Command-line utility for the project


## Future Enhancements

- **Video Calls**: Integration with video calling APIs for job seekers and employers.
- **AI Features**: Integration of AI for personalized job recommendations and resume analysis.


## Contributing

We welcome contributions! If you'd like to contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Create a Pull Request.

