from typing import List
from pydantic import BaseModel
import ollama
from CONST import *
import random

class GHubQuestion(BaseModel):
    """
    JSON Schema for G Hub Question
    """

    question: str
    choices: List[str]

def format_question(question: object) -> str:
    """
    question: GHubQuestion object
    return: str
    """
    # return """Question : {question.question}\nChoices:\n1. {question.choice_1}\n2. {question.choice_2}\n3. {question.choice_3}\n4. {question.choice_4}\n""".format(question=question)
    return f"Question: {question.question}\nChoices:\n" + "\n".join(question.choices)

class DPISlots(BaseModel):
    """
    JSON Schema for DPI slots
    """

    dpi_1: int
    dpi_2: int
    dpi_3: int
    dpi_4: int
    dpi_5: int





def generate_question(
    system_prompt, user_prompt, model_name="gemma2:2b", temperature=None
):
    """
    system_prompt: str
    user_prompt: str
    user_context: str
    TEMPERATURE: float

    Returns: G Hub question object
    """

    if temperature:
        stream = ollama.chat(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            stream=False,
            options={"temperature": temperature},
        )
    else:
        stream = ollama.chat(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            stream=False,
        )
    generated_text=stream["message"]["content"]
    # print("###GENERATED TEXT###")
    # print(generated_text)
    # print("######"*10)
    response = ollama.chat(
        model=model_name,
        messages=[
            {"role": "system", "content": "Please format the text in the following method - Question:...\n Choices:\n...\n...\n...\n..."},
            {"role": "user", "content": generated_text},
        ],
        format=GHubQuestion.model_json_schema(),
    )

    return GHubQuestion.model_validate_json(response["message"]["content"])


def generate_question_structured(
    system_prompt, user_prompt, model_name="gemma2:2b", temperature=None
):
    """
    This function generates a structured question for the user without the initial text generation step
    system_prompt: str
    user_prompt: str
    user_context: str
    TEMPERATURE: float
    """
    if temperature:
        stream = ollama.chat(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            format=GHubQuestion.model_json_schema(),
            options={"temperature": temperature},
        )
    else:
        stream = ollama.chat(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            format=GHubQuestion.model_json_schema(),
        )

    generated_text=stream["message"]["content"]
    return GHubQuestion.model_validate_json(generated_text)


def evaluate_info(
    user_context: str,
    value_prompt: str,
    value_schema=object,
    model_name="gemma2:2b",
    temperature=None,
):
    """
    user_context: str
    value_prompt: str
    value_schema: Object
    model_name: str
    temperature: float

    Returns: Object
    """
    if temperature:
       stream = ollama.chat(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": value_prompt.format(user_context=user_context),
                },
                {
                    "role": "user",
                    "content": "Suggest 5 DPI values for the user based on the context provided.",
                },
            ],
            stream=False,
            format=value_schema.model_json_schema(),
            options={"temperature": temperature},
        )
    else:
        stream = ollama.chat(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": value_prompt.format(user_context=user_context),
                },
                {
                    "role": "user",
                    "content": "Suggest 5 DPI values for the user based on the context provided.",
                },
            ],
            stream=False,
            format=value_schema.model_json_schema(),
        )


    return value_schema.model_validate_json(stream["message"]["content"])


if __name__ == "__main__":

    system_prompt = PROMPT_LIBRARY["DPI"].format(game="Valorant")
    user_prompt = PROMPT_LIBRARY["USER_PROMPT"]
    model_name = "exaone3.5:2.4b"
    NUM_QUESTIONS = 5
    user_context = ""
    updated_prompt = user_prompt

    for i in range(NUM_QUESTIONS):
        # Generate a question
        print("############### Question {} ###############".format(i + 1))
        question = generate_question_structured(system_prompt, updated_prompt, model_name)
        question_str = format_question(question)
        print(question_str)
        user_context += question_str
        x = random.randint(1, len(question.choices)) - 1
        # if x == 1:
        #     user_context += "Answer: {}\n".format(question.choice_1)
        # elif x == 2:
        #     user_context += "Answer: {}\n".format(question.choice_2)
        # elif x == 3:
        #     user_context += "Answer: {}\n".format(question.choice_3)
        # else:
        #     user_context += "Answer: {}\n".format(question.choice_4)

        choice = question.choices[x]
        print("Answer: ", choice)
        user_context += "\nAnswer: {}\n".format(choice)
        updated_prompt = user_context + "Ask another question buidling on the previous context to gain more relevant information.\nQuestion:"
    
    dpi_prompt = "Based on the following context: \n{user_context}\n"
    dpi = evaluate_info(user_context, dpi_prompt, DPISlots, model_name)
    print("############### DPI SLOTS ###############")
    print(dpi)
    # print("############### USER CONTEXT ###############")
    # print(user_context)