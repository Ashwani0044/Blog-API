# Blog API (Instagram-like Backend)

A feature-rich backend API built using **Flask** that simulates core functionalities of a social media platform like Instagram — including posts, comments, likes, follow system, and feed generation.

---

##  Features

###  Authentication

* User Signup & Login
* Password hashing using bcrypt
* JWT-based authentication

###  Posts

* Create, update, delete posts
* Pagination & search support
* Image URL support

###  Comments

* Add, update, delete comments
* Fetch comments for each post

###  Likes

* Like / Unlike posts (toggle system)
* Get total likes per post

###  Follow System

* Follow / Unfollow users
* Get followers & following lists

###  Feed System

* Personalized feed based on followed users
* Sorted by latest posts
* Pagination supported

---

##  Tech Stack

* **Backend Framework:** Flask
* **Database:** SQLite
* **ORM:** SQLAlchemy
* **Authentication:** JWT (Flask-JWT-Extended)
* **Migrations:** Flask-Migrate
* **Security:** bcrypt

---

##  Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Ashwani0044/blog-api.git
cd blog-api
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

```bash
.venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install flask flask_sqlalchemy flask_jwt_extended flask_migrate bcrypt
```

---

### 4️⃣ Setup Database

```bash
flask db init
flask db migrate -m "initial migration"
flask db upgrade
```

---

### 5️⃣ Run the App

```bash
flask run
```

---

##  API Authentication

For protected routes, add header:

```http
Authorization: Bearer <your_token>
```

---

## API Endpoints

### Auth

* `POST /signup`
* `POST /login`

---

###  Posts

* `POST /posts`
* `GET /posts`
* `GET /posts/<id>`
* `PUT /posts/<id>`
* `DELETE /posts/<id>`

---

###  Comments

* `POST /posts/<id>/comments`
* `GET /posts/<id>/comments`
* `PUT /comments/<id>`
* `DELETE /comments/<id>`

---

###  Likes

* `POST /posts/<id>/like`
* `GET /posts/<id>/likes`

---

###  Follow

* `POST /users/<id>/follow`
* `GET /users/<id>/followers`
* `GET /users/<id>/following`

---

###  Feed

* `GET /feed?page=1&per_page=10`

---

##  Testing

Tested using **Thunder Client (VS Code)**

---

##  Common Issues & Fixes

###  Migration Issues

```bash
flask db migrate
flask db upgrade
```

---

###  JWT Errors

Ensure:

* Token is passed in headers
* `@jwt_required()` is added

---

##  Future Improvements

* 🤖 AI Features (Caption Generator, Summarizer)
* ☁️ Cloud Deployment (AWS)
* 🖼️ Image Upload (S3)
* 🌐 Frontend Integration (React)

---

## Conclusion

This project demonstrates strong backend fundamentals including:

* REST API design
* Authentication & authorization
* Database relationships
* Scalable feature development

---

## ⭐ If you like this project

Give it a ⭐ on GitHub and feel free to contribute!

---
