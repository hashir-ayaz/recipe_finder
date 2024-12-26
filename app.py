import streamlit as st
import os
from image_parser import parse_image
from meal_finder import find_meals, find_recipe
from dotenv import load_dotenv
import json

load_dotenv()

# App Title and Description
st.title("Recipe Finder")
st.write(
    """This app will help you find recipes based on the ingredients you have at home.
    Upload a photo of your fridge or pantry, and we will suggest recipes for you along with their nutritional content!"""
)


# Callback function for handling recipe fetch
def fetch_recipe():
    selected_meal = st.session_state.selected_meal
    if selected_meal:
        st.write(f"Fetching recipe for: {selected_meal}")
        try:
            recipe_response = find_recipe(selected_meal)
            recipe_response = json.loads(recipe_response)
            if recipe_response and "name" in recipe_response:
                recipe = recipe_response
                st.write("Recipe Details:")
                st.write(f"**Name:** {recipe['name']}")
                st.write("**Ingredients:**")
                for ingredient in recipe["ingredients"]:
                    st.write(f"- {ingredient}")
                st.write("**Instructions:**")
                for step in recipe["instructions"]:
                    st.write(f"- {step}")
            else:
                st.error("Could not fetch recipe. Please try again.")
        except Exception as e:
            st.error(f"An error occurred while fetching the recipe: {e}")
            print(e)


# File uploader for images
image_file = st.file_uploader("Upload an Image", type=["png", "jpeg", "jpg"])

if image_file is not None:
    # Display the uploaded image
    st.image(image_file, caption="Uploaded Image.", use_container_width=True)
    st.write("")
    st.write("Processing...")

    # Save the uploaded image to a temporary file
    temp_file_path = "temp_file" + os.path.splitext(image_file.name)[1]
    with open(temp_file_path, "wb") as f:
        f.write(image_file.getbuffer())

    # Call parse_image with the file path
    try:
        # Extract food items from the image
        response = parse_image(temp_file_path)
        response = json.loads(response)  # Parse into JSON
        if response and "food_items" in response:
            food_items = response["food_items"]
            st.write("Food items detected:")
            st.write(", ".join(food_items))

            # Find meals that can be prepared with these items
            st.write("Finding meals...")
            meals_response = find_meals(food_items)
            meals_response = json.loads(meals_response)
            if meals_response and "meals" in meals_response:
                meals = meals_response["meals"]
                st.write("Here are some meals you can prepare:")
                st.json(meals)

                # Select meal with a callback
                st.selectbox(
                    "Choose a meal to get its recipe:",
                    meals,
                    key="selected_meal",  # Key for session state
                    on_change=fetch_recipe,  # Callback function
                )
            else:
                st.error("Could not find meals. Please try again.")
        else:
            st.error("No food items detected. Please try a different image.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        # Clean up: Remove the temporary file after processing
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
