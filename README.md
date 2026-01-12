# Event Management System

A production-ready event management platform built with Django, demonstrating clean architecture, role-based access control, and real-world deployment practices. This project evolved through multiple iterations, each adding new layers of complexity while maintaining code quality and user experience.

**Live URL:** https://event-management-system-0lcd.onrender.com/

---

## Demo Access

You can explore the live system using the following roles:

- **Admin**  
  Username: `admin`  
  Password: `1234`

- **Organizer**  
  Username: `arnabsahawrk`  
  Password: `##11aaAA`

- **Participant**  
  Username: `arnabsaha5199`  
  Password: `##11aaAA`

---

## Core Features

**Role-Based Access Control**  
The system implements three distinct user roles using Django Groups. Admins have full system control, organizers manage events and categories, and participants can browse events and handle their RSVPs. This ensures proper access control throughout the application.

**Event Management**  
Complete CRUD operations for events with categories, dates, locations, and images. Events are automatically categorized by their status based on scheduled dates.

**RSVP System**  
Participants can register for events through a one-click RSVP system with duplicate prevention. A personalized dashboard lets users track their registered events, with automated email confirmations sent upon registration.

**Authentication & Notifications**  
New users receive account activation emails with secure token-based links. The system includes password reset functionality and RSVP confirmation emails, all handled through a third-party email service for reliability.

**Query Optimization**  
The application uses Django ORM optimization techniques including `select_related` for foreign keys and `prefetch_related` for many-to-many relationships. Complex filtering and aggregation queries power the dashboard statistics.

**Responsive Interface**  
Server-rendered Django templates styled with Tailwind CSS provide a responsive experience across all devices.

---

## How This Project Evolved

This project grew in three major phases, each teaching important lessons about Django and web development.

**Phase 1: Building the Foundation**  
I started by implementing the core models for events, categories, and participants. This phase focused on understanding Django's MVT architecture and getting CRUD operations working properly. I learned early on to optimize database queries using `select_related` and `prefetch_related` to avoid performance issues. Setting up Tailwind CSS with Django taught me how the framework handles static files and how to structure templates for reusability.

**Phase 2: Adding Complexity**  
The second phase introduced user authentication and role-based access control. Implementing Django Groups for permissions required careful planning around view restrictions and access patterns. The RSVP system needed proper handling of many-to-many relationships and preventing duplicate registrations. Email integration for account activation involved learning about secure token generation and Django signals for automated notifications. Deploying this version exposed differences between development and production environments, particularly around email delivery.

**Phase 3: Refactoring and User Profiles**  
The third phase involved significant refactoring work. Converting function-based views to class-based views required understanding Django's view hierarchy and how to properly use mixins. The conversion revealed subtle differences in form handling, context data management, and method overriding that only became clear through implementation.

Implementing a custom user model was the most challenging part. Extending `AbstractUser` to add profile pictures and phone numbers meant creating migrations for an existing database. This taught me that Django's migration system requires careful attention, especially when modifying core models like the user model. Profile management features including editing, password changes, and password resets required understanding Django's built-in authentication views and customizing them appropriately.

---

## Technical Challenges

**Custom User Model Migration**  
Extending the user model after the database already contained user data required careful migration planning. Foreign key relationships needed updating, and the migration had to be tested thoroughly before applying to production.

**Production Email Configuration**  
Gmail SMTP worked locally but failed in production because Render's infrastructure triggered Gmail's security measures. Switching to Brevo for transactional emails solved this and highlighted how production environments often need different configurations than development setups.

**Static and Media Files**  
Understanding the distinction between static files and media files was important. Static files are collected during deployment and served by WhiteNoise. Media files on Render's free tier are ephemeral, being deleted when the server restarts. While this works for demonstration purposes, it clarified why production applications typically use cloud storage.

**Class-Based Views**  
Converting to class-based views meant understanding Django's generic views and knowing which methods to override. The learning curve involved reading documentation carefully and understanding method resolution order, but the resulting code follows Django conventions more closely.

**Form Validation**  
Implementing custom validation for profile pictures with file size and format restrictions required understanding Django's form processing. This involved overriding `clean_` methods and properly handling file uploads including clearing old files and setting defaults.

---

## Deployment Architecture

The application runs on Render's free tier with automatic builds and deployments from GitHub. The build process installs dependencies, builds Tailwind CSS assets, collects static files, and runs migrations.

PostgreSQL hosting through Neon provides reliable database service with a generous free tier. Database connections are configured through environment variables, making it simple to switch between environments.

WhiteNoise serves static files directly from Django, eliminating the need for separate static file infrastructure. This works well for this scale of application.

After encountering Gmail SMTP issues in production, I switched to Brevo's transactional email service for reliable delivery with proper email authentication.

User-uploaded images are stored on Render's ephemeral file system, meaning they're deleted on server restarts. This is acceptable for demonstration but would require cloud storage for production use.

---

## Running Locally

Clone the repository and create a virtual environment:
```bash
git clone <repository-url>
cd event-management-system
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Create a `.env` file based on `.env.example` with your environment variables. You'll need PostgreSQL database credentials and email service configuration.

Run migrations and create a superuser:
```bash
python manage.py migrate
python manage.py createsuperuser
```

Build Tailwind CSS assets:
```bash
cd theme/static_src
npm install
npm run build
cd ../..
```

Start the development server:
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

---

## What I Learned

This project deepened my understanding of Django as a framework for production applications rather than just simple websites.

I learned to think in terms of reusable components. Template inheritance, form classes, and model managers all encourage writing code once and using it throughout the application. This shift from writing isolated functions to building interconnected systems changed how I approach development.

Query optimization became a consistent consideration. Using Django Debug Toolbar helped me identify inefficient queries and understand when to use `select_related` versus `prefetch_related`. Small inefficiencies become significant as applications scale.

Django's separation of authentication and authorization became clearer through implementing role-based access control. Building this from scratch helped me understand why Django's permission system works the way it does.

Class-based views demonstrated the value of object-oriented programming in web applications. While function-based views are initially simpler, class-based views offer better code reuse through inheritance and mixins. Understanding when to use each approach came from practical implementation.

The deployment process showed that local functionality is just the starting point. Production environments have different constraints and failure modes. Debugging through logs, understanding configuration differences, and implementing proper error handling all came from actual deployment experience.

Building this project iteratively, with each phase building on previous work, sometimes required refactoring earlier code. This mirrors real development where requirements change and code must adapt. Learning to refactor safely and write careful migrations came from working through these iterations.

---

## Technology Stack

**Backend:** Python 3.14, Django 5.2  
**Frontend:** Django Templates, Tailwind CSS 3.4  
**Database:** PostgreSQL 16  
**Deployment:** Render, Neon, WhiteNoise  
**Email:** Brevo  
**Version Control:** Git, GitHub

---