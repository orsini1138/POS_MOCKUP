# pos.py - a mockup of a Point Of Sale system like in restaurants. Be able to add items, remove items, 
#          add quantities of items at any point, and then make bills for however many customers and add
#          up the bill total in the end
#
# TODO:     -make comping items show comped items on the bill


##### DATA HELD HERE #####
class tableData():
    currentTable = ''
    currentServer = ''

    servers = {'madison':{
                        'B1':{'fish':99},
                        'B3':{'monkey brains':2, 'fish':1}
                        }, 
                'chubbs':{}}


# ITEM/PRICE LIST
menuItems = {'fish':10.50, 'monkey brains':25.99}

# ITEM COUNTS
itemCounts = {}#'fish':3}



##### TABLE MENU FUNCTIONS #####

# SERVER MENU - view servers.  
def serverMenu():
    while True:
        print('\n> SERVERS:')
        serverList = list(tableData.servers.keys())
        for server in range(len(serverList)):
            print('-'+serverList[server])
        print('\n-add server')
        serverInput = input('\n> ')
        if serverInput.lower() == 'add':
            addServer()
        elif serverInput.lower() == 'total':
            salesTotalsAll()
        elif serverInput.lower() not in serverList:
            print('\n> INVALID SERVER')
            input()
        else:
            break
    return serverInput

# Main Menu - view customer tables
def mainMenu():
    print('\n>>ENTER TABLE / ADD TABLE / [enter] to return')
    for i in tableData.servers[tableData.currentServer].keys(): 
        print(' -'+i)
    print(' -add')
    userInput = input('> ')
    return userInput

# Add new servers
def addServer():
    serverName = input('\n> SERVER NAME: ')
    tableData.servers[serverName.lower()] = {}


# ADD CUSTOMER TABLE
def addTable():
    newTable = input('\n TABLE NAME: ')
    tableData.servers[tableData.currentServer][newTable.upper()] = {} #= {newTable:{}}



# CALCULATE TOTAL SALES OF ONE SERVER
def salesTotals():
    totalSales = 0.0
    tableList = list(tableData.servers[tableData.currentServer].keys())
    for i in range(len(tableList)):
        for key, value in tableData.servers[tableData.currentServer][tableList[i]].items():
            totalSales += menuItems[key]*value

    print('\n> TOTAL SALES FOR '+ tableData.currentServer+':\n'+ ('${:,.2f}'.format(totalSales)).center(33)+'\n')
    input()


def salesTotalsAll():
    serverSales = {}
    totalSales = 0.0

    #get list of all servers
    serverList = list(tableData.servers.keys())
    for server in range(len(serverList)):
        serverName = serverList[server]
        serverTotal = 0.0
        serverTables =  list(tableData.servers[serverName.lower()].keys())
        for i in range(len(serverTables)):
            for key, value in tableData.servers[serverName][serverTables[i]].items():
                serverTotal += menuItems[key]*value
        serverSales[serverName] = float(serverTotal)
    
    #calculate total
    for key, value in serverSales.items():
        totalSales += value
    
    #format for printing
    print('\n> TOTAL SALES:   ${:,.2f}'.format(totalSales))
    for key, value in serverSales.items():
        print(('-'+key).ljust(12)+('${:,.2f}'.format(value)).rjust(14))
    input()


##### FOOD MENU FUNCTIONS #####

# ADD ITEM TO CUSTOMER BILL
def menuInput():
    while True:
        print('\n>>ENTER item name, -add, -rm, -bill, -comp, -ct or  -done<<')
        for i in menuItems.keys():
            print('-'+i)
        userInput = input('\n> ')
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
        elif userInput.lower() == 'comp':
            compItems()
        elif userInput.lower() in menuItems.keys():
            if userInput.lower() in itemCounts.keys():
                #check if its 86d
                if itemCounts[userInput.lower()] == 0:
                    print('\n>THIS ITEM HAS BEEN 86\'d')
                    input()
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
        #elif userInput.lower() == 'total':
        #    print('\n'+('TOTAL SALES FOR NIGHT').center(33))


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


