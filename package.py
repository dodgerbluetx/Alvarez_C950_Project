import datetime


class Package:
    """Class for defining a package object.

    This class is used to define a deliverable package as an object, and to assign its
        associated attributes to it.

    Attributes:
        id: An integer value for the package id.
        address: A string containing the street address.
        city: A string that contains the city.
        state: A string that contains the state.
        zip: A string that contains the zip code.
        deadline: A string that contains deadline information for a package, like required delivery time.
        weight: An integer of the package weight in kg.
        delivery_status: The current package status or location, example "Hub", "En Route", or "Delivered".
        delivery_time: A datetime time object that represents when the package was delivered.
        delivered_by: A Truck object that represents which truck delivered this package.
    """

    def __init__(self, id: int, address: str, city: str, state: str, zip: str, deadline: str, weight: int) -> None:
        """Initializes a Package instance

        The time and space complexity of initializing the pacakge object are both O(1).

        Args:
            id: An integer value for the package id.
            address: A string containing the street address.
            city: A string that contains the city.
            state: A string that contains the state.
            zip: A string that contains the zip code.
            deadline: A string that contains deadline information for a package, like required delivery time.
            weight: An integer of the package weight in kg.

        Returns:
            None
        """

        # define the instance attribute values
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.delivery_status = "Hub"
        self.delivery_time = datetime.time(0, 0, 0)
        self.delivered_by = "N/A"

    def __str__(self) -> str:
        """Create a printable string for the Package object.

        The time and space complexity of printing the package object attributes are both O(1).

        Args:
            None

        Returns:
            An f-string that contains all the class attributes.
        """

        # create and return the string containing the instance attributes
        ts = self.delivery_time.strftime("%H:%M:%S")
        return f"{self.id}, {self.address}, {self.city}, {self.state}, {self.zip}, {self.deadline}, {self.weight}, {self.delivery_status}, {ts}, {self.delivered_by}"

