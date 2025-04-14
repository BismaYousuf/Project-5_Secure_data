# 🔐 Secure Vault App

A simple and secure Streamlit-based web application that allows users to **create accounts**, **log in**, and **store/retrieve sensitive data** protected by passkeys. Ideal for securely storing notes or small text-based secrets.

---

## 🚀 Features

- 🆕 **User Registration & Login**  
  Create new accounts or log in with encrypted password protection.

- 🔐 **Passkey-Based Data Encryption**  
  Store and retrieve data using a custom passkey that hashes your entries for extra security.

- 🧾 **Per-User Data Storage**  
  Each user can store multiple secure notes, accessible only with the correct passkey.

- 🚪 **Session Handling & Logout**  
  Safe logout and session control using `st.session_state`.

- ⚠️ **Security Lockout**  
  After 3 failed login or retrieval attempts, the user is locked out or logged out for safety.

---

## 🛠️ Installation

1. **Clone the Repository**

```bash
git clone https://github.com/your-username/secure-vault-app.git
cd secure-vault-app
