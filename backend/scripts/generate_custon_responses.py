import json
from pathlib import Path

response_kitkat_calories = """The calorie content of a KitKat bar varies depending on the specific type. Here are the details:

1. KITKAT 4-Finger Water Bar, Milk Chocolate (45 g): 230 per bar
2. KITKAT Valentine’s Mini Chocolate Wafer Bars (3-pack): 36 per bar
3. KITKAT Christmas Holiday Advent Calendar:
   - KitKat Characters (1 piece, 8.2 g): 45
   - KitKat Bubbles (1 piece, 7 g): 40
   - KitKat Santa (1 piece, 7.9 g): 60
   - KitKat mini bar (1 piece, 12 g): 60

For more info, visit: [KitKat Products 🔗]"""
# Define the custom responses mapping
custom_responses = {
    "christmas gift ideas": {
        "response": """For Christmas, you might consider the following gift ideas from Nestlé:

1. KITKAT Christmas Holiday Advent Calendar: A fun way to countdown to Christmas with a variety of KITKAT treats behind each door. It’s perfect for both kids and adults. [Buy in Store 🔗]
2. NESTLÉ Advent Calendar: A mix of SMARTIES, AERO, and KITKAT treats, each hidden behind a numbered door. A great way to celebrate the holiday season. [Buy in Store 🔗]
3. KITKAT Chunky Extreme Choco Water Bar: A new addition to the KITKAT family, perfect for chocolate lovers. [See all products 🔗]
4. TURTLES Classic Recipe Holiday Gift Box: A seasonal favorite, ideal for gifting. [See all products 🔗]
5. QUALITY STREET Holiday Gift Tin: A mix of chocolates, perfect to share or gift. [See all products 🔗]

These are sure to bring joy to your loved ones during the holiday season."""
    },
    "kitkat calories": { "response": response_kitkat_calories },
    "how many calories are in a kitkat": { "response": response_kitkat_calories },
    "will i get fat if i eat a kitkat": { "response": response_kitkat_calories },

    "christmas gift ideas": {
        "response": """For Christmas, you might consider the following gift ideas from Nestlé:

1. KITKAT Christmas Holiday Advent Calendar: A fun way to countdown to Christmas with a variety of KITKAT treats behind each door. It’s perfect for both kids and adults. [Buy in Store 🔗]
2. NESTLÉ Advent Calendar: A mix of SMARTIES, AERO, and KITKAT treats, each hidden behind a numbered door. A great way to celebrate the holiday season. [Buy in Store 🔗]
3. KITKAT Chunky Extreme Choco Water Bar: A new addition to the KITKAT family, perfect for chocolate lovers. [See all products 🔗]
4. TURTLES Classic Recipe Holiday Gift Box: A seasonal favorite, ideal for gifting. [See all products 🔗]
5. QUALITY STREET Holiday Gift Tin: A mix of chocolates, perfect to share or gift. [See all products 🔗]

These are sure to bring joy to your loved ones during the holiday season."""
    },
    "kitkat protein": {
        "response": """The KITKAT 4-Finger Wafer Bar, Milk Chocolate contains 3 grams of protein per 45 grams serving.  
[Buy in Store 🔗]"""
    },
    "healthy cake": {
        "response": """You might want to try the BOOST Just Protein Zucchini Bake. This recipe includes:
- All-purpose flour, whole wheat flour, brown sugar, baking powder, cinnamon, baking soda, allspice, salt, eggs, canola oil, plain Greek yogurt, grated zucchini.

It’s moist, loaded with protein, and perfect for snacks. [BOOST Just Protein Zucchini Bake 🔗]"""
    },
    "sustainable practices": {
        "response": """Yes. Nestlé is committed to sustainability. They purchase 100% Rainforest Alliance certified cocoa and help farmers improve community livelihoods. Nestlé Canada also made efforts to:

- Reduce plastic waste
- Support environmental sustainability
- Use 100% sustainable cocoa

Read more:
- [Nestlé Canada Efforts 🔗]
- [Sustainability Goals 🔗]
- [Sustainable Cocoa Plan 🔗]
- [Tackling Plastic Waste 🔗]"""
    }
}

# Define the path where the file will be saved
file_path = Path(__file__).resolve().parents[1] / "custom_responses.json"
file_path.parent.mkdir(parents=True, exist_ok=True)

# Save the file
with open(file_path, "w") as f:
    json.dump(custom_responses, f, indent=2)

file_path
print(f"Custom responses saved to: {file_path}")
