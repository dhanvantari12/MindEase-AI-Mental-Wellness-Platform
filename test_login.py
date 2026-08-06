from features.auth.services import login_user

success, message, user = login_user(
    email="riza@gmail.com",
    password="Riza@1234"
)

print("Success:", success)
print("Message:", message)
print("User:", user)