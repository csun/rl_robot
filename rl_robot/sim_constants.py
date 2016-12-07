LINKS = map(lambda n: 'redundantRob_link' + str(n), range(8))

JOINTS = map(lambda n: 'redundantRob_joint' + str(n), range(1,8))

ACTOR_LIMITS = [(-1.0, 1.0)] * len(JOINTS)

PROXIMITY_SENSORS = map(lambda n: 'Proximity_sensor' + str(n), [''] + range(6))

COLLISION_OBJECTS = map(lambda n: 'Collision' + str(n), range(5))

TIP_OBJECT = 'redundantRob_tip'

GOAL_OBJECT = 'goalIndicator'

# Note, this is tightly coupled with the currently used scene file. It's not ideal
# to do this like this, but it'll work for now.
POTENTIAL_GOAL_AREAS = [
    [[-0.225, -1.525, 0.7], [0.6, -0.5, -0.1]],
    [[-0.3, -1.25, 0.1], [0.275, -0.825, 0.425]],
    [[0.325, -1.25, 0.1], [0.25, -0.825, 0.425]]
]
