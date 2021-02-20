import cli
import sys
def main():
    def is_pyqt5_exists():
        try:
            from PyQt5 import uic
        except:
            return False
        return True

    if not is_pyqt5_exists():
        print()
        print('='*50)
        print('You need a PyQt5 to run this program.')
        print('Install PyQt5 by entering the following command in the terminal')
        print()
        print('pip install pyqt5')
        print('='*50)
        print()
        sys.exit()
    
    print("In what environment do you want it to work?")
    print("[1] Cli")
    print("[2] Gui")
    environment = int(input("Select Envionment : "))

    if environment == 1 :
        cli.run()
    elif environment == 2 :
        import gui as ui
        ui.main()
    else : 
        print("Wrong Number")

if __name__ == "__main__":
    main()