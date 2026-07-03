def valid_asset_status(status):

    return status in [
        "Available",
        "Assigned",
        "Lost",
        "Maintenance"
    ]


def valid_allocation_status(status):

    return status in [
        "Assigned",
        "Returned",
        "Lost"
    ]
