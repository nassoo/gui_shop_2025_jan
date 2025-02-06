import json
import os
import tkinter as tk
from helpers import clean_screen
from canvas import app
from PIL import Image, ImageTk

base_dir = os.path.dirname(__name__)

def update_current_user(username, p_id):
    with open("db/users.txt", "r+", newline="\n") as f:
        users = [json.loads(u.strip()) for u in f]
        for user in users:
            if user["username"] == username:
                user["products"].append(p_id)
                f.seek(0)
                f.truncate()
                f.writelines([json.dumps(u) + "\n" for u in users])
                return

def purchase_product(p_id):
    with open("db/products.txt", "r+") as f:
        products = [json.loads(p.strip()) for p in f]
        for p in products:
            if p["id"] == p_id:
                p["count"] -= 1
                f.seek(0)
                f.truncate()
                f.writelines([json.dumps(pr) + "\n" for pr in products])
                return

def buy_product(p_id):
    clean_screen()

    with open("db/current_user.txt") as file:
        username = file.read()

    if username:
        update_current_user(username, p_id)
        purchase_product(p_id)

    render_products_screen()

def render_products_screen():
    clean_screen()


    with open("db/products.txt") as file:
        products = [json.loads(p.strip()) for p in file]
        products = [p for p in products if p["count"] > 0]
        products_per_line = 6
        rows_per_product = len(products[0])
        for i, p in enumerate(products):
            row = i // products_per_line * rows_per_product
            column = i % products_per_line

            tk.Label(app, text=p["name"]).grid(row=row, column=column)

            img = Image.open(os.path.join(base_dir, "db/images", p["img_path"])).resize((100, 100))
            photo_image = ImageTk.PhotoImage(img)
            image_label = tk.Label(image=photo_image)
            image_label.image = photo_image
            image_label.grid(row=row+1, column=column)

            tk.Label(app, text=p["count"]).grid(row=row+2, column=column)

            tk.Button(app,
                      text=f"Buy {p['id']}",
                      command=lambda pr=p['id']: buy_product(pr)
                      ).grid(row=row+3, column=column)

