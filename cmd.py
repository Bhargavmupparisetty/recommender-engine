import tkinter as tk
import database
from recommender import RecommenderEngine  # Ensure this import is correct

class TerminalApp:
    def __init__(self, root):
        self.root = root
        self.db = database.Database()  # Database instance
        self.root.title("bills")
        
        self.command_history = []  # To store command history
        self.history_index = -1  # To keep track of current position in history
        
        self.output = tk.Text(root, height=20, width=80, bg="black", fg="white", insertbackground="white")
        self.output.pack(padx=10, pady=10)
        
        self.input = tk.Entry(root, width=80, bg="black", fg="white", insertbackground="white")
        self.input.pack(padx=10, pady=10)
        self.input.bind("<Return>", self.process_command)
        self.input.bind("<Up>", self.previous_command)  # Bind Up arrow key
        self.input.bind("<Down>", self.next_command)  # Bind Down arrow key

        self.output.insert(tk.END, "Welcome to the Recommender engine!\nType 'help' for available commands.\n\n")

    def process_command(self, event):
        command = self.input.get().strip()
        if command:  # Save command if it's not empty
            self.command_history.append(command)
            self.history_index = len(self.command_history)  # Reset history index
            
        self.output.insert(tk.END, f"recommender> {command}\n")

        if command == "exit":
            self.output.insert(tk.END, "Goodbye!\n")
            self.root.quit()
        elif command.startswith("add_billing"):
            self.add_billing(command)
        elif command.startswith("update_billing"):
            self.update_billing(command)
        elif command.startswith("delete_billing"):
            self.delete_billing(command)
        elif command.startswith("recommend"):
            self.recommend_items(command)
        elif command == "help":
            self.show_help()
        else:
            self.output.insert(tk.END, "Unknown command.\n")

        self.input.delete(0, tk.END)
        
    def add_billing(self, command):
        try:
            _, original_string, amount, customer_name = command.split(maxsplit=3)
            amount = float(amount)
            self.db.insert_billed_value(original_string, amount, customer_name)
            self.output.insert(tk.END, f"Added billing for {original_string}.\n")
        except ValueError:
            self.output.insert(tk.END, "Invalid format. Usage: add_billing <item> <amount> <customer>\n")
        except Exception as e:
            self.output.insert(tk.END, f"Error: {e}\n")


    def update_billing(self, command):
        try:
            _, bill_id, new_amount = command.split()
            bill_id = int(bill_id)
            new_amount = float(new_amount)
            self.db.update_billed_value(bill_id, new_amount)
            self.output.insert(tk.END, f"Updated billing ID {bill_id} with new amount {new_amount}.\n")
        except ValueError:
            self.output.insert(tk.END, "Invalid format. Usage: update_billing <id> <new_amount>\n")
        except Exception as e:
            self.output.insert(tk.END, f"Error: {e}\n")

    def delete_billing(self, command):
        try:
            _, bill_id = command.split()
            bill_id = int(bill_id)
            self.db.delete_billed_value(bill_id)
            self.output.insert(tk.END, f"Deleted billing with ID {bill_id}.\n")
        except ValueError:
            self.output.insert(tk.END, "Invalid format. Usage: delete_billing <id>\n")
        except Exception as e:
            self.output.insert(tk.END, f"Error: {e}\n")

    def show_help(self):
        self.output.insert(tk.END, "Available commands:\n")
        self.output.insert(tk.END, "  add_billing <item> <amount> <customer>\n")
        self.output.insert(tk.END, "  update_billing <id> <new_amount>\n")
        self.output.insert(tk.END, "  delete_billing <id>\n")
        self.output.insert(tk.END, "  recommend <start_date> <end_date>\n")
        self.output.insert(tk.END, "  exit - Quit the application\n")

    def recommend_items(self, command):
        try:
            _, start_date, end_date = command.split(maxsplit=2)
            transactions = self.db.get_transactions_by_date(start_date, end_date)
            recommender = RecommenderEngine(transactions)
            recommendations = recommender.generate_recommendations()
            self.output.insert(tk.END, recommendations)
        except ValueError:
            self.output.insert(tk.END, "Invalid format. Usage: recommend <start_date> <end_date>\n")
        except Exception as e:
            self.output.insert(tk.END, f"Error: {e}\n")

    def previous_command(self, event):
        if self.command_history and self.history_index > 0:
            self.history_index -= 1
            self.input.delete(0, tk.END)
            self.input.insert(0, self.command_history[self.history_index])

    def next_command(self, event):
        if self.command_history and self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.input.delete(0, tk.END)
            self.input.insert(0, self.command_history[self.history_index])
        elif self.history_index == len(self.command_history) - 1:
            self.history_index += 1
            self.input.delete(0, tk.END)

if __name__ == '__main__':
    root = tk.Tk()  # Create the main window
    app = TerminalApp(root)
    root.mainloop()  # Start the main event loop
