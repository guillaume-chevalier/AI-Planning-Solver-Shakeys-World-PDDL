
        ;; This is a problem definition for "Shakey's world" problem (Alternative 2).
        ;; We take for granted that the robot is autonomous for low-level tasks,
        ;; as an example, we only consider high-level actions such as moving the box
        ;; from a room to another room without caring about sub-tiles in the rooms
        ;; and other such small logistics details.

        ;; The goal of the agent (Shakey) is to tidy up the room by
        ;; placing every objects on the tablet.
        ;; Also, as initially, the lights must be all turned off and
        ;; the box replaced in room00 as initially.

        ;; Usage: ./ff -o shakey-domain.pddl -f shakey-task-2-3rooms-8objs.pddl
        ;; Usage: ./ipp -o shakey-domain.pddl -f shakey-task-2-3rooms-8objs.pddl



        (define (problem shakey-task-2-3rooms-8objs)
          (:domain shakey)
          (:objects
            ;; static:
            room00 room10 room20
            tiny-door-00-10 tiny-door-10-20
            wide-door-00-10 wide-door-10-20
            tablet
            ;; dynamic:
            shak
            grip1 grip2
            obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7
            box
          )
          (:init
            ;; static:
            (is-room room00) (is-room room10) (is-room room20)
            (is-tiny-door tiny-door-00-10) (are-linked-by room00 room10 tiny-door-00-10) (are-linked-by room10 room00 tiny-door-00-10)
            (is-tiny-door tiny-door-10-20) (are-linked-by room10 room20 tiny-door-10-20) (are-linked-by room20 room10 tiny-door-10-20)
            (is-wide-door wide-door-00-10) (are-linked-by room00 room10 wide-door-00-10) (are-linked-by room10 room00 wide-door-00-10)
            (is-wide-door wide-door-10-20) (are-linked-by room10 room20 wide-door-10-20) (are-linked-by room20 room10 wide-door-10-20)
            (is-tablet tablet) (is-in tablet room00)
            ;; dynamic:
            (is-shakey shak) (is-in shak room00)
            (is-gripper grip1) (is-gripper-empty grip1)
            (is-gripper grip2) (is-gripper-empty grip2)
            (is-small-obj obj0) (is-on-floor obj0) (is-in obj0 room00)
            (is-small-obj obj1) (is-on-floor obj1) (is-in obj1 room10)
            (is-small-obj obj2) (is-on-floor obj2) (is-in obj2 room20)
            (is-small-obj obj3) (is-on-floor obj3) (is-in obj3 room00)
            (is-small-obj obj4) (is-on-floor obj4) (is-in obj4 room10)
            (is-small-obj obj5) (is-on-floor obj5) (is-in obj5 room20)
            (is-small-obj obj6) (is-on-floor obj6) (is-in obj6 room00)
            (is-small-obj obj7) (is-on-floor obj7) (is-in obj7 room10)
            (is-box box) (is-in box room00)
          )

          (:goal
            (and
              (is-in shak room00)
              (is-gripper-empty grip1)
              (is-gripper-empty grip2)
              (is-on-tablet obj0)
              (is-on-tablet obj1)
              (is-on-tablet obj2)
              (is-on-tablet obj3)
              (is-on-tablet obj4)
              (is-on-tablet obj5)
              (is-on-tablet obj6)
              (is-on-tablet obj7)
              (not (is-lit room00) )
              (not (is-lit room10) )
              (not (is-lit room20) )
              (is-in box room00)
            )
          )
        )
        