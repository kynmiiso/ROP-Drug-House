init -5 python:

    def item_dragging_package(drags):
        global default_mouse
        default_mouse = "hand_grab"

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
        """Return the current drag step dict for testing_item at evidence_step_index."""
        if testing_item is None:
            return None
        steps = valid_evidence_steps.get(testing_item, [])
        idx = store.evidence_step_index.get(testing_item, 0)
        drag_step = 0
        for s in steps:
            if isinstance(s, dict):
                if drag_step == idx:
                    return s
                drag_step += 1
        return None

    def _next_marker_after_current():
        """
        Return the string marker (quiz/collect_step/fingerprint_collect) that
        immediately follows the CURRENT drag step index, or None if the next
        thing is another dict step or end of list.
        Only looks at the very next entry after the current drag step position —
        does NOT scan past further dict steps.
        """
        if testing_item is None:
            return None
        steps = valid_evidence_steps.get(testing_item, [])
        idx = store.evidence_step_index.get(testing_item, 0)
        drag_count = 0
        for i, s in enumerate(steps):
            if isinstance(s, dict):
                if drag_count == idx:
                    if i + 1 < len(steps) and isinstance(steps[i + 1], str):
                        return steps[i + 1]
                    return None
                drag_count += 1
        return None

    def _fingerprint_collect_is_next():
        return _next_marker_after_current() == "fingerprint_collect"

    def _quiz_is_next():
        return _next_marker_after_current() == "quiz"

    def _collect_step_is_next():
        return _next_marker_after_current() == "collect_step"

    def _skip_marker(marker_name):
        """
        After completing a string marker step (e.g. fingerprint_collect),
        advance the internal position past it so we don't re-trigger it.
        We do this by tracking a separate marker offset on the store.
        Since markers don't consume evidence_step_index (only dicts do),
        we use a per-item marker index to know which string markers we've passed.
        """
        store.fingerprint_collected = True

    def _total_drag_steps(item):
        return sum(1 for s in valid_evidence_steps.get(item, []) if isinstance(s, dict))

    def _current_drop_image():
        if testing_item is None:
            return None
        steps = valid_evidence_steps.get(testing_item, [])
        idx = store.evidence_step_index.get(testing_item, 0)
        drag_index = 0
        for s in steps:
            if isinstance(s, dict):
                if drag_index == idx:
                    return list(s.keys())[0]
                drag_index += 1
        return None

    def _advance_step():
        steps = valid_evidence_steps.get(testing_item, [])
        idx = store.evidence_step_index.get(testing_item, 0)
        store.evidence_step_index[testing_item] = idx + 1

    def generic_drop(drags, drop):
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

        marker = _next_marker_after_current()

        if marker == "quiz":
            store.evidence_found[store.testing_item + "_presumptive"] = True
            store.quiz_pending = True
        
        store.selected_tool = None
        renpy.restart_interaction()
        return True

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
