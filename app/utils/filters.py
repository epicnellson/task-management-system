def status_color(status):
    """Convert task status to Bootstrap color class."""
    colors = {
        'pending': 'warning',
        'in_progress': 'info',
        'completed': 'success',
        'cancelled': 'danger'
    }
    return colors.get(status.lower(), 'secondary')

def priority_color(priority):
    """Convert task priority to Bootstrap color class."""
    colors = {
        'low': 'success',
        'medium': 'warning',
        'high': 'danger'
    }
    return colors.get(priority.lower(), 'secondary') 