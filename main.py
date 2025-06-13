import tkinter as tk
from tkinter import filedialog, messagebox
import os
import re
import shutil
import json
from pathlib import Path

class ObsidianHugoConverter:
    def __init__(self):
        self.config_file = 'converter_config.json'
        self.config = self.load_config()
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Obsidian to Hugo Converter")
        self.root.geometry("600x400")
        
        # Create and pack widgets
        self.create_widgets()
        
        # Load saved paths if they exist
        self.load_saved_paths()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {
            'obsidian_path': '',
            'hugo_path': ''
        }

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f)

    def create_widgets(self):
        # Obsidian path selection
        tk.Label(self.root, text="Obsidian Vault Path:").pack(pady=5)
        self.obsidian_path_var = tk.StringVar()
        tk.Entry(self.root, textvariable=self.obsidian_path_var, width=50).pack()
        tk.Button(self.root, text="Browse", command=self.select_obsidian_path).pack(pady=5)

        # Hugo path selection
        tk.Label(self.root, text="Hugo Site Path:").pack(pady=5)
        self.hugo_path_var = tk.StringVar()
        tk.Entry(self.root, textvariable=self.hugo_path_var, width=50).pack()
        tk.Button(self.root, text="Browse", command=self.select_hugo_path).pack(pady=5)

        # Convert button
        tk.Button(self.root, text="Convert", command=self.convert_files, bg='green', fg='white').pack(pady=20)

        # Status text
        self.status_text = tk.Text(self.root, height=10, width=50)
        self.status_text.pack(pady=10)

    def load_saved_paths(self):
        self.obsidian_path_var.set(self.config['obsidian_path'])
        self.hugo_path_var.set(self.config['hugo_path'])

    def select_obsidian_path(self):
        path = filedialog.askdirectory(title="Select Obsidian Vault Directory")
        if path:
            self.obsidian_path_var.set(path)
            self.config['obsidian_path'] = path
            self.save_config()

    def select_hugo_path(self):
        path = filedialog.askdirectory(title="Select Hugo Site Directory")
        if path:
            self.hugo_path_var.set(path)
            self.config['hugo_path'] = path
            self.save_config()

    def find_image_file(self, image_name, obsidian_path):
        """Recursively search for image file in obsidian vault"""
        for root, _, files in os.walk(obsidian_path):
            if image_name in files:
                return os.path.join(root, image_name)
        return None

    def convert_link_syntax(self, content):
        # Convert regular markdown image syntax
        def replace_image(match):
            alt_text = match.group(1)
            image_path = match.group(2)
            image_name = os.path.basename(image_path)
            return f'![{alt_text}](/images/{image_name})'

        # Handle standard markdown image syntax: ![alt text](image.png)
        content = re.sub(r'!\[(.*?)\]\(([^)]+)\)', replace_image, content)

        # Convert wiki links
        content = re.sub(r'\[\[([^\]|]*?)\]\]', r'[\1](\1)', content)
        content = re.sub(r'\[\[([^\]|]*?)\|([^\]]*?)\]\]', r'[\2](\1)', content)

        return content

    def copy_images(self, content, obsidian_path, hugo_path):
        """Copy images from Obsidian to Hugo static folder"""
        # Create static/images directory if it doesn't exist
        hugo_images_path = os.path.join(hugo_path, 'static', 'images')
        os.makedirs(hugo_images_path, exist_ok=True)

        # Find all image references
        image_matches = re.findall(r'!\[.*?\]\(([^)]+)\)', content)
        
        # Process found images
        for image_path in image_matches:
            # Get just the filename without any potential path
            image_filename = os.path.basename(image_path)
            
            # First try direct path
            source_path = os.path.join(obsidian_path, image_path)
            if not os.path.exists(source_path):
                # If not found, try searching recursively
                source_path = self.find_image_file(image_filename, obsidian_path)

            if source_path:
                dest_path = os.path.join(hugo_images_path, image_filename)
                try:
                    shutil.copy2(source_path, dest_path)
                    self.status_text.insert(tk.END, f"Copied image: {image_filename}\n")
                except Exception as e:
                    self.status_text.insert(tk.END, f"Error copying image {image_filename}: {str(e)}\n")
            else:
                self.status_text.insert(tk.END, f"Warning: Could not find image {image_filename}\n")

    def convert_files(self):
        obsidian_path = self.obsidian_path_var.get()
        hugo_path = self.hugo_path_var.get()

        if not obsidian_path or not hugo_path:
            messagebox.showerror("Error", "Please select both Obsidian and Hugo paths")
            return

        hugo_posts_path = os.path.join(hugo_path, 'content', 'posts')
        os.makedirs(hugo_posts_path, exist_ok=True)

        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, "Starting conversion...\n")

        # Process all markdown files in Obsidian vault
        for root, _, files in os.walk(obsidian_path):
            for file in files:
                if file.endswith('.md'):
                    input_file = os.path.join(root, file)
                    output_file = os.path.join(hugo_posts_path, file)

                    try:
                        with open(input_file, 'r', encoding='utf-8') as f:
                            content = f.read()

                        # Copy images before converting content
                        self.copy_images(content, obsidian_path, hugo_path)

                        # Convert content
                        converted_content = self.convert_link_syntax(content)

                        # Write converted content
                        with open(output_file, 'w', encoding='utf-8') as f:
                            f.write(converted_content)

                        self.status_text.insert(tk.END, f"Converted: {file}\n")
                        self.status_text.see(tk.END)
                    except Exception as e:
                        self.status_text.insert(tk.END, f"Error processing {file}: {str(e)}\n")

        self.status_text.insert(tk.END, "Conversion completed!\n")
        messagebox.showinfo("Success", "Conversion completed successfully!")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ObsidianHugoConverter()
    app.run()
