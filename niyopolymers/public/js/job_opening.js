frappe.ui.form.on('Job Opening', {
    refresh(frm) {
        // your code here
        console.log('refresh')
        var today = new Date();
        var dd = String(today.getDate()).padStart(2, '0');
        var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
        var yyyy = today.getFullYear();
        today = yyyy + '-' + mm + '-' + dd;
        if (frm.doc.end_date < today) {
            frm.set_value('status', 'Closed')

        }
    }
})