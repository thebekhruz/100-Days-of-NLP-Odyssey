import pandas as pd

def load_dataframe(file_path):
    """Load a DataFrame from a CSV file."""
    return pd.read_csv(file_path, delimiter='\t', header=None, names=['doc_id', 'type', 'value'])

def combine_titles_and_descriptions(titles_df, descriptions_df):
    """Combine titles and descriptions into a single DataFrame."""
    # Merge the dataframes on 'doc_id'
    combined_df = pd.merge(titles_df, descriptions_df, on='doc_id', suffixes=('_title', '_description'))
    
    # Concatenate the title and description values
    combined_df['combined_value'] = combined_df['value_title'] + " " + combined_df['value_description']
    
    # Select the relevant columns for the output
    output_df = combined_df[['doc_id', 'combined_value']]
    return output_df

def save_combined_data(df, output_file_path):
    """Save the combined DataFrame to a CSV file."""
    df.to_csv(output_file_path, sep='\t', index=False, header=None)

def main():
    # Define file paths
    title_file_path = 'data/intermediate/preprocessing/processed_data_title.csv'
    description_file_path = 'data/intermediate/preprocessing/processed_data_descr.csv'
    output_file_path = 'data/intermediate/preprocessing/processed_data_combined.csv'
    
    # Load titles and descriptions
    titles_df = load_dataframe(title_file_path)
    descriptions_df = load_dataframe(description_file_path)
    
    # Combine titles and descriptions
    combined_df = combine_titles_and_descriptions(titles_df, descriptions_df)
    
    # Save the combined data
    save_combined_data(combined_df, output_file_path)
    
    print("Titles and descriptions have been successfully combined.")

if __name__ == '__main__':
    main()
