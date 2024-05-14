from addproduct.models import Product
from viewproducts.models import CartItem

class Cart():
    def __init__(self, request):
        self.session = request.session

        # Retrieve the cart from the session
        cart = self.session.get('session_key')
        self.cart = self.session.get('cart', {})

        # If cart doesn't exist in the session, create an empty one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Make sure cart is available in all pages
        self.cart = cart

    def add(self, product, quantity):
        product_id = product.product_id  # Use product.product_id directly as it's an integer
        cartItem_qty = int(quantity)

        # Check if the product is already in the cart
        if product_id in self.cart:
            pass  # Handle logic for existing product in the cart if needed
        else:
            self.cart[product_id] = cartItem_qty

        # Save the session to persist the changes
        self.session.modified = True

    def cart_total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(product_id__in=product_ids)
        quantities = self.cart
        cart_amt = 0

        for key, value in quantities.items():
            key = str(key)
            for product in products: 
                if str(product.product_id) == key:
                    cart_amt = cart_amt + (product.product_price * value)

        return cart_amt

    def cartItem_subtotal(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(product_id__in=product_ids)
        quantities = self.cart
        cartItem_subtotal_dict = {}

        for key, value in quantities.items():
            key = str(key)
            for product in products:
                if str(product.product_id) == key:
                    product_qty = value
                    product_price = product.product_price
                    subtotal = product_qty * product_price

                    # Store the subtotal in the dictionary with the product_id as the key
                    cartItem_subtotal_dict[key] = {
                        'product_qty': product_qty,
                        'product_price': product_price,
                        'subtotal': subtotal,
                    }

        return cartItem_subtotal_dict


    #get length
    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        # get ids from cart
        product_ids = self.cart.keys()
        
        # use ids to lookup products in db models
        products = Product.objects.filter(product_id__in=product_ids)
        return products

    def get_quants(self):
        quantities = {}
        for product_id, data in self.cart.items():
            if isinstance(data, int):
                quantities[product_id] = data
            else:
                quantities[product_id] = data.get('qty', 0)
        return quantities

    def update(self, product_id, quantity):
        product_id = str(product_id)
        cartItem_qty = int(quantity)
        
        # get cart
        ourcart = self.cart
        # update dictionary/cart
        ourcart[product_id] = cartItem_qty
        
        self.session.modified = True
        
        # return the updated cart if needed
        return ourcart
    
    def delete(self, product):
        product_id = str(product)
        #delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]
            
        self.session.modified = True