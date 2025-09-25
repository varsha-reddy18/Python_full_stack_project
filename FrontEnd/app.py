import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

# ---------------- Custom CSS ----------------
st.markdown("""
<style>
/* Page background */
body {
    background-color: #fff5e6;
}

/* Sticky title at top */
.sticky-title {
    position: sticky;
    top: 0;
    z-index: 999;
    background-color: #fff5e6;
    padding: 15px 0;
    text-align: center;
    font-size: 38px;
    font-family: 'Helvetica', sans-serif;
    font-weight: bold;
    color: #FF6347;
    border-bottom: 2px solid #FF6347;
}

/* Roles container styling */
.left-roles .stRadio > div {
    background-color: #ffe6e6 !important;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 3px 3px 10px rgba(0,0,0,0.1);
}

/* Radio buttons text style */
.left-roles label {
    font-size: 22px !important;
    font-weight: bold !important;
    color: #FF6347 !important;
    margin-left: 8px !important;
}

/* Hover effect for options */
.left-roles div[data-baseweb="radio"] > div:hover {
    background-color: #ffd9d9 !important;
    cursor: pointer;
}

/* Form containers */
.stForm {
    background-color: #e6f7ff;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 4px 4px 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

/* Subheaders */
h2 {
    color: #FF8C00;
    font-family: 'Arial', sans-serif;
}

/* Buttons */
.stButton>button {
    background-color: #4682B4;
    color: white;
    font-weight: bold;
    font-size: 18px;
    border-radius: 8px;
    padding: 8px 20px;
    cursor: pointer;
}

/* Donation cards */
.donation-card {
    background: linear-gradient(120deg, #FFD700, #FFA500);
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 15px;
    color: #000;
    font-weight: bold;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Sticky Title ----------------
st.markdown('<div class="sticky-title">🍲Food Donation and Surplus Management System</div>', unsafe_allow_html=True)

# ---------------- Layout ----------------
col_left, col_right = st.columns([1, 3])

with col_left:
    st.markdown('<div class="left-roles">', unsafe_allow_html=True)
    role = st.radio("I am a:", ["Donor", "NGO"])
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Helpers ----------------
def safe_json(response):
    try:
        return response.json()
    except Exception:
        return {"Success": False, "Message": response.text}

def get_users():
    try:
        response = requests.get(f"{API_URL}/users")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error fetching users: {e}")
        return []

def register_user(name, email, password, role):
    response = requests.post(f"{API_URL}/users", json={
        "name": name,
        "email": email,
        "password": password,
        "role": role,
    })
    return safe_json(response)

def add_donation(user_id, item, quantity, expiry):
    response = requests.post(f"{API_URL}/donations", json={
        "user_id": user_id,
        "food_item": item,
        "quantity": quantity,
        "expiry_date": expiry,
    })
    return safe_json(response)

def get_donations():
    response = requests.get(f"{API_URL}/donations")
    if response.status_code == 200:
        return response.json()
    return []

# ---------------- Donor Panel ----------------
if role == "Donor":
    with col_right:
        st.header("Donor Panel")
        with st.form("donor_form"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Register as Donor")
            if submit:
                result = register_user(name, email, password, "donor")
                st.success(result.get("Message", "User registered!"))

        st.subheader("Add Donation")
        users = get_users()
        donor_ids = [u.get("user_id") for u in users if u.get("role") == "donor"]

        if donor_ids:
            donor_id = donor_ids[-1]
            item = st.text_input("Item")
            quantity = st.number_input("Quantity", min_value=1, step=1)
            expiry = st.date_input("Expiry Date")
            if st.button("Add Donation"):
                result = add_donation(donor_id, item, str(quantity), str(expiry))
                st.success(result.get("Message", "Donation added!"))
        else:
            st.warning("Register as a donor first!")

# ---------------- NGO Panel ----------------
elif role == "NGO":
    with col_right:
        st.header("NGO Panel")
        with st.form("ngo_form"):
            ngo_name = st.text_input("NGO Name")
            ngo_email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Register as NGO")
            if submit:
                result = register_user(ngo_name, ngo_email, password, "ngo")
                st.success(result.get("Message", "NGO registered!"))

        st.subheader("Available Donations")
        donations = get_donations()
        if isinstance(donations, list) and donations:
            for d in donations:
                if d.get("status") == "available":
                    col1, col2 = st.columns([3,1])
                    with col1:
                        st.markdown(f"""
                        <div class="donation-card">
                            🍱 {d['food_item']} - {d['quantity']} units (Expiry: {d['expiry_date']})
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        if st.button("Select", key=f"req{d['donation_id']}"):
                            response = requests.post(
                                f"{API_URL}/requests",
                                json={"donation_id": d["donation_id"], "ngo_email": ngo_email}
                            )
                            if response.status_code == 200:
                                st.success("Item requested successfully!")
                            else:
                                st.error(f"Could not request this item: {response.text}")
        else:
            st.info("No available items.")
