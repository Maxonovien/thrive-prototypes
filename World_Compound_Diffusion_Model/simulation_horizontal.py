import matplotlib.pyplot as plt
import numpy as np
import json

from patch import Patch
from patch_map import PatchMap
from world_diffusion_system import WorldDiffusionSystem
from solver import Solver

SETUP_FILE_PATH = "setups/horizontal.json"
with open(SETUP_FILE_PATH) as f:
    data = json.load(f)

patches = [
    Patch(  patch_data["depth"], patch_data["molecule_speed"],
            patch_data["initial_compound_amount"],
            patch_data["initial_compound_production"],
            compound_name = data["compound"],
            name = patch_data["name"])
    for patch_data in data["patches_data"]
]

for patch in patches:
    print(patch)

patch_links = [
    (link_data["patch1"],link_data["patch2"], link_data["value"])
    for link_data in data["patch_links"]
]

patch_map = PatchMap(patches, patch_links)
print(patch_map)

# Evolve the world

solver = Solver(data["solver"])
world_diffusion_system = WorldDiffusionSystem(patch_map, solver)

initial_productions = [patch.compound_production for patch in patches]
productions_over_time = [initial_productions] + data["future_productions"]
num_steps = len(productions_over_time)

repartition_snapshots = [world_diffusion_system.patch_map.compute_repartition_vector()]

for i in range(num_steps):
    print("# STEP {}".format(i))
    world_diffusion_system.update_production(productions_over_time[i])
    world_diffusion_system.make_step(data["step_duration"])
    repartition_snapshots.append(world_diffusion_system.patch_map.compute_repartition_vector())
    print(world_diffusion_system)

repartition_snapshots = np.asarray(repartition_snapshots)

# Plot snapshots
fig, axes = plt.subplots(ncols = len(patches), sharey = True)

for i in range(len(patches)):
    axes[i].set_title("{0} level in patch {1} over time".format(patches[i].compound_name, patches[i].name))
    axes[i].plot(range(num_steps+1), repartition_snapshots[:,i])
    axes[i].axhline(0, color='black')
plt.show()


# Plot repartitions
fig, axes = plt.subplots(ncols = 2)

barWidth = 0.85
names = range(num_steps+1)
COLORS = ["blue", "green", "orange", "red", "purple"]

bar_values = np.zeros(num_steps+1)
old_values = np.zeros(num_steps+1)
for i in range(len(patches)):
    old_values += bar_values
    bar_values = repartition_snapshots[:,i]
    axes[0].bar(range(num_steps+1), bar_values, bottom=old_values, color=COLORS[i%len(COLORS)], edgecolor='white', width=barWidth)

# Custom x axis
axes[0].set_xticks(range(num_steps+1))
axes[0].set_xlabel("Generations")
axes[0].set_ylabel("Oxygen amount")
axes[0].set_title("Amount of oxygen over time")

bar_values = np.zeros(num_steps+1)
old_values = np.zeros(num_steps+1)
total_per_snapshot = np.sum(repartition_snapshots, axis = 1)

# Avoiding null totals
total_per_snapshot = [1 if x==0 else x for x in total_per_snapshot ]

for i in range(len(patches)):
    old_values += bar_values
    bar_values = repartition_snapshots[:,i]/total_per_snapshot[:]
    axes[1].bar(range(num_steps+1), bar_values, bottom=old_values, color=COLORS[i%len(COLORS)], edgecolor='white', width=barWidth, label = "Patch "+ patches[i].name)

axes[1].set_xticks(range(num_steps+1))
axes[1].set_xlabel("Generations")
axes[1].set_ylabel("% of total Oxygen")
axes[1].set_title("Repartition of oxygen over time")


axes[1].legend(loc='upper left', bbox_to_anchor=(1,1), ncol=1)
# Show graphic
plt.show()
