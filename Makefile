CXX = g++
CXXFLAGS = -O3 -std=c++17 -Iinclude
TARGET = simulacion
SRC = src/main.cpp

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) $(SRC) -o $(TARGET)

clean:
	rm -f $(TARGET) results/*.csv results/*.png
