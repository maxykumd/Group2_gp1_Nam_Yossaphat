from setuptools import find_packages, setup
from glob import glob

package_name = 'group2_gp1f'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch',
        glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='maxz',
    maintainer_email='maxyk@umd.edu',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        'run_lidar_node = group2_gp1f.scripts.run_lidar_node:main',
        'run_camera_node = group2_gp1f.scripts.run_camera_node:main',
        'run_safety_node = group2_gp1f.scripts.run_safety_node:main',
        'run_fusion_node = group2_gp1f.scripts.run_fusion_node:main',
        'run_logger_node = group2_gp1f.scripts.run_logger_node:main'
        #'config_node = group2_gp1f.scripts.run_config_node:main'
        ]     
    },
)
