import os
from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

_src_path = os.path.dirname(os.path.abspath(__file__))

nvcc_flags = [
    '-O3', '-std=c++17',
    "--expt-extended-lambda",
	"--expt-relaxed-constexpr",
    # '-U__CUDA_NO_HALF_OPERATORS__', '-U__CUDA_NO_HALF_CONVERSIONS__', '-U__CUDA_NO_HALF2_OPERATORS__',
]

if os.name == "posix":
    c_flags = ['-O3', '-std=c++17']
elif os.name == "nt":
    c_flags = ['/O2', '/std:c++17']

'''
Usage:
python setup.py build_ext --inplace # build extensions locally, do not install (only can be used from the parent directory)
python setup.py install # build extensions and install (copy) to PATH.
pip install . # ditto but better (e.g., dependency & metadata handling)
python setup.py develop # build extensions and install (symbolic) to PATH.
pip install -e . # ditto but better (e.g., dependency & metadata handling)
'''
setup(
    name='gtracer', # package name, import this to use python API
    version='0.1.0',
    description='3D Gaussian RayTracer',
    packages=['gtracer'],
    ext_modules=[
        CUDAExtension(
            name='gtracer._C', # extension name, import this to use CUDA API
            sources=[os.path.join(_src_path, 'src', f) for f in [
                'bvh.cu',
                'bindings.cu',
            ]],
            include_dirs=[
                os.path.join(_src_path, 'include'),
                os.path.join(_src_path, "build"),
                os.path.join(_src_path, 'include', 'optix'),
                os.path.join(_src_path, 'include', 'glm'),
            ],
            extra_compile_args={
                'cxx': c_flags,
                'nvcc': nvcc_flags,
            },
            libraries=['advapi32'],
        ),
    ],
    cmdclass={
        'build_ext': BuildExtension,
    },
    install_requires=[
        'ninja',
        'trimesh',
        'opencv-python',
        'torch',
        'numpy ',
        'tqdm',
        'dearpygui',
    ],
)