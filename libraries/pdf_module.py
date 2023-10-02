import numpy as np

# importing from a pylatex module
from pylatex import Document, PageStyle, Head, MiniPage, Foot, LargeText, \
    MediumText, LineBreak, simple_page_number, Section, Subsection, Tabularx, NoEscape, \
    TextBlock
from pylatex import Math, TikZ, Axis, Plot, Figure, Matrix, Alignat
from pylatex.utils import italic, bold

# Libraries for date manipulation
from datetime import date
from dateutil.relativedelta import relativedelta

# importing OS for file-structure
import os
import re

# dev variables
from dotenv import load_dotenv
load_dotenv()

# Company Variables
COMPANY_ADRES = str(os.getenv('COMPANY_ADRES'))
COMPANY_NAME = str(os.getenv('COMPANY_NAME'))
COMPANY_POSTAL = str(os.getenv('COMPANY_POSTAL'))
COMPANY_CITY = str(os.getenv('COMPANY_CITY'))
COMPANY_KVK_NUM = str(os.getenv('COMPANY_KVK_NUM'))
COMPANY_BTW_NUM = str(os.getenv('COMPANY_BTW_NUM'))
COMPANY_TOPTEXT = str(os.getenv('COMPANY_TOPTEXT'))
COMPANY_IBAN = str(os.getenv('COMPANY_IBAN'))

# DEV variables
DEV_EMPTY_AMOUNT = os.getenv('DEV_EMPTY_AMOUNT')
DEV_EMPTY_PRICE = os.getenv('DEV_EMPTY_PRICE')
DEV_EMPTY_DESCRIPTION = os.getenv('DEV_EMPTY_DESCRIPTION')
DEV_EMPTY_BTW = os.getenv('DEV_EMPTY_BTW')
DEV_AMOUNT_VARIABLE_INPUT_FORM = int(os.getenv('DEV_AMOUNT_VARIABLE_INPUT_FORM'))

# Recipient placeholders
RECIPIENT_NAME = os.getenv('RECIPIENT_NAME')
RECIPIENT_ADRES = os.getenv('RECIPIENT_ADRES')
RECIPIENT_CITY = os.getenv('RECIPIENT_CITY')
RECIPIENT_POSTAL = os.getenv('RECIPIENT_POSTAL')

LOGO_LOCATION = os.getenv('LOGO_LOCATION')
OUTPUT_DIR = os.getenv('OUTPUT_DIR')

# local variables
current_directory = os.path.dirname(os.path.abspath(__file__))

class NewItem:
    def __init__(self, description, piece_price, amount, btw):
        self.amount = amount
        self.piece_price = piece_price
        self.description = description
        self.btw = btw

    def total_price_incl_btw(self):
        price = float(self.piece_price.replace('.', '')) / 100
        qty = float(self.amount.replace('.', ''))/ 100
        tax_multiplier = 1 + (float(self.btw) / 100)
        return price * qty * tax_multiplier

    def total_price_excl_btw(self):
        price = float(self.piece_price.replace('.', '')) / 100
        qty = float(self.amount.replace('.', ''))/ 100
        return price * qty

empty_item = NewItem(DEV_EMPTY_AMOUNT, DEV_EMPTY_PRICE, DEV_EMPTY_DESCRIPTION, DEV_EMPTY_BTW)

