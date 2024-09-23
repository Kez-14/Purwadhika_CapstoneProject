# Food Raw Material Inventory Program #
# ----------------------------------- #

# Stock Database
stock_dict = {
    'Code'          : ['1001','1002','1003','1008','1004','1005','1006','1007','1009','1010'],
    'Category'      : ['Egg', 'Dairy', 'Dairy', 'Noodles', 'Meat', 'Meat', 'Fresh Item', 'Oil','Seasoning','Seasoning'],
    'ItemName'      : ['Egg', 'Milk', 'Cheese', 'Pasta', 'Chicken', 'Sausage', 'Chilli', 'Cooking Oil','Salt', 'Pepper'],
    'Qty'           : [80, 600, 700, 800, 400, 200, 350, 300, 150, 200],
    'Price'         : [28000, 18000, 22000, 25000, 33000, 70000, 84000, 21500, 11000, 82000],
    'IncomingDate'  : ['2024-09-01', '2024-08-30', '2024-08-31', '2024-09-01', '2024-09-10', '2024-09-11', '2024-08-18', '2024-07-17', '2024-08-11', '2024-07-31']
}

# menu display
tot = 0
def print_menu(stock_dict, head, cart=None):
    global tot
    if head == 'main':                                                                                  # display stock list
        print('RAW MATERIAL STOCK LIST'.center(109,' '))
        print('-'*109)
        print('   Index   |    Code    |    Category     |    Item Name    |  Qty (kg)  |  Price/kg (Rp)  |  Incoming Date')
        print('-'*109)
        for index in range(len(stock_dict['Code'])):                                                    # sequential number (0 - (range in stockdict-1)) for index
            print(f"{index:<10} | {stock_dict['Code'][index]:<10} | {stock_dict['Category'][index]:<15} | {stock_dict['ItemName'][index]:<15} | {stock_dict['Qty'][index]:<10} | {stock_dict['Price'][index]:<15} | {stock_dict['IncomingDate'][index]}")

    elif head == 'pick' :                                                                               # display sorted stock list (based on incomingdate) -> menu 3
        data2 = list(zip(                                                                               # zip -> to combine list data from dict to tuple() that contains each element in same index
            range(len(stock_dict['Code'])),
            stock_dict['Code'],
            stock_dict['Category'],
            stock_dict['ItemName'],
            stock_dict['Qty'],
            stock_dict['Price'],
            stock_dict['IncomingDate']
        ))
        data2.sort(key=lambda x: x[6])                                                                  # choosing 'incomingdate' as key -> index 6
        print('Raw Material Stock for Picked Up'.center(109,' '))
        print('-'*109)
        print('   Index   |    Code    |    Category     |    Item Name    |  Qty (kg)  |  Price/kg (Rp)  |  Incoming Date')
        print('-'*109)
        for item in data2:
            index, Code, Category, ItemName, Qty, Price, IncomingDate = item
            print(f"{index:<10} | {Code:<10} | {Category:<15} | {ItemName:<15} | {Qty:<10} | {Price:<15} | {IncomingDate}")

    elif head == 'cart' :                                                                               # display stock release order cart (picked up list -> menu 3)
        if cart is None:
            print('No item has been added to cart')
            return
        total_amount = 0                                                                                # cart will start from 0, also for reset cart
        print('-'*109)
        print('   Index   |    Code    |    Category     |    Item Name    |  Qty (kg)  |  Price/kg (Rp)  |    Total (Rp)')
        print('-'*109)
        index_counter = 0                                                                               # index for each shown item
        for item_Name, details in cart.items():                                                         # add item name, then get another variable details
            item_totamount = details['carttotal']                                                       # carttotal = qty*price
            print(f"{index_counter:<10} | {details['code']:<10} | {details['category']:<15} | {item_Name:<15} | {details['cartqty']:<10} | {details['cartprice']:<15} | {item_totamount:<10}")  # Index is the item name for cart
            total_amount += details['carttotal']                                                        # update all price from cart 
            index_counter += 1                                                                          # to make different index for each item in table
        print('-' * 109) 
        print(f'{'Total Amount'.rjust(90,' '):<90} | {total_amount:<12}')
        print('\n')

