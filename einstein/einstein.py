cSpeed = 300000000

mass = input("m: ")

if mass.isdigit():
    mass = int(mass)
    energy = mass*cSpeed**2  #(m*c) * (m*c)
    print("E:", energy)
