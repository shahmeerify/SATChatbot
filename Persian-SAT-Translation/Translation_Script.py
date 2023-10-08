import re
import time
from googletrans import Translator
import string

# Read the text file
with open('Persian-SAT-Texts.txt', 'r', encoding='utf-8') as file:
# with open('Persian-SAT-Texts.txt', 'r', encoding='utf-8') as file:
    input_text = file.read()

# Define a regex pattern to match content inside double quotes
# double_quoted_pattern = r'[^A-Za-z\s\d=_",?؟:{}\[\]]+'
double_quoted_pattern = r'"(.*?)"'

# Find all content inside double quotes in the input string
double_quoted_contents = re.findall(double_quoted_pattern, input_text, re.MULTILINE | re.DOTALL)
double_quoted_contents = [item for item in double_quoted_contents if not all(char in string.ascii_letters + ' ' for char in item)]

# Initialize the Translator
translator = Translator()

translate_ultra_pro_max = {}

# Iterate through the extracted contents and translate them
for index, content in enumerate(double_quoted_contents):
    print(f"Algorithm Loading: {index+1}/{len(double_quoted_contents)+1}")
    try:
        # Translate the content into urdu
        translated = translator.translate(content, dest='ur').text
        translate_ultra_pro_max[content] = translated
    except Exception as e:
        print("Translation error:", str(e))

    # Add a delay of a few seconds between requests
    time.sleep(5)

# Replacing the text with the translated content
for key,val in translate_ultra_pro_max.items():
    input_text = input_text.replace(key,val)

# Write the content to another file
with open("Urdu-SAT-Texts.txt", 'w', encoding='utf-8') as f:
    f.write(input_text)