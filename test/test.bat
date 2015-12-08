cd ..
conan export kaosumaru/testing
cd test
conan install --build=missing
