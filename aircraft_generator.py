import json
import sys

def main(argv):
    i = 1
    wp = ""
    wp_prev = ""
    data = {}
    data["vertex"] = []
    data["edge"] = []
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
        wp_prev = wp
        i += 1
    
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
    data["initialSet"] = initialSet
    data["unsafeSet"] = "@Allmode: x<-100"
    data["timeHorizon"] = 100.0
    data["directory"] = "examples/aircraft"

    with open('aircraft.json', 'w') as outfile:
        json.dump(data, outfile)


if __name__ == "__main__":
    main(sys.argv)