import argparse
import sys
from shapes import rectangle_area



def main():
    # Create argument parser
    parser = argparse.ArgumentParser(
        description="Calculate the area of a rect using base and height",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python rect_area_cli.py 10 5
  python rect_area_cli.py --base 7.5 --height 4.2
  python rect_area_cli.py -b 12 --height 8
        """
    )
    
    # Add positional arguments
    parser.add_argument('base', nargs='?', type=float, 
                       help='Base of the rect')
    parser.add_argument('height', nargs='?', type=float, 
                       help='Height of the rect')
    
    # Add optional arguments (alternative way to specify base and height)
    parser.add_argument('-b', '--base', dest='base_opt', type=float,
                       help='Base of the rect (alternative to positional argument)')
    parser.add_argument('--height', dest='height_opt', type=float,
                       help='Height of the rect (alternative to positional argument)')
    
    # Add version option
    parser.add_argument('--version', action='version', version='rect Calculator 1.0')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Determine base and height values
    base = args.base if args.base is not None else args.base_opt
    height = args.height if args.height is not None else args.height_opt
    
    # Validate inputs
    if base is None or height is None:
        print("Error: Both base and height are required.")
        print("\nUsage examples:")
        print("  python rectangle_cil.py 10 5")
        print("  python rectangle_cil.py --base 10 --height 5")
        print("  python rectangle_cil.py -b 10 --height 5")
        sys.exit(1)
    
    # Validate that values are positive
    if base <= 0 or height <= 0:
        print("Error: Base and height must be positive numbers.")
        sys.exit(1)
    
    try:
        # Calculate area
        area = rectangle_area(base, height)
        
        # Display result
        print(f"rect area calculation:")
        print(f"Base: {base}")
        print(f"Height: {height}")
        print(f"Area: {area:.2f}")
        
    except Exception as e:
        print(f"Error calculating area: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
