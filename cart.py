
# SHOPPING CART

# Each item will have all of these parameters in bg.sql
class Item(object): 
	def __init__(self, name, description, productID, price, quantity, cat):
		self._name = name
		self._description = description
		self._productID = productID
		self._price = price
		self._quantity = quantity
		self._cat = cat

	def __str__(self):
		return (self._name)
		
	def __repr__(self):
		return (str(self._productID))

	# Mutator methods for Item class
	def set_description(self, description):
		self._description = description
		
	def set_price(self, price):
		self._price = price
		
	def set_quantity(self, quantity):
		self._quantity = quantity
		
	def set_vat(self, cat):
		self._cat = cat
		
	# Accessor methods for Item class
	def get_name(self):
		return self._name
				
	def get_description(self):
		return self._description
				
	def get_productID(self):
		return self._productID
		
	def get_price(self):
		return self._price
		
	def get_quantity(self):
		return self._quantity 
				
	def get_cat(self):
		return self._cat
		
	def get_total_item_price(self): 
		return self._price * self._quantity
	

		
class Basket(object):
	def __init__(self):
		self._items = []
		self._price = 0 
		self._count = 0
		
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
		if item in self._items:
			item.set_quantity(item.get_quantity()+1)
			self._price += item.get_price()
			self._count += 1
		else:
			self._items.append(item) # Add item to the current list of items 
			self._price += item.get_price() # Add price of current item to the price of items already added 
			self._count += 1 # Add to the total number of items held within the cart
		
	def remove_item(self, item):
		for x in self._items:
			if item == x.get_productID:
				self._items.remove(item)
				self._price -= item.get_price()
				self._count -= 1
		return(currentBasket)



currentBasket = Basket()
print("New Basket Created")


@app.route('/searchresults', methods=['GET','POST'])
def addToCart(PID,WID):
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
		cart = session[currentBasket]
	else:
		user = ['','','','','','','']
		cart = []
	try:
		# itemQuantity = pg.getItemQuantity(PID,WID)
		itemInfo = pg.getItemInfo(PID)
		newItem = Item(itemInfo[3],itemInfo[4],itemInfo[0],float(itemInfo[1]),1,itemInfo[2])
		currentBasket.add_item(newItem)
		# REMOVE QUANTITY FROM WID
		# search=request.form['search']
		# print("***Search Term: " , search)
	except:
		print("Error putting item in cart")
	return render_template('searchresults.html', user=user, cart=cart)
	
	
def listCartItems(cart):
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
		cart = session[currentBasket]
	else:
		user = ['','','','','','','']
		cart = []
	try:
		i = 1
		for item in currentBasket.get_items():
			print(i,item.get_productID(),item.get_quantity(),item.get_price(),round(item.get_total_item_price(),2))
			cart.append(i,item.get_productID(),item.get_quantity(),item.get_price(),round(item.get_total_item_price(),2))
			i+=1
		print("Total: $$$", round(currentBasket.get_price(),2))
		return cart
	except:
		print("Cart is empty?")
		return cart
	# return render_template('searchresults.html', user=user, cart=cart)
	
		
addToCart(841,4)