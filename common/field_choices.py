class POST_FIELD_CHOICES:
    COMPETITION_TYPE = (
        (
            'Online', 'Online'
        ),
        (
            'Onspot', 'Onspot'
        )
    )

    WORK_TYPE = {
        (
            'Full time', 'Full time'
        ),
        (
            'Part time', 'Part time'
        )
    }


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