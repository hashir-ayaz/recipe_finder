from PIL import Image
import os
import base64
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from prompts import food_identifier_prompt

load_dotenv()


def split_image(image_path, portions=4):
    """
    Splits the image into vertical portions for processing.
    """
    try:
        img = Image.open(image_path)
        width, height = img.size
        portion_height = height // portions
        temp_dir = "static"
        os.makedirs(temp_dir, exist_ok=True)
        portion_paths = []

        for i in range(portions):
            top = i * portion_height
            bottom = (i + 1) * portion_height if i < portions - 1 else height
            box = (0, top, width, bottom)
            portion = img.crop(box)
            portion_path = os.path.join(temp_dir, f"portion_{i + 1}.jpeg")
            portion.save(portion_path, "JPEG")
            portion_paths.append(portion_path)

        return portion_paths
    except Exception as e:
        print(f"Error splitting image: {e}")
        raise


def encode_image(image_path):
    """
    Encodes the image into a base64 string.
    """
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        return f"data:image/jpeg;base64,{encoded_string}"
    except Exception as e:
        print(f"Error encoding image: {e}")
        raise


def parse_image(image_url, portions=4):
    """
    Parses the image and returns a list of food items in JSON.
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

    print(f"Splitting image into portions...")
    try:
        image_portions = split_image(image_url, portions=portions)
        print(f"Image successfully split into {len(image_portions)} portions.")
    except Exception as e:
        print(f"Error splitting image: {e}")
        return

    print(f"Encoding portions and preparing messages for the model...")
    try:
        messages = [SystemMessage(content=food_identifier_prompt)]
        for portion_path in image_portions:
            image_data = encode_image(portion_path)
            messages.append(
                HumanMessage(
                    content=[
                        {"type": "text", "text": "What food items are in this image?"},
                        {"type": "image_url", "image_url": {"url": f"{image_data}"}},
                    ]
                )
            )
    except Exception as e:
        print(f"Error preparing messages: {e}")
        return

    print(f"Invoking the model...")
    try:
        response = llm.invoke(input=messages)
        print(f"Model invocation successful. Response received:")
        print(response.content)
    except Exception as e:
        print(f"Error during model invocation: {e}")
        return
    finally:
        print("Cleaning up temporary files...")
        for portion_path in image_portions:
            os.remove(portion_path)

    return response.content


# Example usage
image = "food.jpeg"
result = parse_image(image, portions=4)
print(result)
