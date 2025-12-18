FCR = 5.0
START_WEIGHT = 0.09

def main():

    print("--------------------------------------------------------------------------------")
    print(
    "This tool was created to help you plan and manage your heritage chicken meat production "
    "in an economical and realistic way.\n\n"
    "Remember to provide your day-old chicks with heat, grit, and fresh water, and gradually "
    "give them access to scraps and the outdoors as they mature.\n\n"
    "Now prepare your brooder and order your chicks once you have everything ready."
    )
    print("--------------------------------------------------------------------------------")

    while True:
        try:
            while True:
                try:
                    chicks = int(input("Enter how many day-old chicks you have (max 1000):\n").strip())
                    if 1 <= chicks <= 1000:
                        break
                    print("Enter a number between 1 and 1000.\n")
                except ValueError:
                    print("Enter whole numbers only.\n")

            while True:
                try:
                    harvest_weight = float(input("Desired body weight in pounds for each bird at slaughter (2 to 5 lb):\n").strip())
                    if 2 <= harvest_weight <= 5:
                        break
                    print("Enter a number between 2 and 5.\n")
                except ValueError:
                    print("Enter whole numbers or decimal numbers.\n")

            weight_gain = harvest_weight - START_WEIGHT
            total_feed = chicks * weight_gain * FCR

            corn = total_feed * .55
            soymeal = total_feed * .35
            alfalfa = total_feed * .10  

            print(
                f"The total amount of feed needed to raise your {chicks} chicks to the desired slaughter weight of "
                f"{round(harvest_weight, 1):g} pounds each is {round(total_feed, 1):g} pounds of feed."
            )
            print("--------------------------------------------------------------------------------")
            
            print(
                f"Now you need to source feed for your chicks. You will need approximately "
                f"{round(total_feed, 1):g} pounds of feed."
            )
            print("--------------------------------------------------------------------------------")

            while True:
                feedtype = input("Press a to make your own feed, or press c to use commercial feed:\n").strip().lower()
                print("--------------------------------------------------------------------------------")

                if feedtype in ("a", "c"):
                    break
                print("Enter a or c.\n")

            if feedtype == "c":
                print("You can use commercial feeds; however, they can be more expensive, especially when purchased in small quantities such as 5 to 50 lb bags.")
                option = input("Press q to quit, or any other letter to perform another calculation:\n").strip().lower()
                print("--------------------------------------------------------------------------------")
                if option == "q":
                    break
                continue

            if feedtype == "a":
                print(f"You need {round(total_feed, 1):g} pounds of feed.")
                print("The ingredients you need are cracked corn, heat-treated soymeal, and alfalfa meal.")
                print("These can be purchased in bulk online or in person at farm supply stores, usually in increments of 50 to 1000 pounds.")
                print(
                    f"To meet your needs, mix {round(corn, 1):g} pounds of cracked corn, "
                    f"{round(soymeal, 1):g} pounds of soymeal, and "
                    f"{round(alfalfa, 1):g} pounds of alfalfa meal."
                    )
                print("This mix will produce a feed that is roughly 18% protein and is suitable for chicken growth throughout their life stages.")
                print("--------------------------------------------------------------------------------")

            option = input("Press q to quit, or any other letter to perform another calculation:\n").strip().lower()
            print("--------------------------------------------------------------------------------")

            if option == "q":
                break

        except EOFError:
            print("Exiting.")
            break
        except ValueError:
            print("Enter input according to the instructions.\n")

if __name__ == "__main__":
    main()
