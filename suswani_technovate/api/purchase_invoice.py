
import frappe
import json
@frappe.whitelist()
def get_purchase_invoice_items(purchase_invoice):
    # Validate purchase invoice
    if not purchase_invoice:
        frappe.throw("Purchase Invoice not provided")

    # Fetch Purchase Invoice document
    purchase_invoice_doc = frappe.get_doc("Purchase Invoice", purchase_invoice)

    # Get submitted correction documents
    correction_docs = frappe.get_all(
        "Purchase Invoice Correction",
        filters={"purchase_invoice": purchase_invoice, "docstatus": ["in", [1]]},  # Only include submitted corrections
        pluck="name"
    )

    corrections = []
    if correction_docs:
        corrections = frappe.get_all(
            "Purchase Invoice Correction Item",
            filters={
                "parenttype": "Purchase Invoice Correction",
                "parentfield": "correction_items",
                "parent": ["in", correction_docs]
            },
            fields=["item_code", "batch_no", "SUM(corrected_qty) as corrected_qty"],
            group_by="item_code,  batch_no",
            
        )
    
    # Map corrected quantities
    # corrected_qty_map = {item["item_code"]: item.get("corrected_qty", 0) for item in corrections}
    corrected_qty_map = {}
    for item in corrections:
        key = (item["item_code"], item["batch_no"] or "")  # Handle empty batch_no
        corrected_qty_map[key] = item["corrected_qty"] or 0
        
    # Prepare item data
    items_data = []
    for item in purchase_invoice_doc.items:
        batch_no = item.batch_no or ""
        item_identifier =(item.item_code,batch_no)
        available_qty = item.get("qty", 0) - corrected_qty_map.get(item_identifier, 0)

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

    return items_data

# Get purchase invoice from request
purchase_invoice = frappe.form_dict.get("purchase_invoice")
if not purchase_invoice:
    frappe.throw("Purchase Invoice not provided in request")

frappe.response['message'] = get_purchase_invoice_items(purchase_invoice)
