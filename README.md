# Event Management System

A production-ready event management platform built with Django, focused on clean architecture, role-based access control, and real-world deployment considerations. The application supports event creation, discovery, and participation workflows with secure authentication and email-driven interactions.

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

These accounts are provided to allow reviewers to experience the full feature set without setup.

---

## Core Features

- **Role-Based Access Control (RBAC)**  
  Three clearly separated roles using Django Groups:
  - Admin: full system control
  - Organizer: event and category management
  - Participant: event browsing and RSVP

- **Event Management**  
  Create, update, delete, and view events with categories, images, and rich descriptions.

- **RSVP System**  
  Participants can RSVP to events, with safeguards against duplicate registrations and a personalized dashboard to track their RSVPs.

- **Email-Based Authentication & Notifications**  
  - Account activation via secure email links
  - RSVP confirmation emails

- **Optimized Data Access**  
  Efficient database queries using Django ORM features such as `select_related`, `prefetch_related`, filtering, and aggregation.

- **Responsive UI**  
  Server-rendered Django templates styled with Tailwind CSS for clarity and usability.

---

## What I Learned

This project strengthened my understanding of Django as a production framework, not just a development tool.

- Django MVT architecture and template-driven rendering
- Django ORM in depth, including query optimization strategies
- Designing and enforcing RBAC using Django Groups and permissions
- Secure authentication flows with email activation
- Building real-world features like invitations and RSVPs
- Structuring applications for maintainability and clarity

Beyond features, the project emphasized thinking in terms of **systems**, not just views and models.

---

## Challenges & Deployment Experience

Deploying the application was one of the most valuable learning phases.

- I encountered an issue where a theme-related app worked locally but failed in production due to configuration differences. Resolving this required careful inspection of deployment logs and a deeper understanding of how Django loads apps in production environments.

- Another major issue occurred with email verification. While Gmail SMTP worked locally, it failed in production because Gmail rejected emails sent from Render’s domain. After researching email deliverability constraints, I migrated to a third-party email service, which resolved the issue and reinforced why production systems require dedicated external services.

These challenges clarified why behavior can differ between local and production environments and taught me how to debug deployments systematically rather than by trial and error.

---

## Deployment Stack

- **Application Hosting:** Render
- **Database:** PostgreSQL (Neon)
- **Static Files:** WhiteNoise
- **Email Service:** Third-party provider for production reliability

---

## Run Locally

Clone the repository and set up a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file based on `.env.example` and configure environment variables (SECRET_KEY, database, email settings).

Apply migrations and start the server:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The application will be available at:

```
http://127.0.0.1:8000/
```

---

## Technology Stack

- **Backend:** Python, Django
- **Frontend:** Django Templates, Tailwind CSS
- **Database:** PostgreSQL
- **Deployment:** Render + Neon

---

