def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error! Division by Zero."
    return a / b

def modulus(a, b):
    return a % b

def exponent(a, b):
    return a ** b

def show_history(history):
    if not history:
        print("No calculations in history yet.")
        return
    
    print("\n--- Calculation History ---")
    for i, calc in enumerate(history, 1):
        print(f"{i}. {calc}")
    print("---------------------------\n")

def calculator():
    history = []


    while True:
        print("\n********************Welcome to simple calculator***************************")
        print("Operations available: +, -, *, /, %, **")
        print("Type 'history' to view calculation history")
        print("Type 'quit' to exit")


        user_input = input("\nEnter operation or command: ").strip().lower()

        if user_input == 'quit':
            print("Thank you for using the calculator. Goodbye!")
            break

        elif user_input == 'history':
            show_history(history)
            continue
        
        elif user_input not in ['+', '-', '*', '/', '%', '**']:
            print("Invalid operation! Please use +, -, *, /, %, or **")
            continue
        
        operation = user_input

        try:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            
            if operation == "+":
                result = add(num1, num2)

            elif operation == "-":
                result = subtract(num1, num2)

            elif operation == "*":
                result = multiply(num1, num2)
            
            elif operation == "/":
              result = divide(num1, num2) 

            elif operation == "%":
                result = modulus(num1, num2) 

            elif operation == "**":
                result = exponent(num1, num2) 

            calculation_string = f"{num1} {operation} {num2} = {result}"
            print(f"\nResult: {calculation_string}")
            history.append(calculation_string)
            

        except ValueError:
            print("Invalid input! Please enter numbers only.")

        except Exception as e:
            print(f"An error occurred: {e}")

calculator()
