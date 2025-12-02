#pragma once
#include "Particle.h"

class Box {
private:
    double width;
    double height;

public:
    Box(double w, double h) : width(w), height(h) {}

    void applyBoundaryConditions(Particle& p) {
        // Paredes Reflectivas en X
        if (p.x < 0) {
            p.x = -p.x;
            p.vx = -p.vx;
        } else if (p.x > width) {
            p.x = 2 * width - p.x;
            p.vx = -p.vx;
        }
        // Paredes Reflectivas en Y
        if (p.y < 0) {
            p.y = -p.y;
            p.vy = -p.vy;
        } else if (p.y > height) {
            p.y = 2 * height - p.y;
            p.vy = -p.vy;
        }
    }

    double getWidth() const { return width; }
    double getHeight() const { return height; }
};
