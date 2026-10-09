# generate_robot_images.py
# Downloads and encodes the exact high-res 3D AI Robot for Login & Signup
import os
import base64
import urllib.request

# 1. Create required folders
os.makedirs("assets", exist_ok=True)
os.makedirs("auth", exist_ok=True)

print("Downloading high-resolution 3D AI Robot images...")

# High-resolution 3D humanoid AI robot on laptop
LOGIN_URL = "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800&q=80"
SIGNUP_URL = "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=800&q=80"

headers = {"User-Agent": "Mozilla/5.0"}

# Download Login robot
req1 = urllib.request.Request(LOGIN_URL, headers=headers)
with urllib.request.urlopen(req1) as resp:
    login_bytes = resp.read()

# Download Signup robot
req2 = urllib.request.Request(SIGNUP_URL, headers=headers)
with urllib.request.urlopen(req2) as resp:
    signup_bytes = resp.read()

# 2. Save physical images in assets/
with open("assets/login_robot.jpg", "wb") as f:
    f.write(login_bytes)

with open("assets/signup_robot.jpg", "wb") as f:
    f.write(signup_bytes)

# 3. Create Base64 data module for Streamlit Cloud (avoids broken image 404s)
login_b64 = base64.b64encode(login_bytes).decode("utf-8")
signup_b64 = base64.b64encode(signup_bytes).decode("utf-8")

with open("auth/images_b64.py", "w") as f:
    f.write(f'LOGIN_ROBOT_B64 = "{login_b64}"\nSIGNUP_ROBOT_B64 = "{signup_b64}"\n')

print(" SUCCESS! Created:")
print("  - assets/login_robot.jpg")
print("  - assets/signup_robot.jpg")
print("  - auth/images_b64.py")