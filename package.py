import datetime

class Package:
    def __init__(self, id: int, address: str, city: str, state: str, zip: str,
                 deadline: str, weight: int) -> None:
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
        ts = self.delivery_time.strftime("%H:%M:%S")
        return(f"{self.id}, {self.address}, {self.city}, {self.state}, {self.zip}, {self.deadline}, {self.weight}, {self.delivery_status}, {ts}, {self.delivered_by}")

