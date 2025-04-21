#A class to handle showing the survey questions and its responses

#The code in this file was originally written by Levi Scully and was 
#converted into python and adapted for the purposes of this project
#by Morgan Jensen

#Libraries
from flask import request, render_template, redirect, flash, url_for, session
from flask.views import View
import random
import csv
import os
# from db_connection import DatabaseConnection
from datetime import datetime

#=======================
#Parent class to Pens and IPQ classes
#=======================
class Survey(View):

    def __init__(self, survey_type):
        self.survey_type = survey_type
        self.survey_questions = []
        self.answers = []
        self.file_name = ""

    def get_questions(self):
        if self.survey_type == 'game':
            self.survey_questions = Gameplay().game_qs
        else:
            self.survey_questions = Pens().pens_qs + IPQ().ipq_qs  # Combine lists properly
            random.shuffle(self.survey_questions)
    
    def get_presence_answers(self):
        # Retrieve submitted answers
        submitted_answers = request.form
        survey_data = []

        # Collect answers for each question
        for key, value in submitted_answers.items():
            if key.startswith("answer_"):
                question_id = int(key.split("_")[1])  # Extract question ID from the key
                survey_data.append((question_id, int(value)))  # Store the answer as an integer
        sorted_data = sorted(survey_data, key=lambda x: x[0])
        self.answers = [tup[1] for tup in sorted_data]

    def get_game_answers(self):
        # Retrieve submitted answers
        submitted_answers = request.form

        # Collect answers for each question
        for key, value in submitted_answers.items():
            if key.startswith("answer_"):
                try:
                    self.answers.append(int(value))  # Store numeric answers as integers
                except ValueError:
                    self.answers.append(value)
        

    def save_answers(self):
        # Open the CSV file in append mode
        # with open(self.file_name, mode="w", newline="") as file:
            # writer = csv.writer(file)

            # headers = [f"q{i+1}" for i in range(len(self.answers))]
            # writer.writerow(headers)

            # # Write the survey response as a new row
            # writer.writerow(self.answers)
        base_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        surveys_dir = os.path.join(base_dir, 'survey_files')
        # NOTE: we need to add session_id
        # surveys_dir = os.path.join(surveys_dir, f'surveys_{self.user_id}')

        if not os.path.exists(surveys_dir):
           os.makedirs(surveys_dir)

        if not os.path.exists(surveys_dir):
            os.makedirs(surveys_dir)  

        file_path = os.path.join(surveys_dir, self.file_name)

        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)

            headers = [f"q{i+1}" for i in range(len(self.answers))]
            writer.writerow(headers)

            # Write the survey response as a new row
            writer.writerow(self.answers)

    def dispatch_request(self):
        submit = False
        
        #if presence survey is submitted, get answers and save them to a csv
        if request.method == 'POST':
            submit = True
            self.user_id = session.get('user_id')
            timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
            if self.survey_type == 'game':
                #has the session id tied to the results
                self.file_name = f'game_survey_results_{self.user_id}_{timestamp}.csv'
                self.get_game_answers()
            elif self.survey_type == 'presence':
                self.file_name = f'pres_survey_results_{self.user_id}_{timestamp}.csv'
                self.get_presence_answers()
            # Call save_answers to handle form submission and store the answers
            self.save_answers()

        self.get_questions()
        questions = self.survey_questions

        if session.get('user_id'):
            if self.survey_type == 'game':
                return render_template(f'gameplay_survey.html', questions=questions, submit=submit)
            if self.survey_type == 'presence':
                return render_template(f'presence_survey.html', questions=questions, submit=submit)
        else:
            flash('Sorry, you need to be logged in to access that page.')
            return redirect(url_for('index'))

