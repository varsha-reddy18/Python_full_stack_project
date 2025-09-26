import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

# ---------------- Custom CSS ----------------
st.markdown(f"""
<style>
/* Full-page background image */
.stApp {{
    background: url("file:///{'Screenshot 2025-09-25 212504.png'}") no-repeat center center fixed;
    background-size: cover;
}}

/* Force full width */
.block-container {{
    max-width: 100% !important;
    padding-left: 2rem;
    padding-right: 2rem;
    background-color: rgba(255, 255, 255, 0.85);
    border-radius: 10px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
}}

/* Title bar */
.sticky-title {{
    position: sticky;
    top: 0;
    z-index: 999;
    background-color: rgba(255, 255, 255, 0.95);
    padding: 20px 0;
    text-align: center;
    font-size: 40px;
    font-family: 'Segoe UI', sans-serif;
    font-weight: bold;
    color: #FF5722;
    border-bottom: 3px solid #FF5722;
    width: 100%;
    display: block;
    box-shadow: 0px 2px 5px rgba(0,0,0,0.2);
}}

/* Sidebar roles */
.left-roles .stRadio > div {{
    background-color: #fff;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
}}
.left-roles label {{
    font-size: 18px !important;
    font-weight: bold !important;
    color: #FF5722 !important;
    margin-left: 5px !important;
}}

/* Form cards */
.form-card {{
    background-color: rgba(255,255,255,0.95);
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    margin-bottom: 25px;
}}

/* Section headers */
h2, h3 {{
    color: #FF7043;
    font-family: 'Segoe UI', sans-serif;
    margin-top: 15px;
}}

/* Buttons */
.stButton>button {{
    background: linear-gradient(90deg, #FF5722, #FF7043);
    color: white;
    font-weight: bold;
    font-size: 16px;
    border-radius: 8px;
    padding: 10px 22px;
    border: none;
    cursor: pointer;
    transition: 0.3s;
}}
.stButton>button:hover {{
    background: linear-gradient(90deg, #FF7043, #FF8A65);
}}

/* Donation cards */
.donation-card {{
    background: linear-gradient(120deg, #FFD54F, #FFB300);
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 12px;
    color: #000;
    font-weight: bold;
    box-shadow: 0px 3px 8px rgba(0,0,0,0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
</style>
""", unsafe_allow_html=True)

# ---------------- Title ----------------
st.markdown('<div class="sticky-title">🍲 Food Donation and Surplus Management System</div>', unsafe_allow_html=True)

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
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        st.header("👤 Donor Panel")
        with st.form("donor_form"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Register as Donor")
            if submit:
                result = register_user(name, email, password, "donor")
                st.success(result.get("Message", "User registered!"))
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        st.subheader("🍱 Add Donation")
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
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- NGO Panel ----------------
elif role == "NGO":
    with col_right:
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        st.header("🏢 NGO Panel")
        with st.form("ngo_form"):
            ngo_name = st.text_input("NGO Name")
            ngo_email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Register as NGO")
            if submit:
                result = register_user(ngo_name, ngo_email, password, "ngo")
                st.success(result.get("Message", "NGO registered!"))
        st.markdown('</div>', unsafe_allow_html=True)

        st.subheader("📦 Available Donations")
        donations = get_donations()
        if isinstance(donations, list) and donations:
            for d in donations:
                if d.get("status") == "available":
                    col1, col2 = st.columns([3,1])
                    with col1:
                        st.markdown(f"""
                        <div class="donation-card">
                            🍛 {d['food_item']} - {d['quantity']} units (Expiry: {d['expiry_date']})
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
