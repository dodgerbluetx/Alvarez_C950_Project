from package import Package
from truck import Truck
from hash_table import HashTable
from utils import Style, load_packages, load_distances, load_addresses, load_truck
from utils import deliver_packages, display_all_package_data, first_last_times
import datetime
import time
import os
import sys


def main():

    # define the csv data files
    address_file = "data/addresses.csv"
    distance_file = "data/distances.csv"
    package_file = "data/packages.csv"

    # load the csv data
    package_data = load_packages(package_file)
    distance_data = load_distances(distance_file)
    address_data = load_addresses(address_file)
    # package_data.print_table()

    # create all three trucks at the hub
    truck_a = Truck(id=1, name="Truck A", depart_time=datetime.time(9, 5, 0))
    truck_b = Truck(id=2, name="Truck B", depart_time=datetime.time(8, 0, 0))
    truck_c = Truck(id=3, name="Truck C", depart_time=datetime.time(10, 20, 0))

    # package assignments
    load_a = [[6, 25, 30, 31, 40], [28, 32, 8, 10, 11, 12, 17, 22, 26, 4]]
    load_b = [[15, 20, 16, 14, 1, 13, 29, 21, 34, 37], [3, 18, 36, 38, 2, 5, 7, 19, 33, 39]]
    load_c = [[9, 23, 24, 27, 35]]

    load_a_count = len(load_a[0]) + len(load_a[1])
    load_b_count = len(load_b[0]) + len(load_b[1])
    load_c_count = len(load_c[0])

    # load the trucks
    load_truck(truck=truck_a, load_list=load_a)
    load_truck(truck=truck_b, load_list=load_b)
    load_truck(truck=truck_c, load_list=load_c)

    # view truck status
    # print(truck_a)
    # print(truck_b)
    # print(truck_c)

    truck_a_distance = deliver_packages(truck=truck_a, package_data=package_data,address_data=address_data,
                                       distance_data=distance_data)
    truck_b_distance = deliver_packages(truck=truck_b, package_data=package_data, address_data=address_data,
                                       distance_data=distance_data)
    truck_c_distance = deliver_packages(truck=truck_c, package_data=package_data, address_data=address_data,
                                       distance_data=distance_data)

    total_distance = truck_a_distance + truck_b_distance + truck_c_distance

    truck_a_first_time, truck_a_last_time, truck_a_first_package, truck_a_last_package = first_last_times(package_data,
                                                                                                          "Truck A")
    truck_b_first_time, truck_b_last_time, truck_b_first_package, truck_b_last_package = first_last_times(package_data,
                                                                                                          "Truck B")
    truck_c_first_time, truck_c_last_time, truck_c_first_package, truck_c_last_package = first_last_times(package_data,
                                                                                                          "Truck C")

    # test color printing
    # print(f"{Style.RED}This is RED{Style.RESET}")
    # print(f"{Style.GREEN}This is GREEN{Style.RESET}")
    # print(f"{Style.YELLOW}This is YELLOW{Style.RESET}")
    # print(f"{Style.BLUE}This is BLUE{Style.RESET}")
    # print(f"{Style.MAGENTA}This is MAGENTA{Style.RESET}")
    # print(f"{Style.CYAN}This is CYAN{Style.RESET}")

    selection = 0

    while True:
        # os.system("clear")
        print()
        print("+-------------------------------------------------+")
        print("|  Welcome to the WGUPS Package Delivery System!  |")
        print("+-------------------------------------------------+")
        print(f"|  Total miles traveled: {total_distance:.2f} miles             |")
        print("+-------------------------------------------------+")
        print("|  Select one of the following options:           |")
        print("|                                                 |")  
        print("|  1) Re-deliver all packages                     |")
        print("|  2) Show all delivered package data             |")
        print("|  3) Show package status at specific time        |")
        print("|  4) Show the truck delivery statistics          |")
        print("|  5) Exit the program                            |")
        print("+-------------------------------------------------+")
        selection = input("   Enter a selection: ")

        # re-run the program with this option
        if selection == "1":
            os.execv(sys.executable, [sys.executable] + sys.argv)
        elif selection == "2":
            os.system("clear")
            display_all_package_data(package_data, None)
            print()
            input("  Press Enter to return to main menu...")
        elif selection == "3":
            time_input = input("Enter a time (HH:MM:SS): ")
            display_time = datetime.datetime.strptime(time_input, "%H:%M:%S").time()
            display_all_package_data(package_data, display_time)
            input("  Press Enter to return to main menu...")
        elif selection == "4":
            print("+-------------------------------------------------+")
            print("|  WGUPS Truck Delivery Statistics                |")
            print("+-------------------------------------------------+")
            print(f"|  Truck A                                        |")
            print(f"|  ===============                                |")
            print(f"|  Hub Departure Time: {truck_a.depart_time.strftime('%H:%M:%S %p')}                |")
            print(f"|  Distance Traveled: {truck_a_distance:.2f} miles                 |")
            print(f"|  Packages Delivered: {load_a_count}                         |")
            print(f"|  First Package Delivered At: {truck_a_first_time.strftime('%H:%M:%S %p')} ({truck_a_first_package.id :>2})   |")
            print(f"|  Last Package Delivered At: {truck_a_last_time.strftime('%H:%M:%S %p')} ({truck_a_last_package.id :>2})    |")
            print("|                                                 |")
            print(f"|  Truck B                                        |")
            print(f"|  ===============                                |")
            print(f"|  Hub Departure Time: {truck_b.depart_time.strftime('%H:%M:%S %p')}                |")
            print(f"|  Distance Traveled: {truck_b_distance:.2f} miles                 |")
            print(f"|  Packages Delivered: {load_b_count}                         |")
            print(f"|  First Package Delivered At: {truck_b_first_time.strftime('%H:%M:%S %p')} ({truck_b_first_package.id :>2})   |")
            print(f"|  Last Package Delivered At: {truck_b_last_time.strftime('%H:%M:%S %p')} ({truck_b_last_package.id :>2})    |")
            print("|                                                 |")
            print(f"|  Truck C                                        |")
            print(f"|  ===============                                |")
            print(f"|  Hub Departure Time: {truck_c.depart_time.strftime('%H:%M:%S %p')}                |")
            print(f"|  Distance Traveled: {truck_c_distance:.2f} miles                 |")
            print(f"|  Packages Delivered: {load_c_count}                          |")
            print(f"|  First Package Delivered At: {truck_c_first_time.strftime('%H:%M:%S %p')} ({truck_c_first_package.id :>2})   |")
            print(f"|  Last Package Delivered At: {truck_c_last_time.strftime('%H:%M:%S %p')} ({truck_c_last_package.id :>2})    |")
            print("+-------------------------------------------------+")
            input("  Press Enter to return to main menu...")
        elif selection == "5":
            print()
            print("Thank you for using the WGUPS Package Delivery system!")
            print("Goodbye!")
            print()
            sys.exit(0)
        else:
            print("Invalid selection, please try again!")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()
