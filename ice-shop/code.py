import tkinter as tk
from tkinter import ttk
import yaml

# Get the prices of all the items
prices_information = open("ice-shop/settings.yml", "r")
prices = yaml.safe_load(prices_information)


window = tk.Tk() # Make the window


# Item amount / prices
items = {
    "customer": {
        "scoop": {
            "price": prices['bolletjes'],
            "amount": 0,
        },

        "cone": {
            "price": prices['hoorentjes'],
            "amount": 0,
        },

        "cup": {
            "price": prices['bakjes'],
            "amount": 0,
        },
        
        "whipped_cream": {
            "price": prices['toppings']['slagroom'],
            "amount": 0,
        },
            
        "sprinkles": {
            "price": prices['toppings']['bottetjes'],
            "amount": 0,
        },

        "caramel_sauce": {
            "cone": {
                "price": prices['toppings']['caramel']['hoorentje'],
                "amount": 0
            },

            "cup": {
                "price": prices['toppings']['caramel']['bakje'],
                "amount": 0
            }
        }
    },

    "business": {
        "litre": {
            "price": prices['liter'],
            "amount": 0
        }
    }
}


user_role = tk.StringVar(value="customer") # Users role
scoops_litres_amount = tk.StringVar() # Amount of scoop(s)/litre(s)
scoop_litre = tk.StringVar() # Information if the user must choose the amount of scoop(s) or litre(s)
cone_cup = tk.StringVar() # Users choice for a cone or a cup
label_text = tk.StringVar() # Text inside the label
buy_more = tk.StringVar() # If the user wants the receipt
topping = tk.StringVar()


importance_num = 0 # Index for the dictionary of the function information
question_num = 0
function_importance_num = 0

vat_percentage = prices['btw'] # VAT %


flavour_amounts = []



# Clear the window
def clear_window():
    # Clear the window
    for item in window.winfo_children():
        item.destroy()


# Make the question
def make_label():
    tk.Label(textvariable=label_text, font=('arial', 14)).grid(row=0, column=0, pady=('0', '10')) # Make the question and add it to the window    


# Update the label text
def update_label_text(text):
    label_text.set(text)
    make_label()


# Make the submit button
def make_submit(command):  
    tk.Button(text='submit', bg='gray', font=('arial', 10), command=command).grid(sticky='EW', columnspan=2, pady=('10', '0'))


# Make the input
def make_input(input:str, input_storage, array=None):
    if input == "radiobutton":
        # Make the options
        for role in array:
            ttk.Radiobutton(window, text=f"{role.capitalize()}", value=f"{role}", variable=input_storage).grid()
    
    elif input == "spinbox":
        if isinstance(array, tuple):
            for row, question in enumerate(array):
                question_row = row + 1

                answer = tk.StringVar()
                input_storage.append(answer)


                tk.Label(text=question, font=('arial', 14)).grid(row=question_row, column=0, sticky='w', pady=('0', '10'))
                tk.Spinbox(window, textvariable=answer, from_=0, to=float('inf')).grid(row=question_row, column=1, sticky='w') # Input
        else:
            tk.Spinbox(window, textvariable=input_storage, from_=1, to=float('inf')).grid(row=0, column=1, sticky='w') # Input

    elif input == "combobox":
        combobox = ttk.Combobox(window, textvariable=input_storage, state='readonly')
        combobox['values'] = array # All the options
        combobox.grid(row=0, column=1, sticky='w')


# Get the information what the user can buy
def validate_role():
    global user_chose_role

    user_chose_role = True


    # Add the information what the user can buy
    scoop_litre_information = "scoop" if user_role.get() == "customer" else "litre"
    scoop_litre.set(scoop_litre_information)

    make_dictionary_route() # Go to the next question


# Validate the amount for the scoop(s) / litre(s)
def validate_amount():
    # Check if the user chose a number
    try:
        amount = int(scoops_litres_amount.get()) # Amount the user chose

    # If the user did not choose a number
    except ValueError:
        scoops_litres_amount.set(1) # Reset the amount the user wants to buy

    # If the user chose a number
    else:
        # Standard a cup
        if amount >= 4 and amount <= 8:
            cone_cup.set("cup")

        # If the user chose a number that is not a valid option
        if amount <= 0 or amount > 8:
            scoops_litres_amount.set(1) # Reset the amount the user wants to buy
        else:
            make_dictionary_route() # Go to the next question


