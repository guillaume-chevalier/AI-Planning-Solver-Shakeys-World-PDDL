
# This is some Python 2 meta-programming to generate
# some .pddl problem files automatically from our first problem.

# Parameter 1:
# Number of small objects to pick (total)
small_objects_to_pick = [2, 4, 8, 16]

# Parameter 2:
# Number of rows of room.
rows_of_rooms = [1, 2, 4, 8]
# Each row of rooms contain 3 columns of rooms so that the total number of
# rooms is nb_of_rows*3.
# Example: 2 rows would mean 6 rooms organised in a rectangle of
# 3 rooms wide and 2 rooms of height (top view).

# Room (0, 0) always contains the box and the tablet and it
# is the starting position of Shakey.

# The number of items to pick is always distributed iteratively over
# every rooms, starting from top-left, looping with a modulo if needed.
# Every room is properly interconnected with the two door types.

def save_file(out, rows, objs_count):
    rooms_count = rows*3
    filename = "shakey-task-2-"+str(rooms_count)+"rooms-"+str(objs_count)+"objs.pddl"
    with open(filename, "w") as f:
        f.write(out)

for rows in rows_of_rooms:
    for objs_count in small_objects_to_pick:
        # The written code is generated to the "out" variable.
        out = """
        ;; This is a problem definition for "Shakey's world" problem (Alternative 2).
        ;; We take for granted that the robot is autonomous for low-level tasks,
        ;; as an example, we only consider high-level actions such as moving the box
        ;; from a room to another room without caring about sub-tiles in the rooms
        ;; and other such small logistics details.

        ;; The goal of the agent (Shakey) is to tidy up the room by
        ;; placing every objects on the tablet.
        ;; Also, as initially, the lights must be all turned off and
        ;; the box replaced in room00 as initially.

        ;; Usage: ./ff -o shakey-domain.pddl -f shakey-task-2-{}rooms-{}objs.pddl
        ;; Usage: ./ipp -o shakey-domain.pddl -f shakey-task-2-{}rooms-{}objs.pddl



        (define (problem shakey-task-2-{}rooms-{}objs)
          (:domain shakey)
          (:objects
            ;; static:
            """.format(rows*3, objs_count, rows*3, objs_count, rows*3, objs_count)
        room_names = list()
        pure_room_names = list()
        for i in range(3):
            for j in range(rows):
                name_ = "room"+str(i)+str(j)
                room_names.append(
                    [
                        i, j, name_
                    ]
                )
                pure_room_names.append(name_)
        out += " ".join(pure_room_names)
        out += """
            """
        tiny_door_links = list()
        wide_door_links = list()
        tiny_door_names = list()
        wide_door_names = list()
        for i1, j1, nam1 in room_names:
            for i2, j2, nam2 in room_names:
                if (int(-(i1-i2)) == 1) or (int(-(j1-j2)) == 1):
                    # Do link rooms together
                    tiny_door_name = "tiny-door-{}{}-{}{}".format(i1, j1, i2, j2)
                    tiny_door_names.append(tiny_door_name)
                    wide_door_name = "wide-door-{}{}-{}{}".format(i1, j1, i2, j2)
                    wide_door_names.append(wide_door_name)
                    tiny_door_links.append(
                        [
                            nam1, nam2, tiny_door_name, "tiny"
                        ]
                    )
                    wide_door_links.append(
                        [
                            nam1, nam2, wide_door_name, "wide"
                        ]
                    )
        out += " ".join(tiny_door_names)
        out += """
            """
        out += " ".join(wide_door_names)

        out += """
            tablet
            ;; dynamic:
            shak
            grip1 grip2
            """
        out += ' '.join(
            ["obj"+str(i) for i in range(objs_count )]
        )

        out +="""
            box
          )
          (:init
            ;; static:
            """

        out += "(is-room " + pure_room_names[0]
        for nam in pure_room_names[1:]:
            out += ") (is-room " + nam

        out += """)
            """

        for x_door_links in [tiny_door_links, wide_door_links]:
            for nam1, nam2, x_door_name, door_type in x_door_links:
                app = "(is-{}-door {}) (are-linked-by {} {} {}) (are-linked-by {} {} {})".format(
                    door_type,
                    x_door_name,
                    nam1,
                    nam2,
                    x_door_name,
                    nam2,
                    nam1,
                    x_door_name
                )
                out += app
                out += """
            """


        out += """(is-tablet tablet) (is-in tablet room00)
            ;; dynamic:
            (is-shakey shak) (is-in shak room00)
            (is-gripper grip1) (is-gripper-empty grip1)
            (is-gripper grip2) (is-gripper-empty grip2)
            """

        objs_states = []
        pure_objs_names = []
        for obj_i in range(objs_count):
            name = "obj"+str(obj_i)
            pure_objs_names.append(name)
            objs_states.append([
                obj_i,
                pure_room_names[(obj_i % len(pure_room_names))],
                name
            ])
        for i, room, obj in objs_states:
            out += "(is-small-obj {}) (is-on-floor {}) (is-in {} {})".format(
                obj,
                obj,
                obj,
                room
            )
            out += """
            """

        out += """(is-box box) (is-in box room00)
          )

          (:goal
            (and
              (is-in shak room00)
              (is-gripper-empty grip1)
              (is-gripper-empty grip2)
              """
        for obj in pure_objs_names:
            out += "(is-on-tablet {})".format(obj)
            out += """
              """
        for room in pure_room_names:
            out += "(not (is-lit {}) )".format(room)
            out += """
              """
        out += """(is-in box room00)
            )
          )
        )
        """

        save_file(out, rows, objs_count)
