#pragma once
#include <vector>
#include <cmath>
#include "Particle.h"

// Clase Abstracta
class ForceCalculator {
public:
    virtual void calculateForces(std::vector<Particle>& particles) = 0;
    virtual ~ForceCalculator() = default;
};

// Implementación Lennard-Jones
class LennardJones : public ForceCalculator {
private:
    double epsilon;
    double sigma;
    double cutOff;

public:
    LennardJones(double eps, double sig) : epsilon(eps), sigma(sig), cutOff(0.1 * sig) {}

    void calculateForces(std::vector<Particle>& particles) override {
        for (auto& p : particles) p.resetForce();

        int n = particles.size();
        for (int i = 0; i < n; ++i) {
            for (int j = i + 1; j < n; ++j) {
                double dx = particles[i].x - particles[j].x;
                double dy = particles[i].y - particles[j].y;
                double r2 = dx * dx + dy * dy;
                double r = std::sqrt(r2);

                if (r < cutOff) r = cutOff;

                double sr = sigma / r;
                double sr6 = std::pow(sr, 6);
                double sr12 = sr6 * sr6;
                
                // F = (24*eps/r) * (2*sr12 - sr6)
                double forceMag = (24.0 * epsilon / r) * (2.0 * sr12 - sr6);

                double fx = forceMag * (dx / r);
                double fy = forceMag * (dy / r);

                particles[i].addForce(fx, fy);
                particles[j].addForce(-fx, -fy);
            }
        }
    }
};