# used for menu 2 (add) -> user can input category, name, qty, price, and date. code will generate automatically
def generatecode(item_Name, stock_dict):
    if item_Name in stock_dict['ItemName']:                                                             # to check if item already in stockdict/not. if yes, index will return the code & cat
        index = stock_dict['ItemName'].index(item_Name)
        return {
            'Code'      : stock_dict['Code'][index],
            'Category'  : stock_dict['Category'][index]
        }
    else:
        codenow = stock_dict['Code']
        if codenow:
            thelast = max(codenow, key = int)
            thenew  = str(int(thelast)+1).zfill(4)                                                      # if not, will get from last index in stockdict, then +1-> 4 digit string number
            return {
            'Code'      : thenew
        }

# main function 
while True :                                                                                            # display main menu
    print('='*42)
    print('RAW MATERIAL STOCK'.center(42,' '))
    print('PrimaPasta: Warehouse'.center(42,' '))
    print('='*42)
    print('Select Menu : '.center(42,' '))
    print('[ 1 ] Display stock list\n[ 2 ] Add item(s)\n[ 3 ] Pick item(s)\n[ 4 ] Remove item(s)\n[ 5 ] Exit program\n')
    menu = int(input("Enter number of the menu you want to run: "))

    # 1. Display Stock
    if menu == 1 :
        print_menu(stock_dict,'main')
        print('\n')
        continue

    # 2. Add Item(s)
    elif menu == 2 :
        item_Name  = input('Please enter the item name: ').title()                                      # to process user input into title case (A.. B..)
        if item_Name in stock_dict['ItemName']:                                                         # if user input item that already exist -> code & category = in stockdict
            index      = stock_dict['ItemName'].index(item_Name)
            item_Cat   = stock_dict['Category'][index]
            print(f'Item already exists--> Category: {item_Cat}')
        else:
            item_Cat   = input('Please enter the category: ').title()                                   # if not exist, user need to input manually
        item_Code  = generatecode(item_Name, stock_dict)
        item_Qty   = int(input('Please enter the quantity (kg): '))
        item_Price = int(input('Please enter the price/kg: '))
        item_Date  = input('Please enter the incoming date: (yyyy-mm-dd) ')

        addcart = {                                                                                     # after user add details, will show the cart first before the confirmation (want to add/not)
            item_Name: {
                'code': item_Code['Code'],
                'category': item_Cat,
                'cartqty': item_Qty,
                'cartprice': item_Price,
                'carttotal': item_Qty * item_Price,
                'incomingdate': item_Date
            }
        }
        print('Added Item'.center(109, ' '))
        print_menu(stock_dict, 'cart', addcart)

        addconfirm = input('Are you sure want to add this item to stock list? (yes/no)').capitalize()   # to process user input into capital letter
        if addconfirm == 'Yes':
            stock_dict['Code'].append(item_Code['Code'])
            stock_dict['Category'].append(item_Cat)
            stock_dict['ItemName'].append(item_Name)
            stock_dict['Qty'].append(item_Qty)
            stock_dict['Price'].append(item_Price)
            stock_dict['IncomingDate'].append(item_Date)

            print ('Item already added to stock list!')
            print (f'Admin PIC Name      : {input('Admin PIC Name: ')}')
            print (f'Date of Added Stock : {input('Enter the date the stock was added: (yyyy-mm-dd) ')}')
            print_menu(stock_dict, 'main')
            print('\n')
        
        elif addconfirm == 'No' :
            print('Item is not added to the stock list\n')
            stock_dict['Code'].pop()                                                                    # pop-> if user confirm 'N', each variable that already added will be removed
            stock_dict['Category'].pop()
            stock_dict['ItemName'].pop()
            stock_dict['Qty'].pop()
            stock_dict['Price'].pop()
            stock_dict['IncomingDate'].pop()
        else:
            print('Invalid option!')
        continue

    # 3. Pick Item(s)
    elif menu == 3 :
        item_cart = {}                                                                                  # dict to save user input
        view_stock = False                                                                              # to determine if updated stock will be shown/not

        while True:
            # user manual input and check if item in dictionary/not
            print_menu(stock_dict, 'pick')
            userpick = input('Enter the item name you want to pick: ').strip().title()                  # format user input into title case and delete space
            userpick_title = [item.title() for item in stock_dict['ItemName']]
            if userpick not in userpick_title:
                print('Invalid option!') 
                continue 

            # check index and available qty from stockdict (if item is in stockdict)
            index        = userpick_title.index(userpick)                                               # find index of item
            code         = stock_dict['Code'][index]
            category     = stock_dict['Category'][index]
            availqty     = stock_dict['Qty'][index]
            pickprice    = stock_dict['Price'][index]
            incomingdate = stock_dict['IncomingDate'][index]

            # user manual input
            qtypick   = int(input(f'Enter quantity for "{userpick}" that you want to pick: (available qty: {availqty} kg)'))
            if qtypick > availqty :
                print('Not enough stock')
                continue

            # update cart and stock
            if userpick not in item_cart :                                                              # to add details item in cart
                item_cart[userpick] = {
                    'code'          : code,
                    'category'      : category,
                    'cartqty'       : qtypick,
                    'cartprice'     : pickprice,
                    'carttotal'     : qtypick * pickprice,
                    'incomingdate'  : incomingdate
                }
            else :
                item_cart[userpick]['cartqty'] += qtypick                                               # to count total amount in cart
                item_cart[userpick]['carttotal'] = item_cart[userpick]['cartprice'] * item_cart[userpick]['cartqty']

            # decrease stockdict qty
            stock_dict['Qty'][index] -= qtypick
            print('Item added to cart.')
            print('\n')

            print('LIST OF PICKED UP ITEM(S)'.center(109,' '))
            print_menu(stock_dict, 'cart', item_cart)

            # user confirmation
            pick_another = input("Do you want to pick another item(s)? (yes/no): ")
            if pick_another.lower() != 'yes':
                break

        # display all picked up item(s)
        print (f'Admin PIC      : {input('Admin PIC Name: ')}')
        print (f'Date of Order  : {input('Enter the request date: (yyyy-mm-dd) ')}')
        print (f'Request Number : Based on Request Number#{input('Enter request number: ')}')
        print('STOCK WAREHOUSE RELEASE ORDER'.center(109,' '))
        print_menu(stock_dict, 'cart', item_cart)
        
        view_stock = input("Do you want to view the updated stock? (yes/no): ")
        if view_stock.lower() == 'yes':
            print_menu(stock_dict, 'main')
            print('\n')
        continue

    # 4. Remove Item(s)
    elif menu == 4 :
        print_menu(stock_dict, 'main')
        delcode = input('Enter the item code you want to remove: ')
        if delcode in stock_dict['Code'] :
            while delcode in stock_dict['Code']:
                index = stock_dict['Code'].index(delcode)
                del stock_dict['Code'][index]
                del stock_dict['Category'][index]
                del stock_dict['ItemName'][index]
                del stock_dict['Qty'][index]
                del stock_dict['Price'][index]
                del stock_dict['IncomingDate'][index]
            print(f'Item with code "{delcode}" has been removed.\n')
        else:
            print('Invalid option!\n')
        print_menu(stock_dict,'main')
        print('\n')
        continue

    # Exit Program
    elif menu == 5 : 
        print('Closing the program. Thank you! :)')
        print('\n')
        break
    else:
        print('Invalid option\nEnter number from [ 1 ] - [ 5 ]')
        print('\n') 
