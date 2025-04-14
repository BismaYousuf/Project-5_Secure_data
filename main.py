import streamlit as st
import hashlib
from cryptography.fernet import Fernet

# Initialize session state variables
if "page" not in st.session_state:
    st.session_state.page = "login"
if "wrong_attempt" not in st.session_state:
    st.session_state.wrong_attempt = 0
if "data_store" not in st.session_state:
    st.session_state.data_store = []
if "user_secure_data" not in st.session_state:
    st.session_state.user_secure_data = []
if "current_user" not in st.session_state:
    st.session_state.current_user = None

# Encryption key generation if not already present
if 'key' not in st.session_state:
    st.session_state.key = Fernet.generate_key()
cipher = Fernet(st.session_state.key)

# Function to handle login page
def login_page():
    st.markdown("## 🔐 Welcome to Secure Vault App")
    st.markdown("#### Please login or create an account to continue")

    with st.form(key="login_form", clear_on_submit=False):
        user_name = st.text_input("👤 Username", key="username")
        user_pass = st.text_input("🔑 Password", key="password", type="password")

        col1, col2 = st.columns(2)
        with col1:
            new_account = st.form_submit_button("🆕 Create Account")
        with col2:
            old_account = st.form_submit_button("✅ Login")

    if new_account:
        if not user_name or not user_pass:
            st.warning("🚫 Please enter both username and password")
        elif any(user['username'] == user_name for user in st.session_state.data_store):
            st.error("⚠️ Username already exists. Please login.")
        else:
            encrypted_password = cipher.encrypt(user_pass.encode())
            st.session_state.data_store.append({"username": user_name, "password": encrypted_password})
            st.success("🎉 Account created successfully!")
            st.session_state.current_user = user_name
            st.session_state.page = "home"
            st.rerun()

    if old_account:
        if not user_name or not user_pass:
            st.warning("🚫 Please enter both username and password")
        elif any(user['username'] == user_name for user in st.session_state.data_store):
            user = next(user for user in st.session_state.data_store if user['username'] == user_name)
            try:
                decrypted_password = cipher.decrypt(user['password']).decode()
                if decrypted_password == user_pass:
                    st.success("🔓 Successfully logged in!")
                    st.session_state.current_user = user_name
                    st.session_state.page = "home"
                    st.session_state.wrong_attempt = 0
                    st.rerun()
                else:
                    st.error("❌ Incorrect password.")
                    st.session_state.wrong_attempt += 1
                    if st.session_state.wrong_attempt >= 3:
                        st.error("⛔ Too many failed attempts. Please try again later.")
                        st.session_state.wrong_attempt = 0
            except Exception:
                st.error("⚠️ An error occurred during login.")
        else:
            st.error("❌ Username does not exist.")

# Function to handle home page
def home_page():
    st.markdown(f"## 🔒 Welcome, **{st.session_state.current_user}**")

    # Sidebar
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        st.info(f"👤 Logged in as: `{st.session_state.current_user}`")
        if st.button("🚪 Logout"):
            st.session_state.page = "login"
            st.session_state.current_user = None
            st.rerun()

    st.divider()

    # Data Storage Section
    st.markdown("### 📝 Store Secure Data")
    with st.form(key="store_data_form"):
        user_main_data = st.text_area("🔐 Enter your data")
        pass_key = st.text_input("🧪 Create a passkey", type="password")
        store = st.form_submit_button("💾 Store Data")

    if store:
        if not user_main_data or not pass_key:
            st.warning("🚫 Please enter both data and a passkey")
        else:
            hash_code = hashlib.sha256(pass_key.encode()).hexdigest()
            st.session_state.user_secure_data.append({
                "username": st.session_state.current_user,
                "key": hash_code,
                "data": user_main_data
            })
            st.success("✅ Data stored securely!")

    st.divider()

    # Data Retrieval Section
    st.markdown("### 🔎 Retrieve Stored Data")

    user_data = [
        item for item in st.session_state.user_secure_data 
        if item["username"] == st.session_state.current_user
    ]

    if not user_data:
        st.info("📭 You haven't stored any data yet.")
    else:
        st.write(f"📂 You have `{len(user_data)}` stored data entries.")
        with st.form(key="retrieve_form"):
            retrieve_key = st.text_input("🔐 Enter your passkey", type="password")
            retrieve = st.form_submit_button("📬 Retrieve Data")

        if retrieve:
            if not retrieve_key:
                st.warning("🚫 Please enter your passkey")
            else:
                hash_code = hashlib.sha256(retrieve_key.encode()).hexdigest()
                matching_data = [item["data"] for item in user_data if item["key"] == hash_code]

                if matching_data:
                    st.success("✅ Passkey verified!")
                    for i, data in enumerate(matching_data):
                        st.text_area(f"🔏 Data Entry {i+1}", value=data, height=100, key=f"data_{i}")
                else:
                    st.error("❌ Incorrect passkey.")
                    st.session_state.wrong_attempt += 1
                    if st.session_state.wrong_attempt >= 3:
                        st.error("⛔ Too many failed attempts. Logging out for security.")
                        st.session_state.page = "login"
                        st.session_state.current_user = None
                        st.session_state.wrong_attempt = 0
                        st.rerun()

# Main app logic
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "home":
    home_page()

# Optional Debug Section
with st.expander("🐞 Debug Info"):
    st.json({
        "Current Page": st.session_state.page,
        "Current User": st.session_state.current_user,
        "Wrong Attempts": st.session_state.wrong_attempt,
        "Registered Users": len(st.session_state.data_store),
        "Stored Data Entries": len(st.session_state.user_secure_data)
    })
