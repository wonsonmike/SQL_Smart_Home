# Overview

This software is a program that utilizes SQL Relational Databases to manage the states of smart home sensors. Each room in the home is saved as a table, and each device/sensor is saved as an entry in that table. You can store the device name and the state it's in (on/off, open/closed, etc.). You can create new devices and rooms, modify them, delete them, and merge multiple rooms if you want. Using the program is as simple as running it in the terminal. You'll be provided with options of what you want to do, and guided through the steps needed to do what is desired.

My purpose for creating this software is to familiarize myself with how SQL Relational Databases function. I wanted to learn the basics of how they work, and create a functioning program utilizing this technology. 

[Software Walkthrough Video](https://www.youtube.com/watch?v=SZdBkulonV8)
[Software Demo Video](https://www.youtube.com/watch?v=8iJ8zJFeb7Q)

# Relational Database

I am using sqLite to create the relational database.

The structure of the relational database is a list of rooms with devices in the rooms. Rooms are represented as Tables, and the devices in them are entries on the table. The tables have two columns, name and status.

# Development Environment

I developed this software using the VSCode IDE. 

I used Python and sqLite to develop this software.

# Useful Websites

- [sqLite Tutorial](https://www.sqlitetutorial.net/)
- [w3schools SQL Tutorial](https://www.w3schools.com/sql/)

# Future Work

- Add method to separate room into two rooms/zones
- Add more default columns in the tables
- Add the ability to add/remove columns in the tables
- Add nicer looking formatting