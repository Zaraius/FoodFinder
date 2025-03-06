import pandas as pd
import re

def clean_text(text):
    if pd.isna(text):  # Check if the value is NaN
        return text
    
    # Convert to string if not already
    text = str(text)
    
    # Remove emojis and other non-ASCII characters
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading/trailing whitespace
    return text.strip()

def clean_csv(input_file, output_file):
    try:
        # Read the CSV file with '|' delimiter
        df = pd.read_csv(input_file, sep='|', encoding='utf-8')
        
        # Clean all columns
        for column in df.columns:
            df[column] = df[column].apply(clean_text)
        
        # Drop rows where any review column is NaN
        review_columns = [col for col in df.columns if 'Review' in col]
        df.dropna(subset=review_columns, inplace=True)
        
        # Save the cleaned data
        df.to_csv(output_file, index=False, sep='|', encoding='utf-8')
        print(f"Successfully cleaned {input_file} and saved to {output_file}")
        
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    input_file = "mvp_database.csv"  # Your original CSV file
    output_file = "mvp_database_cleaned.csv"  # The cleaned version
    clean_csv(input_file, output_file)