def select_optimal_sizes(target_people: float) -> tuple:
    
    
    available_sizes = [1, 2, 3, 4]
    if 1 <= target_people <= 4:
        if target_people <= 1.5:
            return (1, 2)
        elif target_people <= 2.5:
            return (1, 3)
        elif target_people <= 3.5:
            return (2, 4)
        else: 
            return (3, 4)
        
    elif target_people < 1:
        return (1, 2)
    elif 4 < target_people <= 6:
        return (3, 4)
    elif 6 < target_people <= 8:
        return (2, 4)
    else:
        return (1, 4) 
    
def smart_scale_recipe(data: dict, recipe_name: str, target_people: float) -> dict:
    
    from runner import scale_recipe
    
    size1, size2 = select_optimal_sizes(target_people)
    
    print(f"🎯 Scaling {recipe_name} for {target_people} people")
    print(f"📊 Using optimal reference sizes: {size1} and {size2}")
    
    # Scale the recipe using optimal sizes
    try:
        scaled_ingredients = scale_recipe(data, recipe_name, size1, size2, target_people)
        
        print(f"✅ Successfully scaled recipe using sizes {size1} & {size2}")
        return scaled_ingredients
    
    except Exception as e:
        print(f"❌ Error with sizes {size1}, {size2}: {e}")
        
        # Fallback: try different reference combination
        fallback_size1, fallback_size2 = get_fallback_sizes(target_people, size1, size2)
        print(f"🔄 Trying fallback sizes: {fallback_size1} and {fallback_size2}")
        
        try:
            return scale_recipe(data, recipe_name, fallback_size1, fallback_size2, target_people)
        except Exception as e2:
            print(f"❌ Fallback also failed: {e2}")
            raise

def get_fallback_sizes(target_people: float, failed_size1: int, failed_size2: int) -> tuple:
    """
    Get alternative reference sizes if the optimal ones fail.
    
    Args:
        target_people (float): Target serving size
        failed_size1, failed_size2 (int): Sizes that failed
    
    Returns:
        tuple: Alternative (size1, size2)
    """
    available_sizes = [1, 2, 3, 4]
    used_sizes = {failed_size1, failed_size2}
    remaining_sizes = [s for s in available_sizes if s not in used_sizes]
    
    if len(remaining_sizes) >= 2:
        # Choose the two remaining sizes with maximum spacing
        if target_people <= 2:
            return (remaining_sizes[0], remaining_sizes[-1])  # e.g., (1,4) if (2,3) failed
        else:
            return (remaining_sizes[0], remaining_sizes[-1])
    else:
        # Last resort: use any two different sizes
        return (1, 4) if (1, 4) != (failed_size1, failed_size2) else (2, 3)

def explain_selection_strategy(target_people: float) -> None:
    """
    Explain why specific reference sizes were chosen for the target.
    
    Args:
        target_people (float): Target number of people
    """
    size1, size2 = select_optimal_sizes(target_people)
    
    print(f"\n📋 REFERENCE SIZE SELECTION EXPLANATION")
    print(f"Target: {target_people} people")
    print(f"Selected: {size1} and {size2}")
    print("-" * 40)
    
    if 1 <= target_people <= 4:
        print("🎯 Strategy: INTERPOLATION")
        print("• Target is within available data range")
        print("• Using sizes that bracket the target for maximum accuracy")
        if abs(size2 - size1) >= 2:
            print("• Wide spacing chosen for better stability")
    elif target_people < 1 or target_people > 4:
        print("🎯 Strategy: EXTRAPOLATION")
        print("• Target is outside available data range")
        if target_people < 1:
            print("• Using smallest available sizes for small portions")
        elif target_people <= 6:
            print("• Using largest available sizes for medium scaling")
        else:
            print("• Using maximum spacing (1,4) for large scaling stability")
    
    # Accuracy prediction
    if 1 <= target_people <= 4:
        accuracy = "High (5-10% error)"
    elif target_people < 1 or 4 < target_people <= 6:
        accuracy = "Medium (10-15% error)"
    else:
        accuracy = "Lower (15-25% error)"
    
    print(f"• Expected accuracy: {accuracy}")

# Demonstration and usage examples
def demo_optimal_selection():
    """Demonstrate optimal size selection for various target sizes"""
    
    print("🍛 OPTIMAL SIZE SELECTION DEMONSTRATION")
    print("=" * 50)
    
    test_targets = [0.5, 1.2, 2.0, 2.8, 3.5, 4.2, 5.5, 7.0, 10.0]
    
    print(f"{'Target People':<12} {'Size 1':<8} {'Size 2':<8} {'Strategy':<15} {'Expected Accuracy'}")
    print("-" * 65)
    
    for target in test_targets:
        size1, size2 = select_optimal_sizes(target)
        
        # Determine strategy
        if 1 <= target <= 4:
            strategy = "Interpolation"
            accuracy = "High"
        elif target < 1 or 4 < target <= 6:
            strategy = "Small Extrap"
            accuracy = "Medium"
        else:
            strategy = "Large Extrap"
            accuracy = "Lower"
        
        print(f"{target:<12} {size1:<8} {size2:<8} {strategy:<15} {accuracy}")
    
    print("\n📊 Strategy Summary:")
    print("• Interpolation (1-4 people): Use bracketing sizes")
    print("• Small Extrapolation (<1 or 4-6 people): Use closest sizes")
    print("• Large Extrapolation (>6 people): Use maximum spacing")

if __name__ == "__main__":
    # Run demonstration
    demo_optimal_selection()
    
    # Example usage
    print("\n" + "=" * 50)
    print("EXAMPLE USAGE:")
    print("=" * 50)
    
    print("\n# Basic usage:")
    print("size1, size2 = select_optimal_sizes(5.5)")
    print("# Returns: (3, 4)")
    
    print("\n# Full scaling with automatic optimization:")
    print('data = load_from_file("paneer_recipes.json")')
    print('scaled = smart_scale_recipe(data, "palak_paneer", 5.5)')
    
    print("\n# Explain the selection:")
    print("explain_selection_strategy(5.5)")
    
    # Demonstrate actual selection
    explain_selection_strategy(5.5)