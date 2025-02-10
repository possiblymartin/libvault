import os

db_path = 'instance/libvault.db'

if os.path.exists(db_path):
  os.remove(db_path)
  print(f"Database file '{db_path}' deleted successfully.")
else:
  print(f"Database file '{db_path}' does not exist.")

