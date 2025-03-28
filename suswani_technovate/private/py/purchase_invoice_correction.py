import frappe
# def create_correction_journal_entry(doc):
#     try:
#         # Fetch Purchase Invoice Details
#         purchase_invoice_doc = frappe.get_doc("Purchase Invoice", doc.purchase_invoice)
#         supplier = purchase_invoice_doc.supplier
#         company = purchase_invoice_doc.company
#         total_correction_amount = float(doc.total_correction_amount or 0)

#         if total_correction_amount == 0:
#             frappe.throw("No correction amount found, Journal Entry not required.")

#         # Determine Journal Entry Type
#         voucher_type = "Debit Note" if total_correction_amount < 0 else "Credit Note"

#         # Fetch Correct Account Details
#         payable_account = frappe.db.get_value("Company", company, "default_payable_account")
#         expense_account = frappe.db.get_value("Company", company, "default_expense_account")

#         if not payable_account:
#             frappe.throw("Payable account not found in company settings.")
        
#         if not expense_account:
#             frappe.throw("Expense account not found in company settings.")

#         # Debugging Messages
        

#         # Prepare Journal Entry
#         journal_entry = frappe.get_doc({
#             "doctype": "Journal Entry",
#             "voucher_type": voucher_type,
#             "posting_date": frappe.utils.today(),
#             "company": company,
#             "user_remark": f"Correction for Purchase Invoice {doc.purchase_invoice}",
#             "accounts": []
#         })

#         # First Entry: Payable Account (linked to Supplier)
#         journal_entry.append("accounts", {
#             "account": payable_account,
#             "party_type": "Supplier",  # Supplier needs a Payable Account
#             "party": supplier,
#             "credit_in_account_currency": abs(total_correction_amount) if total_correction_amount > 0 else 0,
#             "debit_in_account_currency": abs(total_correction_amount) if total_correction_amount < 0 else 0,
#             "reference_type": "Purchase Invoice",
#             "reference_name": doc.purchase_invoice
#         })

#         journal_entry.append("accounts", {
#             "account": expense_account,
#             "debit_in_account_currency": abs(total_correction_amount) if total_correction_amount > 0 else 0,
#             "credit_in_account_currency": abs(total_correction_amount) if total_correction_amount < 0 else 0
#         })

#         for tax in purchase_invoice_doc.get("taxes", []):
#             tax_account = tax.account_head
#             tax_rate = float(tax.rate or 0)
#             tax_correction_amount = (tax_rate / 100) * total_correction_amount

#             if tax_correction_amount != 0:
#                 # Adjust Tax Account
#                 journal_entry.append("accounts", {
#                     "account": tax_account,
#                     "debit_in_account_currency": abs(tax_correction_amount) if tax_correction_amount > 0 else 0,
#                     "credit_in_account_currency": abs(tax_correction_amount) if tax_correction_amount < 0 else 0
#                 })

#                 # Opposite entry (assumed as Income Account, adjust if necessary)
#                 journal_entry.append("accounts", {
#                     "account": expense_account,  # Adjust this if a different offset account is needed
#                     "credit_in_account_currency": abs(tax_correction_amount) if tax_correction_amount > 0 else 0,
#                     "debit_in_account_currency": abs(tax_correction_amount) if tax_correction_amount < 0 else 0
#                 })

#         # Insert and Submit Journal Entry
#         journal_entry.insert()
#         doc.journal_entry = journal_entry.name
#         journal_entry.submit()

#         frappe.msgprint(f"Journal Entry {journal_entry.name} Created Successfully.")
#         return {"status": "success", "journal_entry": journal_entry.name}

#     except Exception as e:
#         frappe.throw(f"Error in create_correction_journal_entry: {str(e)}")
# create_correction_journal_entry(doc)













#script-1 on-submit

def on_submit(doc,method):
    create_correction_journal_entry(doc,method)
def after_cancel(doc,method):
    cancel_linked_journal_entry(doc, method)
def before_save(doc,method):
    validate_purchase_invoice_correction(doc, method)



