from setuptools import find_packages, setup

package_name = 'robotic_arm_custom_nodes'

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
    maintainer='newtonjeri',
    maintainer_email='newtonkaris45@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'fk_test_node = robotic_arm_custom_nodes.fk_test_node:main',
            'ik_node = robotic_arm_custom_nodes.inverse_kinematics_node:main',
            'arduino_data = robotic_arm_custom_nodes.arduino_data:main',
        ],
    },
)
