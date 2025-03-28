import frappe

# def create_correction_journal_entry(doc):
#     try:
#         sales_invoice_doc = frappe.get_doc("Sales Invoice", doc.sales_invoice)
#         customer = sales_invoice_doc.customer
#         company = sales_invoice_doc.company
#         total_correction_amount = float(doc.total_correction_amount or 0)

#         if total_correction_amount == 0:
#             frappe.throw("No correction amount found, Journal Entry not required.")

#         # Determine Journal Entry Type
#         voucher_type = "Credit Note" if total_correction_amount < 0 else "Debit Note"

#         # Fetch Account Details
#         receivable_account = frappe.db.get_value("Company", company, "default_receivable_account")
#         income_account = frappe.db.get_value("Company", company, "default_income_account")

#         if not receivable_account:
#             frappe.throw("Receivable account not found in company settings.")
        
#         if not income_account:
#             frappe.throw("Income account not found in company settings.")

#         # Prepare Journal Entry
#         journal_entry = frappe.get_doc({
#             "doctype": "Journal Entry",
#             "voucher_type": voucher_type,
#             "posting_date": frappe.utils.today(),
#             "company": company,
#             "user_remark": f"Correction for Sales Invoice {doc.sales_invoice}",
#             "accounts": []
#         })
#         journal_entry.append("accounts", {
#                     "account": receivable_account,
#                     "party_type": "Customer",
#                     "party": customer,
#                     "debit_in_account_currency": abs(total_correction_amount) if total_correction_amount > 0 else 0,
#                     "credit_in_account_currency": abs(total_correction_amount) if total_correction_amount < 0 else 0,
#                     "reference_type": "Sales Invoice",
#                     "reference_name": doc.sales_invoice
#                 })
#         journal_entry.append("accounts", {
#                     "account": income_account,
#                     "credit_in_account_currency": abs(total_correction_amount) if total_correction_amount > 0 else 0,
#                     "debit_in_account_currency": abs(total_correction_amount) if total_correction_amount < 0 else 0
#                 })

#         # Debit / Credit Entries
#         # for item in doc.get("correction_items", []):
#         #     corrected_qty = float(item.corrected_qty or 0)
#         #     original_rate = float(item.original_rate or 0)
#         #     corrected_rate = float(item.corrected_rate or 0)
#         #     amount_diff = (corrected_rate - original_rate) * corrected_qty

#         #     if amount_diff != 0:
#         #         # Credit/Debit Customer Account
#         #         journal_entry.append("accounts", {
#         #             "account": receivable_account,
#         #             "party_type": "Customer",
#         #             "party": customer,
#         #             "credit_in_account_currency": abs(amount_diff) if amount_diff > 0 else 0,
#         #             "debit_in_account_currency": abs(amount_diff) if amount_diff < 0 else 0,
#         #             "reference_type": "Sales Invoice",
#         #             "reference_name": doc.sales_invoice
#         #         })

#         #         # Debit/Credit Income Account
#         #         journal_entry.append("accounts", {
#         #             "account": income_account,
#         #             "debit_in_account_currency": abs(amount_diff) if amount_diff > 0 else 0,
#         #             "credit_in_account_currency": abs(amount_diff) if amount_diff < 0 else 0
#         #         })

#         if not journal_entry.accounts:
#             frappe.throw("No valid corrections to create Journal Entry.")

#         # Insert and Submit Journal Entry
#         journal_entry.insert()
#         doc.journal_entry = journal_entry.name
#         journal_entry.submit()

#         frappe.msgprint(f"Journal Entry {journal_entry.name} Created Successfully.")
#         return {"status": "success", "journal_entry": journal_entry.name}

#     except Exception as e:
#         frappe.log_error(f"Error in create_correction_journal_entry: {str(e)}")
#         return {"status": "error", "message": str(e)}
# create_correction_journal_entry(doc)










# def create_correction_journal_entry(doc):
#     # frappe.throw('method')
#     try:
#         sales_invoice_doc = frappe.get_doc("Sales Invoice", doc.sales_invoice)
#         customer = sales_invoice_doc.customer
#         company = sales_invoice_doc.company
#         total_correction_amount = float(doc.total_correction_amount or 0)

