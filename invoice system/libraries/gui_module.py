# importing numpy
import numpy as np

# importing stuff for GUI
from easygui import *
from tkinter import Tk

# Setting app icon
icon = "./images/verisell_Icon.ico"

class GuiWindow:
    def __init__(self, current_window, gui_features, number_of_entries_invoice, gui_header):
        self.current = current_window
        self.features = gui_features
        self.number_of_entries_invoice = number_of_entries_invoice
        self.header = gui_header

    def window_general(self, entries_overview_text):
        feature_buttons = []
        for i in range(1, len(self.features)):
            feature_buttons.append(self.features[i])
        self.current = buttonbox(entries_overview_text,
                                self.header,
                                feature_buttons)

    def window_set_recipient(self, earlierValues):
        fieldNames = ["Full name",
        "Adress",
        "Postal code",
        "City"]

        fieldValues = multenterbox("Recipient adress",
                                   self.header,
                                   fieldNames,
                                   earlierValues)
        self.current = self.features[0]
        if fieldValues == None:
            self.current = self.features[0]
            return earlierValues
        else:
            return fieldValues

    def window_set_invoice_number(self, factuur_nummer):
        fieldNames = ["Invoice number"]
        fieldValues = []
        fieldValues = multenterbox("Change invoice number",
                                   self.header,
                                   fieldNames,
                                   factuur_nummer)
        self.current = self.features[0]
        if fieldValues == None:
            self.current = self.features[0]
            return factuur_nummer
        else:
            return fieldValues

    def window_set_number(self, earlierValues):
        fieldNames = ["Full name",
        "Adress",
        "Postal code",
        "City"]

        fieldValues = multenterbox("Recipient adress",
                                   self.header,
                                   fieldNames,
                                   earlierValues)
        self.current = self.features[0]
        if fieldValues == None:
            self.current = self.features[0]
            return earlierValues
        else:
            return fieldValues

    def window_set_dates(self, earlierValues):
        fieldNames = ["Invoice Date",
        "Expiration Date"]

        fieldValues = multenterbox("Dates",
                                   self.header,
                                   fieldNames,
                                   earlierValues)
        self.current = self.features[0]
        if fieldValues == None:
            self.current = self.features[0]
            return earlierValues
        else:
            return fieldValues

    def window_set_amount_columns(self):
        # First prompt for the amount of entries
        fieldNames = ["Number of entries"]
        fieldValues = []
        fieldValues = multenterbox("Amount of entries in the invoice",
                                   self.header,
                                   fieldNames)

        while 1:
            errmsg = ""
            if fieldValues == None:
                self.current = self.features[0]
                break
            elif not fieldValues[0].strip().isnumeric():
                errmsg = "Input must be a number!"
            else:
                nr_entries_input = int(fieldValues[0].strip())
                if nr_entries_input < 1:
                    errmsg = "Number of entries must be greater than 0"
                elif nr_entries_input > 20:
                    errmsg = "Number of entries must be smaller than 21"
                else:
                    self.number_of_entries_invoice = nr_entries_input
                    break
            fieldValues = multenterbox(errmsg, self.header, fieldNames, fieldValues)

        print("Number of entries: ", self.number_of_entries_invoice)
        self.current = self.features[0]


    def window_set_items(self, earlierValues):
        fieldNames = []
        for i in range(self.number_of_entries_invoice):
            fieldNames.append("Description " + str(i+1))
            fieldNames.append("\t Piece price ")
            fieldNames.append("\t Amount ")
            fieldNames.append("\t BTW (%) ")

        fieldValues = multenterbox("Items and their cost in EUR",
                                   self.header,
                                   fieldNames,
                                   earlierValues)

        self.current = self.features[0]
        return fieldValues
