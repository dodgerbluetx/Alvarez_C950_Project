from fcntl import F_DUPFD
from package import Package
from truck import Truck
from hash_table import HashTable
import csv
import datetime
from typing import List


class Style:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    RESET = '\033[0m'


def load_addresses(file: str) -> List[str]:
    """
        comments here
    """
    address_list = []
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            address_list.append(row[2])
    return address_list


def load_distances(file: str) -> List[str]:
    """
        comments here
    """
    distance_list = []
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            distance_list.append(row)
    return distance_list


def load_packages(file: str) -> HashTable:
    """
        comments here
    """
    ht = HashTable()
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            # print(row)
            id, address, city, state, zip, deadline, weight, undef = row
            pack = Package(id, address, city, state, zip, deadline, weight)
            ht.add(key = id, value = pack)
    return ht


def load_truck(truck: Truck, load_list: List[List[int]]) -> None:
    priority = True
    for load in load_list:
        for package_id in load:
            if priority is True:
                truck.priority_packages.append(package_id)
            else:
                truck.standard_packages.append(package_id)
        priority = False


def get_distance(distance_list: List[str], start_address: int, end_address: int) -> float:
    num = 0.0
    if distance_list[start_address][end_address] != '':
        num = float(distance_list[start_address][end_address])
    else:
        num = float(distance_list[end_address][start_address])
    return num


def first_last_times(package_data, truck_name):
    first_time = datetime.time(23, 59, 59)
    last_time = datetime.time(0, 0, 0)
    first_package = None
    last_package = None

    for i in range(1, 41):
        package = package_data.find(str(i))
        package_truck = package.delivered_by.name

        if truck_name == package_truck:
            if package.delivery_time < first_time:
                first_time = package.delivery_time
                first_package = package
            if package.delivery_time > last_time:
                last_time = package.delivery_time
                last_package = package

    return first_time, last_time, first_package, last_package


def display_all_package_data(package_data, display_time):
    header = "+----+-----------+----------+-------------+-----------+--------+---------------------------------------------------------------------+"
    print(header)
    print(
        f"| Id | Status    | Deadline | Delivered   | Delivered | Weight | Delivery Address                                                    |\n"
        f"|    |           |          | Time        | By        |        |                                                                     |"
    )
    print(header)

    for i in range(1, 41):
        # print(i)
        package = package_data.find(str(i))
        address_str = package.address + ", " + package.city + ", " + package.state + ", " + package.zip

        delivery_status = package.delivery_status
        delivery_time = package.delivery_time
        delivery_truck = package.delivered_by
        truck_name = delivery_truck.name
        truck_start_time = delivery_truck.depart_time

        if display_time is not None:
            if display_time < package.delivery_time and display_time < truck_start_time:
                delivery_status = "Hub"
                delivery_time = datetime.time(0, 0, 0)

                print(
                    f"| "
                    f"{package.id :>2} | "
                    f"{delivery_status :<9} | "
                    f"{package.deadline :<8} | "
                    f"{delivery_time.strftime('%H:%M:%S %p') :<11} | "
                    f"{truck_name :<9} | "
                    f"{package.weight :>6} | "
                    f"{address_str :<67} | "
                )
            elif display_time < package.delivery_time and display_time > truck_start_time:
                delivery_status = "En Route"
                delivery_time = datetime.time(0, 0, 0)

                print(
                    f"| "
                    f"{package.id :>2} | "
                    f"{Style.YELLOW}{delivery_status :<9}{Style.RESET} | "
                    f"{Style.YELLOW}{package.deadline :<8}{Style.RESET} | "
                    f"{Style.YELLOW}{delivery_time.strftime('%H:%M:%S %p') :<11}{Style.RESET} | "
                    f"{Style.YELLOW}{truck_name :<9}{Style.RESET} | "
                    f"{package.weight :>6} | "
                    f"{address_str :<67} | "
                )

            elif display_time >= package.delivery_time:
                print(
                    f"| "
                    f"{package.id :>2} | "
                    f"{Style.GREEN}{delivery_status :<9}{Style.RESET} | "
                    f"{Style.GREEN}{package.deadline :<8}{Style.RESET} | "
                    f"{Style.GREEN}{delivery_time.strftime('%H:%M:%S %p') :<11}{Style.RESET} | "
                    f"{Style.GREEN}{truck_name :<9}{Style.RESET} | "
                    f"{package.weight :>6} | "
                    f"{address_str :<67} | "
                )
        else:
            print(
                f"| "
                f"{package.id :>2} | "
                f"{delivery_status :<9} | "
                f"{package.deadline :<8} | "
                f"{delivery_time.strftime('%H:%M:%S %p') :<11} | "
                f"{truck_name :<9} | "
                f"{package.weight :>6} | "
                f"{address_str :<67} | "
            )

    print(header)


def nearest_neighbor(package_list, package_data, address_data, distance_data, start_index, start_ts):
    min_distance = float('inf')
    nearest_package_id = 0
    nearest_target_index = 0

    for package_id in package_list:
        package = package_data.find(str(package_id))

        # check to see if this is package 9 which had an incorrect address, if so, fix it
        if package_id == 9:
            # 410 S State St., Salt Lake City, UT 84111
            package.address = "410 S State St"
            # package.address = "4300 S 1300 E"
            package.zip = "84111"

        target_address = package.address
        target_index = address_data.index(target_address)
        start_address = address_data[start_index]
        distance = get_distance(distance_list = distance_data, start_address = start_index, end_address = target_index)

        # print(f"Package: {package_id}, Start Time: {start_ts}")
        # print(f"Starting Index: {start_index}, Starting Address: {start_address}")
        # print(f"Target Index: {target_index}, Target Address: {target_address}")
        # print(f"Target Distance: {distance}")
        # print()
        
        if distance < min_distance and nearest_package_id != package_id:
            min_distance = distance
            nearest_package_id = package_id
            nearest_target_index = target_index

    # print()
    # print()
    # print()

    return nearest_package_id, nearest_target_index, min_distance


def deliver_packages(truck, package_data, address_data, distance_data) -> int:
    truck_name = truck.name
    start_index = 0
    distance_traveled = 0
    start_ts = truck.depart_time

    load_list = [truck.priority_packages, truck.standard_packages]
    for package_list in load_list:
        while len(package_list) > 0:
            # print(package_list)
            # find the closest target from the current_list of packages
            next_package, next_address_index, delivery_distance = nearest_neighbor(package_list, package_data,
                                                                                address_data, distance_data, start_index,
                                                                                start_ts)

            # print(f"{Style.GREEN}Delivering Package! {next_package}, {delivery_distance}, {next_address_index}{Style.RESET}")
            # print()
            # print()

            # calculate the drive time and delivery time
            elapsed_time = int(delivery_distance / 18 * 60)
            delta = datetime.timedelta(minutes = elapsed_time)
            delivery_time = (datetime.datetime.combine(datetime.date.today(), start_ts) + delta).time()
            
            start_index = next_address_index
            package_list.remove(next_package)
            start_ts = delivery_time
            distance_traveled += delivery_distance

            # do some updates to the package data
            delivered_package = package_data.find(str(next_package))
            delivered_package.delivery_status = "Delivered"
            delivered_package.delivery_time = delivery_time
            delivered_package.delivered_by = truck

        # print(package_data.print_table())

    return distance_traveled




