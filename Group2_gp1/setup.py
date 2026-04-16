from setuptools import find_packages, setup

package_name = 'group2_gp1'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='maxz , namfacchetti',
    maintainer_email='maxz@todo.todo, gfacchet@terpmail.umd.edu',
    description='ROS 2 sensor fusion pipeline for ENPM605 Group 2 GP1',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
    	'console_scripts': [
           'camera_node = group2_gp1.scripts.main_camera_node:main',
           'lidar_node = group2_gp1.scripts.main_lidar_node:main',
           'fusion_node = group2_gp1.scripts.main_fusion_node:main',
        ],
    },
)
