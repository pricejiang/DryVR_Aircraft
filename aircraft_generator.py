import json
import sys
import os

def main(argv):
    i = 1
    epsilon = 10
    wp = ""
    wp_prev = ""
    data = {}
    data["vertex"] = []
    data["edge"] = []
    data["guards"] = []
    while(True):
        print "Please enter the " + str(i) + " way point in format 'wp_x:wp_y'. "
        print "If not, please press 'N'"
        wp = raw_input()
        if wp == 'N':
            break
        if wp.split(":") == wp:
            print "Please enter the correct format"
        if i == 1:
            wp_prev = wp
            i+=1
            continue
        data["vertex"].append(wp_prev + " " + wp)
        data["edge"].append([i-2, i-1])
        x = int(wp.split(":")[0])
        y = int(wp.split(":")[1])
        data["guards"].append("And(x>="+str(x-epsilon)+", x<="+str(x+epsilon)+", y>="+str(y-epsilon)+", y<="+str(y+epsilon)+")")
        
        wp_prev = wp
        i += 1
    
    if len(data["vertex"]) <= 1:
        print "input at least two waypoints"
        exit()
    data["guards"].pop()
    data["edge"].pop()
    assert len(data["guards"]) == len(data["edge"])
    print "Please enter the initial set in format 'v, psi, x, y': "
    initialSet_input = raw_input().split(",")
    initialSet = []
    initialSetBottom = []
    initialSetUpper = []
    for num in initialSet_input:
        initialSetBottom.append(float(num.strip()))
        initialSetUpper.append(float(num.strip())+0.1)
    initialSet.append(initialSetBottom)
    initialSet.append(initialSetUpper)
    data["variables"] = ["v", "psi", "x", "y"]
    data["initialSet"] = initialSet
    data["unsafeSet"] = "@Allmode: x<-100"
    data["timeHorizon"] = 100.0
    data["directory"] = "examples/aircraft"

    with open('input/aircraft/aircraft.json', 'w') as outfile:
        json.dump(data, outfile)

    os.system('python main.py input/aircraft/aircraft.json')


if __name__ == "__main__":
    main(sys.argv)