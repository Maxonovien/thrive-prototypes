# Primary resources experiment

This first prototype will aim to model a situation where consumers all feed on basic, finite infinitely renewable resources. 

## Framework

We will study here several species (`num_species`) evolving in parallel in a given patch. 
We will make several assumptions that may or may not be conserved for future experiments.
 
### Patch homogeneity

A patch is a part of an environment that roughly has similar conditions across it.
Our first assumption will be the homogeneity of patches, that is that its elements are uniformly distributed over it.
This may not be fully realistic, as noise would inevitably occur in reality, and this would affect other distributions, potentially reinforcing it as a chain-effect.
Furthermore, this does not account for potential clustering or anti-clustering behaviors of living organisms.

### Primary resources

We will consider the following primary resources:
- Sunlight
- Glucose
- Iron
- Hydrogen Sulfide

And their related processes (TODO)
- Glycolysis: glucose -> ATP
- Photosynthesis 
-
-

We'll suppose that, when it comes to primary resources, there is a finite amount for Glucose, Iron, and Hydrogen Sulfide that will have to be shared among the species.
Sunlight,on the other hand, will have no competition and each participant will be given a fixed, patch-dependent amount.

TODO
