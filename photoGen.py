import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image,ImageTk
from pathlib import Path

class PhotoConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Converter - SK")

        self.photo_path = tk.StringVar()
        self.output_path = tk.StringVar()

        # Images to display
        self.uploaded_image_label = tk.Label(self.root)
        self.result_image_label = tk.Label(self.root)

        # Create and place widgets
        self.create_widgets()

    def create_widgets(self):
        # File Upload
        tk.Label(self.root, text="Select Photo:").grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.photo_path, width=40, state="disabled").grid(row=0, column=1, padx=10, pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_photo).grid(row=0, column=2, padx=10, pady=5)
    
        tk.Label(self.root, text="Uploaded Image:").grid(row=1, column=0, padx=10, pady=5)
        self.uploaded_image_label.grid(row=1, column=1, padx=10, pady=5)


        # Output Path
        tk.Label(self.root, text="Output Path:").grid(row=2, column=0, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.output_path, width=40, state="disabled").grid(row=2, column=1, padx=10, pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_output_path).grid(row=2, column=2, padx=10, pady=5)

        # Convert Button
        tk.Button(self.root, text="Convert", command=self.convert_photo).grid(row=3, column=1, pady=10)

        
        # Display result image
        tk.Label(self.root, text="Resulting Canvas:").grid(row=4, column=0, padx=10, pady=5)
        self.result_image_label.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Developed by Sanjay Krishna ").grid(row=6, column=2, padx=5, pady=5)

    def browse_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.photo_path.set(file_path)
            self.display_uploaded_image(file_path)

    def browse_output_path(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_path.set(folder_path)

    def convert_photo(self):
        photo_path = self.photo_path.get()
        output_path = self.output_path.get()

        if not photo_path or not output_path:
            messagebox.showerror("Error", "Please select a photo and an output path.")
            return

        try:
            # Load the photo
            img = Image.open(photo_path)
            file_name =  Path(photo_path).stem
            # Set the desired output size and ratio
            output_width = 6 * 300  # 4 inches at 300 DPI
            output_height = 4 * 300  # 6 inches at 300 DPI
            output_ratio = output_width / output_height
            padding_x = 20
            padding_y = 20
            canvas_padding_x = 30
            canvas_padding_y = 30
            # Calculate the dimensions for each copy
            copy_width =( output_width / 4 ) - 40 # Two copies side by side
            copy_height = copy_width / (4 / 5)  # Maintain the 4:5 ratio

            # Create a new blank canvas
            canvas = Image.new('RGB', (output_width, output_height), 'white')

            # Paste 8 copies onto the canvas in a 2x4 grid
            for i in range(2):
                for j in range(4):
                    x_offset = j * (copy_width + padding_x) +canvas_padding_x
                    y_offset = i * (copy_height + padding_y) +canvas_padding_y
                    canvas.paste(img.resize((int(copy_width), int(copy_height))), (int(x_offset), int(y_offset)))

            # Save the result to the output path
            result_path = f"{output_path}/{file_name}_converted.jpg";
            canvas.save(result_path)
            self.display_result_image(result_path)
            messagebox.showinfo("Success", "Conversion complete.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    def display_uploaded_image(self, image_path):
        img = Image.open(image_path)
        img.thumbnail((200, 200))
        photo = ImageTk.PhotoImage(img)
        self.uploaded_image_label.config(image=photo)
        self.uploaded_image_label.image = photo  # Keep a reference to avoid garbage collection issues

    def display_result_image(self, image_path):
        img = Image.open(image_path)
        img.thumbnail((200, 200))
        photo = ImageTk.PhotoImage(img)
        self.result_image_label.config(image=photo)
        self.result_image_label.image = photo  

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoConverterApp(root)
    root.mainloop()
