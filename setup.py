from setuptools import setup, find_packages

setup(name='pynori', 
      version='1.0', 
      url='https://github.com/gritmind/python-nori', 
      author='Yeongsu Kim', 
      author_email='gritmind@gmail.com', 
      description='Korean Mopological Analyzer, Nori in Python', 
      packages=find_packages(exclude=['tests']), 
      long_description=open('README.md').read(), 
      long_description_content_type='text/markdown', 
      # 마크다운 파일로 description를 지정했다면 text/markdown으로 작성합니다.
      install_requires=['cython'],
      zip_safe=False
)