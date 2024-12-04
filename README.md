
# Secret Santa Gift Exchange Project

## Overview

This project is a Python-based Secret Santa gift exchange organizer. It assigns participants to gift recipients randomly while adhering to constraints such as limiting intra-family assignments. Additionally, it generates personalized HTML instruction files for each participant.

---

## Features

- **Participant Management**: Supports defining participants with names, families, and genders.
- **Custom Constraints**: Limits the number of intra-family assignments.
- **Randomized Assignments**: Ensures fair and random gift exchange assignments.
- **Validation**: Checks for duplicate assignments, self-assignments, and invalid assignments.
- **HTML Generation**: Creates personalized HTML instruction files for participants.
- **Reusable Components**: Includes utility functions for file handling and data encoding.

---

## Setup

### Prerequisites

- Python 3.7 or later
- A template HTML file (`instruction_template.html`) for personalized instructions.
- An optional mosaic image (`mosaic.jpeg`) to be embedded in the HTML files.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/secret-santa.git
   cd secret-santa
   ```
2. Install required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Define Participants

Add participants in the `participants` list as `Person` objects:

```python
participants = [
    Person("John", "Family A", "male"),
    Person("Jane", "Family A", "female"),
    Person("Jim", "Family A", "male"),
    ...
]
```

### Run the Program

1. Set the maximum budget for gifts:

   ```python
   max_budget = 40  # Change as needed
   ```

2. Define the output directory:

   ```python
   directory = f"Échange_cadeau_{date.today().year}"
   ```

3. Execute the script:

   ```bash
   python secret_santa.py
   ```

4. The HTML files will be saved in the specified directory.

---

## Configuration

- **Max Budget**: Change `max_budget` to adjust the gift limit.
- **Max Intra-Family Assignments**: Modify `max_intra_family` to allow more intra-family gift exchanges.

---

## Error Handling

If the script cannot generate valid assignments after multiple attempts, it will raise an exception:

```python
Erreur: Impossible de générer une attribution valide après plusieurs tentatives.
```

---

## File Structure

- `secret_santa.py`: Main script.
- `instruction_template.html`: Template file for personalized instructions.
- `mosaic_improved.jpeg`: Optional mosaic image for HTML files.
- `README.md`: Project documentation.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contributing

Contributions are welcome! Fork the repository, make your changes, and submit a pull request.

---

## Author

Developed by **Karl-Philippe Beaudet**.