#         if total_correction_amount == 0:
#             frappe.throw("No correction amount found, Journal Entry not required.")

#         # Determine Journal Entry Type
#         voucher_type = "Credit Note" if total_correction_amount < 0 else "Debit Note"

#         # Fetch Account Details
#         receivable_account = frappe.db.get_value("Company", company, "default_receivable_account")
#         income_account = frappe.db.get_value("Company", company, "default_income_account")

#         if not receivable_account:
#             frappe.throw("Receivable account not found in company settings.")
        
#         if not income_account:
#             frappe.throw("Income account not found in company settings.")

#         # Prepare Journal Entry
#         journal_entry = frappe.get_doc({
#             "doctype": "Journal Entry",
#             "voucher_type": voucher_type,
#             "posting_date": frappe.utils.today(),
#             "company": company,
#             "user_remark": f"Correction for Sales Invoice {doc.sales_invoice}",
#             "accounts": []
#         })

#         # Main correction entry
#         journal_entry.append("accounts", {
#             "account": receivable_account,
#             "party_type": "Customer",
#             "party": customer,
#             "debit_in_account_currency": abs(total_correction_amount) if total_correction_amount > 0 else 0,
#             "credit_in_account_currency": abs(total_correction_amount) if total_correction_amount < 0 else 0,
#             "reference_type": "Sales Invoice",
#             "reference_name": doc.sales_invoice
#         })
        
#         journal_entry.append("accounts", {
#             "account": income_account,
#             "credit_in_account_currency": abs(total_correction_amount) if total_correction_amount > 0 else 0,
#             "debit_in_account_currency": abs(total_correction_amount) if total_correction_amount < 0 else 0
#         })

#         # Tax Correction
#         for tax in sales_invoice_doc.get("taxes", []):
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
#                     "account": income_account,  # Adjust this if a different offset account is needed
#                     "credit_in_account_currency": abs(tax_correction_amount) if tax_correction_amount > 0 else 0,
#                     "debit_in_account_currency": abs(tax_correction_amount) if tax_correction_amount < 0 else 0
#                 })

#         if not journal_entry.accounts:
#             frappe.throw("No valid corrections to create Journal Entry.")

#         # Insert and Submit Journal Entry
#         # print('JOURNAL ENTRY')
#         # Convert journal entry accounts to a dictionary format
#         # accounts_data = [entry.as_dict() for entry in journal_entry.accounts]
#         # Pretty-print the dictionary in JSON format
#         # print(json.dumps(accounts_data, indent=4))
#         journal_entry.insert()
#         doc.journal_entry = journal_entry.name
#         journal_entry.submit()

#         frappe.msgprint(f"Journal Entry {journal_entry.name} Created Successfully.")
#         return {"status": "success", "journal_entry": journal_entry.name}

#     except Exception as e:
#         frappe.log_error(f"Error in create_correction_journal_entry: {str(e)}")
#         return {"status": "error", "message": str(e)}

# create_correction_journal_entry(doc)




def on_submit(doc,method):
    create_correction_journal_entry(doc,method)
def after_cancel(doc,method):
    cancel_linked_journal_entry(doc,method)
def before_save(doc,method):
    validate_sales_invoice_correction(doc,method)

