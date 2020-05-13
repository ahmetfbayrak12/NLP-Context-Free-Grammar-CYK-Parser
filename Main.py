import itertools
import random

cfg_ruleset = dict()


class CYK():

    def rules(self, folder_path):
        """
            This function reads cfg file and creates rule set dictionary (cfg_ruleset)
            Input: folder path of cfg file.
        """
        train_file = open(folder_path, 'r')
        lines = train_file.readlines()

        for line in lines:
            if(line != "\n" and line[0] != "#"):
                if("#" in line):        # For "ROOT	is it true that S ?" rule line
                    rule_token = line.split("#")[0]
                    rule_token = rule_token.split()
                    special_question = rule_token[1] + " " + rule_token[2] + " " + rule_token[3] + " " +rule_token[4]
                    temp_list = list()
                    temp_list.append(special_question)
                    temp_list.append(rule_token[5])
                    temp_list.append(rule_token[6])
                    cfg_ruleset[rule_token[0]].append(temp_list)
                else:       # Other rules
                    temp_list = list()
                    rule_token = line.split()
                    for rule in rule_token[1:]:
                        temp_list.append(rule)
                    if(rule_token[0] in cfg_ruleset):       # If left non-terminal is already in rule set
                        cfg_ruleset[rule_token[0]].append(temp_list)
                    else:       # If left non-terminal is not in rule set
                        temp_temp_list = list()
                        temp_temp_list.append(temp_list)
                        cfg_ruleset[rule_token[0]] = temp_temp_list

    def randsentence(self, output_folder_path, number_of_sentences, sentence_size):
        """
            This function creates sentences according to rule set randomly and print
            them into txt file.
            Input: folder path for printing out the generated sentences,
                    number of sentences which is going to generate,
                    maximum number of word in the one sentence.
            Output: returns all generated sentences.
        """

        all_sentences = list()
        for i in range(number_of_sentences):
            a_sentence = list()
            selected_token = "ROOT"     # Start with ROOT as a first rule
            self.generate_word(selected_token, a_sentence)      # Create a sentence

            # Since "is it true that" is a word group, it counts 1 word. So I had to check this statement and count size 4.
            if("is it true that" == a_sentence[0] and (len(a_sentence) + 3) > sentence_size):
                a_sentence = a_sentence[0:sentence_size-3]
                #a_sentence.append("?")
            elif(len(a_sentence) > sentence_size):  # If the created sentence exceeds the maximum number of word size
                a_sentence = a_sentence[0:sentence_size]    # Take until the maximum number of word size
                #a_sentence.append(".")
            all_sentences.append(a_sentence)

        # Writing the sentences into the output file
        result_output = open(output_folder_path, "w")
        for sentence in all_sentences:
            for word_index in range(len(sentence)):
                if (word_index == 0):   # For the first word, make first char of sentence capitalize
                    result_output.write(sentence[word_index][0].capitalize() + sentence[word_index][1:] + " ")
                elif (word_index == len(sentence) - 1):     # For the last word, do not add space after word
                    result_output.write(sentence[word_index])
                else:       # For middle words
                    result_output.write(sentence[word_index] + " ")
            result_output.write("\n")
        return all_sentences

    def generate_word(self, token, sentence):
        """
            This function takes a terminal or non-terminal word and call itself recursively  until
            reach the non-terminal word according to the rule set. After finding one non-terminal
            word it comes one step back and try to generate non-terminal word with this rule and so on.
            This algorithm is dept first approach. Every sentence is generated from this function
            will be correct but because of the sentence number boundary, we are going to cut sentence If
            it exceeds.
            Input: token which is going to look for rule set and a list for adding non-terminals
        """

        if(token in cfg_ruleset.keys()):        # If token is non-terminal, generate new rule, until terminal word, according to this non-terminal
            new_token_pair = random.choice(list(cfg_ruleset[token]))
            if(len(new_token_pair) == 3):       # If new randomly generated rule has 3 tokens on the right (for only "ROOT	is it true that S ?" rule
                self.generate_word(new_token_pair[0], sentence)
                self.generate_word(new_token_pair[1], sentence)
                self.generate_word(new_token_pair[2], sentence)
            elif(len(new_token_pair) == 2):     # If new randomly generated rule has 2 tokens on the right
                self.generate_word(new_token_pair[0], sentence)
                self.generate_word(new_token_pair[1], sentence)
            elif(len(new_token_pair) == 1):     # If new randomly generated rule has only 1 token on the right
                self.generate_word(new_token_pair[0], sentence)
        else:           # If token is terminal, add it to the sentence
            sentence.append(token)

    def carthesian_funct(self, list1, list2):
        """
            This function takes two list and generate all possible pairs. Like Cartesian Product.
            Input: two list which are going to product cartesian.
            Output: returns all possible pairs list
        """

        _result_list = list()
        if(not list1 and not list2):    # If both of the lists are empty
            pass
        elif(not list1):        # If list1 is empty
            for item2 in list2:
                _temp_list = list()
                _temp_list.append(item2)
            _result_list.append(_temp_list)
        elif(not list2):        # If list2 is empty
            for item1 in list1:
                _temp_list = list()
                _temp_list.append(item1)
            _result_list.append(_temp_list)
        else:           # If both of the list are not empty
            for item1 in list1:
                for item2 in list2:
                    if(type(item1) == list and type(item2) == list):    # If both of the lists have nested list go into them
                        for item11 in item1:
                            for item22 in item2:
                                _temp_list = list()
                                _temp_list.append(item11)
                                _temp_list.append(item22)
                                _result_list.append(_temp_list)
                    elif(type(item1) == list):              # If only list1 has nested list
                        for item11 in item1:
                            _temp_list=list()
                            _temp_list.append(item11)
                            _temp_list.append(item2)
                            _result_list.append(_temp_list)
                    elif(type(item2) == list):          # If only list2 has nested list
                        for item22 in item2:
                            _temp_list = list()
                            _temp_list.append(item1)
                            _temp_list.append(item22)
                            _result_list.append(_temp_list)
                    elif(type(item1) == str and type(item2) == str):    # If both of them do not have nested list
                        _temp_list = list()
                        _temp_list.append(item1)
                        _temp_list.append(item2)
                        _result_list.append(_temp_list)
        # Eliminate duplicates
        _result_list.sort()
        _result_list = list(k for k,_ in itertools.groupby(_result_list))
        return _result_list

    def CYKParser(self, sentence, output_folder):
        """
            This function is a main CYK Parser function. It takes sentence and check whether it is grammatically correct.
            After that prints the sentence and the result into to txt folder.
            Input: a sentence (string) which is going to check whether it is grammatically correct and a output folder
        """
        sentence = sentence.lower()     # make words to lowercase
        words = sentence.split()
        grammatically_correct = False   # Determining whether the sentence is grammatically correct
        punctuation = ""        # Determining the punctuation of sentence

        if(sentence[-1] == "?"):  # If it is question sentence with a punctuation
            punctuation = "?"
            sentence = sentence[0:-1]       # Get rid of the punctuation
            words = sentence.split()
            words = words [4:]       # Get rid of the "is it true that" word group
            sentence = " ".join(words)

        elif(words[2] == "true"):   # If it is a question sentence without a punctuation
            punctuation = "??"
            words = sentence.split()
            words = words [4:]       # Get rid of the "is it true that" word group
            sentence = " ".join(words)

        elif(sentence[-1] == "."):   # If it is not question sentence
            punctuation = "."
            sentence = sentence[0:-1]       # Get rid of the punctuation
            words = sentence.split()

        elif (sentence[-1] == "!"):  # If it is not question sentence
            punctuation = "!"
            sentence = sentence[0:-1]  # Get rid of the punctuation
            words = sentence.split()

        table = self.init_table(words)  # Initialize an empty table

        # For the filling bottom first row of the matrix
        for row, word in enumerate(words):
            matches = self.find_matches(word)
            table[0][row].extend(matches)

        # For the filling rest of the matrix
        possible_matches = list()
        matches = list()
        for row in range(1, len(words)):
            for col in range(len(words) - row):
                k = col + 1
                j = row - 1

                # Find all possible pairs
                for i in range (row):
                    temp_list = list()
                    temp_list = self.carthesian_funct(table[i][col], table[j][k])   # Find all possible pairs
                    for item in temp_list:
                        if(item not in possible_matches):   # Eliminate duplicates
                            possible_matches.append(item)
                    j = j-1
                    k = k+1

                # Find non-terminals according to founded pairs
                for left, rights in cfg_ruleset.items():
                    for right in rights:
                        for token in possible_matches:
                            token.sort()    # Sorting is necessary since ["NP", "VP"] != ["VP", "NP"] but they are same actually.
                            right.sort()
                            if (token == right and left not in matches):    # Eliminate duplicates
                                matches.append(left)

                # Fill the cell in the matrix
                table[row][col] = matches
                matches = list()
                possible_matches = list()

        if("S" in table[len(words)-1][0]):  # If there is a "S" token in the root
            grammatically_correct = True

        if(punctuation == "?"):     # Question sentence with punctuation
            question_part = "Is it true that "
            final_sentence = question_part + sentence + punctuation
        elif(punctuation == "??"):  # Question sentence without punctuation
            question_part = "Is it true that "
            final_sentence = question_part + sentence
        else:           # Not question sentence
            sentence_splitted = sentence.split()
            sentence_splitted[0] = sentence_splitted[0][0].capitalize() + sentence_splitted[0][1:]
            final_sentence = " ".join(sentence_splitted)
            final_sentence = final_sentence.rstrip()
            if(punctuation == "." or punctuation == "!"):   # If there was a punctuation in the original sentence
                final_sentence = final_sentence + punctuation


        output_folder.write("Sentence: " + final_sentence + "\n")
        print("Sentence: " + final_sentence + "\n")

        # Print the tree structure of sentence
        self.print_table(sentence, table)

        if(grammatically_correct):
            output_folder.write("Grammatically situation: CORRECT.\n")
            print("Grammatically situation: CORRECT.\n")
        else:
            output_folder.write("Grammatically situation: INCORRECT.\n")
            print("Grammatically situation: INCORRECT.\n")

        output_folder.write("**************\n")
        print("**************\n")

    def find_matches(self, word):
        """
            This function is for finding all possible pairs for first bottom of matrix.
            Input: terminal word(string)
            Output: All possible non-terminals
        """
        possible_matches = list()
        for left, rights in cfg_ruleset.items():    # Example of left = ROOT and example of rights = [["S", "."], ["S", "!"]]
            for right in rights:
                for token in right:
                    if(word == token):
                        possible_matches.append(left)
                        # If founded terminal word is also in the right side of an another rule
                        # For example for "you" word, this algorithm finds "Pronoun" first and then
                        # search for "Pronoun" and it will find "NP"
                        for left1, rights1 in cfg_ruleset.items():
                            for right1 in rights1:
                                for token1 in right1:
                                    if(left == token1 and len(right1) == 1):
                                        possible_matches.append(left1)
        return possible_matches

    def init_table(self, words):
        """
            This function initializes an empty table
            Input: list of strings
            Output: table (list)
        """
        _table = list()
        for i in range(len(words)):
            _table.append(list())
            for j in range(len(words)):
                _table[i].append(list())
        return _table

    def print_table(self, sentence, table):
        """
            This function prints matrix.
            Inputs: sentence (string) and table matrix (list)
        """
        print("Table:\n")
        words = sentence.split()
        for row in range(len(words)):
            for col in range(len(words)-row):
                print(table[row][col], end="")
            print()
        print()

if __name__ == '__main__':
    cfg_ruleset_folder_path = "cfg.gr"

    cyk_object = CYK()

    cyk_object.rules(cfg_ruleset_folder_path)   # Create rule set according to cfg.gr file

    # You can change number of sentences and number of words in a sentence by changing second and third parameter
    all_sentences = cyk_object.randsentence("generated_sentences.txt", 10, 15)

    result_output = open("result.txt", "w")

    for sentence in all_sentences:
        sentence_string = " ".join(sentence)
        cyk_object.CYKParser(sentence_string, result_output)


