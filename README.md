# Courier Management System — Backend

A RESTful Django API for managing courier orders, deliverymen, and admins with secure JWT-based access control and Stripe payment integration.

---

## Features

- JWT Authentication (login, register, profile update)
- Role-based permissions (User, Delivery Man, Admin)
- Order Management
  - Create, track, and assign orders
  - Update delivery status
- Stripe Payment Integration
  - Create payment sessions via Stripe
  - Handle webhook for payment confirmation
- Clean API structure with DRF
- Admin interface with full control

---

## Technologies Used

- Django 5.x
- Django REST Framework (DRF)
- djangorestframework-simplejwt
- Stripe Python SDK
- PostgreSQL (or SQLite for dev)
- Render (for deployment)

---

## Live Links

- **Live API** : [https://courier-management-system-backend-api-9bo8.onrender.com](https://courier-management-system-backend-api-9bo8.onrender.com)
- **GitHub Repo** : [https://github.com/Anower77/Anower77-Courier-Management-System-Backend-API](https://github.com/Anower77/Anower77-Courier-Management-System-Backend-API)
- **Postman Collection** : [Open in Postman](https://www.postman.com/aerospace-architect-76028991/workspace/my-workspace/folder/40606912-b732050d-5545-4be3-8a63-36aa9a1a91a6?action=share&creator=40606912&ctx=documentation&active-environment=40606912-d7ff6c1d-3e3e-4cdf-8831-030caad45f03)

- **Postman Collection (Download)** : [Courier Management System Postman Collection JSON](https://github.com/Anower77/Anower77-Courier-Management-System-Backend-API/blob/main/Courier%20Management%20System%20%E2%80%94%20Backend%20API%20%28Local%20Host%29.postman_collection.json)



---

## API Endpoints Summary

| Method  | Endpoint                               | Role       | Purpose                           |
| ------- | -------------------------------------- | ---------- | --------------------------------- |
| `POST`  | `/api/v1/auth/register/`               | All        | Register a new user               |
| `POST`  | `/api/v1/auth/login/`                  | All        | Login to receive JWT token        |
| `GET`   | `/api/v1/orders/user/orders/`          | `user`     | View user's own orders            |
| `POST`  | `/api/v1/orders/user/create/`          | `user`     | Place a new courier order         |
| `POST`  | `/api/v1/orders/payment/session/`      | `user`     | Create Stripe payment session     |
| `GET`   | `/api/v1/orders/delivery/orders/`      | `delivery` | Delivery man views their orders   |
| `PATCH` | `/api/v1/orders/delivery/status/<id>/` | `delivery` | Update status of an assigned order|
| `GET`   | `/api/v1/orders/admin/orders/`         | `admin`    | Admin views all orders            |
| `PATCH` | `/api/v1/orders/admin/assign/<id>/`    | `admin`    | Admin assigns delivery man        |

---

## Login Credentials (Test Accounts)

| Role         | Username     | Password         |
|--------------|--------------|------------------|
| Admin        | `admin1`     | `AdminPass123!`  |
| Delivery Man | `delivery1`  | `Delivery123!`   |
| User         | `user1`      | `UserPass123!`   |

> Use these accounts to test role-based permissions for endpoints in Postman.

---

## Entity Relationship Diagram (ERD)

![ERD Diagram](/staticfiles/image/ERD.png)

---

## How to Test

1. Use `/api/v1/auth/login/` to get JWT token
2. Add header: Authorization: Bearer <your_access_token>
3. Use the endpoints based on the logged-in user role
4. Use Stripe test card: ``` Card Number: 4242 4242 4242 4242
Exp: any future date
CVC: 123
ZIP: 12345 ```



---

