import matplotlib.pyplot as plt
import numpy as np

from patch import Patch
from patch_map import PatchMap
from world_diffusion_system import WorldDiffusionSystem
from solver import Solver

patch_depths = [200,200,200,200]
molecule_speeds = [1,1,2,1]
initial_oxygen_amounts = [0,0,0,0]
initial_oxygen_production = [1,0,0,0]
patch_names = ['"Producer"', '"Neighbour"', '"Fast Transit"', '"Enclosed"']

patches = [
    Patch(  patch_depths[i], molecule_speeds[i],
            initial_oxygen_amounts[i],
            initial_oxygen_production[i],
            compound_name = "Oxygen",
            name = patch_names[i])
    for i in range(len(patch_depths))
]

for patch in patches:
    print(patch)

# patch_links = [
#     (i,j,1) for (i,j) in [(0,1),(1,2),(2,3)]
# ]

patch_links = [(0,1,1),(1,2,1),(2,3,0.5)]

patch_map = PatchMap(patches, patch_links)

print(patch_map)

# Evolve the world

solver = Solver("np-least_squares")
world_diffusion_system = WorldDiffusionSystem(patch_map, solver)

PRODUCTION_VECTORS = (
    [initial_oxygen_production]*7+
    [[1,-1,-1,-1]]*3
)

STEP_DURATION = 10
NUM_STEPS = 10
repartition_snapshots = [world_diffusion_system.patch_map.compute_repartition_vector()]
for i in range(NUM_STEPS):
    print("# STEP {}".format(i))
    world_diffusion_system.update_production(PRODUCTION_VECTORS[i])
    world_diffusion_system.make_step(STEP_DURATION)
    repartition_snapshots.append(world_diffusion_system.patch_map.compute_repartition_vector())
    print(world_diffusion_system)

repartition_snapshots = np.asarray(repartition_snapshots)

# Plot snapshots
fig, axes = plt.subplots(ncols = 4, sharey = True)
#max_tick = np.max(repartition_snapshots)
#plt.setp(axes, yticks=np.arange(0, max_tick, max_tick/10), yticklabels=np.arange(0, max_tick, max_tick/10))


for i in range(len(patches)):
    axes[i].set_title("{0} level in patch {1} over time".format(patches[i].compound_name, patches[i].name))
    axes[i].plot(range(NUM_STEPS+1), repartition_snapshots[:,i])
    axes[i].axhline(0, color='black')
plt.show()


# Plot repartitions
fig, axes = plt.subplots(ncols = 2)

barWidth = 0.85
names = range(NUM_STEPS+1)
COLORS = ["blue", "green", "orange", "red", "purple"]

bar_values = np.zeros(NUM_STEPS+1)
old_values = np.zeros(NUM_STEPS+1)
for i in range(len(patches)):
    old_values += bar_values
    bar_values = repartition_snapshots[:,i]
    axes[0].bar(range(NUM_STEPS+1), bar_values, bottom=old_values, color=COLORS[i%len(COLORS)], edgecolor='white', width=barWidth)

# Custom x axis
axes[0].set_xticks(range(NUM_STEPS+1))
axes[0].set_xlabel("Generations")
axes[0].set_ylabel("Oxygen amount")
axes[0].set_title("Amount of oxygen over time")

bar_values = np.zeros(NUM_STEPS+1)
old_values = np.zeros(NUM_STEPS+1)
total_per_snapshot = np.sum(repartition_snapshots, axis = 1)

# Avoiding null totals
total_per_snapshot = [1 if x==0 else x for x in total_per_snapshot ]

for i in range(len(patches)):
    old_values += bar_values
    bar_values = repartition_snapshots[:,i]/total_per_snapshot[:]
    axes[1].bar(range(NUM_STEPS+1), bar_values, bottom=old_values, color=COLORS[i%len(COLORS)], edgecolor='white', width=barWidth, label = "Patch "+ patches[i].name)

axes[1].set_xticks(range(NUM_STEPS+1))
axes[1].set_xlabel("Generations")
axes[1].set_ylabel("% of total Oxygen")
axes[1].set_title("Repartition of oxygen over time")


axes[1].legend(loc='upper left', bbox_to_anchor=(1,1), ncol=1)
# Show graphic
plt.show()
