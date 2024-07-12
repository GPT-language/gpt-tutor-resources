import pandas as pd


def load_data(filtered_word, book_file, relation_file):
    # Load the CSV files with error handling to skip bad lines
    words_df = pd.read_csv(filtered_word, on_bad_lines='skip')
    books_df = pd.read_csv(book_file, on_bad_lines='skip')
    relations_df = pd.read_csv(relation_file, on_bad_lines='skip')
    return words_df, books_df, relations_df


def create_word_books(words_df, books_df, relations_df):
    # Merge relations with words to get the vocabulary
    word_relation_df = pd.merge(relations_df, words_df, left_on='bv_voc_id', right_on='vc_id')

    # Merge the result with books to get the book names
    word_book_df = pd.merge(word_relation_df, books_df, left_on='bv_book_id', right_on='bk_id')

    # Extract the required columns
    final_df = word_book_df[['bk_name', 'vc_vocabulary']].rename(columns={'vc_vocabulary': 'Word'})

    # Group by book name and save to separate CSV files
    for name, group in final_df.groupby('bk_name'):
        group['Word'].to_csv(f"{name}.csv", index=False)


if __name__ == "__main__":
    # Paths to your CSV files
    word_file = 'D:/tempory/filtered_word.csv'
    book_file = 'D:/tempory/filtered_book.csv'
    relation_file = 'D:/tempory/relation_book_word.csv'

    words_df, books_df, relations_df = load_data(word_file, book_file, relation_file)
    create_word_books(words_df, books_df, relations_df)