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
               "Clear all"]

DEV_NR_ENTRIES_INVOICE = 5
gui_header = "Application overview"

if __name__ == '__main__':
    gui_object = gui.GuiWindow(gui_windows[0], gui_windows, DEV_NR_ENTRIES_INVOICE, gui_header)
    pdf_file = pdf.GeneralPDF()

    pdf_file.entries_clear(gui_object.number_of_entries_invoice)

    pdf_file.entries_print()

    pdf.save_pdf(pdf_file, gui_object)
    gui_object.current = gui_object.features[0]
