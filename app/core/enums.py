from enum import Enum

class OrderStatus(str, Enum):
    PLACED = "PLACED"
    ACCEPTED = "ACCEPTED"
    DISPATCHED = "DISPATCHED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"



class PharmacyStatus(str,Enum):
    PENDING = "PENDING"
    APPPROVED = "APPROVED"
    REJECTED = "REJECTED"
