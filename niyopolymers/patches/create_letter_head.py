import frappe

def execute():
    try:
        frappe.get_doc({
            'doctype': 'Letter Head',
            'letter_head_name': 'Niyopolymers - Default',
            'is_default': 1,
            'source': 'Image',
            'image': '/assets/niyopolymers/images/niyopolymer_letter_head.png'
        }).insert()
        frappe.db.commit()
    except frappe.DuplicateEntryError:
        pass
