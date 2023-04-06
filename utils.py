from package import Package
from truck import Truck
from hash_table import HashTable
import csv
import datetime
from typing import List, Tuple, Optional, Union


class Style:
    # style class used for font coloring
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    RESET = '\033[0m'


def load_addresses(file: str) -> List[str]:
    """Load address data from a csv file into a list.

    The time complexity is O(n) where n is the number of rows in the file to iterate through.
    The space complexity is O(n) as we only append a single value for each iteration of the for loop.

    Args:
        file: The path and file name of the csv file containing the list of addresses.

    Returns:
        address_list: The list of addresses.
    """

    # define the empty list for addresses
    address_list = []

    # open the csv file, and then iterate through each row of the file
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        # for each row in the file, add the third field to the address list
        for row in csv_reader:
            address_list.append(row[2])

    # return the populated list of addresses
    return address_list


def load_distances(file: str) -> List[List[str]]:
    """Load distance data from a csv file into a list.

    The time complexity is O(n) where n is the number of rows in the file to iterate through.
    The space complexity is O(n) as we only append a single row for each iteration of the for loop.

    Args:
        file: The path and file name of the csv file containing the list of distances.

    Returns:
        distance_list: The list of distances.
    """
    # define the empty list  for distances
    distance_list = []

    # open the csv file, and then iterate through each row of the file
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        # for each row in the file, add the row of distances to the distance list
        for row in csv_reader:
            distance_list.append(row)

    # return the populated distance list
    return distance_list


def load_packages(file: str) -> HashTable:
    """Load package data from a csv file into a list.

    The time complexity is O(n) where n is the number of rows in the file to iterate through.
    The space complexity is O(n+k) where n is the number of rows, and k is number of Package
        objects created.

    Args:
        file: The path and file name of the csv file containing the list of addresses.

    Returns:
        ht: The HashTable of packages.
    """

    # create an empty instance of a hash table
    ht = HashTable()

    # open the csv file, and then iterate through each row of the file
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        # for each row in the file, create individual variables for each of the package attributes
        for row in csv_reader:
            # print(row)
            id, address, city, state, zip, deadline, weight, undef = row

            # using the package attributes, create a new Package object
            pack = Package(id, address, city, state, zip, deadline, weight)

            # add the created Package object to the hash table using the package id as the index
            ht.add(key=id, value=pack)

    # return the populated hash table
    return ht


def load_truck(truck: Truck, load_list: List[List[int]]) -> None:
    """Load packages to a particular truck.

    The time and space complexity of loading the truck are in O(nm) where n is the number of lists in
        the input load_list, and m represents the number of packages within the list.

    Args:
        truck: The truck the load the packages to.
        load_list: A list of lists that contain packages.

    Returns:
        None
    """

    # set the initial priority flag to true
    priority = True

    # iterate through each of the two lists in the load list
    for load in load_list:

        # for each package in the load, add to the priority list if the priority flag is true
        # this ensures that the priority list is loaded first, then the standard list
        for package_id in load:
            if priority is True:
                truck.priority_packages.append(package_id)
            else:
                truck.standard_packages.append(package_id)

        # with all priority packages loaded, set the priority flag to false before the next iteration
        priority = False


def get_distance(distance_list: List[List[str]], start_address: int, end_address: int) -> float:
    """Find the distance between two points.

    The two-dimensional distance list is half filled, so this method will search in both directions to
        find the distance value between two points.

    The time and space complexity of determining the distance are in O(1) as we have a single comparison
        and a single value returned.

    Args:
        distance_list: Two-dimensional list of distances.
        start_address: The starting location.
        end_address: The ending location.

    Returns:
        distance: Float that represents distance between start and end address.
    """

    # set the initial distance value to 0.0
    num = 0.0

    # determine which table lookup is not empty, then set the num value to that distance
    if distance_list[start_address][end_address] != '':
        distance = float(distance_list[start_address][end_address])
    else:
        distance = float(distance_list[end_address][start_address])

    # return the distance value
    return distance


def first_last_times(package_data: HashTable, truck_name: str)\
        -> Tuple[datetime.time, datetime.time, Optional[Package], Optional[Package]]:
    """Parse package data and determine the first and last package and time.

    This method determines which package was delivered first and which was delivered last for
        a given truck. These values are used when viewing the truck deliver statistics.

    The time complexity is O(n) where n is the number of packages in the list.
    The space complexity is O(1) as we are defining a constant set of variables for each package that
        are reused.

    Args:
        package_data: The HashTable containing package data.
        truck_name: The string containing the name of the delivery truck.

    Returns:
        first_time: The datetime.time object for the first delivered package.
        last_time: The datetime.time object for the last delivered package.
        first_package: The package object for the first package delivered.
        last_package: The package object for the last package delivered.
    """

    # define initial values for the first/last times and package objects
    first_time = datetime.time(23, 59, 59)
    last_time = datetime.time(0, 0, 0)
    first_package = None
    last_package = None

    # iterate through the package list
    for i in range(1, 41):
        # find the package object using package id
        package = package_data.find(str(i))
        package_truck = package.delivered_by.name

        # if the package was loaded to the truck, determine if the delivery time was prior to the current
        # first time, and if so, then set the first package time to the current package
        # also perform the same test against the current last time
        if truck_name == package_truck:
            if package.delivery_time < first_time:
                first_time = package.delivery_time
                first_package = package
            if package.delivery_time > last_time:
                last_time = package.delivery_time
                last_package = package

    # return the first/last time values, and the first/last package objects
    return first_time, last_time, first_package, last_package


