# script to count the number of word occurrences in the ALICE'S ADVENTURES IN WONDERLAND book
def get_word_occurrences():
    # Ask for the word?
    word = input('\n\tEnter the word you need to search?\t\t')
    # Targeting the file
    file = open("./book.txt", "r")
    # Read content of file to string
    data = file.read()
    # Get number of occurrences of the substring in the string
    occurrences = data.count(str(word))
    print('********************************')
    print('*\tOccurrences: \t', occurrences)
    print('********************************\n')

    return occurrences


get_word_occurrences()
