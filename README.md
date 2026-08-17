# 🍽️ Roy's Bistro - Table Reservation System

A modern, full-featured web application for restaurant table reservation management, customer tracking, payment logging, and administrative analytics built with **Django**, **MySQL**, and **Tailwind CSS**.

---

## 🌟 Features

- 📊 **Interactive Analytics Dashboard**: Overview of revenue, table occupancy, upcoming bookings, reservation status breakdowns, and real-time audit logs.
- 👥 **Customer Management**: Full CRUD operations for customer records, searchable contact details, and complete reservation histories.
- 🪑 **Tables & Categories**: Group tables by seating categories (e.g., Main Dining, VIP Lounge, Patio Outdoor), manage seating capacities, locations, and active status toggles.
- 📅 **Reservation System**: Book tables with party guest counts, time slots, special notes, and status workflows (Pending, Confirmed, Cancelled, Completed).
- 💳 **Payment Tracking**: Record booking transactions, payment methods, status tracking (Paid, Pending, Failed, Refunded), and transaction references.
- 📜 **Audit Logging**: Comprehensive activity log tracking system actions and reservation updates.
- 🔐 **Staff Authentication & Django Admin**: Secure staff sign-in/sign-out workflow and customized Django Admin interface at `/admin/`.
- 🌙 **Dark Mode & Responsive UI**: Glassmorphic modern aesthetic built with Tailwind CSS, supporting dark/light mode toggles across mobile and desktop.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.14 / Django 5.0+
- **Database**: MySQL (via `mysqlclient` / `PyMySQL`)
- **Frontend**: HTML5, Vanilla JavaScript, Tailwind CSS (via CDN), FontAwesome Icons
- **Fonts**: Google Fonts (*Plus Jakarta Sans*, *Outfit*)

---

## 🚀 Getting Started

### 1. Prerequisites

Make sure you have the following installed on your machine:
- **Python 3.10+**: [python.org](https://www.python.org/downloads/)
- **MySQL Database**: (e.g., Laragon, XAMPP, or MySQL Server running on `127.0.0.1:3306`)

---

### 2. Installation & Setup

1. **Clone or Open Project Directory**:
   ```bash
   cd Reservation_system
   ```

2. **Create and Activate Virtual Environment**:
   - **Windows (Command Prompt / PowerShell)**:
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **Linux / macOS**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies**:
   ```bash
   pip install django mysqlclient PyMySQL sqlparse tzdata
   ```

4. **Configure Environment Variables**:
   Copy `.env.example` to `.env` (or configure settings in `reservation_sys/settings.py`):
   ```bash
   cp .env.example .env
   ```

5. **Run Database Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Seed Sample Data**:
   Populate the database with initial categories, tables, customer profiles, sample reservations, and payments:
   ```bash
   python populate_sample_data.py
   ```

7. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the Application**:
   - **Main Web App Dashboard**: `http://127.0.0.1:8000/`
   - **Staff Sign In**: `http://127.0.0.1:8000/login/`
   - **Django Admin Interface**: `http://127.0.0.1:8000/admin/`

---

## 👤 Admin & Staff Access

| Panel | URL | Username |
| :--- | :--- | :--- |
| **Django Admin** | `http://127.0.0.1:8000/admin/` | `ivanroy` |
| **Staff App Login** | `http://127.0.0.1:8000/login/` | `ivanroy` |

*(To create additional admin accounts, run: `python manage.py createsuperuser`)*

---

## 🗄️ Database Models Overview

- **`Customer`**: `first_name`, `last_name`, `email`, `phone`
- **`TableCategory`**: `name`, `description`
- **`Table`**: `table_number`, `capacity`, `location`, `is_active`, `category` (FK)
- **`ReservationStatus`**: `name`, `description`, `is_active`
- **`Reservation`**: `customer` (FK), `table` (FK), `reservation_date`, `start_time`, `end_time`, `guests`, `status` (FK), `notes`
- **`Payment`**: `reservation` (FK), `amount`, `payment_method`, `payment_status`, `transaction_ref`, `paid_at`
- **`AuditLog`**: `reservation` (FK), `action`, `performed_by`, `action_time`, `details`

---

## 📄 License

This project is licensed under the MIT License.
