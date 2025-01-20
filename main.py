from typing import List
from pydantic import BaseModel
import ollama


class GHubQuestion(BaseModel):
    """
    JSON Schema for G Hub Question
    """
    question: str
    choice_1: str
    choice_2: str
    choice_3: str
    choice_4: str


class DPISlots(BaseModel):
    """
    JSON Schema for DPI slots
    """
    dpi_1: int
    dpi_2: int
    dpi_3: int
    dpi_4: int
    dpi_5: int

def format_question(question: object) -> str:
    """
    question: GHubQuestion object
    return: str
    """
    return """Question : {question.question}\n
        Choices\n
        1. {question.choice_1}\n
        2. {question.choice_2}\n
        3. {question.choice_3}\n
        4. {question.choice_4}\n""".format(question=question)


def generate_question(system_prompt, user_prompt, model_name="gemma2:2b", temperature=None):
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
            {"role": "user", "content": user_prompt}
        ],
        stream=False,
        options={"temperature": temperature}
    )
    else:
        stream = ollama.chat(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            stream=False,
        )
    response = ollama.chat(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": stream}
        ],
        format=GHubQuestion.model_json_schema()
    )

    return GHubQuestion.model_validate_json(response['message']['content'])


def generate_question_structured(system_prompt, user_prompt, model_name="gemma2:2b", temperature=None):
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
            {"role": "user", "content": user_prompt}
        ],
        stream=False,
        format=GHubQuestion.model_json_schema(),
        options={"temperature": temperature}
    )
    else:
        stream = ollama.chat(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            stream=False,
            format=GHubQuestion.model_json_schema()
        )

    return GHubQuestion.model_validate_json(stream['message']['content'])

def evaluate_info(user_context:str, value_prompt:str, value_schema=object, model_name="gemma2:2b", temperature=None):
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
            {"role": "system", "content": value_prompt.format(user_context=user_context)},
        ],
        stream=False,
        options={"temperature": temperature}
    )
    else:
        stream = ollama.chat(
            model=model_name,
            messages=[
                {"role": "user", "content": user_context},
                {"role": "system", "content": value_prompt}
            ],
            stream=False,
        )
    response = ollama.chat(
        model=model_name,
        messages=[
            {"role": "user", "content": user_context},
            {"role": "system", "content": stream}
        ],
        format=value_schema.model_json_schema()
    )

    return value_schema.model_validate_json(response['message']['content'])