#script-1 on-submit
def create_correction_journal_entry(doc,method):
    try:
        sales_invoice_doc = frappe.get_doc("Sales Invoice", doc.sales_invoice)
        customer = sales_invoice_doc.customer
        company = sales_invoice_doc.company
        company_gstin = sales_invoice_doc.company_gstin
        total_correction_amount = float(doc.total_correction_amount or 0)

        if total_correction_amount == 0:
            frappe.throw("No correction amount found, Journal Entry not required.")

        # Determine Journal Entry Type
        voucher_type = "Credit Note" if total_correction_amount < 0 else "Debit Note"

        # Fetch Account Details
        receivable_account = frappe.db.get_value("Company", company, "default_receivable_account")
        income_account = frappe.db.get_value("Company", company, "default_income_account")
        
        if not receivable_account:
            frappe.throw("Receivable account not found in company settings.")
        if not income_account:
            frappe.throw("Income account not found in company settings.")

        # Prepare Journal Entry
        journal_entry = frappe.get_doc({
            "doctype": "Journal Entry",
            "voucher_type": voucher_type,
            "posting_date": frappe.utils.today(),
            "company": company,
            "company_gstin": company_gstin,
            "user_remark": f"Correction for Sales Invoice {doc.sales_invoice}",
            "cheque_no":doc.sales_invoice,
            "cheque_date":sales_invoice_doc.posting_date,
            "accounts": []
        })
        
        # Adjust Sales Account (Rate Difference)
        journal_entry.append("accounts", {
            "account": income_account,
            "debit_in_account_currency": abs(total_correction_amount) if total_correction_amount < 0 else 0,
            "credit_in_account_currency": abs(total_correction_amount) if total_correction_amount > 0 else 0
        })
        
        # Tax Correction Calculation
        total_tax_correction = 0
        for tax in sales_invoice_doc.get("taxes", []):
            tax_account = tax.account_head
            tax_rate = float(tax.rate or 0)  
            tax_correction_amount = (tax_rate / 100) * abs(total_correction_amount)  
            total_tax_correction = total_tax_correction + tax_correction_amount
            
            if tax_correction_amount != 0:
                journal_entry.append("accounts", {
                    "account": tax_account,
                    "debit_in_account_currency": tax_correction_amount if total_correction_amount < 0 else 0,
                    "credit_in_account_currency": tax_correction_amount if total_correction_amount > 0 else 0
                })
                
        # Adjust Customer's Receivable Account (To Balance)
        total_receivable_adjustment = abs(total_correction_amount) + total_tax_correction
        
        journal_entry.append("accounts", {
            "account": receivable_account,
            "party_type": "Customer",
            "party": customer,
            "debit_in_account_currency": total_receivable_adjustment if total_correction_amount > 0 else 0,
            "credit_in_account_currency": total_receivable_adjustment if total_correction_amount < 0 else 0,
            "reference_type": "Sales Invoice",
            "reference_name": doc.sales_invoice
        })

        # Insert and Submit Journal Entry
        journal_entry.insert()
        doc.journal_entry = journal_entry.name
        journal_entry.submit()

        frappe.msgprint(f"Journal Entry {journal_entry.name} Created Successfully.")
        return {"status": "success", "journal_entry": journal_entry.name}

    except Exception as e:
        frappe.log_error(f"Error in create_correction_journal_entry: {str(e)}")
        return {"status": "error", "message": str(e)}



# frappe.call("get_sales_invoice_items", sales_invoice=str(doc.sales_invoice))
# res = frappe.response['message']
# print(res)


#script-2 before-save
def validate_sales_invoice_correction(doc,method):
    response = frappe.call("get_sales_invoice_items", sales_invoice=doc.sales_invoice)
    available_qty_map = {}

    # Convert response list into a dictionary for easy lookup (item_code, batch_no → available_qty)
    for item in frappe.response["message"]:
        key = (item["item_code"], item["batch_no"])
        available_qty_map[key] = item["available_qty"]

    # Validate each correction item in the current doc
    for item in doc.correction_items:
        key = (item.item_code, item.batch_no or "")  # Ensure batch_no is handled properly
        available_qty = available_qty_map.get(key, 0)  # Default to 0 if not found

        # Check if corrected qty is within available limits
        if item.corrected_qty > available_qty:
            frappe.throw(
                title=f"Correction Not Allowed for {item.item_code}",
                msg=f"Batch {item.batch_no}: Available Qty = {available_qty}, Attempted Correction = {item.corrected_qty}"
            )

#script-3 after-cancel

def cancel_linked_journal_entry(doc, method):
    if doc.journal_entry:
        journal_entry = frappe.get_doc("Journal Entry", doc.journal_entry)
        if journal_entry.docstatus == 1:
            journal_entry.cancel()
            frappe.msgprint(f"Linked Journal Entry {journal_entry.name} has been cancelled.")