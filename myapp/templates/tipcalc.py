

print("\n***\nINSTRUCTIONS: This program accepts your bill amount and level of satisfaction with your service, and returns an appropriate tip amount.\n***\n")

def main():
    # ask for bill amount
    bill = float(input("What is the amount of your bill? $"))

    # ask for satisfaction level
    service = input("\nHow was the service?\ngood\nfair\nbad\nPlease choose one of the above options, then press Enter. ").lower()


    # calculate tip amount
    tips = {"good" : 0.20,
            "fair" : 0.15,
            "bad" : 0.10}
    tip_percentage = tips[service]
    tip = bill * tip_percentage

    # print message with tip amount
    print("\nYour bill was ${bill:.2f}, and your service was {service}.\n\nYou should tip ${tip:.2f}\n".format(bill=bill, service=service, tip=tip))

main()
