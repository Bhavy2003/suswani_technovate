frappe.ui.form.on('Purchase Receipt', {
    refresh: function(frm) {
        // Add a custom button to open the dialog
        frm.add_custom_button(__('Add Bulk Items'), function() {
            open_custom_dialog(frm);
        }, __());
    }
});

// Function to open the custom dialog
function open_custom_dialog(frm) {
    const dialog = new frappe.ui.Dialog({
        title: 'Add Items with Batch Numbers',
        fields: [
            {
                label: 'Item Code',
                fieldname: 'item_code',
                fieldtype: 'Link',
                options: 'Item',
                reqd: 1,
                // default: 'Silver 999',
            },
            {
                label: 'Weight (Grams)',
                fieldname: 'weight',
                fieldtype: 'Float',
                reqd: 1,
                // default: 500,
            },
            {
                label: 'Quantity',
                fieldname: 'quantity',
                fieldtype: 'Int',
                reqd: 1,
                // default: 10,
            },
            {
                fieldtype: 'Column Break',  // This creates a column break
            },
            {
                label: 'Brand',
                fieldname: 'brand',
                fieldtype: 'Link',
                options: 'Brand',
                reqd: 1,
                // default: 'PSJ',
            },
            {
                label: 'Fineness',
                fieldname: 'fineness',
                fieldtype: 'Float',
                reqd: 1,
                // default: 99,
            },
            {
                label: 'Rate',
                fieldname: 'rate',
                fieldtype: 'Currency',
                reqd: 1,
                // default: 1200,
            },
            {
                fieldtype: 'Column Break',  // Another column break
            },
            {
                label: 'Bar No (Prefix)',
                fieldname: 'bar_prefix',
                fieldtype: 'Data',
                reqd: 1,
            },
            {
                label: 'Bar No (Start Number)',
                fieldname: 'bar_start',
                fieldtype: 'Int',
                reqd: 1,
            },
            {
                label: 'Bar No (Suffix)',
                fieldname: 'bar_suffix',
                fieldtype: 'Data',
                reqd: 1,
            }
        ],
        size: 'large',
        primary_action_label: 'Add Rows',
        primary_action: async function(values) {
            dialog.hide();
            await add_items_with_batches(frm, values);
        }
    });

    dialog.show();
}

// // Function to add rows to the child table with unique batch numbers
// async function add_items_with_batches(frm, values) {
//     const { item_code, weight, quantity, brand, fineness, rate, bar_prefix, bar_start, bar_suffix } = values;
//     // frm.doc.items = []
//     frappe.dom.freeze();
//     for (let i = 0; i < quantity; i++) {
        
        

//         const bar_number = `${bar_prefix}${bar_start + i}${bar_suffix || ''}`;
//         console.log(`Checking batch: ${bar_number}`);

//         try {
//             // Check and create the batch
//             const batch_number = await generate_batch(frm, bar_number, item_code);

//             // Add the row to the child table
            
//             frm.add_child('items', {
//                 item_code: item_code,
//                 item_name: item_code,
//                 qty: weight,
//                 uom: 'Gram',
//                 custom_brand: brand,
//                 custom_fineness: fineness,
//                 rate: rate,
//                 // amount: rate*weight,
//                 use_serial_batch_fields : 1,
//                 batch_no: batch_number,
//             });
//         } catch (error) {
//             // Stop further processing and notify the user
//             frappe.msgprint(error.message || `Error for Batch Number: ${bar_number}`);
//             break;
//         }
//     }

//     // Refresh the child table to show the new rows
//     frm.refresh_field('items');
//     frappe.dom.unfreeze();

//     // frappe.msgprint(`${quantity} rows added successfully!`);
// }

// Function to add rows to the child table with unique batch numbers
async function add_items_with_batches(frm, values) {
    const { item_code, weight, quantity, brand, fineness, rate, bar_prefix, bar_start, bar_suffix } = values;

    frappe.dom.freeze();

    // Check if the first row exists and is empty
    if (frm.doc.items && frm.doc.items.length > 0) {
        const first_row = frm.doc.items[0];
        if (!first_row.item_code && !first_row.qty && !first_row.batch_no) {
            // Remove the first row if it's empty
            frm.doc.items.splice(0, 1);
        }
    }

    // Add new rows with unique batch numbers
    for (let i = 0; i < quantity; i++) {
        const bar_number = `${bar_prefix}${bar_start + i}${bar_suffix || ''}`;

        try {
            // Check and create the batch
            const batch_number = await generate_batch(frm, bar_number, item_code);

            // Add a new row to the child table
            frm.add_child('items', {
                item_code: item_code,
                item_name: item_code,
                qty: weight,
                uom: 'Gram',
                custom_brand: brand,
                custom_fineness: fineness,
                rate: rate,
                use_serial_batch_fields: 1,
                batch_no: batch_number,
            });
        } catch (error) {
            // Stop further processing and notify the user
            frappe.msgprint(error.message || `Error for Batch Number: ${bar_number}`);
            break;
        }
    }

    // Refresh the child table to show the new rows
    frm.refresh_field('items');
    frappe.dom.unfreeze();
}

// Function to check and create a batch with async/await
async function generate_batch(frm, bar_number, item_code) {
    // Check if the batch already exists using `frappe.db.exists`
    // const batch_exists = await frappe.db.exists('Batch', { 'batch_id': bar_number });
    // const batch_exists = 0
    // if (batch_exists) {
    //     // Throw an error if the batch exists
    //     throw new Error(__('Batch with Bar Number {0} already exists!', [bar_number]));
    // }

    // If batch does not exist, create a new batch
    const new_batch = await frappe.call({
        method: 'frappe.client.insert',
        args: {
            doc: {
                doctype: 'Batch',
                batch_id: bar_number,
                item: item_code,
                reference_doctype: frm.doc.doctype,
                // reference_name: frm.doc.name
            }
        }
    });

    if (!new_batch.message) {
        throw new Error(__('Failed to create batch for Bar Number: {0}', [bar_number]));
    }

    return new_batch.message.batch_id;
}

