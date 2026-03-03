from setuptools import setup, find_packages

setup(
    name="misinformation-platform",
    version="1.0.0",
    description="AI-powered Real-Time Misinformation Analysis & Correction Platform",
    packages=find_packages(),
    install_requires=[
        "flask>=3.0.0",
        "flask-cors>=4.0.0",
        "scikit-learn>=1.3.2",
        "numpy>=1.26.2",
        "requests>=2.31.0",
        "python-dateutil>=2.8.2",
    ],
    python_requires=">=3.8",
)
