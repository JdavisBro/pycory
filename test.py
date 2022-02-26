"""
Tests for pycory!

Runs tests specified in arguments or all if no arguments.

Tests:
- playdata
- level_data

Usage example:
`python3 test.py playdata level_data`
"""

import sys
import random
import inspect

import pycory

def test_playdata():
    print("\n== playdata Test ==\n")

    save = pycory.path.find_save()

    with save.playdata.open("w") as playdata:
        print(f"Screen: {playdata.screen}, Position: {playdata.position}")
        playdata.state["color_part_0"] = random.randint(1,16777215) # Decimal color range.
        playdata.state["color_part_1"] = random.randint(1,16777215)
        playdata.state["color_part_2"] = random.randint(1,16777215)
        print("Dog colour randomised.")

def test_level_data():
    print("\n== level_data Test ==\n")

    level = pycory.path.find_level_data()

    with level.open("w") as level_data:
        print(inspect.cleandoc(
            f"""0_0_0
            Geo: {level_data['0_0_0'].geo}
            Ambiance: {level_data['0_0_0'].ambiance}
            Palette: {level_data['0_0_0'].palette}
            Title: {level_data['0_0_0'].title}
            Area: {level_data['0_0_0'].area}
            Transition: {level_data['0_0_0'].transition}
            Music: {level_data['0_0_0'].music}
            Object_Id: {level_data['0_0_0'].object_id}
            Name: {level_data['0_0_0'].name}
            """
        ))
        level_data["0_0_0"].geo = level_data["0_1_2"].geo
        print("0_0_0 now has 0_1_2 geo")
        level_data["0_0_0"].objects[2]["x"], level_data["0_0_0"].objects[2]["y"] = random.randint(0,1920), random.randint(0,720)
        print(f"0_0_0 tree randomised. Now at {level_data['0_0_0'].objects[2]['x']}, {level_data['0_0_0'].objects[2]['y']}")


tests = {
    "playdata": test_playdata,
    "level_data": test_level_data,
}

def main(args):
    if args:
        for i in args:
            if i in tests:
                tests[i]()
    else:
        for test in tests.values():
            test()

if __name__ == "__main__":
    main(sys.argv[1:])