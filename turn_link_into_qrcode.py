import os
import qrcode
from urllib.parse import urlparse
import re

input_file = input("please enter name of your link file: ").strip()
if not os.path.isfile(input_file):
    print(f"filename '{input_file}' is invalid.")
    exit(1)

try:
    box_size = int(input("size of QRCode squares(1 to 100): ").strip())
    if box_size < 1 or box_size > 100:
        raise ValueError()
except ValueError:
    print("invalid size! please enter a number between 1 and 100.")
    exit(1)

try:
    dpi = int(input("please enter DPI(example 300): ").strip())
    if dpi < 50 or dpi > 1200:
        raise ValueError()
except ValueError:
    print("invalid value! please enter a number between 50 and 1200.")
    exit(1)

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

def make_safe_filename(url):
    parsed = urlparse(url)
    path = parsed.path.strip("/").replace("/", "_") or "home"
    netloc = parsed.netloc.replace(".", "_")
    filename = f"{netloc}_{path}"
    filename = re.sub(r'[^a-zA-Z0-9_\-]', '', filename)
    return filename[:50]

with open(input_file, "r") as f:
    for line in f:
        url = line.strip()
        if not url:
            continue

        filename = make_safe_filename(url)

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=box_size,
            border=4,
        )

        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        qr_path = os.path.join(output_dir, f"{filename}.png")
        img.save(qr_path, dpi=(dpi, dpi))

        print(f"file {qr_path} with DPI={dpi} is created.")

print("\n🎉 all QR Codes have been created successfully.")
