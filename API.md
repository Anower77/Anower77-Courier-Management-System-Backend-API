| Method  | Endpoint                               | Role       | Purpose                           |
| ------- | -------------------------------------- | ---------- | --------------------------------- |
| `POST`  | `/api/v1/orders/user/create/`          | `user`     | Place a new courier order         |
| `GET`   | `/api/v1/orders/user/orders/`          | `user`     | View user's own orders            |
| `GET`   | `/api/v1/orders/delivery/orders/`      | `delivery` | Delivery man sees assigned orders |
| `PATCH` | `/api/v1/orders/delivery/status/<id>/` | `delivery` | Update order status               |
| `GET`   | `/api/v1/orders/admin/orders/`         | `admin`    | View all orders                   |
| `PATCH` | `/api/v1/orders/admin/assign/<id>/`    | `admin`    | Assign delivery man to order      |
| `POST`  | `/api/v1/orders/payment/session/`      | `user`     | Create Stripe payment session     |





{ "username": "admin1", "password": "Admin123!", "role": "admin" }

{ "username": "delivery1", "password": "Delivery123!", "role": "delivery" }

{ "username": "user1", "password": "User123!", "role": "user" }




pass: anower77