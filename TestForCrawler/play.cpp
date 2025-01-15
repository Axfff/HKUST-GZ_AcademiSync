#include <iostream>
#include <map>
class Shape {  

public:
    Shape(int x, int y) : x(x), y(y) {
        std::cout << "Shape constructor" << std::endl;
    }
    void print() {
        std::cout << "Shape print" << std::endl;
    }
private:
    int x,y;
};

class Circle : public Shape {
public:
    Circle(int x, int y, int r) : Shape(x,y), r(r) {
        std::cout << "Circle constructor" << std::endl;
    }
    void print() {
        std::cout << "Circle print" << std::endl;
    }
private:
    int r;
};
std::string createString() {
    std::string temp = "Hello, World!";
    return std::move(temp); // 触发移动语义
}
std::map<int,int> m;
int main() {
    m.insert(std::pair<int,int>(1,2));
    m[2] = 3;
    for( auto &i : m) {
        std::cout << i.first << " " << i.second << std::endl;
    }

    return 0;
}