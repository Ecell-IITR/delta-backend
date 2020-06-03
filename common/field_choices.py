class POST_FIELD_CHOICES:
    ONLINE = 1
    ONSPOT = 2

    COMPETITION_TYPE = (
        (ONLINE, 'Online'),
        (ONSPOT, 'Onspot'),
    )

    FULL_TIME = 1
    PART_TIME = 2

    WORK_TYPE = [
        (FULL_TIME, 'Full time'),
        (PART_TIME, 'Part time'),
    ]

    DAY = 1
    WEEK = 2
    MONTH = 3
    YEAR = 4

    DURATION_UNIT = (
        (DAY, 'Day'),
        (WEEK, 'Week'),
        (MONTH, 'Month'),
        (YEAR, 'Year')
    )


class USER_FIELD_CHOICES:
    FOLLOW = 1
    UNFOLLOW = 2
    
    ACTIONS = (
        (FOLLOW, 'Follow'),
        (UNFOLLOW, 'UnFollow')
    )


def get_opposite_action(action):
    if int(action) == USER_FIELD_CHOICES.FOLLOW:
        return USER_FIELD_CHOICES.UNFOLLOW
    elif int(action) == USER_FIELD_CHOICES.UNFOLLOW:
        return USER_FIELD_CHOICES.FOLLOW
    return 0