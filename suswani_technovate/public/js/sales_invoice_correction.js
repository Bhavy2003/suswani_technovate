frappe.ui.form.on("Sales Invoice Correction", {
    sales_invoice: function (frm) {
        if (frm.doc.sales_invoice) {
            frappe.call({
                method: "get_sales_invoice_items",
                args: {
                    sales_invoice: frm.doc.sales_invoice
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
                            child.corrected_qty = item.corrected_qty;
                            child.batch_no = item.batch_no;
                        });
                        // Loop through dictionary response
                        // Object.entries(r.message).forEach(([key, item]) => {
                        //     let child = frm.add_child("correction_items");
                        //     child.item_code = item.item_code;
                        //     child.actual_qty = item.actual_qty;
                        //     child.available_qty = item.available_qty;
                        //     child.original_rate = item.original_rate;
                        //     child.corrected_qty = item.corrected_qty;
                        //     child.batch_no = item.batch_no;
                        // });
                        frm.refresh_field("correction_items");
                    }
                }
            });
        }
    },
    before_save: function(frm){
        if(frm.doc.correction_items){
            total_amount = 0;
            total_qty = 0;
            frm.doc.correction_items.forEach(item =>{
                // console.log('before if condition')
                if (item.corrected_amount) {  // Avoids null, undefined, or 0
                    // console.log('adding correction amount', item.corrected_amount);
                    total_amount += item.corrected_amount;
                    // console.log(total);
                }
                if(item.corrected_qty){
                    total_qty += item.corrected_qty;
                }
            })
            frm.set_value('total_correction_amount',total_amount)
            frm.set_value('total_correction_qty',total_qty)
            
        }
    }
});

frappe.ui.form.on("Sales Invoice Correction Item", {
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
    // console.log('calculate_correction_amount')
    // console.log(row.original_rate)
    // console.log(row.actual_qty)
    // console.log(row.corrected_rate)
    // console.log(row.corrected_qty)
    
    row.corrected_amount = (row.corrected_rate - row.original_rate) * row.corrected_qty;
    // console.log('row.correction_amount : ',row.correction_amount)
    cur_frm.refresh_field("correction_items");
}
