import pycory
import random
import inspect

print("\n== playdata Test ==\n")

save = pycory.path.find_save()

with save.playdata.open("w") as playdata:
    print(f"Screen: {playdata.screen}, Position: {playdata.position}")
    playdata.state["color_part_0"] = random.randint(1,16777215) # Decimal color range.
    playdata.state["color_part_1"] = random.randint(1,16777215)
    playdata.state["color_part_2"] = random.randint(1,16777215)
    print("Dog colour randomised.")

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
    print(level_data["0_0_0"].objects[2]["x"])
    level_data["0_0_0"].objects[2]["x"], level_data["0_0_0"].objects[2]["y"] = random.randint(0,1920), random.randint(0,720)
    #print("0_0_0 tree randomised.")
