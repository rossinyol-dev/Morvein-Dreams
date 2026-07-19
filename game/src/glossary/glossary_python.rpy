default glossary_entries = []
default glossary_read_entry_ids = []
default glossary_selected_entry_id = None

init python:
    class GlossaryEntry:
        def __init__(self, entry_id, title, text, sketch=None):
            self.id = entry_id
            self.title = title
            self.text = text
            self.sketch = sketch

    def get_glossary_entry(entry_id):
        for entry in glossary_entries:
            if entry.id == entry_id:
                return entry

        return None

    def has_glossary_entry(entry_id):
        return get_glossary_entry(entry_id) is not None

    def add_glossary_entry(entry_id, title, text, sketch=None):
        if has_glossary_entry(entry_id):
            return

        glossary_entries.append(GlossaryEntry(entry_id, title, text, sketch))

    def update_glossary_entry(entry_id, title=None, text=None, sketch=None):
        entry = get_glossary_entry(entry_id)
        if entry is None:
            return False

        if title is not None:
            entry.title = title

        if text is not None:
            entry.text = text

        if sketch is not None:
            entry.sketch = sketch

        return True

    def add_glossary_note(entry_id, text, title=None, sketch=None):
        entry = get_glossary_entry(entry_id)
        if entry is None:
            return False

        if title is not None:
            entry.title = title

        if sketch is not None:
            entry.sketch = sketch

        if text in entry.text:
            return False

        if entry.text:
            entry.text = entry.text + "\n\n" + text
        else:
            entry.text = text

        if entry_id in glossary_read_entry_ids:
            glossary_read_entry_ids.remove(entry_id)

        return True

    def add_glossary_conditional_note(entry_id, flag, true_text, false_text, title=None, sketch=None):
        if flag:
            return add_glossary_note(entry_id, true_text, title, sketch)

        return add_glossary_note(entry_id, false_text, title, sketch)

    def glossary_unread_count():
        return len([entry for entry in glossary_entries if entry.id not in glossary_read_entry_ids])

    def mark_glossary_entry_read(entry_id):
        if entry_id not in glossary_read_entry_ids:
            glossary_read_entry_ids.append(entry_id)

    def open_glossary_entry(entry_id):
        renpy.store.glossary_selected_entry_id = entry_id
        mark_glossary_entry_read(entry_id)
        renpy.restart_interaction()

    def open_first_glossary_entry():
        if not glossary_entries:
            renpy.store.glossary_selected_entry_id = None
            return

        if get_glossary_entry(renpy.store.glossary_selected_entry_id) is not None:
            return

        first_unread = next((entry for entry in glossary_entries if entry.id not in glossary_read_entry_ids), None)
        if first_unread is not None:
            open_glossary_entry(first_unread.id)
        else:
            renpy.store.glossary_selected_entry_id = glossary_entries[0].id
