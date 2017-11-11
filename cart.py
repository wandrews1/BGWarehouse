# Each item will have all of these parameters
class Item(object): 
	def __init__(self, name, description, barcode, price, units, vat):
		self._name = name
		self._description = description
		self._barcode = barcode
		self._price = price
		self._units = units
		self._vat = vat
		
	def __str__(self):
		return ("Item: " + self._name + "\nDescription: " + self._description + "\nBarcode: " + str(self._barcode) + "\nPrice: £" + int(self._price) + "\nUnits: " + str(self._units) + "\nVAT: " + str(self._vat))
		
	def __repr__(self):
		return ("Item(" + self._name + ", " + self._description + ", " + self._barcode + ", " + self._price + ", " + self._units + ", " + self._vat + ")")
	
	# Mutator methods for Item class
	def set_description(self, description):
		self._description = description
		
	def set_price(self, price):
		self._price = price
		
	def set_units(self, units):
		self._units = units
		
	def set_vat(self, vat):
		self._vat = vat
		
	# Accessor methods for Item class
	def get_name(self):
		return self._name
				
	def get_description(self):
		return self._description
				
	def get_barcode(self):
		return self._barcode
		
	def get_price(self):
		return self._price
		
	def get_units(self):
		return self._units 
				
	def get_vat(self):
		return self._vat
		
	def get_total_item_price(self):
		total_price = self._price * self._units 
		price_with_vat = total_price + (total_price * self._vat)
		return price_with_vat
	
class Clothing(Item):
	def __init__(self, size):
		self._size = size
		
	def get_size(self):
		return self._size
	

class Electronic(Item):
	def __init__(self, brand, warranty, name, description, barcode, price, units, vat):
		super(Electronic, self).__init__(self, name, description, barcode, price, units, vat)
		self._brand = brand
		self._warranty = warranty
		
	def get_brand(self):
		return self._brand
		
	def get_warranty(self):
		return self._warranty
		
		
		
		
class Basket(object):
	def __init__(self):
		self._items = []
		self._price = 0 
		
	def __str__(self):
		output = ("Items currently in your basket: ")
		for x in self._items:
			output += x.get_name() + ", " # Add each item to the string, followed by a comma
		return output[0:-2] + "." # When the final item in the string is reached, remove the comma and add a full stop

			
	def __repr__(self):
		for x in self._items:
			return str(x)
		
	def get_price(self):
		return self._price
		
	def get_items(self):
		return self._items
		
	def add_item(self, item): 
		self._items.append(item) # Add item to the current list of items 
		self._price += item.get_price() # Add price of current item to the price of items already added 
		
	def remove_item(self, item):
		for x in self._items:
			if item == x:
				self._items.remove(item)
				self._price -= item.get_price()
		return(currentBasket)




# A list of the items currently in stock which the user can choose from
print("Items currently in stock: \nBook \nCup \nKettle \nCoat \n")		
book = Item('Pride and Prejudice', 'Jane Austen', '4394839', 10, '1', '0.1')
cup = Item('Red cup', 'a cup that is red', '432432', 3, '2', '0.2')
kettle = Item('Blue kettle', 'a kettle that is blue', '323232', 12, '2', '0.3')
coat = Item('Children\'s coat', 'a coat for children', '43232', 20, '1', '0.2')
list = ['book','cup','kettle','coat']

currentBasket = Basket() 
# Initialise cont variable to True to ensure while loop runs at least once
cont = True
while cont:
	add_to_basket = input("Select an item to add to your basket: ").lower() # Give user option to add something to the basket
# If the user the item selects is in the list above, add it to the basket
	for x in list:
		if add_to_basket == x:
			currentBasket.add_item(eval(add_to_basket))
# If the item is not in list, return an erorr.		
	if add_to_basket not in list:
		print("Sorry! We do not have this item in stock.")
# If the length of the string is 0 then the user has not added any items to the basket and it is empty.		
	if len(currentBasket.get_items()) == 0:
		print("Your basket is empty.")
	else:
		print(currentBasket) # If the length of the string is not 0 then there is something in the basket. Print this to allow the user to see it.
# After adding something to the basket or realising it is out of stock, ask the user if they want to add anything else.
	choice = input("Would you like to add something else? ")
	if choice.lower() == "no":
		cont = False # If the answer is no, set cont to False and end while loop. Else, cont will remain as true and loop will restart.
		print(currentBasket)
		print("Total price: £" + str(currentBasket.get_price())) # Finally, return the overall price of the basket by adding up price of all items.
		
# Remove item from basket
remove = input("Would you like to remove an item? ").lower()
remove_item = True
while remove_item:
	if remove == "yes":
		item = input("Select an item to remove: ")
		if eval(item) in currentBasket.get_items():
			currentBasket.remove_item(eval(item))
			choice = input("Remove something else? ").lower()
	print(currentBasket)
	print("Total price: £" + str(currentBasket.get_price()))
	if choice == "no":
		remove_item = False
		print(currentBasket)
		print("Total price: £" + str(currentBasket.get_price()))

# Price is 0, therefore no items left in basket		
if currentBasket.get_price() == 0:
    print("Your basket is empty!")