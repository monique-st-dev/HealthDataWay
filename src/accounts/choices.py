class UserRoles:
    PATIENT = 'patient'
    DOCTOR = 'doctor'
    STAFF = 'staff'
    ADMIN = 'admin'

    CHOICES = [
        (PATIENT, 'Patient'),
        (DOCTOR, 'Doctor'),
        (STAFF, 'Staff'),
        (ADMIN, 'Admin'),
    ]


class GenderChoices:
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

    CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    ]