class GeneralPDF:
    def __init__(self):
        # No clue wat to do with these
        self.btw_nummer = 20123
        #self.relatie_nummer = 3151

        # Variables that can be changed but can also be set on initialization
        today = date.today()
        self.entries = []
        self.factuur_datum = today.strftime("%B %d, %Y")
        self.verval_datum = (today + relativedelta(months=2)).strftime("%B %d, %Y")

        # Recipient info that will probably be changed every time
        self.recipient_name = RECIPIENT_NAME
        self.recipient_adres = RECIPIENT_ADRES
        self.recipient_city = RECIPIENT_CITY
        self.recipient_postal = RECIPIENT_POSTAL

        # Can be changed but should be done automatically
        self.factuur_nummer = get_highest_invoice_number()

    def entries_clear(self, num_columns):
        self.factuur_nummer = get_highest_invoice_number()
        self.entries.clear()
        self.entries = []
        for i in range(num_columns):
            self.entries.append(empty_item)

    def entries_print(self):
        for i in range(len(self.entries)):
            if not self.entries[i] is empty_item:
                print("item " + str(i+1))
                print("\tDescription\t" + self.entries[i].description)
                print("\tPiece Price\t" + self.entries[i].piece_price)
                print("\tAmount\t" + self.entries[i].amount)
                print("\tBTW\t" + self.entries[i].btw)
            else:
                print("item " +str(i+1)+ " is empty")

    def entries_overview_text(self, num_columns):
        total_text = ""
        total_text += "Date information"
        total_text += "\n\tInvoice date\t\t  "
        total_text += self.factuur_datum
        total_text += "\n\tExpiration date\t\t"
        total_text += self.verval_datum

        total_text += "\n\nRecipient information\n"
        total_text += "\tName\t"
        total_text += self.recipient_name
        total_text += "\n\tAdres\t"
        total_text += self.recipient_adres
        total_text += "\n\tPostal\t"
        total_text += self.recipient_postal
        total_text += "\n\tCity\t"
        total_text += self.recipient_city

        total_text += "\n\nEmpty items will be removed on the final invoice\n"
        for i in range(num_columns):
            total_text += "Item "
            total_text += str(i+1)
            if not self.entries[i] is empty_item:
                total_text += "\n Description:\t\t"
                total_text += self.entries[i].description
                total_text += "\n Piece Price:\t\t"
                total_text += self.entries[i].piece_price
                total_text += "\n Amount:\t\t"
                total_text += self.entries[i].amount
                total_text += "\n BTW (%):\t\t"
                total_text += self.entries[i].btw
                total_text += ""
            total_text += "\n"
        return total_text

    def entries_generate(self, num_columns, input_array):
        if not input_array == None:
            for i in range(num_columns):
                input_description = input_array[i*DEV_AMOUNT_VARIABLE_INPUT_FORM]
                input_piece_price = input_array[i*DEV_AMOUNT_VARIABLE_INPUT_FORM+1]
                input_amount = input_array[i*DEV_AMOUNT_VARIABLE_INPUT_FORM+2]
                input_btw = input_array[i*DEV_AMOUNT_VARIABLE_INPUT_FORM+3]

                if (input_description == None) or (input_piece_price == ''):
                    self.entries[i] = empty_item
                else:
                    self.entries[i] = NewItem(
                    input_description, # Description
                    input_piece_price.replace(",","."), # Piece-price
                    input_amount.replace(",","."), # Amount
                    input_btw) # BTW

                    if "." not in self.entries[i].piece_price:
                        self.entries[i].piece_price += ".00"

                    if "." not in self.entries[i].amount:
                        self.entries[i].amount += ".00"

    def entries_array(self, num_columns):
        entries_array = []
        for i in range(num_columns):
            if self.entries[i] is empty_item:
                entries_array.append(None)
                entries_array.append(None)
                entries_array.append(DEV_EMPTY_AMOUNT)
                entries_array.append(DEV_EMPTY_BTW)
            else:
                entries_array.append(self.entries[i].description)
                entries_array.append(self.entries[i].piece_price)
                entries_array.append(self.entries[i].amount)
                entries_array.append(self.entries[i].btw)
        return entries_array

    def entries_insert(self, num_columns, items):
        for i in range(min(num_columns, len(items))):
            if items[i] is empty_item:
                self.entries[i] = items[i]

    def entries_no_btw(self):
        total_no_btw = 0
        for i in range(len(self.entries)):
            if not self.entries[i] is empty_item:
                total_no_btw += self.entries[i].total_price_excl_btw()
        return total_no_btw

    def entries_btw(self):
        total_btw = 0
        for i in range(len(self.entries)):
            if not self.entries[i] is empty_item:
                total_btw += self.entries[i].total_price_incl_btw()
        return total_btw

def get_highest_invoice_number(directory_path='./invoices/'):
    files = os.listdir(directory_path)
    pattern = re.compile(r'invoice_(\d+)')
    numbers = [int(match.group(1)) for file in files if (match := pattern.search(file))]
    return format(max(numbers)+1, '04') if numbers else '0000'

