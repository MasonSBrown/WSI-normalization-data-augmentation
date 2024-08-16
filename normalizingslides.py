"""
This code normalizes staining appearance of H&E stained images.
It also separates the hematoxylin and eosing stains in to different images. 

Other useful references:
    https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5226799/
    https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0169875

PROPOSED WORKFLOW:  
    
Input: RGB image
Step 1: Convert RGB to OD (optical density)
Step 2: Remove data with OD intensity less than β
Step 3: Calculate  singular value decomposition (SVD) on the OD tuples
Step 4: Create plane from the SVD directions corresponding to the
two largest singular values
Step 5: Project data onto the plane, and normalize to unit length
Step 6: Calculate angle of each point wrt the first SVD direction
Step 7: Find robust extremes (αth and (100−α)th 7 percentiles) of the
angle
Step 8: Convert extreme values back to OD space

Output: Optimal Stain Vectors

"""