# Check if the user chose a flavour for every scoop / litre 
def validate_flavour():
    validation = True
    flavour_total_amount = 0
    max_amount = int(scoops_litres_amount.get())

    for flavour_amount in flavour_amounts:
        if not flavour_amount.get().isdigit():
            break
        else:
            flavour_total_amount += int(flavour_amount.get())
    
    else:
        if flavour_total_amount > max_amount:
            difference = flavour_total_amount - max_amount 

            message = f"You added {difference} {scoop_litre.get()}(s) too much"
        
        elif flavour_total_amount < max_amount:
            difference = max_amount - flavour_total_amount 

            message = f"You can add {difference} more {scoop_litre.get()}(s)"

        if flavour_total_amount != max_amount:
            label_text.set(message)

        else:
            make_dictionary_route()


# Check if the user wants to see the receipt
def validate_ask_receipt():
    add_items()

    if buy_more.get() == "yes":
        item_values() # Reset the values

        make_dictionary_route() # Ask the same questions again
    else:
        show_receipt() # Show the receipt to the user


def item_values():
    global flavour_amounts

    scoops_litres_amount.set(value="1") # Amount of scoop(s)/litre(s)
    cone_cup.set("cone") # Users choice for a cone or a cup
    buy_more.set("no") # If the user wants the receipt
    topping.set("none") # Topping the user chose

    flavour_amounts.clear() # Delete all the flavour amounts


# Add the items to the receipt dictionary
def add_items():
    amount = int(scoops_litres_amount.get())
    role = user_role.get()
    

    items[role][scoop_litre.get()]['amount'] += amount

    if cone_cup.get() and user_role.get() == "customer":
        items[role][cone_cup.get()]['amount'] += 1

    if topping.get() != "none" and topping.get():
        bought_topping = topping.get().replace(" ", "_").lower()

        items[role][bought_topping]['amount'] += 1


# Add the items that the user bought to the receipt
def bought_item_information():
    bought_items = {'items': {}, 'end_price': {}}
    role = user_role.get()

    receipt_price = 0

    for key, item_information in zip(items[role], items[role].values()):     
        try:
            item_information[cone_cup.get()]
        except KeyError:
            amount = item_information['amount']
            price = item_information['price']
        else:
            amount = item_information[cone_cup.get()]['amount']
            price = item_information[cone_cup.get()]['price']
        

        if amount > 0:
            if key == "whipped_cream" or key == "sprinkles" or key == "caramel_sauce":
                route_info = 'toppings'

                try:
                    bought_items['items'][route_info]
                except KeyError:
                    bought_items['items'][route_info] = {}

        
            else:
                route_info = key

                try:
                    bought_items['items'][route_info]
                except KeyError:
                    bought_items['items'][route_info] = {}

            
            try:
                bought_items['items'][route_info]['amount']
                bought_items['items'][route_info]['price']
            except KeyError:
                bought_items['items'][route_info]['amount'] = amount
                bought_items['items'][route_info]['price'] = price
            else:
                bought_items['items'][route_info]['amount'] += amount
                bought_items['items'][route_info]['price'] += price

    for item in bought_items['items']:
        item_amount = bought_items['items'][item]['amount']
        item_price = bought_items['items'][item]['price']
        item_end_price = round(item_amount * item_price, 2)
        
        bought_items['items'][item]['end_price'] = item_end_price
        bought_items['items'][item]['price'] = round(item_price, 2)
    
        receipt_price += item_end_price
    else:
        bought_items['end_price'] = receipt_price


    return bought_items


# Show the bought items to the user
def show_receipt():
    clear_window()

    topping_options = list( prices['toppings'].keys() )


    bought_items = bought_item_information()


    tk.Label(text='---------["Papi Gelato"]---------', font=('arial', 14)).grid(pady=('5', '10')) # Receipt start

    # For every item that the user can buy
    for key in bought_items['items']:    
        item_amount = bought_items['items'][key]['amount']
        item_price = bought_items['items'][key]['price']
        total_item_price = bought_items['items'][key]['end_price']


        if "_" in key:
            key = key.replace("_", " ")
    
        tk.Label(text=f"{key.capitalize()}           {item_amount} * {item_price}   = €{total_item_price}", font=('arial', 14)).grid(pady=('0', '5')) # Show the item, amount, price and the total price for the item
    else:
        receipt_price = bought_items['end_price']

        # Make the ending of the receipt
        tk.Label(text="                              ---------", font=('arial', 14)).grid(pady=('0', '5'))  
        tk.Label(text=f"Total                     = €{receipt_price}", font=('arial', 14)).grid() # Show the total price with VAT

        # If the users role is business
        if user_role.get() == "business":
            vat_price = round(bought_items['end_price'] / 100 * vat_percentage)

            tk.Label(text=f"VAT ({vat_percentage}%)               = €{vat_price}", font=('arial', 14)).grid() # Show the VAT price


