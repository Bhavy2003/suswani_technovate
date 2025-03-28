# def get_sales_invoice_items(sales_invoice):
#     # Fetch Sales Invoice document
#     sales_invoice_doc = frappe.get_doc("Sales Invoice", sales_invoice)

#     # Get previous corrections only for submitted invoices (docstatus = 1)
#     corrections = frappe.get_all(
#         "Sales Invoice Correction Item",
#         filters={
#             "parenttype": "Sales Invoice Correction",
#             "parentfield": "correction_items",
#             "parent": ["in", frappe.get_all(
#                 "Sales Invoice Correction",
#                 filters={"sales_invoice": sales_invoice, "docstatus": 1},  # Only include submitted corrections
#                 pluck="name"
#             )]
#         },
#         fields=["item_code", "SUM(corrected_qty) as corrected_qty"],
#         group_by="item_code"
#     )

#     # Map corrected quantities
#     corrected_qty_map = {item["item_code"]: item["corrected_qty"] or 0 for item in corrections}

#     # Prepare item data
#     items_data = []
#     for item in sales_invoice_doc.items:
#         available_qty = item.qty - corrected_qty_map.get(item.item_code, 0)
#         if available_qty > 0:
#             items_data.append({
#                 "item_code": item.item_code,
#                 "actual_qty": item.qty,
#                 "original_rate": item.rate,
#                 "available_qty": available_qty,
#                 "corrected_qty": item.qty,
#                 "corrected_rate": item.rate,
#             })

#     return items_data

# # Get sales invoice from request
# sales_invoice = frappe.form_dict.get("sales_invoice")
# frappe.response['message'] = get_sales_invoice_items(sales_invoice)


import frappe
import json
@frappe.whitelist()
def get_sales_invoice_items(sales_invoice):
    # print('get_sales_invoice_items',sales_invoice)
    # Fetch Sales Invoice document
    sales_invoice_doc = frappe.get_doc("Sales Invoice", sales_invoice)

    # Get previous corrections grouped by item_code and batch_no
    corrections = frappe.get_all(
        "Sales Invoice Correction Item",
        filters={
            "parenttype": "Sales Invoice Correction",
            "parentfield": "correction_items",
            "parent": ["in", frappe.get_all(
                "Sales Invoice Correction",
                filters={"sales_invoice": sales_invoice, "docstatus": ["in", [1]]},  # Only include submitted corrections
                pluck="name"
            )]
        },
        fields=["item_code", "batch_no", "SUM(corrected_qty) as corrected_qty"],
        group_by="item_code, batch_no"
    )

    # Map corrected quantities per item_code & batch_no
    corrected_qty_map = {}
    for item in corrections:
        key = (item["item_code"], item["batch_no"] or "")  # Handle empty batch_no
        corrected_qty_map[key] = item["corrected_qty"] or 0

    # Prepare item data
    items_data = []
    for item in sales_invoice_doc.items:
        batch_no = item.batch_no or ""  # Default to empty string if batch_no is None
        key = (item.item_code, batch_no)
        available_qty = item.qty - corrected_qty_map.get(key, 0)  # Compare using item_code & batch_no

        if available_qty > 0:
            items_data.append({
                "item_code": item.item_code,
                "batch_no": batch_no,
                "actual_qty": item.qty,
                "original_rate": item.rate,
                "available_qty": available_qty,
                "corrected_qty": available_qty,  # Default to max available
                "corrected_rate": item.rate,
            })
    # print('API',items_data)
    return items_data
    # return 'hello ' + sales_invoice

# Get sales invoice from request
sales_invoice = frappe.form_dict.get("sales_invoice")
frappe.response['message'] = get_sales_invoice_items(sales_invoice)
