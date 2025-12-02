#pragma once
#include <vector>
#include "Particle.h"
#include "Box.h"
#include "Potential.h"

class Integrator {
protected:
    double dt;
public:
    Integrator(double timeStep) : dt(timeStep) {}
    virtual void step(std::vector<Particle>& particles, Box& box, ForceCalculator& potentials) = 0;
    virtual ~Integrator() = default;
};

class VelocityVerlet : public Integrator {
public:
    VelocityVerlet(double dt) : Integrator(dt) {}

    void step(std::vector<Particle>& particles, Box& box, ForceCalculator& potentials) override {
        // Paso 1: r(t+dt), v(t+0.5dt)
        for (auto& p : particles) {
            double ax = p.fx / p.mass;
            double ay = p.fy / p.mass;
            p.vx += 0.5 * ax * dt;
            p.vy += 0.5 * ay * dt;
            p.x += p.vx * dt;
            p.y += p.vy * dt;
            box.applyBoundaryConditions(p);
        }

        // Paso 2: Fuerzas nuevas
        potentials.calculateForces(particles);

        // Paso 3: v(t+dt)
        for (auto& p : particles) {
            double ax = p.fx / p.mass;
            double ay = p.fy / p.mass;
            p.vx += 0.5 * ax * dt;
            p.vy += 0.5 * ay * dt;
        }
    }
};
