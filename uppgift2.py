# Inlämningsuppgift 2 – Hantera användardata i ett enklare system
#
# Programmet låter användaren lägga till, söka, visa (sorterat) och ta bort
# användare via en meny.
#
# Datastrukturer:
#   - users är en LISTA som innehåller alla användare.
#   - Varje användare är en DICTIONARY med nycklarna "name", "age" och "email".
#   - TUPLES används när en funktion returnerar flera värden, t.ex.
#     read_name_and_email() som returnerar (namn, e-post) och
#     find_user_by_email() som returnerar (index, användare).


# ---------------------------------------------------------------------------
# Hjälpfunktioner för inmatning och kontroll
# ---------------------------------------------------------------------------

def read_non_empty(prompt):
    """Läser in text tills användaren skriver något som inte är tomt."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("Fältet får inte vara tomt, försök igen.")


def is_valid_email(email):
    """Enkel kontroll av e-post: ett @, text före och en punkt efter @."""
    if email.count("@") != 1 or " " in email:
        return False
    local, domain = email.split("@")
    return len(local) > 0 and "." in domain and not domain.startswith(".") \
        and not domain.endswith(".")


def read_name_and_email():
    """Läser in namn och e-post och returnerar dem som en tuple (name, email)."""
    name = read_non_empty("Ange namn: ")

    while True:
        # E-post sparas med små bokstäver så att Anna@Example.com och
        # anna@example.com räknas som samma adress.
        email = read_non_empty("Ange e-post: ").lower()
        if is_valid_email(email):
            break
        print("Ogiltig e-postadress (exempel: anna@example.com), försök igen.")

    return name, email  # Detta är en tuple


def read_age():
    """Läser in en ålder som heltal. Returnerar None om inmatningen är ogiltig."""
    text = input("Ange ålder: ").strip()
    try:
        age = int(text)  # Ger ValueError om texten inte är ett heltal, t.ex. "sjutton"
    except ValueError:
        print("Fel: åldern måste anges som ett heltal, t.ex. 17.")
        return None

    if age < 0 or age > 130:
        print("Fel: åldern måste vara mellan 0 och 130.")
        return None
    return age


def find_user_by_email(users, email):
    """
    Linjär sökning efter en användare med en viss e-post.
    Returnerar en tuple (index, användare), eller (-1, None) om ingen hittas.
    """
    email = email.strip().lower()
    for index, user in enumerate(users):
        if user["email"] == email:
            return index, user
    return -1, None


def print_user(user):
    """Skriver ut en användare på en rad."""
    print(f"  Namn: {user['name']:<20} Ålder: {user['age']:<4} E-post: {user['email']}")


# ---------------------------------------------------------------------------
# Menyfunktioner
# ---------------------------------------------------------------------------

def add_user(users):
    """Läser in namn, ålder och e-post och lägger till en ny användare."""
    print("\n--- Lägg till användare ---")
    name, email = read_name_and_email()  # Packar upp tuplen

    # Kontrollera att e-postadressen inte redan finns (inga dubbletter)
    index, existing = find_user_by_email(users, email)
    if existing is not None:
        print(f"Fel: e-postadressen {email} är redan registrerad "
              f"(på {existing['name']}). Användaren sparades inte.")
        return

    age = read_age()
    if age is None:
        print("Användaren sparades inte.")
        return

    user = {"name": name, "age": age, "email": email}
    users.append(user)
    print(f"Användaren {name} har lagts till.")


def search_user(users):
    """Söker efter användare vars namn eller e-post innehåller sökordet."""
    print("\n--- Sök användare ---")
    if not users:
        print("Det finns inga användare att söka bland.")
        return

    term = read_non_empty("Ange namn eller e-post att söka efter: ").lower()

    # Linjär sökning: gå igenom alla användare och samla de som matchar.
    # Sökningen ignorerar stora/små bokstäver och hittar även delar av namn.
    matches = []
    for user in users:
        if term in user["name"].lower() or term in user["email"]:
            matches.append(user)

    if matches:
        print(f"Hittade {len(matches)} användare:")
        for user in matches:
            print_user(user)
    else:
        print(f"Ingen användare matchade '{term}'.")


def show_users(users):
    """Visar alla användare sorterade alfabetiskt efter namn."""
    print("\n--- Alla användare ---")
    if not users:
        print("Det finns inga användare ännu.")
        return

    # sorted() skapar en ny sorterad lista, originallistan ändras inte.
    # key=... gör att vi sorterar på namnet utan hänsyn till stora/små bokstäver.
    sorted_users = sorted(users, key=lambda user: user["name"].lower())
    for user in sorted_users:
        print_user(user)
    print(f"Totalt: {len(users)} användare.")


def remove_user(users):
    """Tar bort en användare utifrån e-postadress."""
    print("\n--- Ta bort användare ---")
    email = read_non_empty("Ange e-post för användaren som ska tas bort: ")

    index, user = find_user_by_email(users, email)  # Packar upp tuplen
    if user is None:
        print(f"Ingen användare med e-postadressen {email.lower()} hittades.")
        return

    users.pop(index)
    print(f"Användaren {user['name']} ({user['email']}) har tagits bort.")


# ---------------------------------------------------------------------------
# Huvudprogram
# ---------------------------------------------------------------------------

def main():
    """Sköter meny och programflöde."""
    users = []  # Här lagras användarna som dictionaries

    while True:
        print("\n===== Användarregister =====")
        print("1. Lägg till användare")
        print("2. Sök användare")
        print("3. Visa alla användare")
        print("4. Ta bort användare")
        print("5. Avsluta")
        choice = input("Välj ett alternativ: ").strip()

        if choice == "1":
            add_user(users)
        elif choice == "2":
            search_user(users)
        elif choice == "3":
            show_users(users)
        elif choice == "4":
            remove_user(users)
        elif choice == "5":
            print("Programmet avslutas.")
            break
        else:
            print("Ogiltigt val, ange en siffra mellan 1 och 5.")


# Kör bara main() när filen startas direkt
if __name__ == "__main__":
    main()
