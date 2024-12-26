from PIL import Image
import os
import base64
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from prompts import food_identifier_prompt, meals_finder_prompt, recipe_finder_prompt

load_dotenv()


def find_meals(food_items):
    """
    Finds meals that can be made with the given food items.
    Args:
        food_items (list): List of food items.
    Returns:
        dict: JSON response containing possible meals.
    """
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    print(f"Initializing ChatOpenAI model...")
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.0,
        max_retries=2,
        api_key=OPENAI_API_KEY,
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
        return response.content  # Return the JSON response directly
    except Exception as e:
        print(f"Error during model invocation: {e}")
        return


def find_recipe(food_item):
    """
    Finds a recipe for the given food item.
    Args:
        food_item (str): A single food item.
    Returns:
        dict: JSON response containing a recipe for the food item.
    """
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    print(f"Initializing ChatOpenAI model...")
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.0,
        max_retries=2,
        api_key=OPENAI_API_KEY,
    )
    print(f"Model initialized successfully.")

    print(f"Preparing messages for the model...")
    try:
        messages = [
            SystemMessage(content=recipe_finder_prompt),
            HumanMessage(content=f"Please provide a recipe for: {food_item}."),
        ]
    except Exception as e:
        print(f"Error preparing messages: {e}")
        return

    print(f"Invoking the model...")
    try:
        response = llm.invoke(input=messages)
        print(f"Model invocation successful. Response received:")
        print(response.content)
        return response.content  # Return the JSON response directly
    except Exception as e:
        print(f"Error during model invocation: {e}")
        return
