frappe.ui.form.on("Purchase Invoice", {
    refresh: function (frm) {
        if (frm.doc.docstatus === 1  && frm.doc.custom_unfix_purchase == 1) {  // Only show when Purchase Invoice is submitted
            frm.add_custom_button(__('Create Correction'), function () {
                frappe.new_doc('Purchase Invoice Correction', {
                    purchase_invoice: frm.doc.name
                });
            });
        }
    }
});