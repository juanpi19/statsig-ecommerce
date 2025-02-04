import streamlit as st
from PIL import Image
from statsig import statsig
from statsig.statsig_user import StatsigUser
from statsig.statsig_event import StatsigEvent
import uuid 

secret_key = st.secrets["secret_key"]

def initialize_statsig(api_key: str):
    statsig.initialize(api_key)  

def check_experiment(user_id, experiment_name: str):
    return statsig.get_experiment(user_id, experiment_name)


def render(user):
    # Page config
    st.set_page_config(page_title="Simple E-commerce", layout="wide")

    # Initialize session state for cart if it doesn't exist
    if 'cart' not in st.session_state:
        st.session_state.cart = {}

    # Sample product data with placeholder values
    products = [
        {
            "name": "Shoes",
            "price": 10.99,
            "description": "The best shoes",
            "image": "docs/pictures/shoes.jpg"
        },
        {
            "name": "Skateboard",
            "price": 20.99,
            "description": "The best skateboard",
            "image": "docs/pictures/skateboard.jpg"
        },
        {
            "name": "Hat",
            "price": 30.99,
            "description": "The best hat",
            "image": "docs/pictures/hat.jpg"
        },
            {
            "name": "Soccer Ball",
            "price": 10.99,
            "description": "The best ball",
            "image": "docs/pictures/soccer.jpg"
        },
        {
            "name": "Book",
            "price": 20.99,
            "description": "Books for a month",
            "image": "docs/pictures/book.jpg"
        },
        {
            "name": "Bottle",
            "price": 30.99,
            "description": "Minimal water bottle",
            "image": "docs/pictures/water.jpg"
        }
    ]

    # Header
    st.title("E-commerce Store")

    # Display cart status in sidebar
    st.sidebar.header("Shopping Cart")
    cart_total = sum(st.session_state.cart.values())
    st.sidebar.write(f"Items in cart: {cart_total}")

    # Display products in a grid
    cols = st.columns(3)

    for idx, product in enumerate(products):
        with cols[idx % 3]:

            # Open the image using PIL
            img = Image.open(product['image'])
            img = img.resize((500, 500))

            st.image(img, caption=product['name'])
            st.write(f"${product['price']:.2f}")
            st.write(product["description"])
            
            # Add to cart button
            text_to_show = statsig.get_experiment(user, "cta_button_variations").get("text_to_show", False)
            if st.button(f"{text_to_show}", key=f"add_{idx}"):
                statsig.log_event(StatsigEvent(user, "button_clicked")) # logging experiment data
                if product["name"] in st.session_state.cart:
                    st.session_state.cart[product["name"]] += 1
                else:
                    st.session_state.cart[product["name"]] = 1

    # Display cart contents in sidebar
    if st.session_state.cart:
        st.sidebar.write("---")
        st.sidebar.write("Cart Contents:")
        total_price = 0
        for product_name, quantity in st.session_state.cart.items():
            product_info = next((p for p in products if p["name"] == product_name), None)
            if product_info:
                price = product_info["price"] * quantity
                total_price += price
                st.sidebar.write(f"{product_name} (x{quantity}): ${price:.2f}")
        st.sidebar.write("---")
        st.sidebar.write(f"Total: ${total_price:.2f}")
        
        if st.sidebar.button("Checkout"):
            statsig.log_event(StatsigEvent(user, "user revenue", value=total_price)) #metadata={"product_id": product_id}
            st.sidebar.success("Thank you for your purchase!")
            st.session_state.cart = {}


if "user_id" not in st.session_state:
    st.session_state["user_id"] = str(uuid.uuid4())

def main():
    user_id = StatsigUser(st.session_state["user_id"])
    initialize_statsig(api_key=secret_key)
    render(user_id)


if __name__ == '__main__':
    main()

