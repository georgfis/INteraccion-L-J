#include <iostream>
#include <vector>
#include <memory>
#include <fstream>
#include <string>
#include <random>
#include "../include/Particle.h"
#include "../include/Box.h"
#include "../include/Potential.h"
#include "../include/Integrator.h"

class Simulation {
private:
    std::vector<Particle> particles;
    Box box;
    std::unique_ptr<ForceCalculator> potential;
    std::unique_ptr<Integrator> integrator;
    double time;

public:
    Simulation(double w, double h, double dt) 
        : box(w, h), time(0) {
        potential = std::make_unique<LennardJones>(1.0, 1.0);
        integrator = std::make_unique<VelocityVerlet>(dt);
    }

    void initGrid(int nParticles, double vMax) {
        int side = std::ceil(std::sqrt(nParticles));
        double spacing = box.getWidth() / (side + 1.0);
        std::mt19937 gen(42);
        std::uniform_real_distribution<> disV(-vMax, vMax);

        int count = 0;
        for(int i=0; i<side && count < nParticles; ++i){
            for(int j=0; j<side && count < nParticles; ++j){
                double x = (i + 1) * spacing;
                double y = (j + 1) * spacing;
                particles.emplace_back(count, x, y, disV(gen), disV(gen));
                count++;
            }
        }
        potential->calculateForces(particles);
    }

    void run(int steps, const std::string& filename) {
        std::ofstream file(filename);
        file << "t";
        for (const auto& p : particles) file << ",x" << p.id << ",y" << p.id << ",vx" << p.id << ",vy" << p.id;
        file << "\n";

        for (int s = 0; s < steps; ++s) {
            file << time;
            for (const auto& p : particles) {
                file << "," << p.x << "," << p.y << "," << p.vx << "," << p.vy;
            }
            file << "\n";
            integrator->step(particles, box, *potential);
            time += 0.005; 
        }
        file.close();
        std::cout << "Datos guardados en " << filename << std::endl;
    }
};

int main(int argc, char* argv[]) {
    int N = 16;
    double W = 20.0;
    int steps = 2000;
    std::string output = "results/data.csv";

    if(argc > 1) N = std::atoi(argv[1]);
    if(argc > 2) W = std::atof(argv[2]);
    if(argc > 3) steps = std::atoi(argv[3]);
    if(argc > 4) output = argv[4];

    Simulation sim(W, W, 0.005);
    sim.initGrid(N, 1.0); 
    sim.run(steps, output);

    return 0;
}
