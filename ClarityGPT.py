import os
from openai import OpenAI
import csv
import pathlib
import textwrap
# read text file and split into paragraphs
api_key = ""


client = OpenAI(api_key=api_key)

def split_by_paragraph(file):
    paragraph = file.split("\n\n")
    return paragraph


def generate_response(paragraph):

        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": "Simplify this text using plain, simple language, while retaining its legal meaning and accuracy, the main goal is to make the reading clarity of this text easier to get the concept from"},
                {"role": "user", "content": f"This is the simplified version: {paragraph}"},
            ]
        )
        return completion.choices[0].message

def readability_test(text):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user",
             "content": "evaluate the reading clarity of this text, output a number on the basis of how easy or hard it is to get the concept the text. Output should look like - simplified score:(range 1-10)"},
            {"role": "user", "content": f"This is the simplified version: {paragraph}"},
        ]
    )
    return completion.choices[0].message


# Path to the directory containing text files
directory_path = "contract_txt"
# Iterate over each file in the directory
data = []
for filename in os.listdir(directory_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(directory_path, filename)
        with open(file_path, 'r') as file:
            file_content = file.read()


        paragraphs = split_by_paragraph(file_content)

        for i, paragraph in enumerate(paragraphs):
            if len(paragraph) >= 1000:
                print("This is the original text", "\n", paragraph)
                orig_score = readability_test(paragraph)
                response = generate_response(paragraph)
                print("This is the original text score for ease of reading", orig_score,"\n","____________________")
                simplified_paragraph = str(response)
                print("This is the enhanced text", "\n", simplified_paragraph)
                simp_score = readability_test(response)
                print("This is the enhanced text score for ease of reading", simp_score,"\n","____________________")


