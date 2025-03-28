frappe.ui.form.on("Sales Invoice", {
    refresh: function (frm) {
        if (frm.doc.docstatus === 1 && frm.doc.custom_unfix_sales == 1) {  // Only show when Sales Invoice is submitted
            frm.add_custom_button(__('Create Correction'), function () {
                frappe.new_doc('Sales Invoice Correction', {
                    sales_invoice: frm.doc.name
                });
            });
        }
    }
});

frappe.ui.form.on('Sales Invoice', {
    refresh(frm) {
        if (frm.is_new() && frm.doc.is_return && frm.doc.custom_unfix_sales) {
            frm.set_value('update_stock',0);

            // Keep only the first row, remove others
            if (frm.doc.items.length > 1) {
                frm.doc.items = [frm.doc.items[0]];
            }

            // Set qty of the first row to zero
            if (frm.doc.items.length > 0) {
                frm.doc.items[0].qty = 0;
            }

            // Refresh the items field
            frm.refresh_field('items');
        }
    }
});

frappe.ui.form.on('Sales Invoice', {
    refresh: function (frm) {
        // frm.clear_custom_buttons()
        // if (frm.doc.docstatus !== 0) {
        //     return;
        // }
        
        frm.add_custom_button('Add Bulk Items', () => {
            let dialog = new frappe.ui.Dialog({
                title: 'Select Item and Warehouse',
                fields: [
                    {
                        label: 'Item',
                        fieldname: 'item',
                        fieldtype: 'Link',
                        options: 'Item',
                        reqd: 1,
                        change: async function () {
                            const new_item = dialog.get_value('item');
                            if (!new_item || dialog.current_item === new_item) return;
                            dialog.current_item = new_item;
                            await fetch_batch_details(dialog, new_item);
                        },
                    },
                    {
                        label: 'Rate',
                        fieldname: 'rate',
                        fieldtype: 'Currency',
                        reqd: 1,
                        // default: 1200,
                    },
                    {
                        label: 'Item Details',
                        fieldname: 'batch_table',
                        fieldtype: 'Table',
                        cannot_add_rows: true,
                        in_place_edit: false,
                        fields: [
                            { fieldtype: 'Data', fieldname: 'batch_no', label: 'Bar No', read_only: 1, in_list_view: 1, width: 150 },
                            { fieldtype: 'Link', fieldname: 'warehouse', label: 'Warehouse', options: 'Warehouse', read_only: 1, in_list_view: 1, width: 150 },
                            { fieldtype: 'Float', fieldname: 'qty', label: 'Weight (Grams)', read_only: 1, in_list_view: 1, width: 100 },
                        ],
                        data: [],
                    },
                ],
                size: 'large',
                primary_action_label: 'Add to Invoice',
                primary_action: async function () {
                    const selected_rows = dialog.fields_dict['batch_table'].grid.get_selected_children();
                    if (!selected_rows.length) {
                        frappe.msgprint(__('Please select at least one batch.'));
                        return;
                    }
                    if(dialog.get_value('rate') <= 0){
                        frappe.msgprint(__('Rate should be greater than 0'));
                        return;
                    }

                    // console.log("Selected Rows:", selected_rows);
                    
                    if (frm.doc.items.length === 1 && !frm.doc.items[0].item_code) {
                        frm.clear_table('items');
                        frm.refresh_field('items');
                    }

                    for (const row of selected_rows) {
                        // Check if the batch, warehouse, and quantity combination already exists in the items table
                        const exists = frm.doc.items.some(item => 
                            item.batch_no === row.batch_no && 
                            item.warehouse === row.warehouse && 
                            item.qty === row.qty
                        );

                        if (exists) {
                            frappe.show_alert({
                                message: __(`Batch ${row.batch_no} in Warehouse ${row.warehouse} with Quantity ${row.qty} already exists in the invoice.`),
                                indicator: 'orange'
                            });
                            continue; // Skip adding this row
                        }

                        const batch_details = await frappe.call({
                            method: 'frappe.client.get',
                            args: { doctype: 'Batch', name: row.batch_no },
                        });

                        if (batch_details.message) {
                            frm.add_child('items', {
                                item_code: dialog.get_value('item'),
                                item_name: dialog.get_value('item'),
                                qty: row.qty,
                                uom: batch_details.message.stock_uom,
                                rate:  dialog.get_value('rate'),
                                use_serial_batch_fields: 1,
                                batch_no: row.batch_no,
                                warehouse: row.warehouse,
                                expense_account: 'Cost of Goods Sold - SJPL',
                                income_account: 'Sales - SJPL',
                            });
                        }
                    }

                    frm.refresh_field('items');
                    dialog.hide();
                    // frappe.show_alert({ message: 'Items Added', indicator: 'green' });
                },
            });
            dialog.show();
        });
    },
});

