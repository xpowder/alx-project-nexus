# ALX Project Nexus - E-Commerce Backend

A comprehensive e-commerce backend system built with Django and Django REST Framework, developed as part of the ProDev Backend Engineering Program. This project demonstrates advanced backend development skills including API design, authentication, database optimization, and deployment strategies.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Challenges & Solutions](#challenges--solutions)
- [Best Practices](#best-practices)
- [Collaboration](#collaboration)
- [Future Enhancements](#future-enhancements)
- [Resources](#resources)

## Overview

Project Nexus serves as the capstone project of the ProDev Backend Engineering program. This e-commerce backend system showcases expertise in Python, Django, database design, API development, and deployment. The project implements a scalable architecture with secure authentication, efficient data management, and comprehensive API documentation.

## Features

- 🔐 **JWT Authentication** - Secure user authentication and authorization
- 📦 **Product Management** - Complete CRUD operations for products
- 🛒 **Shopping Cart** - User-specific cart management
- 📋 **Order Processing** - Full order lifecycle management
- 🔍 **Advanced Filtering** - Filtering and pagination for large datasets
- 📚 **API Documentation** - Interactive Swagger/OpenAPI documentation
- 🗄️ **PostgreSQL Database** - Efficient relational database management
- 🔒 **Security Best Practices** - CSRF protection and input validation

## Tech Stack

### Core Technologies

- **Python** - Core programming language for backend logic
- **Django** - High-level framework for building scalable web applications
- **Django REST Framework** - Powerful toolkit for building REST APIs
- **PostgreSQL** - Relational database for efficient data management

### Authentication & Security

- **JWT (JSON Web Tokens)** - Secure user authentication and authorization
- **Role-Based Access Control** - User permission management

### API & Documentation

- **Swagger/OpenAPI** - Comprehensive API documentation and testing interface
- **RESTful APIs** - Standard REST architecture for CRUD operations

### Development & Deployment

- **GitHub Actions** - CI/CD pipelines for automated testing and deployment
- **Railway** - Cloud platform for deployment (current)
- **Docker** - Containerization for deployment (planned)

### Planned Integrations

- **Celery & RabbitMQ** - Background task management
- **Redis** - Caching strategies for performance optimization
- **GraphQL** - Flexible data fetching (optional implementation)

## Project Structure

```
alx-project-nexus/
├── config/              # Django project configuration
├── products/            # Product management app
├── orders/              # Order processing app
├── users/               # User authentication app
├── carts/               # Shopping cart app
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/xpowder/alx-project-nexus.git
   cd alx-project-nexus
   ```

2. **Create a virtual environment**

   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **Linux/Mac:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the root directory. For local development with SQLite (easiest), you only need:

   ```env
   SECRET_KEY=your_secret_key_here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
   ```

   **Generate a secret key:**
   ```bash
   python generate_secret_key.py
   ```
   
   Copy the generated key to your `.env` file.

   **Note:** The project uses SQLite by default for local development (no database setup needed). If you want to use PostgreSQL, see the deployment section.

5. **Run migrations**

   ```bash
   python manage.py migrate
   ```

6. **Create a superuser** (optional)

   ```bash
   python manage.py createsuperuser
   ```

7. **Load sample products** (optional but recommended)

   ```bash
   python manage.py load_sample_data
   ```
   
   This will create sample categories and products for testing.

8. **Run the development server**

   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/`

### Quick Setup (Automated)

**Windows:**
```bash
setup_local.bat
```

**Linux/Mac:**
```bash
chmod +x setup_local.sh
./setup_local.sh
```

Then follow the prompts to complete the setup.

## API Documentation

### Interactive Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: `http://localhost:8000/api/docs/`
- **Production API Docs**: [Live API Documentation](https://alx-project-nexus-production-53e7.up.railway.app/api/docs/)

### Example Endpoints

- **GET** `/api/products/` - List all products with filtering and pagination
- **POST** `/api/auth/login/` - Authenticate and receive JWT token
- **POST** `/api/auth/register/` - Register a new user
- **GET** `/api/carts/` - Retrieve user's shopping cart
- **POST** `/api/carts/` - Add items to the user's cart
- **POST** `/api/orders/` - Create a new order
- **GET** `/api/orders/` - List user's orders

## Deployment

This project is configured for deployment on [Render](https://render.com/), a modern cloud platform that provides seamless deployment for Django applications.

### Quick Deploy to Render

1. **Fork/Clone this repository** to your GitHub account

2. **Create a new Web Service on Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure the Web Service**
   - **Name**: `alx-project-nexus` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn config.wsgi:application`
   - **Plan**: Free (or upgrade for production)

4. **Create a PostgreSQL Database**
   - Click "New +" → "PostgreSQL"
   - Name: `alx-project-nexus-db`
   - Plan: Free (or upgrade for production)
   - Copy the Internal Database URL

5. **Set Environment Variables**
   Add the following environment variables in the Render dashboard:

   ```
   SECRET_KEY=your-secret-key-here (generate a strong random key)
   DEBUG=False
   DATABASE_URL=<automatically set if using render.yaml>
   PYTHON_VERSION=3.11.0
   ALLOWED_HOSTS=your-app-name.onrender.com
   CSRF_TRUSTED_ORIGINS=https://your-app-name.onrender.com
   ```

6. **Deploy using render.yaml (Recommended)**
   
   The project includes a `render.yaml` file for automatic configuration:
   - Render will automatically detect `render.yaml`
   - It will create the web service and database automatically
   - Environment variables can be set manually or through the dashboard

7. **Run Migrations**
   After the first deployment, run migrations:
   - Go to your service → "Shell"
   - Run: `python manage.py migrate`
   - Create superuser: `python manage.py createsuperuser`

8. **Your app is live!** 🎉
   - Access at: `https://your-app-name.onrender.com`
   - Admin panel: `https://your-app-name.onrender.com/admin/`
   - API docs: `https://your-app-name.onrender.com/api/docs/`

### Manual Deployment Steps

If you prefer manual setup without `render.yaml`:

1. **Create Web Service** in Render dashboard
2. **Set Build Command**:
   ```bash
   pip install -r requirements.txt && python manage.py collectstatic --noinput
   ```
3. **Set Start Command**:
   ```bash
   gunicorn config.wsgi:application
   ```
4. **Create PostgreSQL Database** and link it to your service
5. **Configure Environment Variables** as listed above
6. **Deploy**

### Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Django secret key for cryptographic signing | ✅ Yes |
| `DEBUG` | Set to `False` in production | ✅ Yes |
| `DATABASE_URL` | PostgreSQL connection string (auto-set by Render) | ✅ Yes |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hostnames | ✅ Yes |
| `CSRF_TRUSTED_ORIGINS` | Comma-separated list of trusted origins | ✅ Yes |
| `PYTHON_VERSION` | Python version (e.g., 3.11.0) | Optional |

### Troubleshooting Deployment

**Issue: Static files not loading**
- Solution: Ensure `collectstatic` runs during build and WhiteNoise is configured (already set up)

**Issue: Database connection errors**
- Solution: Verify `DATABASE_URL` is set correctly and database is running

**Issue: 500 errors after deployment**
- Solution: Check Render logs, ensure all environment variables are set, and migrations are run

**Issue: CSRF verification failed**
- Solution: Add your Render URL to `CSRF_TRUSTED_ORIGINS` environment variable

### Previous Deployment

The project was previously deployed on Railway:
- **Railway Deployment**: [Production Site](https://alx-project-nexus-production-53e7.up.railway.app/)
- **Admin Panel**: [Admin Dashboard](https://alx-project-nexus-production-53e7.up.railway.app/admin/)

## Challenges & Solutions

### Challenge: Database Schema Design

**Problem**: Designing an efficient database schema for complex e-commerce operations.

**Solution**: Created a comprehensive Entity Relationship Diagram (ERD) using Draw.io to visualize and optimize relationships between entities (User, Cart, Product, Order, OrderItem). Implemented normalized schemas with foreign key relationships for scalability.

### Challenge: Secure User Authentication

**Problem**: Ensuring secure user authentication in a RESTful API environment.

**Solution**: Integrated JWT (JSON Web Tokens) authentication with Django REST Framework, implementing token-based authentication with refresh token capabilities and role-based access control.

### Challenge: Large Dataset Management

**Problem**: Efficiently managing and retrieving large datasets with optimal performance.

**Solution**: Implemented Django filters and pagination in API endpoints, allowing clients to filter, sort, and paginate results efficiently.

### Challenge: API Documentation

**Problem**: Providing comprehensive API documentation for frontend integration and team collaboration.

**Solution**: Utilized Swagger/OpenAPI to generate interactive, comprehensive API documentation that allows developers to test endpoints directly from the browser.

## Best Practices

### Code Quality

- ✅ Followed Django conventions for app structure and ORM usage
- ✅ Maintained clean, modular code with separation of concerns
- ✅ Used descriptive Git commit messages following conventional commit format
- ✅ Implemented comprehensive error handling and validation

### Security

- ✅ Used environment variables for sensitive data (database credentials, API keys)
- ✅ Implemented CSRF protection and input validation
- ✅ Secure password hashing and JWT token management
- ✅ Role-based access control for API endpoints

### Development Workflow

- ✅ Version control with Git and GitHub
- ✅ CI/CD pipelines with GitHub Actions
- ✅ Comprehensive API documentation
- ✅ Test-driven development approach

## Collaboration

This project was developed in collaboration with ProDev Backend and Frontend learners:

- **Communication**: Coordinated via the `#ProDevProjectNexus` Discord channel
- **Integration**: Aligned API endpoints with frontend requirements
- **Knowledge Sharing**: Exchanged ideas and organized coding sessions
- **Code Review**: Participated in peer code reviews and feedback sessions

## Future Enhancements

- [ ] **Docker Integration** - Containerized deployment for consistency across environments
- [ ] **Celery & RabbitMQ** - Background task management for order processing and notifications
- [ ] **Redis Caching** - Implement caching strategies for improved performance
- [ ] **GraphQL API** - Alternative API layer for flexible data fetching
- [ ] **Unit & Integration Tests** - Comprehensive test coverage
- [ ] **API Rate Limiting** - Protect endpoints from abuse
- [ ] **Email Notifications** - Order confirmations and status updates
- [ ] **Payment Integration** - Stripe or PayPal integration for transactions
- [ ] **Search Functionality** - Full-text search for products
- [ ] **Image Upload** - Cloud storage integration for product images

## Resources

### Project Links

- **Repository**: [GitHub Repository](https://github.com/xpowder/alx-project-nexus.git)
- **Live Application**: [Production Site](https://alx-project-nexus-production-53e7.up.railway.app/)
- **API Documentation**: [Interactive API Docs](https://alx-project-nexus-production-53e7.up.railway.app/api/docs/)
- **Admin Panel**: [Admin Dashboard](https://alx-project-nexus-production-53e7.up.railway.app/admin/)

### Documentation & Design

- **ERD Diagram**: [Database Schema](https://drive.google.com/file/d/1Ia26xv9PQZlnbwLdQ-9RcaB1qN6G5w8g/view?usp=sharing)
- **Presentation Slides**: [Project Presentation](https://docs.google.com/presentation/d/1z4o_UOKDW_0jvJ6VSJtcUD_MOooUVFktt2YEX7ZhhqU/edit?usp=sharing)
- **Demo Video**: [Video Demonstration](https://mega.nz/file/p64XRJhT#7ZV-G7edxcpZYuJ1OVy4Nr3ilqS4UqqEOHHUrC_fEuM)

### Technologies & Frameworks

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [JWT Authentication](https://jwt.io/)

---

**Developed as part of the ProDev Backend Engineering Program**

For questions or contributions, please open an issue or submit a pull request.
