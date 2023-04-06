import datetime


class Truck:
    """Class for defining a Truck object.

    This class is used to define a truck object that will be used to deliver packages.

    Attributes:
        id: An integer value for the truck id.
        name: A string containing the truck name, "Truck A".
        depart_time: A datetime time object that represents when the truck will leave the hub.
        location: An integer value that represents an address index, used to reference in the address and distances data.
        priority_packages: A list of package ids that will be delivered first.
        standard_packages: A list of package ids that will be delivered after the priority packages are delivered.
    """

    def __init__(self, id: int, name: str, depart_time: datetime.time) -> None:
        """Initializes a Truck instance.

        The time and space complexity of initializing the truck object are both O(1).

        Args:
            id: An integer value for the truck id.
            name: A string containing the truck name, "Truck A".
            depart_time: A datetime time object that represents when the truck will leave the hub.

        Returns:
            None
        """

        # define the instance attribute values
        self.id = id
        self.name = name
        self.depart_time = depart_time
        self.return_time = datetime.time(0, 0, 0)
        self.location = 0
        self.priority_packages = []
        self.standard_packages = []

    def __str__(self) -> str:
        """Create a printable string for the Truck object.

        The time and space complexity of printing the truck object attributes are both O(1).

        Args:
            None

        Returns:
            An f-string that contains all the class attributes.
        """

        # create and return the string containing the instance attributes
        return f"{self.id}, {self.name}, {self.depart_time}, {self.return_time}, {self.location}, {self.priority_packages}, {self.standard_packages}"