async function fetch_batch_details(dialog, item) {
    frappe.show_alert({ message: 'Fetching Item details...', indicator: 'blue' });

    try {
        const batch_response = await frappe.call({
            method: 'frappe.client.get_list',
            args: { doctype: 'Batch', fields: ['name'], filters: { item: item }, limit_page_length: 0 },
        });

        let batches = batch_response.message;
        // console.log("Batches found:", batches);

        if (!batches || batches.length === 0) {
            frappe.msgprint('No batches found for this item.');
            return;
        }

        let batch_details = [];
        const processed_batches = new Set();

        for (let batch of batches) {
            let batch_no = String(batch.name).trim();
            if (!processed_batches.has(batch_no)) {
                // console.log("Fetching details for batch:", batch_no);
                
                const response = await frappe.call({
                    method: 'erpnext.stock.doctype.batch.batch.get_batch_qty',
                    args: { batch_no: batch_no },
                });

                // console.log("Batch details received:", response.message);
                
                if (response.message) {
                    response.message.forEach(detail => {
                        if (detail.qty > 0) batch_details.push(detail);
                    });
                }
                processed_batches.add(batch_no);
            }
        }

        if (batch_details.length > 0) {
            const table = dialog.fields_dict['batch_table'];
            let unique_batches = batch_details.filter((detail, index, self) =>
                index === self.findIndex(d => d.batch_no === detail.batch_no && d.warehouse === detail.warehouse)
            );

            table.df.data = unique_batches;
            table.refresh();
        } else {
            frappe.msgprint('No available batches with stock for this item.');
        }
    } catch (error) {
        // console.error("Error fetching batch details:", error);
        frappe.msgprint('An error occurred while fetching batch details.');
    }
}



frappe.ui.form.on('Sales Invoice', {
    custom_batch_scan: function (frm) {
        if (frm.doc.custom_batch_scan) {
            const batch_no = frm.doc.custom_batch_scan.trim();

            frappe.dom.freeze(__('Fetching batch details...'));

            // Fetch batch details
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'Batch',
                    name: batch_no,
                },
                callback: function (batch_res) {
                    if (!batch_res.message) {
                        frappe.msgprint(__('Batch not found.'));
                        frappe.dom.unfreeze();
                        return;
                    }

                    const batch_data = batch_res.message;

                    // Get batch quantity and warehouse
                    frappe.call({
                        method: 'erpnext.stock.doctype.batch.batch.get_batch_qty',
                        args: {
                            batch_no: batch_no,
                        },
                        callback: function (qty_res) {
                            frappe.dom.unfreeze();

                            if (!qty_res.message || qty_res.message.length === 0) {
                                frappe.msgprint(__('No stock found for the selected batch.'));
                                return;
                            }

                            const warehouse_data = qty_res.message[0];
                            const warehouse = warehouse_data.warehouse;
                            const batch_qty = warehouse_data.qty || 0;

                            // Check if the first row is empty and remove it if so
                            if (frm.doc.items && frm.doc.items.length > 0) {
                                const first_row = frm.doc.items[0];
                                if (!first_row.item_code && !first_row.qty) {
                                    frm.doc.items.splice(0, 1);
                                }
                            }

                            // Add new row to the items table
                            const row = frm.add_child('items', {
                                item_code: batch_data.item,
                                item_name: batch_data.item,
                                qty: batch_qty,
                                uom: batch_data.stock_uom,
                                warehouse: warehouse,
                                use_serial_batch_fields: 1,
                                batch_no: batch_no,
                                expense_account: 'Cost of Goods Sold - SJPL',
                                income_account: 'Sales - SJPL',
                            });

                            // Trigger the item_code field's onchange handler
                            // frm.script_manager.trigger('item_code', row);

                            frm.refresh_field('items');
                            // frappe.msgprint(__('Item added successfully!'));
                            frm.set_value('custom_batch_scan', null);
                        },
                        error: function () {
                            frappe.msgprint(__('Error fetching batch quantity.'));
                            frappe.dom.unfreeze();
                        },
                    });
                },
                error: function () {
                    frappe.msgprint(__('Error fetching batch details.'));
                    frappe.dom.unfreeze();
                },
            });
        }
    },
});
