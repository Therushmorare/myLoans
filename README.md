# ![Logo](https://via.placeholder.com/30) Nexus Finance - Loan Application Platform

[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/) 
[![Django](https://img.shields.io/badge/Django-5.1.3-green)](https://www.djangoproject.com/) 
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5-orange)](https://getbootstrap.com/) 
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

---

## 🌟 Project Overview

**Nexus Finance** is a **modern, responsive web application** that simplifies loan applications for users.  

It provides:  
- **Multi-step loan application forms** with animated progress bars  
- **Document uploads** (ID, proof of income/residence, employment)  
- **Loan tracking & repayment dashboards**  
- **Interactive tables** for repayments with modals to submit payments  
- **Email notifications** for password recovery and loan updates  

---

## 🛠 Features

### Loan Application
- Multi-step forms with floating labels
- Real-time input validation
- Upload supporting documents
- Direct submission to backend

### Dashboard
- View loans, interest, and repayment history
- Submit repayments via modals
- Calculates maximum allowable payments per loan

### User Management
- Registration/login with secure password reset
- Role-based access (client/admin)
- Verification status tracking

---

## 🎨 UI & UX
- Mobile-first **Bootstrap 5** design  
- Floating inputs and textareas  
- Animated progress bars for multi-step forms  
- Smooth transitions between form steps  
- Captivating visuals for loan information  

*Example Screenshots*  

| Loan Application Form | Dashboard |
|----------------------|-----------|
| ![Loan Form](https://via.placeholder.com/400x300) | ![Dashboard](https://via.placeholder.com/400x300) |

---

## ⚙ Tech Stack

| Layer       | Technology                        |
|------------|----------------------------------|
| Backend    | Django 5.1.3, Python 3.10         |
| Frontend   | HTML5, CSS3, Bootstrap 5, JS      |
| Database   | PostgreSQL                        |
| Email      | Django `EmailMultiAlternatives`   |
| Deployment | AWS ECS / Heroku / PythonAnywhere |

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/your-username/nexus-finance.git
cd nexus-finance

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run dev server
python manage.py runserver
