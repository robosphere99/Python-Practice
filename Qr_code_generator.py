import qrcode

# Data you want to encode
data = "Anil is your father man!"

# Create QR code instance
qr = qrcode.QRCode(
    version=1,  # Controls the size of the QR code (1 is the smallest)
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # Less error correction (7%)
    box_size=10,  # Size of each box where dots are placed
    border=4,  # Thickness of the border
)

# Add the data to the QR code
qr.add_data(data)
qr.make(fit=True)

# Create an image of the QR code
qr_image = qr.make_image(fill='black', back_color='white')

# Save the generated QR code as an image file
qr_image.save("qrcode.png")

print("QR code generated and saved as 'qrcode.png'.")
