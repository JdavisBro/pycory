import pycory
import random

print("== playdata Test ==")

save = pycory.path.find_save()

with save.playdata.open("w") as playdata:
    print(playdata.screen, playdata.position)
    playdata.state["color_part_0"] = random.randint(1,16777215) # Decimal color range.
    playdata.state["color_part_1"] = random.randint(1,16777215)
    playdata.state["color_part_2"] = random.randint(1,16777215)
    print("Dog colour randomised.")

print("== level_data Test ==")

level = pycory.path.find_level_data()

with level.open("w") as level_data:
    print(level_data["0_0_0"]["geo"])
    level_data["0_0_0"]["objects"][2]["x"], level_data["0_0_0"]["objects"][2]["y"] = random.randint(0,1920), random.randint(0,720)
    print("0_0_0 tree randomised.")
