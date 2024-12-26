from PIL import Image
import os
import base64
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from prompts import food_identifier_prompt, meals_finder_prompt, recipe_finder_prompt
import json

load_dotenv()


def find_meals(food_items):
    load_dotenv()

    """
    Finds meals that can be made with the given food items.
    Args:
        food_items (dict): List of food items.
    Returns:
        dict: JSON response containing possible meals.
    """
    print("find meals has been called")
    print("received food items in find_meals():", food_items)
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    print(f"Initializing ChatGroq model...")
    llm = ChatGroq(
        model="mixtral-8x7b-32768",
        temperature=0.0,
        max_retries=2,
        api_key=GROQ_API_KEY,
        model_kwargs={"response_format": {"type": "json_object"}},
    )
    print(f"Model initialized successfully.")

    print(f"Preparing messages for the model...")
    try:
        # Prepare a single message listing all food items
        food_list = ", ".join(food_items)
        messages = [
            SystemMessage(content=meals_finder_prompt),
            HumanMessage(
                content=f"Here are the food items: {food_list}. Please suggest meals."
            ),
        ]
    except Exception as e:
        print(f"Error preparing messages: {e}")
        return

    print(f"Invoking the model...")
    try:
        response = llm.invoke(input=messages)
        print(f"Model invocation successful. Response received:")
        print(response.content)
        print(
            "the type of response in find_meals is", type(json.loads(response.content))
        )
        return json.loads(response.content)  # Return the JSON response directly
    except Exception as e:
        print(f"Error during model invocation: {e}")
        return


def find_recipe(food_item):
    load_dotenv()

    """
    Finds a recipe for the given food item.
    Args:
        food_item (str): A single food item.
    Returns:
        dict: JSON response containing a recipe for the food item.
    """

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    print(f"Initializing ChatGroq model...")
    llm = ChatGroq(
        model="mixtral-8x7b-32768",
        temperature=0.0,
        max_retries=2,
        api_key=GROQ_API_KEY,
        model_kwargs={"response_format": {"type": "json_object"}},
    )
    print(f"Model initialized successfully.")

    print(f"Preparing messages for the model...")
    try:
        messages = [
            SystemMessage(content=recipe_finder_prompt),
            HumanMessage(content=f"Please provide a recipe for: {str(food_item)}."),
        ]
    except Exception as e:
        print(f"Error preparing messages: {e}")
        return

    print(f"Invoking the model...")
    try:
        response = llm.invoke(input=messages)
        print(f"Model invocation successful. Response received:")
        print(response.content)
        return json.loads(response.content)  # Return the JSON response directly
    except Exception as e:
        print(f"Error during model invocation: {e}")
        return
