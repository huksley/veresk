"""General health information endpoint"""

def status():
    """Health status information"""

    result = {
        "status": "OK"
    }

    return (result, 200)
