import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

room_file = 'rooms.csv'


# Add a room
def add_room():
    rooms = pd.read_csv(room_file)

    room_no = input('Enter the room number: ')
    room_type = input('Enter the room type: ')
    floor_no = input('Enter the floor number: ')

    room_data = {
        'Room_No': int(room_no),
        'Type': room_type,
        'Floor': int(floor_no),
        'Status': 'Available',
        'Booking_Count': 0,
        'Guest_Name': '',
        'Check_In': ''
    }

    rooms.loc[len(rooms)] = room_data
    rooms.to_csv(room_file, index=False)

    print("Room successfully added.")


# Check room number
def check_room(room_no, rooms):
    try:
        room_no = int(room_no)
    except:
        print("Room number can only be an integer.")
        return False

    room_list = list(rooms['Room_No'])

    if room_no in room_list:
        return True
    else:
        print("This room number does not exist.")
        return False


# Display all rooms
def display_rooms():
    rooms = pd.read_csv(room_file)

    print("\nAll Rooms")
    print("-" * 50)
    print(rooms)


# Search room by number
def search_room_by_number():
    rooms = pd.read_csv(room_file)

    room_no = input("Enter the room number: ")

    if check_room(room_no, rooms):
        room_no = int(room_no)

        result = rooms[rooms['Room_No'] == room_no]
        print(result)


# Search room by type
def search_room_by_type():
    rooms = pd.read_csv(room_file)

    room_type = input("Enter the room type: ")

    result = rooms[rooms['Type'].str.lower() == room_type.lower()]

    if len(result) == 0:
        print("No room of this type was found.")
    else:
        print(result)


# Update room
def update_room():
    rooms = pd.read_csv(room_file)

    room_no = input("Enter the room number: ")

    if not check_room(room_no, rooms):
        return

    room_no = int(room_no)

    row = rooms[rooms['Room_No'] == room_no].index[0]

    print("Enter the new details.")

    new_type = input("Enter the new room type: ")
    new_floor = input("Enter the new floor number: ")

    rooms.loc[row, 'Type'] = new_type
    rooms.loc[row, 'Floor'] = int(new_floor)

    rooms.to_csv(room_file, index=False)

    print("Room details updated successfully.")


# Delete room
def delete_room():
    rooms = pd.read_csv(room_file)

    room_no = input("Enter the room number: ")

    if not check_room(room_no, rooms):
        return

    room_no = int(room_no)

    row = rooms[rooms['Room_No'] == room_no].index[0]

    if rooms.loc[row, 'Status'] == 'Occupied':
        print("This room is currently occupied.")
        print("It cannot be deleted.")
        return

    print("Are you sure you want to delete room", room_no, "?")

    answer = input("Enter Yes or No: ")

    if answer == "No" or answer == "no" or answer == "NO":
        return

    rooms = rooms.drop(row)
    rooms = rooms.reset_index(drop=True)

    rooms.to_csv(room_file, index=False)

    print("Room deleted successfully.")


# Book a room
def book_room():
    rooms = pd.read_csv(room_file)

    room_no = input("Enter the room number: ")

    if not check_room(room_no, rooms):
        return

    room_no = int(room_no)

    row = rooms[rooms['Room_No'] == room_no].index[0]

    if rooms.loc[row, 'Status'] == 'Occupied':
        print("This room is already occupied.")
        return

    guest = input("Enter guest name: ")

    rooms.loc[row, 'Status'] = 'Occupied'
    rooms.loc[row, 'Guest_Name'] = guest
    rooms.loc[row, 'Booking_Count'] += 1
    rooms.loc[row, 'Check_In'] = str(date.today())

    rooms.to_csv(room_file, index=False)

    print("Room successfully booked.")
    print("Guest has been checked in.")


# Check out a guest
def checkout():
    rooms = pd.read_csv(room_file)

    room_no = input("Enter the room number: ")

    if not check_room(room_no, rooms):
        return

    room_no = int(room_no)

    row = rooms[rooms['Room_No'] == room_no].index[0]

    if rooms.loc[row, 'Status'] == 'Available':
        print("This room is already available.")
        return

    rooms.loc[row, 'Status'] = 'Available'
    rooms.loc[row, 'Guest_Name'] = ''
    rooms.loc[row, 'Check_In'] = ''

    rooms.to_csv(room_file, index=False)

    print("Guest successfully checked out.")
    print("Room is now available.")


# Display occupied rooms
def show_occupied():
    rooms = pd.read_csv(room_file)

    occupied = rooms[rooms['Status'] == 'Occupied']

    print("\nOccupied Rooms")
    print("-" * 30)

    print(occupied)


# Display available rooms
def show_available():
    rooms = pd.read_csv(room_file)

    available = rooms[rooms['Status'] == 'Available']

    print("\nAvailable Rooms")
    print("-" * 30)

    print(available)


# Graph showing bookings by room type
def graph_room_types():
    rooms = pd.read_csv(room_file)

    booking_data = rooms.groupby('Type')['Booking_Count'].sum()

    plt.bar(
        booking_data.keys(),
        booking_data.values
    )

    plt.xlabel('Room Type')
    plt.ylabel('Number of Bookings')
    plt.title('Bookings by Room Type')

    plt.xticks(rotation=30)
    plt.show()


