# slotify-backend


##  Project Description

Slotify is a smart parking reservation platform designed to simplify the way you find and book parking. Whether you're heading to work, shopping, or an event, Slotify lets you reserve your parking space in advance, saving you time, reducing stress, and helping you avoid the hassle of circling around.

With just a few clicks, users can view available slots in real-time, choose the most convenient location, and secure their spot instantly. Our mission is to make urban parking effortless by combining intuitive design with reliable, up-to-date information.

Slotify is built with convenience in mind, so your parking is one less thing to worry about.


---

## Story 

Users can register on the Slotify platform by providing a username, email, and password. Once registered and logged in, users can browse available garages and view open parking spots. They can reserve spots, as well as create, view, update, and cancel their own reservations. Additionally, users have full control over their vehicles, with the ability to add, edit, or delete vehicle details. Company administrators have access to manage garage facilities and oversee reservation activity. The admin interface is being designed to resemble the SDA management system, offering a more intuitive and structured experience for administrative users.




---

##  Repository Description
This backend handles:
- User authentication (signup/login)
- Managing garages and parking spots
- Managing user vehicles
- Managing reservations

---


## Model 

- Garage with parking spot (one - to -many)
- Parking spot with a reservation (one - to -one)
- User with reservation (one - to - many)
- User with vehicle (one - to -many)
- Reservation with vehicle (one - to - one)


---

## Tech Stack
- Python
- Django
- PostgreSQL
- Docker 

---

## Front End Repo Link

(https://github.com/Rana370/slotify-frontend)

---

## 🗺️ ERD Diagram



<img width="100%" src="./ERD.png">


## Routing Table

Method          URL                     Purpose
POST        /user/signup/                   Create new user account
POST        /user/login/                    Log in existing user
GET         /dashboard/                     List all garages
GET         /garage/:garage_id/             List all parking spots in selected garage
POST        /parking_spot/:id/reservation/  Create a new reservation
GET         /reservations/                  View my reservations
PUT         /reservations/:id/              Update my reservation
DELETE      /reservation/:id/               Cancel my reservation
GET         /vehicle/                       View my vehicle(s)
PUT         /vehicle/:id/                   Update my vehicle
DELETE      /vehicle/:id/                   Delete my vehicle


---

## IceBox Features
Add role field to User model for Garage Manager functionality

Create permission logic for garage managers to assign and manage parking spots

Build analytics endpoints for admin dashboard (e.g., reservation trends, peak times)

Integrate email notification system for upcoming or cancelled reservations

Implement real-time spot availability using WebSockets or polling

Use Redis or caching to improve performance of live availability updates

Create Payment model with amount, status, timestamp, and reservation relation

Integrate third-party payment gateway (e.g., Stripe or PayPal)

Add passkey field to Company model for secure company-linked registration

Validate passkey during signup and auto-link user to corresponding company