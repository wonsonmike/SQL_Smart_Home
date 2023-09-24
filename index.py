"""
SQL Database - Smart Home sensor tracker

This simple program will allow for tracking of smart sensors in the home through an SQL database.
There is an option to use a database file or store the database in memory, simply change which line is commented out
"""

#--------SETUP------------------------------------------

import sqlite3

# Connect to the database
con = sqlite3.connect('database')
#con = sqlite3.connect(':memory:')
cur = con.cursor()


#--------ACTION----FUNCTIONS-----------------------------

# Create new entry (device)
def newDevice():
    # Select a room
    room = selectRoom()

    # Get device name
    device = input("Enter device name: ")

    # Loop through until it's a new device name
    while (ifDeviceExists(room, device)):
        print("Device with that name already exists. Please create a new device name.")
        print("Here is a list of the current devices in that room, to prevent confusion:")
        cur.execute("SELECT name FROM "+room)
        print(cur.fetchall(), "\n")
        device = input("Please enter a new device name: ")

    # Device name has been verified as new, now get the status
    status = input("Enter device status: ")

    # Add the device to the room
    cur.execute("INSERT INTO "+room+" VALUES (?, ?)", (device, status))
    con.commit()

    # Sanity check and verify to the user that the device was added
    if(ifDeviceExists(room, device)):
        print("Device "+device+" added to "+room+" successfully.")

# Create a new table (room)
def newRoom():
    # Get room name
    room = input("Enter room name: ")

    # Loop through until it's a new room
    while (ifRoomExists(room)):
        print("That room already exists.")
        room = input("Please enter a new room name: ")
    
    # Create the room
    cur.execute('CREATE TABLE '+room+' (name, status)')
    con.commit()
    
    # Sanity check and verify to the user that the room was created
    if (ifRoomExists(room)):
        print("Room "+room+" created successfully.")

# Edit an existing entry (device)
def editDevice():
    # Get room and device, then show current status
    room = selectRoom()
    device = selectDevice(room)
    cur.execute("SELECT status FROM "+room+" WHERE name='"+device+"'")
    status = cur.fetchall()
    print("Current device status: "+status[0][0])

    # Get new status, and update it
    status = input("Enter new device status: ")
    cur.execute("UPDATE "+room+" SET status='"+status+"' WHERE name='"+device+"'")
    con.commit()
    print(device+" successfully updated.")

# Remove an entry (device)
def removeDevice():
    # Get room and device
    room = selectRoom()
    device = selectDevice(room)

    # Delete that device
    cur.execute("DELETE FROM "+room+" WHERE name='"+device+"'")
    con.commit()
    
    # Sanity check that the device is gone, and verification for the user
    if not (ifDeviceExists(room, device)):
        print(device+" removed from "+room+" successfully.")

# Drop a table (room)
def clearRoom():
    # Select the room
    room = selectRoom()
    
    # Drop that table
    cur.execute("DROP TABLE "+room)
    con.commit()

    # Sanity check that the room is gone, and verification for the user
    if not (ifRoomExists(room)):
        print(room+" removed successfully.")

# Query data from a table (room)
def showDevices():
    # Get room
    room = selectRoom()

    # Query all devices from that room
    cur.execute('SELECT * FROM '+room)
    devices = cur.fetchall()

    # Display the devices
    if len(devices) == 0:
        print("No devices in this room yet")
    for i in range(len(devices)):
        print(f"{i+1}) {devices[i][0]} - {devices[i][1]}")

# Show a list of the tables (rooms)
def showRooms():
    # Query all rooms
    cur.execute("SELECT * FROM sqlite_master WHERE type='table'")
    rooms = cur.fetchall()
    
    # Display the rooms
    if len(rooms) == 0:
        print("No rooms yet")
    for i in range(len(rooms)):
        print(f"{i+1}) {rooms[i][1]}")

