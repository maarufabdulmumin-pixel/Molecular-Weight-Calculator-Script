import re

def calculate_molecular_weight(formula):
    """
    Calculates the molecular weight of a chemical compound from its formula.

    Args:
        formula (str): The chemical formula (e.g., "H2O", "C6H12O6", "Fe2(SO4)3").

    Returns:
        float: The calculated molecular weight in g/mol.
        str: An error message if the formula is invalid.
    """
    # Dictionary of atomic weights for common elements (g/mol)
    atomic_weights = {
        'H': 1.008, 'He': 4.0026, 'Li': 6.94, 'Be': 9.0122, 'B': 10.81,
        'C': 12.011, 'N': 14.007, 'O': 15.999, 'F': 18.998, 'Ne': 20.180,
        'Na': 22.990, 'Mg': 24.305, 'Al': 26.982, 'Si': 28.085, 'P': 30.974,
        'S': 32.06, 'Cl': 35.45, 'K': 39.098, 'Ar': 39.948, 'Ca': 40.078,
        'Fe': 55.845, 'Cu': 63.546, 'Zn': 65.38, 'Br': 79.904, 'Ag': 107.868,
        'I': 126.904, 'Ba': 137.327, 'Au': 196.967, 'Hg': 200.59, 'Pb': 207.2
    }

    # Use regex to find all elements and their counts
    # It handles formulas like 'Fe2(SO4)3' by breaking down groups
    element_pattern = re.compile(r'([A-Z][a-z]*)(\d*)|(?:\()([A-Z][a-z]*)(\d*)(?:\)(\d*))?')
    
    total_weight = 0.0
    
    # Check for parentheses for complex formulas
    if '(' in formula and ')' in formula:
        # Split formula by parentheses
        parts = re.split(r'(\(.*?\)\d*)', formula)
        
        for part in parts:
            if part.startswith('(') and part.endswith(')'):
                # Handle group inside parentheses
                group_match = re.match(r'\((.*?)\)(\d*)', part)
                if not group_match:
                    return "Invalid formula format.", None
                
                group_formula, group_count_str = group_match.groups()
                group_count = int(group_count_str) if group_count_str else 1
                
                # Recursively calculate the weight of the group
                matches = re.findall(r'([A-Z][a-z]*)(\d*)', group_formula)
                group_weight = 0.0
                for element, count_str in matches:
                    count = int(count_str) if count_str else 1
                    if element not in atomic_weights:
                        return f"Unknown element: {element}", None
                    group_weight += atomic_weights[element] * count
                
                total_weight += group_weight * group_count
                
            else:
                # Handle elements outside parentheses
                matches = re.findall(r'([A-Z][a-z]*)(\d*)', part)
                for element, count_str in matches:
                    count = int(count_str) if count_str else 1
                    if element not in atomic_weights:
                        return f"Unknown element: {element}", None
                    total_weight += atomic_weights[element] * count

    else:
        # Simple formula without parentheses
        matches = re.findall(r'([A-Z][a-z]*)(\d*)', formula)
        
        for element, count_str in matches:
            count = int(count_str) if count_str else 1
            if element not in atomic_weights:
                return f"Unknown element: {element}", None
            total_weight += atomic_weights[element] * count

    return total_weight, None

# --- Example Usage ---
formulas = ["H2O", "C6H12O6", "Fe2(SO4)3", "NaCl", "KMnO4"]

print("Molecular Weight Calculations:")
print("-" * 30)

for formula in formulas:
    mw, error = calculate_molecular_weight(formula)
    if error:
        print(f"Formula: {formula} -> Error: {error}")
    else:
        print(f"Formula: {formula:<10} -> Molecular Weight: {mw:.3f} g/mol")
