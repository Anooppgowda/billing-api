# Billing Backend API

A simple Billing Backend API developed using FastAPI, MySQL and SQLAlchemy.
# Project Overview

The Billing Backend API is a REST API developed using FastAPI, MySQL, and SQLAlchemy to manage invoices and payments.
It provides CRUD operations, validation, error handling, and database integration for billing management.
The APIs were tested using Swagger UI and Postman as part of the project testing and documentation.


## GitHub Repository

https://github.com/Anooppgowda/billing-api

## Project Date

13 July 2026

---

## Team Members and Responsibilities

| Team Member | Responsibility |
|---|---|
| Anoop P | Billing API basic setup |
| ARAGONDA NIKHIL | Billing database and models |
| Chintha Gayathri | Billing CRUD operations |
| Kallam Poojitha | Billing validation and error handling |
| Sheetal | Billing API testing and documentation |

---

## Technologies Used

- Python
- FastAPI
- MySQL
- SQLAlchemy
- Pydantic
- PyMySQL
- Uvicorn
- Swagger UI
- Postman
- Git
- GitHub

---

## Project Structure

billing-api/
│
├── app/
│   ├── api/
│   │   └── routes/
│   │       └── billing.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── exceptions.py
│   │
│   ├── crud/
│   │   └── billing.py
│   │
│   ├── db/
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── billing.py
│   │   ├── customer.py
│   │   ├── invoice_item.py
│   │   └── payment.py
│   │
│   ├── schemas/
│   │   └── billing.py
│   │
│   └── main.py
│
├── tests/
├── .gitignore
├── README.md
└── requirements.txt


## Run the Project

uvicorn app.main:app --reload