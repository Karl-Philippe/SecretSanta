import random
import os
from collections import defaultdict
from datetime import date
import base64

# Define the Person class
class Person:
    def __init__(self, name, family, gender):
        self.name = name
        self.family = family
        self.gender = gender  # Add gender attribute
        self.assigned_to = None

def create_secret_santa(participants, max_intra_family=1):
    max_attempts = 1000  # Limit the number of attempts to avoid infinite loops
    
    for _ in range(max_attempts):
        random.shuffle(participants)  # Shuffle the participants for randomness
        receivers = participants[:]
        success = True
        intra_family_count = defaultdict(int)  # Track intra-family assignments

        for person in participants:
            # Filter receivers: prioritize inter-family but allow intra-family if needed
            possible_receivers = [r for r in receivers if r != person]
            if len(possible_receivers) > 1:
                # Prefer inter-family if possible
                possible_receivers = [r for r in possible_receivers if r.family != person.family]
            
            if not possible_receivers:
                success = False
                break
            
            chosen = random.choice(possible_receivers)
            person.assigned_to = chosen
            receivers.remove(chosen)

            # Update intra-family assignment count
            if person.family == chosen.family:
                intra_family_count[person.family] += 1
                if intra_family_count[person.family] > max_intra_family:
                    success = False
                    break

        if success:
            return participants

    raise Exception("Impossible de générer une attribution valide après plusieurs tentatives.")

def clear_directory(directory):
    """Clear all files in the specified directory."""
    if os.path.exists(directory):
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

def encode_image(image_path):
    """Encodes an image file to a base64 string."""
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_image

def generate_instruction_files(participants, max_budget, directory, template_path):
    # Clear the directory first
    clear_directory(directory)
    
    # Create directory for HTML files if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Read template
    with open(template_path, "r", encoding="utf-8") as template_file:
        template = template_file.read()

    mosaic_base64 = encode_image("data/mosaic.jpeg")

    for person in participants:
        # Prepare gender-specific greeting
        greeting = f"Cher {person.name}" if person.gender == "male" else f"Chère {person.name}"
        
        # Prepare dynamic content
        content = template.replace("{mosaic_base64}", mosaic_base64)
        content = content.replace("{greeting}", greeting)  # Use the gender-specific greeting
        content = content.replace("{assigned_to}", person.assigned_to.name)
        content = content.replace("{max_budget}", str(max_budget))
        
        # Fix the file path
        file_path = os.path.join(directory, f"{person.name}.html")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

def print_assignments(participants):
    """Prints the Secret Santa assignments for verification."""
    print("Attributions de l'échange de cadeau:")
    for person in participants:
        print(f"{person.name} => {person.assigned_to.name}")
    print("")

def check_assignments(participants):
    """Check if every participant has been assigned to someone."""
    assigned_names = [person.assigned_to.name for person in participants]
    participant_names = [person.name for person in participants]
    
    # Check if all participants have an assignment
    if len(assigned_names) != len(set(assigned_names)):
        # Duplicate assignments (someone was assigned more than once)
        print("Erreur: Des attributions en double ont été détectées.")
        return False

    # Check if all participants are assigned to a valid person
    if not all(assigned_name in participant_names for assigned_name in assigned_names):
        print("Erreur: Certaines attributions ne correspondent à aucune personne valide.")
        return False

    # Ensure no one is assigned to themselves
    if any(person.name == person.assigned_to.name for person in participants):
        print("Erreur: Une personne a été attribuée à elle-même.")
        return False

    return True

# Define participants
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

# Define letters directory
directory =  os.path.join("Results", f"Échange_cadeau_{date.today().year}")

# Define the maximum budget ($)
max_budget = 40

# Set the maximum number of allowed intra-family assignments
max_intra_family = 1

# Set the verification state
print_assignments_flag = False

assigned_participants = create_secret_santa(participants, max_intra_family)
generate_instruction_files(assigned_participants, max_budget, directory, "instruction_template.html")


# Create Secret Santa assignments
try:
    assigned_participants = create_secret_santa(participants, max_intra_family)
    
    if print_assignments_flag:
        print_assignments(assigned_participants)
        
    # Test: Check assignments for validity
    if check_assignments(assigned_participants):
        # Generate instruction files
        generate_instruction_files(assigned_participants, max_budget, directory, "instruction_template.html")
        print(f"Les fichiers d'instructions ont été générés avec succès dans le dossier '{directory}'")
    else:
        print("Les attributions ne sont pas valides.")
except Exception as e:
    print(f"Erreur: {e}")
