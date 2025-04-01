#!/usr/bin/env python
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib
# Configure for GitHub compatibility
if 'DISPLAY' not in os.environ:
    matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GPAPredictorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Study Hours GPA Predictor")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Sample dataset
        self.data = {
            'study_hours': [5, 10, 15, 20, 25, 30],
            'gpa': [2.0, 2.7, 3.3, 3.7, 3.9, 4.0]
        }
        
        self.setup_ui()
        self.plot_data()
    
    def setup_ui(self):
        """Initialize all UI components"""
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10), padding=5)
        style.configure('Header.TLabel', font=('Arial', 14, 'bold'))

        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(pady=10, fill=tk.X)
        ttk.Label(header_frame, text="Study Hours GPA Predictor", style='Header.TLabel').pack()
        
        # Input section
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=20, fill=tk.X)
        
        ttk.Label(input_frame, text="Study Hours:").grid(row=0, column=0, padx=5)
        self.hours_entry = ttk.Entry(input_frame, width=10)
        self.hours_entry.grid(row=0, column=1, padx=5)
        
        ttk.Button(
            input_frame, 
            text="Predict GPA", 
            command=self.predict_gpa
        ).grid(row=0, column=2, padx=10)
        
        # Results display
        self.result_frame = ttk.Frame(self.root)
        self.result_frame.pack(pady=10, fill=tk.X)
        
        # Data table
        table_frame = ttk.Frame(self.root)
        table_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(table_frame, columns=('Hours', 'GPA'), show='headings')
        self.tree.heading('Hours', text='Study Hours')
        self.tree.heading('GPA', text='GPA')
        self.tree.column('Hours', width=100, anchor=tk.CENTER)
        self.tree.column('GPA', width=100, anchor=tk.CENTER)
        
        for hours, gpa in zip(self.data['study_hours'], self.data['gpa']):
            self.tree.insert('', tk.END, values=(hours, gpa))
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Plot area
        self.plot_frame = ttk.Frame(self.root)
        self.plot_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Add data button
        ttk.Button(
            self.root, 
            text="Add Data Point", 
            command=self.show_add_data_dialog
        ).pack(pady=10)
    
    def plot_data(self):
        """Create/update the plot"""
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(self.data['study_hours'], self.data['gpa'], 'bo-')
        ax.set_title('Study Hours vs GPA')
        ax.set_xlabel('Weekly Study Hours')
        ax.set_ylabel('GPA')
        ax.grid(True)
        
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def predict_gpa(self):
        """Handle GPA prediction"""
        try:
            hours = float(self.hours_entry.get())
            
            for widget in self.result_frame.winfo_children():
                widget.destroy()
                
            predicted_gpa = self.calculate_gpa(hours)
            
            ttk.Label(
                self.result_frame,
                text=f"Predicted GPA for {hours} study hours: {predicted_gpa:.2f}",
                font=('Arial', 12, 'bold'),
                foreground='green'
            ).pack()
            
            ttk.Label(
                self.result_frame,
                text=f"Tip: {self.get_study_tip(hours)}",
                font=('Arial', 10),
                foreground='blue'
            ).pack()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
    
    def calculate_gpa(self, hours):
        """Calculate predicted GPA"""
        if hours <= self.data['study_hours'][0]:
            return self.data['gpa'][0]
        elif hours >= self.data['study_hours'][-1]:
            return self.data['gpa'][-1]
        else:
            for i in range(len(self.data['study_hours']) - 1):
                if self.data['study_hours'][i] <= hours <= self.data['study_hours'][i+1]:
                    ratio = (hours - self.data['study_hours'][i]) / (self.data['study_hours'][i+1] - self.data['study_hours'][i])
                    return self.data['gpa'][i] + ratio * (self.data['gpa'][i+1] - self.data['gpa'][i])
        return 0.0
    
    def get_study_tip(self, hours):
        """Generate study tips"""
        if hours < 10:
            return "Consider increasing your study time for better results."
        elif 10 <= hours < 20:
            return "You're on a good path. Maintain consistency!"
        else:
            return "Excellent study habits! Make sure to balance with rest."
    
    def show_add_data_dialog(self):
        """Dialog for adding new data points"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Data Point")
        dialog.geometry("300x200")
        dialog.configure(bg="#f0f0f0")
        
        ttk.Label(dialog, text="Study Hours:").pack(pady=5)
        hours_entry = ttk.Entry(dialog)
        hours_entry.pack(pady=5)
        
        ttk.Label(dialog, text="GPA:").pack(pady=5)
        gpa_entry = ttk.Entry(dialog)
        gpa_entry.pack(pady=5)
        
        def add_data():
            try:
                hours = float(hours_entry.get())
                gpa = float(gpa_entry.get())
                
                self.data['study_hours'].append(hours)
                self.data['gpa'].append(gpa)
                
                # Sort data
                combined = sorted(zip(self.data['study_hours'], self.data['gpa']))
                self.data['study_hours'], self.data['gpa'] = zip(*combined)
                self.data['study_hours'] = list(self.data['study_hours'])
                self.data['gpa'] = list(self.data['gpa'])
                
                # Update UI
                self.tree.delete(*self.tree.get_children())
                for h, g in zip(self.data['study_hours'], self.data['gpa']):
                    self.tree.insert('', tk.END, values=(h, g))
                
                self.plot_data()
                dialog.destroy()
                messagebox.showinfo("Success", "Data point added successfully")
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers")
        
        ttk.Button(dialog, text="Add", command=add_data).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = GPAPredictorApp(root)
    root.mainloop()