def display_all_package_data(package_data: HashTable, display_time: Union[datetime.time, None]) -> None:
    """Generate a report for pacakge information in the UI.

    This method creates a viewable report of delivered package data. If a time is provided then the report will
        be customized to that time frame by looking at each package and determining what the package status was
        at that point in time. If no time is provided, then final delivery data is displayed.

    The time complexity of the report generation is O(n), where n is the number of packages in the
        package hash table.
    The space complexity of the report generation is O(1) as there are fixed number of values created for
        each package that is evaluated and are reused.

    Args:
        package_data: The HashTable containing package data.
        display_time: The time to use when creating an on demand report.

    Returns:
        None
    """

    # print a custom header depending on if a time was provided or not
    print()
    if display_time is None:
        print(" Displaying the status of all packages:")
    else:
        print(f" Displaying the status of all packages at: {display_time.strftime('%I:%M:%S %p')}")
    header = "+----+-----------+----------+-------------+-----------+--------+---------------------------------------------------------------------+"
    print(header)
    print(
        f"| Id | Status    | Deadline | Delivered   | Delivered | Weight | Delivery Address                                                    |\n"
        f"|    |           |          | Time        | By        |        |                                                                     |"
    )
    print(header)

    # iterate through the pacakge data hash table
    for i in range(1, 41):
        # retrieve the package object from the hash table
        package = package_data.find(str(i))
        address_str = package.address + ", " + package.city + ", " + package.state + ", " + package.zip

        # define package data variables from package object attributes
        delivery_status = package.delivery_status
        delivery_time = package.delivery_time
        delivery_truck = package.delivered_by
        truck_name = delivery_truck.name
        truck_start_time = delivery_truck.depart_time

        # create the custom display
        if display_time is not None:
            # if the display time is less than the delivered time and less than the truck depart time, then
            # the package is still in the hub
            if display_time < package.delivery_time and display_time < truck_start_time:
                delivery_status = "Hub"
                delivery_time = datetime.time(0, 0, 0)

                print(
                    f"| "
                    f"{package.id :>2} | "
                    f"{delivery_status :<9} | "
                    f"{package.deadline :<8} | "
                    f"{delivery_time.strftime('%I:%M:%S %p') :<11} | "
                    f"{truck_name :<9} | "
                    f"{package.weight :>6} | "
                    f"{address_str :<67} | "
                )
            # if the display time is less than the delivered time and greater than the truck depart time, then
            # the package is en route but not yet delivered
            elif package.delivery_time > display_time > truck_start_time:
                delivery_status = "En Route"
                delivery_time = datetime.time(0, 0, 0)

                print(
                    f"| "
                    f"{package.id :>2} | "
                    f"{Style.YELLOW}{delivery_status :<9}{Style.RESET} | "
                    f"{Style.YELLOW}{package.deadline :<8}{Style.RESET} | "
                    f"{Style.YELLOW}{delivery_time.strftime('%I:%M:%S %p') :<11}{Style.RESET} | "
                    f"{Style.YELLOW}{truck_name :<9}{Style.RESET} | "
                    f"{package.weight :>6} | "
                    f"{address_str :<67} | "
                )
            # if the display time is greater than the delivery time, then the package has been delivered
            elif display_time >= package.delivery_time:
                print(
                    f"| "
                    f"{package.id :>2} | "
                    f"{Style.GREEN}{delivery_status :<9}{Style.RESET} | "
                    f"{Style.GREEN}{package.deadline :<8}{Style.RESET} | "
                    f"{Style.GREEN}{delivery_time.strftime('%I:%M:%S %p') :<11}{Style.RESET} | "
                    f"{Style.GREEN}{truck_name :<9}{Style.RESET} | "
                    f"{package.weight :>6} | "
                    f"{address_str :<67} | "
                )
        else:
            # in this case no display time has been provided, so display all data as it currently is
            print(
                f"| "
                f"{package.id :>2} | "
                f"{delivery_status :<9} | "
                f"{package.deadline :<8} | "
                f"{delivery_time.strftime('%I:%M:%S %p') :<11} | "
                f"{truck_name :<9} | "
                f"{package.weight :>6} | "
                f"{address_str :<67} | "
            )

    print(header)