# Merge two tables
def mergeRooms():
    # Select 2 rooms to merge
    room1 = selectRoom()
    room2 = selectRoom()

    # Check that they're not the same room
    while (room1 == room2):
        print("Those are the same room. Choose a different room.")
        room2 = selectRoom()

    # Join the two rooms
    cur.execute("SELECT * FROM "+room2)
    devices = cur.fetchall()
    for device in devices:
        # If that device name is taken in room1, add a number to the end
        i = 1
        while (ifDeviceExists(room1, device[0])):
            list1 = list(device)
            list1[0] = list1[0] + f"{i}"
            device = tuple(list1)
            i += 1
        # Device name should be unique now, so add it to room1
        cur.execute("INSERT INTO "+room1+" VALUES (?, ?)", (device[0], device[1]))

    # Get rid of room2
    cur.execute("DROP TABLE "+room2)
    con.commit()

# Get the next action from the user
def showOptions():
    print("Choose from the following options: ")
    print("1) Create new device")
    print("2) Create new room")
    print("3) Edit device status")
    print("4) Remove device")
    print("5) Remove room")
    print("6) Show devices in room")
    print("7) Show a list of rooms")
    print("8) Merge two rooms")
    print("e) Exit\n")
    return "-->"

# Handle the user's selection
def handleOption():
    next = ''
    while (next != 'e'):
        next = input(showOptions())
        if next == '1':
            newDevice()
        elif next == '2':
            newRoom()
        elif next == '3':
            editDevice()
        elif next == '4':
            removeDevice()
        elif next == '5':
            clearRoom()
        elif next == '6':
            showDevices()
        elif next == '7':
            showRooms()
        elif next == '8':
            mergeRooms()
        elif next == 'e':
            pass
        else:
            print("Command not accepted. Please try again.")
        print("\n\n")


#--------ASSISTING-----FUNCTIONS-----------------------------


# Check if entry (device) exists 
def ifDeviceExists(room, device):
    if (ifRoomExists(room)):
        # If room is valid, query all devices there
        cur.execute("SELECT * FROM "+room)
        devices = cur.fetchall()
        # Loop through all devices, checking if that name exists
        for i in range(len(devices)):
            if devices[i-1][0] == device:
                return True
        # If it got through the loop, the device isn't in the room
        return False
    #If room doesn't exist, also return false
    return False

# Check if the table (room) exists
def ifRoomExists(room):
    # Query all rooms
    cur.execute("SELECT * FROM sqlite_master WHERE type='table'")
    rooms = cur.fetchall()

    # Loop through all rooms, checking if that name exists
    for i in range(len(rooms)):
        if rooms[i-1][1] == room:
            return True
    # If it got through the loop, the room doesn't exist
    return False

# Select an entry (device) from a table (room). This function assumes the room exists.
def selectDevice(room):
    # Query all devices from the room provided
    cur.execute("SELECT * FROM "+room)
    devices = cur.fetchall()

    # If the room is empty, keep asking to create devices until the room has a device
    while (len(devices) == 0):
        print("No devices in "+room+" yet. Please create a device first")
        newDevice()
        cur.execute("SELECT * FROM "+room)
        devices = cur.fetchall()

    # List the devices in the room
    print("Devices in "+room+":")
    for i in range(len(devices)):
        print(f"{i+1}) {devices[i][0]}")

    # Choose one of the devices in the room
    choice = int(input("Select device number: "))
    while choice < 1 or choice > len(devices):
        print("Invalid device number. Try again.")
        choice = int(input("Select device number: "))
    return devices[choice-1][0]

# Select a table (room)
def selectRoom():
    # Query all tables
    cur.execute("SELECT * FROM sqlite_master WHERE type='table'")
    rooms = cur.fetchall()

    # If there are no rooms, make them create one, and use that room
    if len(rooms) == 0:
        print("No rooms yet. Please create a room first")
        newRoom()
        cur.execute("SELECT * FROM sqlite_master WHERE type='table'")
        oneRoom = cur.fetchone()
        return oneRoom[1]
    
    # List the rooms
    for i in range(len(rooms)):
        print(f"{i+1}) {rooms[i][1]}")

    # Select the desired room
    choice = int(input("Select room number: "))
    while choice < 1 or choice > len(rooms):
        print("Invalid room number. Try again.")
        choice = int(input("Select room number: "))
    return rooms[choice-1][1]


#--------------PROGRAM---START------------------------

# Start the program
handleOption()

# Close the connection before ending the program
con.close()