def create_correction_journal_entry(doc,method):
    try:
        # Fetch Purchase Invoice Details
        purchase_invoice_doc = frappe.get_doc("Purchase Invoice", doc.purchase_invoice)
        supplier = purchase_invoice_doc.supplier
        company = purchase_invoice_doc.company
        company_gstin = purchase_invoice_doc.company_gstin
        total_correction_amount = float(doc.total_correction_amount or 0)

        if total_correction_amount == 0:
            frappe.throw("No correction amount found, Journal Entry not required.")

        # Determine Journal Entry Type
        voucher_type = "Debit Note" if total_correction_amount < 0 else "Credit Note"

        # Fetch Correct Account Details
        payable_account = frappe.db.get_value("Company", company, "default_payable_account")
        expense_account = frappe.db.get_value("Company", company, "default_expense_account")

        if not payable_account:
            frappe.throw("Payable account not found in company settings.")
        
        if not expense_account:
            frappe.throw("Expense account not found in company settings.")

        # Debugging Messages
        

        # Prepare Journal Entry
        journal_entry = frappe.get_doc({
            "doctype": "Journal Entry",
            "voucher_type": voucher_type,
            "posting_date": frappe.utils.today(),
            "company": company,
            "company_gstin": company_gstin,
            "user_remark": f"Correction for Purchase Invoice {doc.purchase_invoice}",
            "cheque_no":doc.purchase_invoice,
            "cheque_date":purchase_invoice_doc.posting_date,
            "accounts": []
        })
        
        # Adjust Purchase Account (Rate Difference)
        journal_entry.append("accounts", {
            "account": expense_account,
            "debit_in_account_currency": abs(total_correction_amount) if total_correction_amount > 0 else 0,
            "credit_in_account_currency": abs(total_correction_amount) if total_correction_amount < 0 else 0
        })
        
        # Tax Correction Calculation
        total_tax_correction = 0
        for tax in purchase_invoice_doc.get("taxes", []):
            tax_account = tax.account_head
            tax_rate = float(tax.rate or 0)  
            tax_correction_amount = (tax_rate / 100) * abs(total_correction_amount)  
            total_tax_correction = total_tax_correction + tax_correction_amount
            
            if tax_correction_amount != 0:
                journal_entry.append("accounts", {
                    "account": tax_account,
                    "credit_in_account_currency": tax_correction_amount if total_correction_amount < 0 else 0,
                    "debit_in_account_currency": tax_correction_amount if total_correction_amount > 0 else 0
                })
        
        # Adjust Customer's Receivable Account (To Balance)
        total_payable_adjustment = abs(total_correction_amount) + total_tax_correction
        
        # First Entry: Payable Account (linked to Supplier)
        journal_entry.append("accounts", {
            "account": payable_account,
            "party_type": "Supplier",  # Supplier needs a Payable Account
            "party": supplier,
            "credit_in_account_currency": abs(total_payable_adjustment) if total_correction_amount > 0 else 0,
            "debit_in_account_currency": abs(total_payable_adjustment) if total_correction_amount < 0 else 0,
            "reference_type": "Purchase Invoice",
            "reference_name": doc.purchase_invoice
        })
        
        
        
        
        
        
        # Insert and Submit Journal Entry
        journal_entry.insert()
        doc.journal_entry = journal_entry.name
        # journal_entry.save()
        journal_entry.submit()

        frappe.msgprint(f"Journal Entry {journal_entry.name} Created Successfully.")
        return {"status": "success", "journal_entry": journal_entry.name}

    except Exception as e:
        frappe.throw(f"Error in create_correction_journal_entry: {str(e)}")



#script-2 before save

def validate_purchase_invoice_correction(doc, method):
    """Validate correction items in a Purchase Invoice before saving."""

    response = frappe.call("get_purchase_invoice_items", purchase_invoice=doc.purchase_invoice)
    available_qty_map = {}
    # Convert response list into a dictionary for easy lookup (item_code, batch_no → available_qty)
    for item in frappe.response["message"]:
        key = (item["item_code"], item["batch_no"] or "")  # Handle batch_no safely
        available_qty_map[key] = item["available_qty"]

    # Validate each correction item in the current document
    for item in doc.correction_items:
        key = (item.item_code, item.batch_no or "")  # Ensure batch_no is handled properly
        available_qty = available_qty_map.get(key, 0)  # Default to 0 if not found

        # Check if corrected qty is within available limits
        if item.corrected_qty > available_qty:
            frappe.throw(
                title=f"Correction Not Allowed for {item.item_code}",
                msg=f"Batch {item.batch_no or 'N/A'}: Available Qty = {available_qty}, Attempted Correction = {item.corrected_qty}"
            )
        

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



def cancel_linked_journal_entry(doc, method):
    if doc.journal_entry:
        journal_entry = frappe.get_doc("Journal Entry", doc.journal_entry)
        if journal_entry.docstatus == 1:
            journal_entry.cancel()
            frappe.msgprint(f"Linked Journal Entry {journal_entry.name} has been cancelled.")