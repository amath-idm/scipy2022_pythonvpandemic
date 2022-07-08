# Set parameters and define random wave generator
import numpy as np
xmin = 0
xmax = 10
npts = 50
noisevals = np.linspace(0, 1, 11)

def randwave(std):
    np.random.seed() # Ensure differences between runs
    a = np.cos(np.linspace(xmin, xmax, npts))
    b = np.random.randn(npts)
    return a + b*std

# Other imports
import sciris as sc

# Start timing
sc.tic()

# Create object in parallel
output = sc.parallelize(randwave, noisevals)

# Save to files
filenames = []
for n,noiseval in enumerate(noisevals):
    filename = f'noise{n}.obj'
    sc.save(filename, output[n])
    filenames.append(filename)

# Create dict from files
data = sc.odict({filename:sc.load(filename) for filename in filenames})

# Create 3D plot
sc.surf3d(data[:])

# Print elapsed time
sc.toc()


