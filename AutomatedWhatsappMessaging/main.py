import pywhatkit
import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('test_sheet.csv')

# Process the phone_no column to add "+20" at the start of each number
def add_country_code(phone_no):
    # Check if the number starts with a '+' (indicating it already has a country code)
    if str(phone_no).startswith('+'):
        return phone_no
    else:
        return f"+20{phone_no}"

number_list = df['رقم الموبايل'].apply(add_country_code).tolist()

if pywhatkit:
    print("library is loaded")
else:
    print("can't load library")
    exit

print("loading numbers in PyWhatKit database...")
# Read the history of messages sent
sent_numbers = []
with open('PyWhatKit_DB.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
    i = 0
    while i < len(lines):
        if lines[i].startswith("Phone Number:"):
            sent_numbers.append(lines[i].split(": ")[1].strip())
            i += 3  # Move to the next message block
        else:
            i += 1

print("loading the message from msg.txt...")
# Read the message from message.txt
with open('msg.txt', 'r', encoding='utf-8') as file:
    message = file.read()

print("Began sending messages...")
messages_sent = 0
messages_skipped = 0

for number in number_list:
    if number not in sent_numbers:
        pywhatkit.sendwhatmsg_instantly(number, message, 15, True, 4)
        messages_sent += 1
    else:
        messages_skipped += 1

print("Complete!")

# Calculate and print statistics
total_numbers_processed = len(number_list)
print(f"Total Numbers Processed: {total_numbers_processed}")
print(f"Numbers Sent Messages: {messages_sent}")
print(f"Numbers Skipped (Already Sent Messages): {messages_skipped}")