def save_pdf(pdf, gui):
    image_logo = os.path.join(current_directory, LOGO_LOCATION)
    output_directory = os.path.join(current_directory, OUTPUT_DIR)
    output_name = os.path.join(output_directory, './invoice_'+str(''.join(pdf.factuur_nummer)))

    geometry_options = {"tmargin": "2cm", "lmargin": "1cm", "rmargin": "1cm", "bmargin" : "2cm"}
    doc = Document(geometry_options=geometry_options)

    doc.append(NoEscape(r'''
        \definecolor{fill_color}{HTML}{063970}
    '''))

    header = PageStyle("header")
    with header.create(Head("L")):
        with doc.create(TextBlock(5, 8, 0.3)) as block:
            block.append(NoEscape(r'\raggedright'))

            # Company information
            block.append(bold(COMPANY_NAME))
            block.append(LineBreak())
            block.append(italic(COMPANY_TOPTEXT))
            block.append(LineBreak())
            block.append(COMPANY_ADRES)
            block.append(LineBreak())
            block.append(COMPANY_POSTAL + ", " + COMPANY_CITY)
        with doc.create(Figure(position='h!')) as logo_image:
            logo_image.add_image(image_logo, width='200px', placement='')

    with doc.create(TextBlock(5, 1, 0)) as block:
        block.append(NoEscape(r'\raggedright'))
        block.append(pdf.recipient_name)
        block.append(LineBreak())
        block.append(pdf.recipient_adres)
        block.append(LineBreak())
        block.append(pdf.recipient_postal + ", " + pdf.recipient_city)

    with header.create(Foot("L")):
        header.append("Geliefde binnen 14 dagen te betalen op " + COMPANY_IBAN)

    doc.preamble.append(header)
    doc.change_document_style("header")

    # Bottom line
    with doc.create(TikZ()):
        doc.append(NoEscape(r'''
            \begin{scope}[transform canvas={rotate=70, anchor=south east}]
                \fill[fill_color] ([xshift=0cm, yshift=-25cm]current page.south east) rectangle ++(-50cm,1cm);
            \end{scope}
        '''))
    # Top line
    with doc.create(TikZ()):
        doc.append(NoEscape(r'''
            \begin{scope}[transform canvas={rotate=-30, anchor=south east}]
                \fill[fill_color] ([xshift=10cm, yshift=10cm]current page.south east) rectangle ++(-50cm,0.5cm);
            \end{scope}
        '''))


    doc.append(LineBreak())
    doc.append(LineBreak())
    doc.append(LineBreak())
    doc.append(LineBreak())
    doc.append(LineBreak())
    doc.append(LineBreak())
    doc.append(LineBreak())
    doc.append(LineBreak())

    with doc.create(MiniPage(align='l')):
        with doc.create(Tabularx('XXXXX', width_argument=NoEscape(r'\textwidth'))) as table:
            table.add_row(bold("Factuurnummer"),bold("Factuurdatum"),bold("Vervaldatum"),bold("BTW Nummer"),bold("KVK Nummer"))
            table.add_row(pdf.factuur_nummer, pdf.factuur_datum, pdf.verval_datum, COMPANY_BTW_NUM, COMPANY_KVK_NUM)

        doc.append(LineBreak())
        doc.append(LineBreak())
        doc.append(LineBreak())
        doc.append(LineBreak())

        with doc.create(Tabularx('lXlll', width_argument=NoEscape(r'\textwidth'))) as table:
            table.add_row(bold("#"), bold("Omschrijving"), bold("Prijs"), bold("Bedrag"), bold("Btw"))
            table.add_hline()
            # Items
            for i in range(gui.number_of_entries_invoice):
                item = pdf.entries[i]
                if not item is empty_item:
                    total_ecxl_btw = item.total_price_excl_btw()
                    table.add_row(item.amount, item.description, f"€ {item.piece_price}", f"€ {total_ecxl_btw:.2f}", f"{item.btw}%")
                    table.add_hline()
            # Total W/O Btw
            table.add_row('', '', bold("Subtotaal"), f"€ {pdf.entries_no_btw():.2f}", '')
            table.add_row('', '', NoEscape("incl. BTW"), NoEscape(f"€ {pdf.entries_btw():.2f}" + " \\\ \cline{3-4}"), '')

    doc.generate_pdf(output_name, clean_tex=True)

    pdf.factuur_nummer = get_highest_invoice_number()
