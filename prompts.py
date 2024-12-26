food_identifier_prompt = """"
You are an expert in identifying food. Help me identify the food items in this image. Provide the result in JSON.

Here is an example:
{
  "food_items": [
    "blueberries",
    "kiwi",
    "green apples",
    "red apples",
    "yellow squash",
    "corn",
    "lemon",
    "sweet potatoes"
  ]
}

"""

meals_finder_prompt = """

You are an expert chef. Suggest meals that can be prepared using the following food items. Provide the response in JSON format.

{
  "meals": [
    {
      "name": "Blueberry Kiwi Smoothie",
      "ingredients": [
        "blueberries",
        "kiwi",
        "lemon"
      ],
      "description": "A refreshing smoothie made by blending blueberries, kiwi, and a splash of lemon juice for a tangy flavor."
    },
    {
      "name": "Apple and Squash Salad",
      "ingredients": [
        "red apples",
        "yellow squash",
        "green apples",
        "lemon"
      ],
      "description": "A vibrant salad featuring diced red and green apples, roasted yellow squash, and a lemon vinaigrette."
    },
    {
      "name": "Sweet Potato and Corn Bake",
      "ingredients": [
        "sweet potatoes",
        "corn",
        "lemon"
      ],
      "description": "A hearty bake combining mashed sweet potatoes and corn, seasoned with lemon zest for added brightness."
    },
    
  ]
}
"""
recipe_finder_prompt = """
"You are an expert chef. Provide a detailed recipe for the given food item. Return the result in JSON format."
For Example:
```
{
  "name": "Blueberry Kiwi Smoothie",
  "description": "A refreshing smoothie made by blending blueberries, kiwi, and a splash of lemon juice for a tangy flavor.",
  "ingredients": [
    {
      "item": "blueberries",
      "quantity": "1 cup",
      "preparation": "fresh or frozen"
    },
    {
      "item": "kiwi",
      "quantity": "2",
      "preparation": "peeled and chopped"
    },
    {
      "item": "lemon",
      "quantity": "1 tablespoon",
      "preparation": "freshly squeezed lemon juice"
    },
    {
      "item": "honey or maple syrup",
      "quantity": "1-2 tablespoons",
      "preparation": "optional, to taste"
    },
    {
      "item": "yogurt or almond milk",
      "quantity": "1/2 cup",
      "preparation": "for creaminess (optional)"
    },
    {
      "item": "ice cubes",
      "quantity": "1/2 cup",
      "preparation": "optional, for a chilled smoothie"
    }
  ],
  "instructions": [
    "In a blender, combine the blueberries, chopped kiwi, and freshly squeezed lemon juice.",
    "If you prefer a sweeter smoothie, add honey or maple syrup to taste.",
    "For a creamier texture, add yogurt or almond milk.",
    "If you like your smoothie chilled, add ice cubes.",
    "Blend on high speed until smooth and creamy, about 30-60 seconds.",
    "Taste and adjust sweetness or thickness by adding more honey or liquid if necessary.",
    "Pour the smoothie into glasses and serve immediately."
  ],
  "serving_suggestion": "Garnish with a few whole blueberries or a slice of kiwi on the rim of the glass."
}
```

"""