def nearest_neighbor(package_list: List[int],package_data: HashTable, address_data: List[str],
                     distance_data: List[List[str]], start_index: int) -> Tuple[int, int, float]:
    """Determine the nearest location to the current location.

    This method uses the nearest neighbor algorithm to find the closest delivery location when provided a list
        of packages and a starting address location.

    The time complexity of this method is O(n), where n is the number of packages in the package list.
    The space complexity is O(1) as we are creating a constant number of variables per package that are reused
        for each iteration.

    Args:
        package_list: The list of packages to iterate through.
        package_data: The HashTable containing all package data.
        address_data: The list containing all address data.
        distance_data: The list containing all distance data.
        start_index: The starting address index.

    Returns:
        nearest_package_id: The integer value of the package with the closest distance.
        nearest_target_index: The integer value that represents the address index of the closest address location.
        min_distance: The distance from the current location to the closest delivery location.
    """

    # set the initial values, with the min distance being set to an infinite value
    min_distance = float('inf')
    nearest_package_id = 0
    nearest_target_index = 0

    # iterate through the list of packages provided
    for package_id in package_list:
        # retrieve the package object from the hash table
        package = package_data.find(str(package_id))

        # check to see if this is package #9 which had an incorrect address, if so, update the address
        if package_id == 9:
            package.address = "410 S State St"
            package.zip = "84111"

        # set the target address and index values, and then retrieve the distance
        target_address = package.address
        target_index = address_data.index(target_address)
        distance = get_distance(distance_list=distance_data, start_address=start_index, end_address=target_index)

        # determine if the distance is less than the current min distance
        # if the distance is lower, than update the current min distance with this package info
        if distance < min_distance and nearest_package_id != package_id:
            min_distance = distance
            nearest_package_id = package_id
            nearest_target_index = target_index

    # return the id of the nearest package, the index of the nearest address, and the distance of the closest packge
    return nearest_package_id, nearest_target_index, min_distance


def deliver_packages(truck: Truck, package_data: HashTable, address_data: List[str], distance_data: List[List[str]]) -> int:
    """Deliver packages to a destination with a provided package list and delivery truck.

    This method will process all packages loaded to a truck, determine an optimal delivery order, and then
        deliver all packages.

    The time complexity of the package delivery function is O(n^2) as we iterate through all packages lists, while
        also executing the nearest neighbor algorithm to determine each package to deliver next.
    The space complexity of the pacakge delivery function is O(1), as we create a constant number of variables that
        are reused for each iteration.

    Args:
        truck: The Truck object that will deliver the packages.
        package_data: The HashTable containing all package data.
        address_data: The list containing all address data.
        distance_data: The list containing all distance data.

    Returns:
        distance_traveled: The integer value of the total cumulative distance traveled.
    """

    # define some initial starting variables
    truck_name = truck.name
    start_index = 0
    distance_traveled = 0
    start_ts = truck.depart_time
    current_location = 0
    last_delivery_time = datetime.time(0, 0, 0)

    # create a list of two lists, with the priority packages first, then standard packages
    load_list = [truck.priority_packages, truck.standard_packages]

    # iterate through each one of the packages lists
    for package_list in load_list:
        # iterate through the packages in the list until they are all delivered
        while len(package_list) > 0:
            # use the nearest neighbor algorithm to determine the closest target from the list of packages
            next_package, next_address_index, delivery_distance = nearest_neighbor(package_list, package_data,
                                                                                   address_data, distance_data,
                                                                                   start_index)

            # calculate the drive time and delivery time
            elapsed_time = int(delivery_distance / 18 * 60)
            delta_minutes = datetime.timedelta(minutes=elapsed_time)
            delta_seconds = datetime.timedelta(seconds=elapsed_time)
            delivery_time = (datetime.datetime.combine(datetime.date.today(), start_ts) + delta_minutes + delta_seconds).time()

            # do some updates to the package data
            delivered_package = package_data.find(str(next_package))
            delivered_package.delivery_status = "Delivered"
            delivered_package.delivery_time = delivery_time
            delivered_package.delivered_by = truck

            # update values for the next iteration
            start_ts = delivery_time
            distance_traveled += delivery_distance
            start_index = next_address_index
            current_location = next_address_index
            last_delivery_time = delivery_time

            # remove the delivered package from the list
            package_list.remove(next_package)

    # return the truck back to the hub after all packages are delivered
    hub_distance = get_distance(distance_list=distance_data, start_address=current_location, end_address=0)
    distance_traveled += hub_distance
    hub_elapsed_time = int(hub_distance / 18 * 60)
    hub_delta = datetime.timedelta(minutes=hub_elapsed_time)
    truck.return_time = (datetime.datetime.combine(datetime.date.today(), last_delivery_time) + hub_delta).time()

    # finally, return the total distance traveled for all delivery trucks
    return distance_traveled





