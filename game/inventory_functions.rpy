init -5 python:

    def item_dragging_package(drags):
        global default_mouse
        default_mouse = "hand_grab"

    # ------------------------------------------------------------------
    # Map tool image names (as they appear in valid_evidence_steps values)
    # to the drag_name key used to identify the tool in a drop callback.
    # This is how we check "did the player drag the right thing?"
    # ------------------------------------------------------------------
    _IMAGE_TO_DRAG_NAME = {
        "marquis_reagent_idle":      "marquis_reagent_idle",
        "cobalt_thiocynate_idle":    "cobalt_thiocynate_idle",
        "hydrochloric_acid_idle":    "hydrochloric_acid_idle",
        "chloroform_idle":           "chloroform_idle",
        "tube_idle":                 "tube_idle",
        "evidence_bag_idle":         "evidence_bag_idle",
        "tamper_evident_tape_idle":  "tamper_evident_tape_idle",
        "backing_card_idle":         "backing_card_idle",
        "tape_idle":                 "tape_idle",
        "uv_light_idle":             "uv_light_idle",
        "magnetic_powder_idle":      "magnetic_powder_idle", 
        "scalebar_idle":             "scalebar_idle", 
        "pen_idle":                  "pen_idle"
    }

    # Map toolbox item names (from toolbox.json "name" field) to their
    # image_name_idle used in valid_evidence_steps
    _TOOL_NAME_TO_IMAGE = {
        "Marquis Reagent":      "marquis_reagent_idle",
        "Cobalt Thiocynate":    "cobalt_thiocynate_idle",
        "Hydrochloric Acid":    "hydrochloric_acid_idle",
        "Chloroform":           "chloroform_idle",
        "Tube":                 "tube_idle",
        "Evidence Bag":         "evidence_bag_idle",
        "Tamper Evident Tape":  "tamper_evident_tape_idle",
        "Backing Card":         "backing_card_idle",
        "Tape":                 "tape_idle",
        "UV Light":             "uv_light_idle",
        "Magnetic Powder":      "magnetic_powder_idle", 
        "Scalebar":             "scalebar_idle", 
        "Pen":                  "pen_idle"
    }

    def _get_current_step():
        """Return the current non-quiz step dict for testing_item, or None."""
        if testing_item is None:
            return None
        steps = valid_evidence_steps.get(testing_item, [])
        idx = store.evidence_step_index.get(testing_item, 0)
        drag_step = 0
        for s in steps:
            if s == "quiz":
                continue
            if drag_step == idx:
                return s
            drag_step += 1
        return None

    def _advance_step():
        """Advance evidence_step_index for testing_item past any following quiz."""
        steps = valid_evidence_steps.get(testing_item, [])
        idx = store.evidence_step_index.get(testing_item, 0)
        store.evidence_step_index[testing_item] = idx + 1
    def generic_drop(drags, drop):
        """
        Single drop callback used by the generic drag screen.
        Checks whether the dragged tool image matches the correct tool
        for the current step of the active evidence item.
        """
        if not drop:
            store.selected_tool = None
            renpy.restart_interaction()
            return False

        dragged_image = drags[0].drag_name
        step = _get_current_step()

        if step is None:
            store.selected_tool = None
            renpy.restart_interaction()
            return False

        correct_tool_image = list(step.values())[0]

        if dragged_image != correct_tool_image:
            renpy.notify("That's not the right tool for this step.")
            store.selected_tool = None
            renpy.restart_interaction()
            return False
        _advance_step()
        
        current_idx = store.evidence_step_index.get(store.testing_item, 0)
        steps = store.valid_evidence_steps.get(store.testing_item, [])
        drag_counter = 0
        next_marker = None
        
        for item in steps:
            if isinstance(item, dict):
                drag_counter += 1
            else:
                if drag_counter == current_idx:
                    next_marker = item
                    break

        if next_marker == "quiz":
            store.evidence_found[store.testing_item + "_presumptive"] = True
            store.quiz_pending = True
        elif next_marker == "collect_step":
            store.evidence_found[store.testing_item + "_packaged"] = True

        total_drag_steps = sum(1 for s in steps if isinstance(s, dict))
        if current_idx >= total_drag_steps:
            store.evidence_found[store.testing_item + "_packaged"] = True

        store.selected_tool = None
        renpy.restart_interaction()
        return True

    # ------------------------------------------------------------------
    # use_* functions called when player clicks the hand icon.
    # Sets selected_tool to this tool's image name.
    # The drag screen will show it as a draggable.
    # ------------------------------------------------------------------

    def _use_tool(tool_name):
        if testing_item is None:
            renpy.notify("Select an evidence item first.")
            return
        image_name = _TOOL_NAME_TO_IMAGE.get(tool_name)
        if image_name is None:
            renpy.notify("This tool can't be used here.")
            return
        store.selected_tool = image_name
        renpy.restart_interaction()

    def use_marquis_reagent():      _use_tool("Marquis Reagent")
    def use_cobalt_thiocynate():    _use_tool("Cobalt Thiocynate")
    def use_hydrochloric_acid():    _use_tool("Hydrochloric Acid")
    def use_chloroform():           _use_tool("Chloroform")
    def use_tube():                 _use_tool("Tube")
    def use_evidence_bag():         _use_tool("Evidence Bag")
    def use_tamper_evident_tape():  _use_tool("Tamper Evident Tape")
    def use_backing_card():         _use_tool("Backing Card")
    def use_tape():                 _use_tool("Tape")
    def use_uv_light():             _use_tool("UV Light")
    def use_magnetic_powder():      _use_tool("Magnetic Powder")
    def use_scalebar():             _use_tool("Scalebar")
    def use_pen():                  _use_tool("Pen")