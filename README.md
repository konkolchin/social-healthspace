# Social HealthSpace

A modern social network platform built with Python FastAPI and React, designed to create health-focused communities and facilitate discussions around health and wellness topics.

## Features

- User authentication with JWT
- Community creation and management
- Social feed with posts and comments
- User profiles and settings
- Modern, responsive UI built with Tailwind CSS
- Real-time form validation
- Comprehensive error handling

## Tech Stack

### Backend
- Python 3.11
- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Alembic for migrations
- JWT authentication
- CORS middleware

### Frontend
- React 18
- TypeScript
- Vite
- Tailwind CSS
- Axios for API calls
- React Router v6
- Context API for state management

## Prerequisites

- Python 3.11
- Node.js 16+ and npm
- PostgreSQL 13+
- Git

## Setup Instructions

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/social-healthspace.git
cd social-healthspace
```

2. Create a Python virtual environment:
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Update the values in `.env` with your configuration:
```env
PROJECT_NAME=Social HealthSpace
VERSION=1.0.0
API_V1_STR=/api/v1
POSTGRES_SERVER=localhost
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=social_healthspace
JWT_SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. Initialize the database:
```bash
# Create the database
psql -U postgres
CREATE DATABASE social_healthspace;
\q

# Run migrations
alembic upgrade head
```

6. Start the backend server:
```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000` with Swagger documentation at `/docs`.

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`.

## Project Structure

```
social-healthspace/
├── app/                    # Backend application
│   ├── api/               # API endpoints
│   │   └── api_v1/        # API version 1
│   ├── core/              # Core functionality
│   ├── db/                # Database configuration
│   ├── models/            # SQLAlchemy models
│   └── schemas/           # Pydantic schemas
├── frontend/              # Frontend application
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── context/       # React context providers
│   │   ├── services/      # API services
│   │   └── utils/         # Utility functions
│   └── package.json
├── alembic/               # Database migrations
├── tests/                 # Test suite
├── .env.example           # Example environment variables
├── requirements.txt       # Python dependencies
└── README.md
```

## Development Workflow

1. Create a new branch for your feature:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and commit them:
```bash
git add .
git commit -m "Add your feature description"
```

3. Push to your branch:
```bash
git push origin feature/your-feature-name
```

4. Create a Pull Request on GitHub

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions, please file an issue on the GitHub repository. 