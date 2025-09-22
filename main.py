import subprocess
import sys

def main():
    try:
        print("Creating visualizations...")
        subprocess.run([sys.executable, "create_visualizations.py"], check=True)
        
        print("Generating README...")
        subprocess.run([sys.executable, "analyze_data.py"], check=True)
        
        print("Analysis complete!")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