# COMP ITEMS ON BILLS
def compItems():
    print()

    # print out items list
    for key, value in tableData.servers[tableData.currentServer][tableData.currentTable].items():
        if value == 1:
            # single items
            print(('- '+str(value)+' '+key).ljust(25, ' ')+('${:,.2f}'.format(menuItems[key])).rjust(15))
        else:
            #if multiple of item
            print(('- '+str(value)+' '+key+' @ $'+str(menuItems[key])).ljust(25, ' ')+('${:,.2f}'.format(menuItems[key]*value)).rjust(15))
    
    # comp items here
    while True:
        itemToComp = input('\n> Item to comp: ')
        
        # make sure chosen item is in table bill
        if itemToComp not in tableData.servers[tableData.currentServer][tableData.currentTable].keys():
            print('\n> ITEM NOT IN BILL')
            input()
            continue
        
        # check if there's multiple of item on bill
        if tableData.servers[tableData.currentServer][tableData.currentTable][itemToComp] > 1:
            compQuantity = input('\n> Quantity to comp: ')
            
            # make sure input is valid quantity
            if int(compQuantity) > tableData.servers[tableData.currentServer][tableData.currentTable][itemToComp]:
                print('\n> INVALID QUANTITY')
                input()
                continue
            
            # remove quantity from bill
            tableData.servers[tableData.currentServer][tableData.currentTable][itemToComp] -= int(compQuantity)
           
            # if quantity is 0, remove entirely from bill
            if tableData.servers[tableData.currentServer][tableData.currentTable][itemToComp] == 0:
                del tableData.servers[tableData.currentServer][tableData.currentTable][itemToComp]
            break
        
        
        else:
            #remove single item entirely from bill
            del tableData.servers[tableData.currentServer][tableData.currentTable][itemToComp]
            break



# ADD COUNT
def addCount():
    itemToAdd = input('>ITEM TO ADD COUNT: ')
    if itemToAdd not in menuItems.keys():
        print('\n>ITEM NOT ON MENU')
        input('>')
    else:
        itemCount = input('>ITEM COUNT: ')
        itemCounts[itemToAdd.lower()] = int(itemCount)


# Return table bill
def printTicket(tableName):
    ticketTotal = 0.0
    print()
    for key, value in tableData.servers[tableData.currentServer][tableData.currentTable].items():
        if value == 1:
            # single items
            print(('- '+str(value)+' '+key).ljust(25, ' ')+('${:,.2f}'.format(menuItems[key])).rjust(15))
            ticketTotal += menuItems[key]
        else:
            #if multiple of item
            print(('- '+str(value)+' '+key+' @ $'+str(menuItems[key])).ljust(25, ' ')+('${:,.2f}'.format(menuItems[key]*value)).rjust(15))
            ticketTotal += menuItems[key]*value
    
    #print total
    if ticketTotal >= 200.0:
        print('- 20% gratuity of ${:,.2f}'.format(ticketTotal*0.2))
        ticketTotal+= ticketTotal*0.2
    print('\n'+('TOTAL = ${:,.2f}'.format(ticketTotal)).center(33)+'\n')
    input('>')



##### RUN AND OUTPUT HERE #####
def mainLoop():
    serverInUse = False
    while True:
        if serverInUse == False:
            server = serverMenu()
        tableData.currentServer = server
        userInput = mainMenu()
        if userInput.lower() == 'add':
            addTable()
            serverInUse = True
        elif userInput.lower() == 'total':
            salesTotals()
            serverInUse = True
        elif userInput.upper() in list(tableData.servers[tableData.currentServer].keys()):
            tableData.currentTable = userInput.upper()
            menuInput()
        elif userInput.lower() == '':
            serverInUse = False
        else:
            print('\n>ENTER VALID INPUT')
            serverInUse = False
            input()
            

mainLoop()