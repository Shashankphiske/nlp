# --- Simple Expert System using Forward Chaining ---

# Knowledge Base: (rules)
rules = {
    "fever & cough": "flu",
    "fever & rash": "measles",
    "headache & nausea": "migraine",
    "fatigue & weight loss": "diabetes",
    "fever & cough & chest pain": "pneumonia",
}

# Askable facts (symptoms)
symptoms = ["fever", "cough", "rash", "headache", "nausea", "fatigue", "weight loss", "chest pain"]

def forward_chaining():
    print("🤖 Welcome to the Medical Expert System!")
    print("Please answer 'yes' or 'no' for the following symptoms:\n")

    # Collect user input
    facts = set()
    for s in symptoms:
        ans = input(f"Do you have {s}? ").strip().lower()
        if ans == "yes":
            facts.add(s)

    # Infer new facts (diseases)
    inferred = None
    for condition, disease in rules.items():
        conditions = set(condition.split(" & "))
        if conditions.issubset(facts):
            inferred = disease
            break

    # Output result
    print("\n--- Diagnosis Result ---")
    if inferred:
        print(f"✅ Based on your symptoms, you may have: {inferred.upper()}")
    else:
        print("❌ No matching disease found. Please consult a doctor.")

# Run the expert system
if __name__ == "__main__":
    forward_chaining()
