from enum import Enum


class UserRole(str, Enum):
    GUEST = "Guest"
    HOST = "Host"
    ADMIN = "Admin"


class NidStatus(str, Enum):
    VERIFIED = "Verified"
    UNVERIFIED = "Unverified"


class ListingCategory(str, Enum):
    SHORT_STAY = "Short-Stay"
    BACHELOR = "Bachelor"
    FAMILY = "Family"
    TOURISM = "Tourism"


class BookingStatus(str, Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    COMPLETED = "Completed"


class SleepCycle(str, Enum):
    """Roommate matching: typical active/sleep window."""

    EARLY_BIRD = "early_bird"
    NORMAL = "normal"
    NIGHT_OWL = "night_owl"
