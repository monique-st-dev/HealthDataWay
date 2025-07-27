# --- Connection Notifications ---
CONNECTION_REQUEST = 'connection_request'
CONNECTION_APPROVED = 'connection_approved'
CONNECTION_DENIED = 'connection_denied'
CONNECTION_TERMINATED = 'connection_terminated'

# --- General Notifications ---
REMINDER = 'reminder'

# --- Appointment Notifications ---
APPOINTMENT_REQUEST = 'appointment_request'
APPOINTMENT_APPROVED = 'appointment_approved'
APPOINTMENT_REJECTED = 'appointment_rejected'
APPOINTMENT_CANCELLED = 'appointment_cancelled'
APPOINTMENT_REMINDER = 'appointment_reminder'


# --- All Notification Types ---
NOTIFICATION_TYPES = [
    # --- Connections ---
    (CONNECTION_REQUEST, 'Connection Request'),
    (CONNECTION_APPROVED, 'Connection Approved'),
    (CONNECTION_DENIED, 'Connection Denied'),
    (CONNECTION_TERMINATED, 'Connection Terminated'),

    # --- General ---
    (REMINDER, 'Reminder'),

    # --- Appointments ---
    (APPOINTMENT_REQUEST, 'Appointment Request'),
    (APPOINTMENT_APPROVED, 'Appointment Approved'),
    (APPOINTMENT_REJECTED, 'Appointment Rejected'),
    (APPOINTMENT_CANCELLED, 'Appointment Cancelled'),
    (APPOINTMENT_REMINDER, 'Appointment Reminder'),
]
