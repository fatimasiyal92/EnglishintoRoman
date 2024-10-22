import streamlit as st
from transformers import MarianMTModel, MarianTokenizer
import torch

# Function to handle the English to Urdu translation
def translate_to_urdu(text):
    # Special cases dictionary for common phrases
    special_cases = {
        "how are you": "tum kyse ho",
        "hello": "assalam o alaikum",
        "thank you": "shukriya",
        "goodbye": "allah hafiz"
    }
    
    # Check for special cases first
    text_lower = text.lower().strip()
    if text_lower in special_cases:
        return special_cases[text_lower]

    # For other cases, use the translation model
    try:
        # Initialize tokenizer and model
        model_name = "Helsinki-NLP/opus-mt-en-ur"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        
        # Translate
        inputs = tokenizer(text, return_tensors="pt", padding=True)
        outputs = model.generate(**inputs)
        translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Convert to Roman Urdu
        roman_translation = convert_to_roman_urdu(translation)
        return roman_translation
    
    except Exception as e:
        return f"Translation error: {str(e)}"

def convert_to_roman_urdu(urdu_text):
    # Mapping dictionary for Urdu to Roman Urdu
    mapping = {
        'ا': 'a', 'آ': 'a', 'ب': 'b', 'پ': 'p', 'ت': 't', 'ٹ': 't', 'ث': 's',
        'ج': 'j', 'چ': 'ch', 'ح': 'h', 'خ': 'kh', 'د': 'd', 'ڈ': 'd', 'ذ': 'z',
        'ر': 'r', 'ڑ': 'r', 'ز': 'z', 'ژ': 'zh', 'س': 's', 'ش': 'sh', 'ص': 's',
        'ض': 'z', 'ط': 't', 'ظ': 'z', 'ع': 'a', 'غ': 'gh', 'ف': 'f', 'ق': 'q',
        'ک': 'k', 'گ': 'g', 'ل': 'l', 'م': 'm', 'ن': 'n', 'ں': 'n', 'و': 'o',
        'ہ': 'h', 'ھ': 'h', 'ء': "'", 'ی': 'y', 'ے': 'e', 'ئ': 'y',
        '۔': '.', '،': ',', ' ': ' '
    }
    
    # Common word replacements
    word_replacements = {
        'کیسے': 'kyse',
        'تم': 'tum',
        'ہو': 'ho',
        'کیا': 'kya',
        'ہے': 'hai',
        'میں': 'main',
        'آپ': 'aap',
        'ہیں': 'hain'
    }
    
    # First try to replace common words
    for urdu_word, roman_word in word_replacements.items():
        urdu_text = urdu_text.replace(urdu_word, roman_word)
    
    # Then convert remaining characters
    result = ''
    i = 0
    while i < len(urdu_text):
        if urdu_text[i] in mapping:
            result += mapping[urdu_text[i]]
        else:
            result += urdu_text[i]
        i += 1
    
    return result.strip()

# Streamlit UI
st.title("English to Roman Urdu Translation")

# Input text box
input_text = st.text_input("Enter English text for translation", "")

# Translate button
if st.button("Translate"):
    if input_text:
        translation = translate_to_urdu(input_text)
        st.success("Translation:")
        st.write(translation)
    else:
        st.warning("Please enter some text to translate.")

# Main function
def main():
    pass

if __name__ == "__main__":
    main()
