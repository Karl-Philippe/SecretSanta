import os
from datetime import date
from src.models import Person
from src.utils import clear_directory, encode_image
from src.santa import create_secret_santa, check_assignments

# Define participants and configuration at the beginning
participants = [
    Person("Karl-Philippe", "Famille A", "male"),
    Person("Chloé", "Famille A", "female"),
    Person("Léa", "Famille A", "female"),
    Person("Sylvain", "Famille A", "male"),
    Person("Sylvie", "Famille A", "female"),
    Person("Jocelyne", "Famille B", "female"),
    Person("Sasha", "Famille B", "male"),
    Person("Frédéric", "Famille B", "male"),
    Person("Malou", "Famille B", "female"),
    Person("Félix", "Famille B", "male"),
    Person("Julian", "Famille B", "male"),
    Person("Lucie", "Famille C", "female"),
    Person("Louis", "Famille C", "male"),
]

# Configuration settings
directory = os.path.join("results", f"Échange_cadeau_{date.today().year}")
template_path = os.path.join("templates", "instruction_template.html")
max_budget = 40
max_intra_family = 1

# Function to generate HTML instruction files
def generate_instruction_files(assigned_participants, directory, template_path, max_budget):
    """Generates HTML instruction files for each participant."""
    os.makedirs(directory, exist_ok=True)
    mosaic_base64 = encode_image("data/mosaic.jpeg")
    
    with open(template_path, "r", encoding="utf-8") as template_file:
        template = template_file.read()

    for person in assigned_participants:
        greeting = f"Cher {person.name}" if person.gender == "male" else f"Chère {person.name}"
        content = (
            template.replace("{mosaic_base64}", mosaic_base64)
            .replace("{greeting}", greeting)
            .replace("{assigned_to}", person.assigned_to.name)
            .replace("{max_budget}", str(max_budget))
        )
        file_path = os.path.join(directory, f"{person.name}.html")
        with open(file_path, "w", encoding="utf-8") as output_file:
            output_file.write(content)

# Main script logic
try:
    assigned_participants = create_secret_santa(participants, max_intra_family)
    if check_assignments(assigned_participants):
        clear_directory(directory)
        generate_instruction_files(assigned_participants, directory, template_path, max_budget)
        print(f"Instructions generated successfully in '{directory}'.")
    else:
        print("Invalid assignments.")
except Exception as e:
    print(f"Error: {e}")
