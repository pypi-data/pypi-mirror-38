import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deepmg",
    version="0.4.9",
    author="Thanh-Hai Nguyen",
    author_email="hainguyen579@gmail.com",
    description="A python package to visualize/train/predict data using machine/deep learning algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.integromics.fr/published/deepMG_tf",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

#what's NEW ###
# version: 0.4.5: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + fix name log of vgg, cnn model (with padding)
# + rename "ab" --> "spb"
# + set up to use all available gpus cudaid < -1

# version: 0.4.6: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + fix folder in creating images for whole dataset

# version: 0.4.7: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + add gpu_memory_fraction to control memory of gpu required used, to be able to run multiple jobs using gpu
#      The second method is the gpu_memory_fraction option, 
#      which determines the fraction of the overall amount of memory that each visible GPU should be allocated
#      if gpu_memory_fraction = 0: attempts to allocate only as much GPU memory based on runtime allocations: 
#               it starts out allocating very little memory, and as Sessions get run and more GPU memory is needed, 
#               we extend the GPU memory region needed by the TensorFlow process
# + cudaid : <-1: use cpu, -1: use all available gpus, >-1: use specific gpu 

# version: 0.4.8: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + cudaid : <-2: use cpu; -2: use cpu if there is no available gpu; -1: use all available gpus; >-1: use specific gpu 

# version: 0.4.9: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + change ab -> spb in vis_data.py
