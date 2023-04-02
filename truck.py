import datetime

class Truck:
    def __init__(self, id: int, name: str, depart_time: datetime.time) -> None:
        self.id = id
        self.name = name
        self.depart_time = depart_time
        self.location = 0
        self.priority_packages = []
        self.standard_packages = []

    def __str__(self) -> str:
        return(f"{self.id}, {self.name}, {self.depart_time}, {self.location}, {self.priority_packages}, {self.standard_packages}")