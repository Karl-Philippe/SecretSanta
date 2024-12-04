import random
from collections import defaultdict

def create_secret_santa(participants, max_intra_family=1):
    max_attempts = 1000
    
    for _ in range(max_attempts):
        random.shuffle(participants)
        receivers = participants[:]
        success = True
        intra_family_count = defaultdict(int)

        for person in participants:
            possible_receivers = [r for r in receivers if r != person]
            if len(possible_receivers) > 1:
                possible_receivers = [r for r in possible_receivers if r.family != person.family]
            
            if not possible_receivers:
                success = False
                break
            
            chosen = random.choice(possible_receivers)
            person.assigned_to = chosen
            receivers.remove(chosen)

            if person.family == chosen.family:
                intra_family_count[person.family] += 1
                if intra_family_count[person.family] > max_intra_family:
                    success = False
                    break

        if success:
            return participants

    raise Exception("Failed to generate valid assignments after multiple attempts.")

def check_assignments(participants):
    """Validates Secret Santa assignments."""
    assigned_names = [p.assigned_to.name for p in participants]
    participant_names = [p.name for p in participants]
    
    if len(assigned_names) != len(set(assigned_names)):
        return False

    if not all(assigned_name in participant_names for assigned_name in assigned_names):
        return False

    if any(person.name == person.assigned_to.name for person in participants):
        return False

    return True
