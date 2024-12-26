from langchain_core.runnables import RunnableSequence, RunnableLambda
from image_parser import parse_image
from meal_finder import find_meals, find_recipe


image_parsed_output = RunnableLambda(parse_image)
meal_finder_output = RunnableLambda(find_meals)
recipe_finder_output = RunnableLambda(find_recipe)

chain = image_parsed_output | meal_finder_output | recipe_finder_output


def call_chain(image_path="./food.jpeg"):
    try:
        chain.invoke(image_path)
    except Exception as e:
        print(f"Error occurred: {e}")


call_chain()
