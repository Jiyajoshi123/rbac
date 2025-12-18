import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "users.csv")

# ---------- INIT USERS FILE ----------
def init_users():
    if not os.path.exists(USERS_FILE):
        pd.DataFrame(
            columns=["username", "password", "role"]
        ).to_csv(USERS_FILE, index=False)

init_users()

def load_users():
    return pd.read_csv(USERS_FILE, dtype=str, keep_default_na=False)

# ---------- CREATE DEFAULT ADMIN ----------
def create_default_admin():
    users = load_users()
    if "admin" not in users["username"].values:
        admin = pd.DataFrame(
            [["admin", "admin123", "Admin"]],
            columns=["username", "password", "role"]
        )
        users = pd.concat([users, admin], ignore_index=True)
        users.to_csv(USERS_FILE, index=False)

create_default_admin()

# ---------- SIGNUP ----------
def signup_user(username, password, role):
    username = username.strip()
    password = password.strip()

    if role == "Admin":
        return False, "Admin signup is disabled"

    if not username or not password:
        return False, "Fields cannot be empty"

    users = load_users()

    if username in users["username"].values:
        return False, "User already exists"

    users.loc[len(users)] = [username, password, role]
    users.to_csv(USERS_FILE, index=False)

    return True, "Signup successful"

# ---------- LOGIN ----------
def authenticate_user(username, password, role):
    users = load_users()

    user = users[
        (users["username"].str.strip() == username.strip()) &
        (users["password"].str.strip() == password.strip()) &
        (users["role"] == role)
    ]

    return not user.empty
