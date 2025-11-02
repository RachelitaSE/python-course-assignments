from shapes import *


if __name__ == "__main__":

    # Get base and height from user input
    try:
        base = float(input("Enter the base of the rectangle: "))
        height = float(input("Enter the height of the rectangle: "))
        
        # Calculate and display the area
        area = rectangle_area(base, height)
        print(f"rectangle with base {base} and height {height} has area: {area}")
        
    except ValueError:
        print("Please enter valid numbers for base and height.")