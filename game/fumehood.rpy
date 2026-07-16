screen fumehood_screen():
    if fumehood_state == "empty":
        add "fumehood_empty"
    elif fumehood_state == "loaded":
        add "fumehood_firearm"
    elif fumehood_state == "closed":
        add "fumehood_closed"

    if fumehood_state == "empty":
        draggroup:
            if selected_tool is not None:
                drag:
                    drag_name selected_tool
                    draggable True
                    droppable False
                    dragging item_dragging_package
                    dragged  fumehood_drop
                    xpos 0.75 ypos 0.35
                    child Transform(selected_tool, zoom=1.5)
            drag:
                drag_name "fumehood_dropzone"
                draggable False
                droppable True
                xalign 0.5 yalign 0.5
                child Transform("fumehood_dropzone_idle", zoom=1.0)

        textbutton "Load Fumehood":
            xpos 0.4 ypos 0.85
            sensitive (fumehood_water_added and fumehood_glue_added and fumehood_firearm_placed)
            action Function(load_fumehood)

    elif fumehood_state == "loaded":
        textbutton "Close Fumehood":
            xpos 0.4 ypos 0.85
            action Function(close_fumehood)

label fumehood:
    $ hide_all_inventory()
    $ location = "fumehood"
    scene materials_lab
    show screen fumehood_screen
    show screen inventory
    show screen back_button_screen('materials_lab') onlayer over_screens

    label fumehood_wait_step:
        if fumehood_state == "closed" and not fumehood_done:
            jump fumehood_finish
        $ renpy.pause(0.3)
        jump fumehood_wait_step

label fumehood_finish:
    $ fumehood_done = True
    hide screen fumehood_screen
    hide screen inventory
    hide screen back_button_screen onlayer over_screens
    n normal1 "The superglue fumes have bonded to the amino acids in the print."
    n normal3 "Let's take the firearm out and photograph it."
    "You took a photo of the fingerprints on the fumed firearm."
    $ evidence.add_to_inventory(evids_by_key["firearm_fingerprint"])
    jump materials_lab