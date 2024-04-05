#Kelompok PSO/ACO
#Soal PSO
#c14220293 Nikolas 
#c14220304 Nicholas 
#c14220331 Yesto 
#c14220329 Daniel
#c14220332 Audric

#pip install numpy
#pip install matplot

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

variables = 5 #TH, WLB, JS, HW, CE              
batasB = [10, 0, 0, 0, 0]     
batasA = [40, 100, 100, 100, 100]  
populasi = 50            
velocityMax = 1                 
personalC = 2.0 #C1         
socialC = 2.0 #C2          
maxIter = 100               

class Particle:
    def __init__(self, pos, velocity):
        self.pos = pos
        self.velocity = velocity
        self.fitness = 0
        self.best_pos = pos.copy()
        self.best_fitness = float('-inf')

class Swarm:
    def __init__(self, pop, velocityMax):
        self.particles = []
        self.best_pos = None
        self.best_fitness = float('-inf')

        for _ in range(pop):
            pos = np.random.uniform(batasB, batasA)
            velocity = np.random.rand(variables) * velocityMax
            particle = Particle(pos, velocity)
            particle.fitness = hpi(particle.pos)
            if self.best_pos is None or self.best_fitness < particle.fitness:
                self.best_pos = particle.pos.copy()
                self.best_fitness = particle.fitness
            self.particles.append(particle)

def hpi(position):
    WEIGHTS = [0.2, 0.2, 0.2, 0.2, 0.2] # w1,w2,w3,w4,w5 
    hpi = np.dot(position, WEIGHTS) #rumus hpi
    return hpi

def pso():
    swarm = Swarm(populasi, velocityMax)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    converged = False
    curr_iter = 0
 
    while curr_iter < maxIter and not converged:
        ax.clear()
        all_particles_converged = True
        for particle in swarm.particles:
            personalCoefficient = np.random.rand(variables) * personalC
            socialCoefficient = np.random.rand(variables) * socialC

            new_velocity = (particle.velocity +
                            personalCoefficient * (particle.best_pos - particle.pos) +
                            socialCoefficient * (swarm.best_pos - particle.pos))

            # update velocity
            new_velocity = np.clip(new_velocity, -velocityMax, velocityMax)

            # update posisi
            new_pos = np.clip(particle.pos + new_velocity, batasB, batasA)

            # update hpi
            particle.fitness = hpi(new_pos)

            # update personal best
            if particle.fitness > particle.best_fitness:
                particle.best_pos = new_pos
                particle.best_fitness = particle.fitness

                # update global best
                if particle.fitness > swarm.best_fitness:
                    swarm.best_pos = new_pos
                    swarm.best_fitness = particle.fitness
           
            # cek fitness particle dengan swarm (converged)
            if particle.fitness < swarm.best_fitness:
                all_particles_converged = False

            # update particle position dan velocity
            particle.pos = new_pos
            particle.velocity = new_velocity

        for particle in swarm.particles:
            ax.scatter(particle.pos[1], particle.pos[2], particle.best_fitness, c='b', marker='o')
            # untuk mengganti plot axis X dan Y Personal Best

        ax.scatter(swarm.best_pos[1], swarm.best_pos[2], swarm.best_fitness, c='r', marker='o')
        # untuk mengganti plot axis X dan Y Global Best
        # 0 = TH, 1 = WLB, 2 = JS, 3 = HW, 4 = CE

        ax.set_xlabel('Work-Life Balance')
        ax.set_ylabel('Job Satisfaction')
        ax.set_zlabel('HPI')

        ax.text2D(0.95, 1, f"Best Values: {swarm.best_pos}", transform=ax.transAxes, horizontalalignment='right')
        ax.text2D(0.08, 0.85, "Best HPI: {:.2f}".format(swarm.best_fitness), transform=ax.transAxes)
        ax.text2D(0.08, 0.80, "Particle Fitness (Local Best): {:.2f}".format(particle.best_fitness), transform=ax.transAxes)
        ax.text2D(0.08, 0.90, f"Iteration: {curr_iter}", transform=ax.transAxes)

        plt.pause(0.00001)

        # check convergence
        if all_particles_converged:
            print("The swarm has met convergence criteria after " + str(curr_iter) + " iterations.")
            converged = True
            break

        curr_iter += 1

    plt.show()


if __name__ == "__main__":
    pso()