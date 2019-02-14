# pos.py - a mockup of a Point Of Sale system like in restaurants. Be able to add items, remove items, 
#          add quantities of items at any point, and then make bills for however many customers and add
#          up the bill total in the end
#
# TODO:       -print total nights sales for each server and whole team
#             -comp items in bill 


##### DATA HELD HERE #####
class tableData():
    currentTable = ''
    currentServer = 'madison'

    servers = {'madison':{
                        'B1':{'fish':2},
                        'B3':{'monkey brains':2, 'fish':1}
                        }, 
               'chubbs':{}}


# ITEM/PRICE LIST
menuItems = {'fish':10.50, 'monkey brains':25.99}

# ITEM COUNTS
itemCounts = {'fish':3}



##### TABLE MENU FUNCTIONS #####

# SERVER MENU - view servers.  
def serverMenu():
    while True:
        print('\n> SERVERS:')
        serverList = list(tableData.servers.keys())
        for server in range(len(serverList)):
            print('-'+serverList[server])
        print('\n-add')
        serverInput = input('\n> ')
        if serverInput.lower() == 'add':
            addServer()
        elif serverInput.lower() not in serverList:
            print('\n> INVALID SERVER')
            input()
        else:
            break
    return serverInput

# Main Menu - view customer tables
def mainMenu():
    print(' ENTER TABLE NAME or ADD TABLE:')
    for i in tableData.servers[tableData.currentServer].keys(): 
        print('-'+i)
    print('-add')
    userInput = input('> ')
    return userInput

# Add new servers
def addServer():
    serverName = input('\n> SERVER NAME: ')
    tableData.servers[serverName.lower()] = {}


# ADD CUSTOMER TABLE
def addTable():
    newTable = input(' TABLE NAME: ')
    tableData.servers[tableData.currentServer][newTable.upper()] = {} #= {newTable:{}}
    #print(tableData.servers[tableData.currentServer])



##### FOOD MENU FUNCTIONS #####

# ADD ITEM TO CUSTOMER BILL
def menuInput():
    while True:
        print('\n>>ENTER item name, -add, -rm, -bill, -ct or -done<<')
        for i in menuItems.keys():
            print('-'+i)
        userInput = input('> ')
        if userInput.lower() == 'done':
            break
        elif userInput.lower() == 'add':
            addItem()
        elif userInput.lower() == 'rm':
            removeItem()
        elif userInput.lower() == 'ct':
            addCount()
        elif userInput.lower() == 'bill':
            printTicket(tableData.currentTable)
        elif userInput.lower() in menuItems.keys():
            if userInput.lower() in itemCounts.keys():
                #check if its 86d
                if itemCounts[userInput.lower()] == 0:
                    print('>THIS ITEM HAS BEEN 86\'d')
                    input('>')
                    break
                else:
                    #otherwise print count and ask for quantity
                    print('>ITEM COUNT: '+str(itemCounts[userInput.lower()]))

            quantity = int(input('-QUANTITY: '))
            
            #make sure the count is higher than the quantity
            if userInput.lower() in itemCounts.keys() and quantity > itemCounts[userInput.lower()]:
                print('>QUANTITY TOO HIGH FOR COUNT')
                input()
                continue
            
            #add the item to the bill
            try:
                if userInput not in list(tableData.servers[tableData.currentServer][tableData.currentTable].keys()):
                    tableData.servers[tableData.currentServer][tableData.currentTable]
                    tableData.servers[tableData.currentServer][tableData.currentTable][userInput] = quantity
                else:
                    tableData.servers[tableData.currentServer][tableData.currentTable][userInput] += quantity
                    itemCounts[userInput.lower()] -= quantity
            except ValueError:
                print('\n>QUANTITY MUST BE NUMBER ONLY')
                input()
        elif userInput.lower() == 'total':
            print('\n'+('TOTAL SALES FOR NIGHT').center(33))


# ADD ITEM+PRICE
def addItem():
    while True:
        itemName = input('\n-ITEM NAME: ')
        try:
            itemPrice = input('-ITEM PRICE: $')
            menuItems[itemName.lower()] = float(itemPrice)
            break
        except ValueError:
            print('>PRICE MUST BE NUMBERS ONLY')


# REMOVE ITEM
def removeItem():
    itemToRemove = input('\n>ENTER FOOD ITEM TO REMOVE: ')
    if itemToRemove in menuItems.keys():
        del menuItems[itemToRemove]
        print('>ITEM REMOVED')
    else:
        print('\n>ITEM NOT IN MENU')
        input()

# ADD COUNT
def addCount():
    itemToAdd = input('>ITEM TO ADD COUNT: ')
    if itemToAdd not in menuItems.keys():
        print('\n>ITEM NOT ON MENU')
        input('>')
    else:
        itemCount = input('>ITEM COUNT: ')
        itemCounts[itemToAdd] = int(itemCount)


# Return table bill
def printTicket(tableName):
    ticketTotal = 0.0
    print()
    for key, value in tableData.servers[tableData.currentServer][tableData.currentTable].items():
        if value == 1:
            # single items
            print(('- '+str(value)+' '+key).ljust(25, ' ')+('${:,.2f}'.format(menuItems[key])).rjust(10))
            ticketTotal += menuItems[key]
        else:
            #if multiple of item
            print(('- '+str(value)+' '+key+' @ $'+str(menuItems[key])).ljust(25, ' ')+('${:,.2f}'.format(menuItems[key]*value)).rjust(10))
            ticketTotal += menuItems[key]*value
    
    #print total
    print('\n'+('TOTAL = ${:,.2f}'.format(ticketTotal)).center(33)+'\n')
    input('>')



##### RUN AND OUTPUT HERE #####
def mainLoop():
    while True:
        server = serverMenu()
        tableData.currentServer = server
        userInput = mainMenu()
        if userInput.lower() == 'add':
            addTable()
        elif userInput.upper() in list(tableData.servers[tableData.currentServer].keys()):
            tableData.currentTable = userInput.upper()
            menuInput()
        else:
            print('\n>ENTER VALID INPUT')
            

mainLoop()