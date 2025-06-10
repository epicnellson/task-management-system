def status_color(status):
    """Return Bootstrap color class based on task status."""
    colors = {
        'pending': 'secondary',
        'in_progress': 'warning',
        'completed': 'success'
    }
    return colors.get(status, 'primary') 