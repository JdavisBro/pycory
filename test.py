import pycory
import random

save = pycory.path.find_save()

with save.playdata.open("w") as playdata:
    print(playdata.screen, playdata.position)
    playdata.state["color_part_0"] = random.randint(1,16777215) # Decimal color range.
    playdata.state["color_part_1"] = random.randint(1,16777215)
    playdata.state["color_part_2"] = random.randint(1,16777215)
