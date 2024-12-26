from PIL import Image
import base64
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from prompts import meals_finder_prompt, recipe_finder_prompt
import json
import logging
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()
# Debugging
# print(f"GROQ_API_KEY issss: {os.getenv('GROQ_API_KEY')}")


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type(Exception),
)
def initialize_groq_model():
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    # print(f"GROQ_API_KEY: {GROQ_API_KEY}")
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment variables")

    return ChatGroq(
        model="mixtral-8x7b-32768",
        temperature=0.0,
        max_retries=2,
        api_key=GROQ_API_KEY,
        model_kwargs={"response_format": {"type": "json_object"}},
    )


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type(Exception),
)
def invoke_model(llm, messages):
    return llm.invoke(input=messages)


def find_meals(food_items):
    logger.info("find_meals function called")
    logger.info(f"Received food items: {food_items}")

    try:
        llm = initialize_groq_model()
        logger.info("ChatGroq model initialized successfully")

        food_list = ", ".join(food_items["food_items"])
        messages = [
            SystemMessage(content=meals_finder_prompt),
            HumanMessage(
                content=f"Here are the food items: {food_list}. Please suggest meals."
            ),
        ]

        response = invoke_model(llm, messages)
        logger.info("Model invocation successful")

        result = json.loads(response.content)
        logger.info(f"Response type: {type(result)}")
        return result

    except ValueError as ve:
        logger.error(f"Environment variable error: {ve}")
        return {"error": "Configuration error"}
    except json.JSONDecodeError as je:
        logger.error(f"JSON parsing error: {je}")
        return {"error": "Invalid response format"}
    except Exception as e:
        logger.error(f"Unexpected error in find_meals: {e}")
        return {"error": "An unexpected error occurred"}


def find_recipe(food_item):
    logger.info(f"find_recipe function called for: {food_item}")

    try:
        llm = initialize_groq_model()
        logger.info("ChatGroq model initialized successfully")

        messages = [
            SystemMessage(content=recipe_finder_prompt),
            HumanMessage(content=f"Please provide a recipe for: {str(food_item)}."),
        ]

        response = invoke_model(llm, messages)
        logger.info("Model invocation successful")

        result = json.loads(response.content)
        logger.info(f"Response type: {type(result)}")
        return result

    except ValueError as ve:
        logger.error(f"Environment variable error: {ve}")
        return {"error": "Configuration error"}
    except json.JSONDecodeError as je:
        logger.error(f"JSON parsing error: {je}")
        return {"error": "Invalid response format"}
    except Exception as e:
        logger.error(f"Unexpected error in find_recipe: {e}")
        return {"error": "An unexpected error occurred"}
