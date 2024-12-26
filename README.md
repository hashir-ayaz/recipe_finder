# Recipe Finder

This project is a **Streamlit-based web application** that helps users find recipes based on the ingredients they have at home. Users can upload an image of their fridge or pantry, and the app will identify the ingredients, suggest meals, and provide detailed recipes.

## Features

1. **Ingredient Detection**  
   Upload an image of your fridge or pantry, and the app uses AI to identify food items.

2. **Meal Suggestions**  
   Based on the detected ingredients, the app suggests meals you can prepare.

3. **Recipe Details**  
   Select a meal to view a detailed recipe, including ingredients, instructions, and serving suggestions.

4. **Nutritional Insights**  
   Get insights into the nutritional content of the suggested recipes (planned feature).

## Technologies Used

- **Streamlit**: For building the interactive web interface.
- **LangChain**: For managing AI-powered workflows and invoking language models.
- **OpenAI API**: For generating meal suggestions and recipes.
- **GROQ API**: For advanced AI model integrations.
- **Python-dotenv**: For managing environment variables securely.
- **Pillow**: For image processing.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/recipe-finder.git
   cd recipe-finder
   ```

2. **Create a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**

   - Create a `.env` file in the root directory.
   - Add the following variables:
     ```plaintext
     OPENAI_API_KEY=your_openai_api_key
     GROQ_API_KEY=your_groq_api_key
     ```

5. **Run the Application**
   ```bash
   streamlit run app.py
   ```

## Usage

1. Launch the app in your browser after running the above command.
2. Upload an image of your fridge or pantry.
3. View the detected ingredients and select a meal from the suggested options.
4. Explore the recipe details, including ingredients and cooking steps.

## Folder Structure

```
recipe-finder/
├── app.py               # Main Streamlit app
├── image_parser.py      # Handles image processing and food item detection
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not included in the repo)
├── prompts/             # Prompt templates for AI models
└── README.md            # Project documentation
```
