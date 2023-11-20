# DONE Route the items that are set in the GUI to some kind of object
# DONE Add these items from the object into the PDF
# DONE Add a button to compile the PDF using the given items

# TODO Fix the formatting of the table
# TODO Calucluate total cost of all items incl btw
# TODO Add env file for easy to implement transfer between companies
# TODO Style the actual pdf
# TODO Add small table for total cost of everything
# TODO Manage title of document
# TODO Add recipients name as an option and add this to the shown text in general window_general
# TODO Option to change the compiled PDF number, automatically or by hand
# TODO Pipeline the actual PDF to the online board so that everyone can see it

# importing custom libraries
import libraries.gui_module as gui
import libraries.pdf_module as pdf

# importing OS for file-structure
import os

# local variables
current_directory = os.path.dirname(os.path.abspath(__file__))

# DEV variables
gui_windows = ["Overview",
               "Set Number Of Entries",
               "Set Entries",
               "Generate PDF",
               "Clear All",
               "Set Recipient",
               "Change Date",
               "Change Number"]

DEV_NR_ENTRIES_INVOICE = 5
gui_header = "Application overview"

if __name__ == '__main__':
    gui_object = gui.GuiWindow(gui_windows[0], gui_windows, DEV_NR_ENTRIES_INVOICE, gui_header)
    pdf_file = pdf.GeneralPDF()

    pdf_file.entries_clear(gui_object.number_of_entries_invoice)

    pdf_file.entries_print()

    gui_object.window_general(pdf_file.entries_overview_text(gui_object.number_of_entries_invoice))

    while(1):
        print("Current window: ", gui_object.current)
        # Quitting application
        if gui_object.current is None:
            break
        # Return to overview
        elif gui_object.current is gui_object.features[0]:
            gui_object.window_general(pdf_file.entries_overview_text(gui_object.number_of_entries_invoice))
        # Set number of entries in invoice
        elif gui_object.current is gui_object.features[1]:
            stached_items = pdf_file.entries.copy()
            gui_object.window_set_amount_columns()
            pdf_file.entries_clear(gui_object.number_of_entries_invoice)
            pdf_file.entries_insert(gui_object.number_of_entries_invoice, stached_items)
        # Set entries of invoice
        elif gui_object.current is gui_object.features[2]:
            pdf_file.entries_generate(gui_object.number_of_entries_invoice, gui_object.window_set_items(pdf_file.entries_array(gui_object.number_of_entries_invoice)))
            pdf_file.entries_print()
        # Generate pdf
        elif gui_object.current is gui_object.features[3]:
            pdf.save_pdf(pdf_file, gui_object)
            gui_object.current = gui_object.features[0]
        # Clear all
        elif gui_object.current is gui_object.features[4]:
            pdf_file.entries_clear(gui_object.number_of_entries_invoice)
            gui_object.number_of_entries_invoice = DEV_NR_ENTRIES_INVOICE
            gui_object.current = gui_object.features[0]
        # Set recipient
        elif gui_object.current is gui_object.features[5]:
            earlier_values=[pdf_file.recipient_name,pdf_file.recipient_adres,pdf_file.recipient_postal,pdf_file.recipient_city]
            [pdf_file.recipient_name,pdf_file.recipient_adres,pdf_file.recipient_postal,pdf_file.recipient_city] = gui_object.window_set_recipient(earlier_values)
        elif gui_object.current is gui_object.features[6]:
            [pdf_file.factuur_datum, pdf_file.verval_datum] = gui_object.window_set_dates([pdf_file.factuur_datum, pdf_file.verval_datum])
        elif gui_object.current is gui_object.features[7]:
            [pdf_file.factuur_nummer] = gui_object.window_set_invoice_number([pdf_file.factuur_nummer])