# Graph showing most booked rooms
def graph_top_rooms():
    rooms = pd.read_csv(room_file)

    rooms = rooms.sort_values(
        by='Booking_Count',
        ascending=False
    )

    rooms = rooms.head(10)

    plt.bar(
        rooms['Room_No'].astype(str),
        rooms['Booking_Count']
    )

    plt.xlabel('Room Number')
    plt.ylabel('Number of Bookings')
    plt.title('Most Booked Rooms')

    plt.show()


# Graph showing number of rooms of each type
def graph_room_count():
    rooms = pd.read_csv(room_file)

    room_count = rooms['Type'].value_counts()

    plt.bar(
        room_count.keys(),
        room_count.values
    )

    plt.xlabel('Room Type')
    plt.ylabel('Number of Rooms')
    plt.title('Number of Rooms by Type')

    plt.xticks(rotation=30)
    plt.show()


# Generate bill
def generate_bill():
    rooms = pd.read_csv(room_file)
    setup = pd.read_csv('hotelsetup.csv')

    room_no = input("Enter the room number: ")

    if not check_room(room_no, rooms):
        return

    room_no = int(room_no)

    row = rooms[
        rooms['Room_No'] == room_no
    ].index[0]

    if rooms.loc[row, 'Status'] == 'Available':
        print("This room is not currently occupied.")
        return

    guest = rooms.loc[row, 'Guest_Name']
    room_type = rooms.loc[row, 'Type']

    check_in_date = pd.to_datetime(
        rooms.loc[row, 'Check_In']
    ).date()

    today = date.today()

    days = max(
        1,
        (today - check_in_date).days
    )

    type_data = setup[
        setup['Room_Type'] == room_type
    ]

    if len(type_data) == 0:
        print("Room type not found in hotel setup.")
        return

    per_day = float(
        type_data.iloc[0]['Per_Day_Charge']
    )

    fixed_charge = float(
        setup.loc[0, 'Fixed_Charge']
    )

    room_charge = days * per_day
    total = fixed_charge + room_charge

    print()
    print("---------------------------------------------")
    print("             CITY HOTEL")
    print("             GUEST BILL")
    print("---------------------------------------------")

    print("Guest Name  :", guest)
    print("Room No.    :", room_no)
    print("Room Type   :", room_type)
    print("Check-in    :", check_in_date.strftime("%d-%m-%Y"))
    print("Check-out   :", today.strftime("%d-%m-%Y"))
    print("Days Stayed :", days)

    print("---------------------------------------------")

    print("Fixed Charge :", fixed_charge, "/-")
    print("Room Charge  :", room_charge, "/-")
    print("Total Amount :", total, "/-")

    print("---------------------------------------------")
    print("Thank you for staying at City Hotel!")
    print("---------------------------------------------")

    checkout_room_after_bill(room_no)


# Make room available after billing
def checkout_room_after_bill(room_no):
    rooms = pd.read_csv(room_file)

    row = rooms[
        rooms['Room_No'] == room_no
    ].index[0]

    rooms.loc[row, 'Status'] = 'Available'
    rooms.loc[row, 'Guest_Name'] = ''
    rooms.loc[row, 'Check_In'] = ''

    rooms.to_csv(room_file, index=False)

    print("Room has been checked out.")


# Main menu
def menu():
    print("\n")
    print("==============================================")
    print("          HOTEL MANAGEMENT SYSTEM")
    print("==============================================")

    print("1. Add a New Room")
    print("2. Update Room")
    print("3. Delete Room")
    print("4. Search Room")
    print("5. Display All Rooms")
    print("6. Book Room / Check-in")
    print("7. Check-out")
    print("8. Show Occupied Rooms")
    print("9. Show Available Rooms")
    print("10. Room Type Booking Graph")
    print("11. Most Booked Rooms Graph")
    print("12. Room Count Graph")
    print("13. Generate Bill")

    print("\n0. Exit")
    print("==============================================")


menu()

choice = input("\nEnter your choice: ")

if choice == '1':
    add_room()

elif choice == '2':
    update_room()

elif choice == '3':
    delete_room()

elif choice == '4':
    print("\nSearch Room")
    print("-" * 25)
    print("1. Search by Room Number")
    print("2. Search by Room Type")

    search_choice = input("\nEnter your choice: ")

    if search_choice == '1':
        search_room_by_number()

    elif search_choice == '2':
        search_room_by_type()

    else:
        print("Invalid choice.")

elif choice == '5':
    display_rooms()

elif choice == '6':
    book_room()

elif choice == '7':
    checkout()

elif choice == '8':
    show_occupied()

elif choice == '9':
    show_available()

elif choice == '10':
    graph_room_types()

elif choice == '11':
    graph_top_rooms()

elif choice == '12':
    graph_room_count()

elif choice == '13':
    generate_bill()

elif choice == '0':
    print("\nThank you for using the Hotel Management System!")

else:
    print("\nInvalid choice.")

