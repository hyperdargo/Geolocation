import requests
import tkinter as tk
from tkinter import messagebox, filedialog

def get_geolocation(ip_address):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "success":
                return {
                    "IP": data.get("query"),
                    "City": data.get("city"),
                    "Region": data.get("regionName"),
                    "Country": data.get("country"),
                    "Latitude": data.get("lat"),
                    "Longitude": data.get("lon"),
                    "Organization": data.get("isp"),
                    "Timezone": data.get("timezone")
                }
            else:
                return {"error": data.get("message")}
        else:
            return {"error": f"Unable to fetch data. Status code: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def show_geolocation():
    ip_address = ip_entry.get()
    geolocation_data = get_geolocation(ip_address)
    if "error" in geolocation_data:
        messagebox.showerror("Error", geolocation_data["error"])
    else:
        result = (
            f"IP: {geolocation_data['IP']}\n"
            f"City: {geolocation_data['City']}\n"
            f"Region: {geolocation_data['Region']}\n"
            f"Country: {geolocation_data['Country']}\n"
            f"Latitude: {geolocation_data['Latitude']}\n"
            f"Longitude: {geolocation_data['Longitude']}\n"
            f"Organization: {geolocation_data['Organization']}\n"
            f"Timezone: {geolocation_data['Timezone']}"
        )
        result_label.config(text=result)

def save_to_file():
    geolocation_data = result_label.cget("text")
    if geolocation_data:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(geolocation_data)
            messagebox.showinfo("Saved", "Geolocation data saved successfully!")
    else:
        messagebox.showwarning("Warning", "No geolocation data to save!")


root = tk.Tk()
root.title("IP Geolocation")
root.geometry("600x500")  # Increased window size

tk.Label(root, text="Enter IP address:", font=("Arial", 16)).pack(pady=15)
ip_entry = tk.Entry(root, font=("Arial", 16), width=45)  # Increased entry box width and font size
ip_entry.pack(pady=15)

tk.Button(root, text="Get Geolocation", command=show_geolocation, font=("Arial", 16)).pack(pady=15)
tk.Button(root, text="Save to File", command=save_to_file, font=("Arial", 16)).pack(pady=15)

result_label = tk.Label(root, text="", justify="left", font=("Arial", 16), anchor="nw")
result_label.pack(pady=15, padx=15, fill="both", expand=True)  # Increased padding

root.mainloop()