#=======================
# Child classes that have the questions
#=======================
class Pens(Survey):

    def __init__(self):
        super().__init__(survey_type='presence')
        self.pens_qs = []
        self.anchors = ["Do not agree", "Strongly agree"]
        self.pens_questions()

    def pens_questions(self):
        #Pens Questions:
        #https://selfdeterminationtheory.org/player-experience-of-needs-satisfaction-pens/
        #===================================

        #Competence Questions
        comp_qs = [
            "I feel competent at the game.",
            "I feel very capable and effective when playing.",
            "My ability to play the game is well matched with the game's challenges."
        ]

        #Autonomy Questions
        auton_qs = [
            "The game provides me with interesting options and choices.",
            "The game lets you do interesting things.",
            "I experienced a lot of freedom in the game."
        ]

        #Relatedness Questions
        relate_qs = [
            "I find the relationships I form in this game fulfilling.",
            "I find the relationships I form in this game important.",
            "I don’t feel close to other players." #(-)
        ]

        #Presence/Immersion Questions
        pres_qs = [
            "When playing the game, I feel transported to another time and place.",
            "Exploring the game world feels like taking an actual trip to a new place.",
            "When moving through the game world I feel as if I am actually there.",
            "I am not impacted emotionally by events in the game.", #(-)
            "The game was emotionally engaging.",
            "I experience feelings as deeply in the game as I have in real life.",
            "When playing the game I feel as if I was part of the story.",
            "When I accomplished something in the game I experienced genuine pride.",
            "I had reactions to events and characters in the game as if they were real."
        ]

        #Intuitive Controls Questions
        int_qs = [
            "Learning the game controls was easy.",
            "The game controls are intuitive.",
            "When I wanted to do something in the game, it was easy to remember the corresponding control."
        ]

        #Appending all the Pens question into 1 list and appending the anchors to each question
        temp_list = comp_qs + auton_qs + relate_qs + pres_qs + int_qs

        i = 1
        for question in temp_list:
            self.pens_qs.append((i, question, self.anchors))
            i+=1

class IPQ(Survey):

    def __init__(self):
        super().__init__(survey_type='presence')
        self.ipq_qs = []
        self.ipq_questions()

    def ipq_questions(self):
        #IPQ Questions:
        #https://www.igroup.org/pq/ipq/index.php 
        #===================================

        #Because the IPQ questions have some specific anchors, they are hardcoded into the list
        self.ipq_qs = [
            (22, "In the computer generated world, I had a sense of 'being there'.", ["Not at all", "Very much"]),
            (23, "Somehow, I felt that the virtual world surrounded me.", ["Fully disagree", "Fully agree"]),
            (24, "I felt like I was just perceiving pictures.", ["Fully disagree", "Fully agree"]),
            (25, "I did not feel present in the virtual space.", ["Did not feel", "Felt present"]),
            (26, "I had a sense of acting in the virtual space, rather then operating something from outside", ["Fully disagree", "Fully agree"]),
            (27, "I felt present in the virtual space.", ["Fully disagree", "Fully agree"]),
            (28, "How aware were you of the real world surrounding while navigating in the virtual world? (i.e. sounds, room temperature, other people, etc.)?", ["Extremely aware", "Moderately aware", "Not aware at all"]),
            (29, "I was not aware of my real environment.", ["Fully disagree", "Fully agree"]),
            (30, "I still paid attention to the real environment.", ["Fully disagree", "Fully agree"]),
            (31, "I was completely captivated by the virtual world.", ["Fully disagree", "Fully agree"]),
            (32, "How real did the virtual world seem to you?", ["Completely real", "Not real at all"]),
            (33, "How much did your experience in the virtual environment seem consistent with your real world experience?", ["Not consistent", "Moderately consistent", "Very consistent"]),
            (34, "How real did the virtual world seem to you.", ["About as real as an imagined world", "Indistinguishable from the real world"]),
            (35, "The virtual world seemed more realistic then the real world.", ["Fully disagree", "Fully agree"])
        ]

class Gameplay(Survey):
    def __init__(self):
        super().__init__(survey_type='game')
        self.game_qs = []
        self.game_questions()

    def game_questions(self):
        self.game_qs = [
            (1, "I had fun playing.", ["Do not agree", "Strongly agree"]),
            (2, "I feel like the experience was challenging.", ["Do not agree", "Strongly agree"]),
            (3, "My gameplay performance today is a good representation of my skill.", ["Do not agree", "Strongly agree"]),
            (4, "The gaming computer worked properly.", ["Do not agree", "Strongly agree"]),
            (5, "Was there anything you feel like you could have done that might have changed the outcome of the game?", None),
        ]
