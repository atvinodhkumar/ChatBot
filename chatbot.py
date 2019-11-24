# -*- coding: utf-8 -*-

from difflib import SequenceMatcher

import sys
import csv
import time
import webbrowser


class ChatBot:
    """Collects information from the customer and stores them in a CSV file.
    """

    def __init__(self):
        self.customer_information = []
        self.count_number_of_trucks = None
        self.total_number_of_trucks = None
        self.total_number_of_trucks_copy = None
        self.number_of_trucks_in_this_brand = None
        self.positive_input = ["Y", "y", "Yes", "yes", "YES", "Ya", "ya", "Yeah", "yeah", "Yea", "yea", "Yep", "yep", "Yup", "yup"]
        self.negative_input = ["N", "n", "No", "no", "NO", "Nope", "nope", "Nah", "nah", "Nay", "nay"]

    @staticmethod
    def blank_input():
        """Condition to avoid the blank input from the user.
        """
        user_input = input().strip()
        while user_input == "":
            print("Entered an empty input. Please enter a valid input.")
            user_input = input().strip()
        return user_input
    
    def store_information(self, store):
        """Appends every detail into a list.
        """
        return self.customer_information.append(store)
    
    @staticmethod
    def read_text_file(text_file_path):
        """To read a text file.
        """
        with open(text_file_path, 'r') as question:
            questions = question.read().split('\n')
        return questions
    
    def trucks_availability(self, trucks_available, questions, condition=None, brand=None, mode=None):
        """Checking if the customer wants to interact with regarding trucks. 
           If not, they are redirected to the contact page of the company.
        """
        if trucks_available in self.positive_input:
            return

        elif trucks_available in self.negative_input:
            print("\n")
            print(questions[0])
            print("\n")
            for second in range(11, 0, -1):
                sys.stdout.write("\r")
                sys.stdout.write(questions[1].format(second))
                sys.stdout.flush()
                time.sleep(1)

            print("\n")
            webbrowser.open(questions[2])
            sys.exit(0)

        else:
            return ChatBot.check_for_yes_no(self.trucks_availability, questions, None, None, None)

    @staticmethod
    def check_for_yes_no(function_name, questions, condition, brand, mode):
        """Making sure that the customer enters a valid input.
        """
        print("\nPlease enter a valid input.")
        return function_name(ChatBot.blank_input(), questions, condition, brand, mode)

    def is_number(self, input_number):
        """Making sure that the customer does not input other than a number.
        """
        if input_number.isdigit():
            return int(input_number)

        else:
            print("\nPlease reply with a number.")
            return self.is_number(ChatBot.blank_input())
        
    def similarity_checker(self, string1):
        """Making sure that the customer enters a valid truck name.
        """
        truck_names = ChatBot.read_text_file(text_file_path + "trucks_brand_name_europe.txt")
        
        if string1 in truck_names:
            return "Same"
        
        else:
            similarity_ratio = [SequenceMatcher(None, string1, string2).ratio() for string2 in truck_names]
            highest_match_index = similarity_ratio.index(max(similarity_ratio))
            print("\nDo you mean {}?".format(truck_names[highest_match_index]))
            
            exit_loop = False
            
            while not exit_loop:
                corrected_input = ChatBot.blank_input()
                
                if corrected_input in self.positive_input:
                    exit_loop = True
                    return truck_names[highest_match_index]
        
                elif corrected_input in self.negative_input:
                    print("\nThen, please enter the correct name: ")
                    exit_loop = True
                    return ChatBot.blank_input()
                else:
                    print("\nPlease enter a valid input.") 
                    
    @staticmethod
    def generate_correct_name(collection, check_collection):
        """Generate the corrected truck names.
        """
        index_value_collection = [idx for idx, item in enumerate(check_collection) if item == "Same"]

        for index_value in index_value_collection:
            check_collection[index_value] = collection[index_value]
        
        return check_collection

    def condition_check(self, questions, brand, mode):
        """Making sure the customer enters matching information.
           For instance:
               The customer says he/she has 3 brands of trucks. When asked for 
               names, if the customer replies with less or more than 3 names, 
               this function asks until the customer enters matching information.
        """
        condition = True
        
        while condition:
            if self.total_number_of_trucks == 1 or self.number_of_trucks_in_this_brand == 1:
                collection, condition = self.collect_information("yes", questions, condition, brand, mode)
            else:
                print("\n")
                print(questions[0])
                collection, condition = self.collect_information(ChatBot.blank_input(), questions, condition, brand, mode)

        return collection

    def collect_information(self, yes_no_input, questions, condition, brand, mode):
        """Conditions to make sure the customer enters matching information.
        """

        if yes_no_input.strip() in self.positive_input or yes_no_input.strip() in self.negative_input:

            if yes_no_input in self.positive_input:
                same_or_different_numbers = 1
                print("\n")
                print(questions[1].format(brand))
                collection = [collect.capitalize() for collect in input().split(",")]
                if mode == "Brand":
                    check_collection = [self.similarity_checker(string1) for string1 in collection]
                    collection = ChatBot.generate_correct_name(collection, check_collection)
                self.count_number_of_trucks = same_or_different_numbers

            else:
                if self.number_of_trucks_in_this_brand == 2:
                    same_or_different_numbers = 2
                else:
                    print("\n")
                    print(questions[2])
                    same_or_different_numbers = self.is_number(input())
                print("\n")
                print(questions[3])
                collection = [collect.capitalize() for collect in input().split(",")]
                if mode == "Brand":
                    check_collection = [self.similarity_checker(string1) for string1 in collection]
                    collection = ChatBot.generate_correct_name(collection, check_collection)
                self.count_number_of_trucks = same_or_different_numbers

            correct_match = True

            while correct_match:

                if same_or_different_numbers == len(collection):
                    correct_match = False
                    condition = False

                elif same_or_different_numbers > len(collection):
                    print("\n")
                    print(questions[4].format((same_or_different_numbers - len(collection))))
                    collection.extend(input().split(","))
                    continue

                elif same_or_different_numbers < len(collection):

                    if yes_no_input in self.positive_input:
                        print("\n")
                        print(questions[5])

                    else:
                        print("\n")
                        print(questions[6])

                    correct_match = False

                else:
                    pass

            return collection, condition

        else:
            return ChatBot.check_for_yes_no(self.collect_information, questions, condition, brand, mode)

    def specifications_validation(self, check_valid_specification, validation_check_count, specification_validation_questions):
        """Validates the specifications of the trucks.
        """
        specifications_validation_values_minimum = [0, 660, 200, 0, 4, 0, 30, 20800, 8, 2, 4, 11000, 2400, 2000, 0]
        specifications_validation_values_maximum = [0, 14100, 500, 0, 12, 0, 100, 43900, 20, 8, 18, 17000, 2600, 15500, 0]
        
        if check_valid_specification < specifications_validation_values_minimum[validation_check_count] or check_valid_specification > specifications_validation_values_maximum[validation_check_count]:
            print("\n")
            print(specification_validation_questions[validation_check_count])
            exit_loop = False
            
            while not exit_loop:
                corrected_input = ChatBot.blank_input()
                
                if corrected_input in self.positive_input:
                    exit_loop = True
                    return check_valid_specification
        
                elif corrected_input in self.negative_input:
                    print("\nThen, please enter an appropriate value: ")
                    exit_loop = True
                    return self.is_number(ChatBot.blank_input())
                else:
                    print("\nPlease enter a valid input.") 
        else:
            return check_valid_specification

    def specifications(self, questions, brand, model):
        """Collects the specifications of the trucks.
        """
        print("\nPlease state the specifications of {} truck ({} model): ".format(brand, model))
        specification_validation_questions = ChatBot.read_text_file(text_file_path + "trucks_specification_questions_validation.txt")
        validation_check_count = 0
        for question in questions:
            print("\n")
            print(question)
            if validation_check_count in (0, 3, 5, 14):
                valid_specification = ChatBot.blank_input()
            else:
                check_valid_specification = self.is_number(ChatBot.blank_input())
                valid_specification = self.specifications_validation(check_valid_specification, validation_check_count, specification_validation_questions)
            self.store_information(valid_specification)
            validation_check_count += 1

    def chatbot(self, csv_file_path, text_file_path):
        """Working of ChatBot.
        """
        print("Welcome! Can you please state your name?")
        self.store_information(ChatBot.blank_input())

        print("\nHello {}! I am Chatty. Let's Chat.\nCan you please state the name of your company?".format(self.customer_information[0]))
        self.store_information(ChatBot.blank_input())

        questions = ChatBot.read_text_file(text_file_path + "trucks_availability_questions.txt")
        print("\nDo you own trucks?")
        self.trucks_availability(ChatBot.blank_input(), questions)

        print("\nHow many trucks do you have in total?")
        self.total_number_of_trucks = self.is_number(ChatBot.blank_input())
        self.total_number_of_trucks_copy = self.total_number_of_trucks
        self.store_information(self.total_number_of_trucks)

        headers = ['Customer Name', 'Company Name', 'Total Number of Trucks', 'Truck Brand',
                   'Number of Trucks in this Brand', 'Truck Model', 'Number of Trucks in this Models',
                   'Engine Type', 'Engine Capacity (cc)', 'Engine Horsepower (HP/rpm)', 'Steering Type',
                   'Steering Turning Radius (m)', 'Battery Capacity', 'Maximum Speed (Km/h)',
                   'Fuel Tank Capacity (litres)', 'Gears', 'Axles', 'Wheels', 'Truck Length (mm)',
                   'Truck Width (mm)', 'Truck Weight (Kg)', 'License Plate Number']

        with open(csv_file_path + self.customer_information[1] + ".csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(headers)

        questions = ChatBot.read_text_file(text_file_path + "trucks_brand_questions.txt")
        brand_names = self.condition_check(questions, None, "Brand")
        brand_loop_count = len(brand_names)

        for brand in brand_names:

            if len(brand_names) == 1:
                self.store_information(brand)
                self.number_of_trucks_in_this_brand = self.total_number_of_trucks
                self.store_information(self.number_of_trucks_in_this_brand)

            elif len(brand_names) == self.total_number_of_trucks or self.count_number_of_trucks == 1 or \
                    self.total_number_of_trucks_copy == 1 or brand_loop_count == self.total_number_of_trucks_copy:
                self.store_information(brand)
                self.number_of_trucks_in_this_brand = 1
                self.store_information(self.number_of_trucks_in_this_brand)

            elif brand_loop_count == 1:
                self.store_information(brand)
                self.number_of_trucks_in_this_brand = self.total_number_of_trucks_copy
                self.store_information(self.number_of_trucks_in_this_brand)
                print("\n{} trucks: ".format(brand))

            else:
                self.store_information(brand)
                print("\nHow many {} trucks do you have?".format(brand))
                self.number_of_trucks_in_this_brand = self.is_number(ChatBot.blank_input())
                self.store_information(self.number_of_trucks_in_this_brand)

            questions = ChatBot.read_text_file(text_file_path + "trucks_model_questions.txt")
            model_names = self.condition_check(questions, brand, None)

            model_loop_count = len(model_names)
            number_of_trucks_in_this_brand_model = self.number_of_trucks_in_this_brand

            for model in model_names:

                questions = ChatBot.read_text_file(text_file_path + "trucks_specification_questions.txt")

                if len(model_names) == 1:
                    self.store_information(model)
                    if len(brand_names) == 1:
                        trucks_in_this_model = self.total_number_of_trucks
                        self.store_information(trucks_in_this_model)
                    else:
                        trucks_in_this_model = self.customer_information[4]
                        self.store_information(trucks_in_this_model)
                    self.specifications(questions, brand, model)
                    self.convert_to_csv()
                    del self.customer_information[3:]

                elif self.number_of_trucks_in_this_brand == 1 or self.number_of_trucks_in_this_brand == self.count_number_of_trucks:
                    self.store_information(model)
                    trucks_in_this_model = 1
                    self.store_information(trucks_in_this_model)
                    self.specifications(questions, brand, model)
                    self.convert_to_csv()
                    del self.customer_information[5:]

                elif model_loop_count == 1:
                    self.store_information(model)
                    trucks_in_this_model = number_of_trucks_in_this_brand_model
                    self.store_information(trucks_in_this_model)
                    print("\n{} model trucks: ".format(model))
                    self.specifications(questions, brand, model)
                    self.convert_to_csv()
                    del self.customer_information[5:]

                else:
                    self.store_information(model)
                    print("\nHow many {} trucks of {} model do you have?".format(brand, model))
                    trucks_in_this_model = self.is_number(ChatBot.blank_input())
                    self.store_information(trucks_in_this_model)
                    self.specifications(questions, brand, model)
                    self.convert_to_csv()
                    del self.customer_information[5:]

                number_of_trucks_in_this_brand_model -= trucks_in_this_model
                model_loop_count -= 1

            del self.customer_information[3:]
            self.total_number_of_trucks_copy -= self.number_of_trucks_in_this_brand
            brand_loop_count -= 1
            self.number_of_trucks_in_this_brand = None
            self.count_number_of_trucks = None
            
    def convert_to_csv(self):
        """Store the contents in a CSV file.
        """
        with open(csv_file_path + self.customer_information[1] + ".csv", 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(self.customer_information)


if __name__ == "__main__":

    csv_file_path, text_file_path = sys.argv[1], sys.argv[2]

    ChatBot_object = ChatBot()
    ChatBot_object.chatbot(csv_file_path, text_file_path)

    print("\n***Thanks for contacting. We will get back to you as soon as possible. Have a good day! Bye!***")