def make_dictionary_route():
    global function_importance_num
    global question_num

    # Get the key of all the questions
    function_importance_names = list(function_information)
    function_importance_name = function_importance_names[function_importance_num]

    # Get the key with all the information for the question in it
    function_names = list( function_information[function_importance_name] )
    function_name = function_names[question_num]

    question_information = function_information[function_importance_name][function_name] # Get all the information about the question


    if user_role.get() == "business" and len(flavour_amounts) > 0:
        add_items()
        show_receipt()
    else:
        question_num += 1 # Go to the next question


        # If it is the last question of the dictionary
        if question_num == len(function_information[function_importance_name]):
            # Check if the next key for all the questions is for a specific role
            try:
                testing_function_num = function_importance_num + 1

                # If the key name is the same as all the possible roles
                if list(function_information)[testing_function_num] in ("customer", "business"):
                    # While the key name is not the role the user chose, or a name that is not a role
                    while list(function_information)[testing_function_num] != user_role.get():
                        testing_function_num += 1 # Go to the next key
                    
                    # If it is the role the user chose
                    else:
                        function_importance_num = testing_function_num # Set the index to that key
                
                else:
                    function_importance_num += 1 # Go to the next key

            # When all the questions are done
            except IndexError:            
                function_importance_num = 1 # Go to all the questions after the "starting questions" list with questions
            finally:
                question_num = 0 # Reset the index of the question

        make_question(question_information) # Make the question


# Make the question with the function information
def make_question(question_information): 
    # Get all the information to make the question
    question = question_information['question']() # Question
    input_name = question_information['input'] # Type of input
    stringvar = question_information['stringvar'] # Storage for the answer of the user
    submit_function = question_information['submit_function'] # Submit function


    clear_window() # Clear the window
    update_label_text(question) # Add the title

    try:
        input_array = question_information['input_array'] # List with options for the input
    
    # If there is not a list with options
    except KeyError:
        make_input(input_name, stringvar) # Make the input to choice the option
    
    # If there is a list with options
    else:   
        make_input(input_name, stringvar, input_array) # Make the input to choice the option

    make_submit(submit_function) # Make the submit button




function_information = {
    "starting_questions": {
        "question": {
            "question": lambda: "Are you a customer or a business?",
            "input": "radiobutton",
            "input_array": ("customer", "business"),
            "submit_function": validate_role,
            "stringvar": user_role
        }
    },

    "always": {
        "amount": {
            "question": lambda: f"How many {scoop_litre.get()}(s) do you want?",
            "input": "spinbox",
            "submit_function": validate_amount,
            "stringvar": scoops_litres_amount
        },

        "flavour": {
            "question": lambda: f"You can add {scoops_litres_amount.get()} more {scoop_litre.get()}(s)",
            "input": "spinbox",
            "input_array": ("Amount of strawberry", "Amount of chocolate", "Amount of vanilla"),
            "submit_function": validate_flavour,
            "stringvar": flavour_amounts
        }
    },

    "customer": {
        "cone_cup": {
            "question": lambda: f"Do you want the {scoops_litres_amount.get()} in a cup or a bucket?",
            "input": "combobox",
            "input_array": ("cone", "cup"),
            "submit_function": make_dictionary_route,
            "stringvar": cone_cup
        },

        "topping": {
            "question": lambda: f"Which topping do you want to add to your {scoops_litres_amount.get()} scoops?",
            "input": "combobox",
            "input_array": ("None", "Whipped cream", "Sprinkles", "Caramel sauce"),
            "submit_function": make_dictionary_route,
            "stringvar": topping        
        },

        "ask_receipt": {
            "question": lambda: f"Do you want to buy more?",
            "input": "radiobutton",
            "input_array": ("yes", "no"),
            "submit_function": validate_ask_receipt,
            "stringvar": buy_more
        }
    }
}




# When the program starts
if __name__ == "__main__":
    item_values()
    make_dictionary_route()
    window.mainloop() # Starts the window