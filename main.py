# Mark Alvarez, Student ID: 001369334

from truck import Truck
from utils import Style, load_packages, load_distances, load_addresses, load_truck
from utils import deliver_packages, display_all_package_data, first_last_times
import datetime
import os
import sys

__author__ = "Mark Alvarez"
__copyright__ = "Copyright 2023"
__credits__ = "Mark Alvarez, Student ID: 001369334"
__version__ = "1.0.0"
__status__ = "Production"


def main():
    """The main program function.

    The overall time complexity of the program is in O(n^2) time. This is due to nested loops that need to iterate
        through each truck, each truck's package list, and then finally repeated at each stop along the route. The
        time complexity increases exponentially as the input list (amount of packages) grows.

    The overall space complexity of the program is O(n), as the memory required scales based on the input (the package
        list, the address list, and the distance list). As these lists grown, the required storage spaces grows in a
        linear fashion.

    Space and Time complexity for methods used below are detailed in the docstrings comments for each specific method.

    Args:
        None

    Returns:
        None
    """

    # define the csv data file locations
    address_file = "data/addresses.csv"
    distance_file = "data/distances.csv"
    package_file = "data/packages.csv"

    # load the package, distance, and address csv data
    package_data = load_packages(file=package_file)
    distance_data = load_distances(file=distance_file)
    address_data = load_addresses(file=address_file)

    # create all three truck instances - a, b, c
    truck_a = Truck(id=1, name="Truck A", depart_time=datetime.time(9, 5, 0))
    truck_b = Truck(id=2, name="Truck B", depart_time=datetime.time(8, 0, 0))
    truck_c = Truck(id=3, name="Truck C", depart_time=datetime.time(12, 30, 0))

    # create package loads for each of the three trucks
    load_a = [[6, 25, 30, 31, 40, 13], [28, 32, 8, 12, 17, 22, 26, 4, 39]]
    load_b = [[15, 20, 16, 14, 1, 29, 21, 34, 37], [3, 18, 36, 38, 5, 7, 19]]
    load_c = [[9, 23, 24, 27, 35, 10, 11, 2, 33]]

    # calculate and summarize the length of each load list
    load_a_count = len(load_a[0]) + len(load_a[1])
    load_b_count = len(load_b[0]) + len(load_b[1])
    load_c_count = len(load_c[0])

    # load the trucks with the packages in the load lists
    load_truck(truck=truck_a, load_list=load_a)
    load_truck(truck=truck_b, load_list=load_b)
    load_truck(truck=truck_c, load_list=load_c)

    # run each truck's delivery routine
    truck_a_distance = deliver_packages(truck=truck_a, package_data=package_data, address_data=address_data,
                                        distance_data=distance_data)
    truck_b_distance = deliver_packages(truck=truck_b, package_data=package_data, address_data=address_data,
                                        distance_data=distance_data)
    truck_c_distance = deliver_packages(truck=truck_c, package_data=package_data, address_data=address_data,
                                        distance_data=distance_data)

    # add all three truck route milage into total distance
    total_distance = truck_a_distance + truck_b_distance + truck_c_distance

    # calculate delivery time statistics for each truck
    a_first_time, a_last_time, a_first_package, a_last_package = first_last_times(package_data=package_data,
                                                                                  truck_name="Truck A")
    b_first_time, b_last_time, b_first_package, b_last_package = first_last_times(package_data=package_data,
                                                                                  truck_name="Truck B")
    c_first_time, c_last_time, c_first_package, c_last_package = first_last_times(package_data=package_data,
                                                                                  truck_name="Truck C")

    # set the default selection value to 0
    selection = 0

    # display the user interface welcome screen
    while True:
        print()
        print("+-------------------------------------------------+")
        print("|  Welcome to the WGUPS Package Delivery System!  |")
        print("+-------------------------------------------------+")
        print(f"|  Total miles traveled: {Style.GREEN}{total_distance:.2f}{Style.RESET} miles             |")
        print("+-------------------------------------------------+")
        print("|  Select one of the following options:           |")
        print("|                                                 |")  
        print("|  1) Re-deliver all packages                     |")
        print("|  2) Show all delivered package data             |")
        print("|  3) Show package status at specific time        |")
        print("|  4) Show the truck delivery statistics          |")
        print("|  5) Exit the program                            |")
        print("+-------------------------------------------------+")
        selection = input(" Enter a selection: ")

        # when option 1 is selected, restart the program
        if selection == "1":
            os.execv(sys.executable, [sys.executable] + sys.argv)

        # when option 2 is selected, display all package delivery data
        elif selection == "2":
            os.system("clear")
            display_all_package_data(package_data=package_data, display_time=None)
            print()
            input(" Press Enter to return to main menu...")

        # when option 3 is selected, ask the user to input a time, and then display the delivery data for that time
        elif selection == "3":
            time_input = input(" Enter a (24-hour format) time (HH:MM:SS): ")
            display_time = datetime.datetime.strptime(time_input, "%H:%M:%S").time()
            display_all_package_data(package_data=package_data, display_time=display_time)
            input(" Press Enter to return to main menu...")

        # when option 4 is selected, display the individual truck delivery statistics
        elif selection == "4":
            print("+-------------------------------------------------+")
            print("|  WGUPS Truck Delivery Statistics                |")
            print("+-------------------------------------------------+")
            print(f"|  Truck A                                        |")
            print(f"|  ===============                                |")
            print(f"|  Hub Departure Time: {truck_a.depart_time.strftime('%I:%M:%S %p')}                |")
            print(f"|  Distance Traveled: {truck_a_distance:.2f} miles                 |")
            print(f"|  Packages Delivered: {load_a_count}                         |")
            print(f"|  First Package Delivered At: {a_first_time.strftime('%I:%M:%S %p')} ({a_first_package.id :>2})   |")
            print(f"|  Last Package Delivered At: {a_last_time.strftime('%I:%M:%S %p')} ({a_last_package.id :>2})    |")
            print(f"|  Hub Return Time: {truck_a.return_time.strftime('%I:%M:%S %p')}                   |")

            print("|                                                 |")
            print(f"|  Truck B                                        |")
            print(f"|  ===============                                |")
            print(f"|  Hub Departure Time: {truck_b.depart_time.strftime('%I:%M:%S %p')}                |")
            print(f"|  Distance Traveled: {truck_b_distance:.2f} miles                 |")
            print(f"|  Packages Delivered: {load_b_count}                         |")
            print(f"|  First Package Delivered At: {b_first_time.strftime('%I:%M:%S %p')} ({b_first_package.id :>2})   |")
            print(f"|  Last Package Delivered At: {b_last_time.strftime('%I:%M:%S %p')} ({b_last_package.id :>2})    |")
            print(f"|  Hub Return Time: {truck_b.return_time.strftime('%I:%M:%S %p')}                   |")
            print("|                                                 |")
            print(f"|  Truck C                                        |")
            print(f"|  ===============                                |")
            print(f"|  Hub Departure Time: {truck_c.depart_time.strftime('%I:%M:%S %p')}                |")
            print(f"|  Distance Traveled: {truck_c_distance:.2f} miles                 |")
            print(f"|  Packages Delivered: {load_c_count}                          |")
            print(f"|  First Package Delivered At: {c_first_time.strftime('%I:%M:%S %p')} ({c_first_package.id :>2})   |")
            print(f"|  Last Package Delivered At: {c_last_time.strftime('%I:%M:%S %p')} ({c_last_package.id :>2})    |")
            print(f"|  Hub Return Time: {truck_c.return_time.strftime('%I:%M:%S %p')}                   |")
            print("+-------------------------------------------------+")
            input(" Press Enter to return to main menu...")

        # when option 5 is selected, exit the program
        elif selection == "5":
            print()
            print(" Thank you for using the WGUPS Package Delivery system!")
            print(" Goodbye!")
            print()
            sys.exit(0)

        # when none of the previous 5 options are entered, instruct the user to try again
        else:
            print(" Invalid selection, please try again!")
            input(" Press Enter to continue...")


if __name__ == "__main__":
    main()
