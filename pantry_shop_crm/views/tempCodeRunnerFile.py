        def show_user_list_frame(content_frame):
            # Create the frame for the user list
            frame = ttk.Frame(content_frame)
            
            # Title Label
            ttk.Label(frame, text="User List", font=("Helvetica", 16)).pack(pady=20)
            
            # Filter Frame
            filter_frame = ttk.Frame(frame)
            filter_frame.pack(pady=10)
            
            # Entry fields for filter
            filter_user_id_var = tk.StringVar()
            filter_username_var = tk.StringVar()
            
            ttk.Label(filter_frame, text="User ID").grid(row=0, column=0, padx=5)
            ttk.Entry(filter_frame, textvariable=filter_user_id_var).grid(row=0, column=1, padx=5)
            
            ttk.Label(filter_frame, text="Username").grid(row=0, column=2, padx=5)
            ttk.Entry(filter_frame, textvariable=filter_username_var).grid(row=0, column=3, padx=5)
            
            # Filter button
            ttk.Button(filter_frame, text="Apply Filter", command=lambda: filter_user_list(filter_user_id_var, filter_username_var)).grid(row=1, column=0, columnspan=4, pady=10)
            
            # Treeview to display user data
            tree_frame = ttk.Frame(frame)
            tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Dummy data for users (replace this with real data in actual app)
            user_data = [
                {"user_id": 1, "username": "john_doe", "first_name": "John", "last_name": "Doe", "email": "john@example.com"},
                {"user_id": 2, "username": "jane_doe", "first_name": "Jane", "last_name": "Doe", "email": "jane@example.com"},
                {"user_id": 3, "username": "alice_smith", "first_name": "Alice", "last_name": "Smith", "email": "alice@example.com"},
                {"user_id": 4, "username": "bob_jones", "first_name": "Bob", "last_name": "Jones", "email": "bob@example.com"},
                # Add more dummy users here...
            ]
            
            # Create a DataFrame for easier manipulation
            user_df = pd.DataFrame(user_data)
            
            # Treeview definition
            columns = ("user_id", "username", "first_name", "last_name", "email")
            user_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
            
            # Defining headings
            for col in columns:
                user_tree.heading(col, text=col.replace("_", " ").title())
                user_tree.column(col, anchor="center")
            
            # Scrollbar for the Treeview
            vert_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=user_tree.yview)
            vert_scrollbar.pack(side="right", fill="y")
            
            # Horizontal scrollbar
            horiz_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=user_tree.xview)
            horiz_scrollbar.pack(side="bottom", fill="x")
            
            user_tree.configure(yscrollcommand=vert_scrollbar.set, xscrollcommand=horiz_scrollbar.set)
            
            # Add the user data to the Treeview
            def update_treeview(data):
                # Clear existing rows in the treeview
                for row in user_tree.get_children():
                    user_tree.delete(row)
                
                # Insert new rows into the treeview
                for user in data:
                    user_tree.insert("", "end", values=(user["user_id"], user["username"], user["first_name"], 
                                                        user["last_name"], user["email"]))
            
            update_treeview(user_data)
            
            user_tree.pack(fill="both", expand=True)
            
            # Pagination controls
            pagination_frame = ttk.Frame(frame)
            pagination_frame.pack(pady=10)
            
            ttk.Button(pagination_frame, text="Previous", command=lambda: previous_page()).grid(row=0, column=0, padx=5)
            ttk.Button(pagination_frame, text="Next", command=lambda: next_page()).grid(row=0, column=1, padx=5)
            
            # Home button to return to the main menu
            ttk.Button(frame, text="Home", command=lambda: show_home()).pack(pady=10)
            
            frame.pack(fill="both", expand=True)
            
            def filter_user_list(filter_user_id_var, filter_username_var):
                # Get filter criteria
                filter_user_id = filter_user_id_var.get()
                filter_username = filter_username_var.get()
                
                # Apply filters to the user data (for testing, we use basic string matching)
                filtered_data = user_data
                
                if filter_user_id:
                    filtered_data = [user for user in filtered_data if str(user["user_id"]).startswith(filter_user_id)]
                
                if filter_username:
                    filtered_data = [user for user in filtered_data if filter_username.lower() in user["username"].lower()]
                
                # Update the Treeview with filtered data
                update_treeview(filtered_data)
            
            def previous_page():
                # Logic for previous page pagination (not implemented yet)
                print("Previous page")
            
            def next_page():
                # Logic for next page pagination (not implemented yet)
                print("Next page")
            
            def show_home():
                # Logic to go back to the home frame
                print("Home button pressed")
                # You can implement the home functionality based on your app's flow.
                pass