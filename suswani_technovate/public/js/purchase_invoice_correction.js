frappe.ui.form.on("Purchase Invoice Correction", {
    purchase_invoice: function (frm) {
        if (frm.doc.purchase_invoice) {
            frappe.call({
                method: "get_purchase_invoice_items",
                args: {
                    purchase_invoice: frm.doc.purchase_invoice
                },
                callback: function (r) {
                    if (r.message) {
                        frm.clear_table("correction_items");
                        r.message.forEach(item => {
                            let child = frm.add_child("correction_items");
                            child.item_code = item.item_code;
                            child.actual_qty = item.actual_qty;
                            child.available_qty = item.available_qty;
                            child.original_rate = item.original_rate;
                            child.batch_no = item.batch_no;
                        });
                        frm.refresh_field("correction_items");
                    }
                }
            });
        }
    },
    before_save: function (frm) {
        if (frm.doc.correction_items) {
            let total_amount = 0;
            let total_qty = 0;
            frm.doc.correction_items.forEach(item => {
                if (item.corrected_amount) {  // Avoids null, undefined, or 0
                    total_amount += item.corrected_amount;
                }
                if (item.corrected_qty){
                    total_qty += item.corrected_qty;
                }
            });
            frm.set_value('total_correction_amount', total_amount);
            frm.set_value('total_correction_qty',total_qty)
        }
    }
});

frappe.ui.form.on("Purchase Invoice Correction Item", {
    corrected_qty: function (frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.corrected_qty > row.available_qty) {
            frappe.msgprint(__("Corrected quantity cannot exceed available quantity"));
            row.corrected_qty = row.available_qty;
            frm.refresh_field("correction_items");
        }
        calculate_correction_amount(row);
    },
    corrected_rate: function (frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        calculate_correction_amount(row);
    }
});

function calculate_correction_amount(row) {
    row.corrected_amount = (row.corrected_rate - row.original_rate) * row.corrected_qty;
    cur_frm.refresh_field("correction_items");
}



