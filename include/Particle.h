#pragma once

class Particle {
public:
    double x, y;       // Posición
    double vx, vy;     // Velocidad
    double fx, fy;     // Fuerza
    double mass;
    int id;

    Particle(int id, double x, double y, double vx, double vy, double m = 1.0)
        : id(id), x(x), y(y), vx(vx), vy(vy), mass(m), fx(0), fy(0) {}

    void resetForce() {
        fx = 0.0;
        fy = 0.0;
    }

    void addForce(double f_x, double f_y) {
        fx += f_x;
        fy += f_y;
    }
};
