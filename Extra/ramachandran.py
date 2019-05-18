import math
import requests
from scipy import stats, integrate
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def get_coordinates(data, chain):
    atoms = {'N','CA','C',}   
    residue = ''
    residues = {}
    for line in data.split('\n'):
        if line.startswith('ATOM') and line[21]==chain.upper():
            line = line.split()
            atom = line[2]
            if atom in atoms:
                x = float(line[6])
                y = float(line[7])
                z = float(line[8])
                if line[5]!=residue: 
                    residue=int(line[5])
                if residue in residues:
                    residues[residue].update({atom : (x,y,z)})
                else:
                    residues[residue] = {atom : (x,y,z)}
    return residues

def calculate_cross_prod(vec1, vec2):
    return (vec1[1]*vec2[2]-vec1[2]*vec2[1],
            vec1[2]*vec2[0]-vec1[0]*vec2[2],
            vec1[0]*vec2[1]-vec1[1]*vec2[0])

def calculate_norm(vec):
    return [coordinate/sum(x**2 for x in vec)**0.5 for coordinate in vec]

def calculate_dot(vec1,vec2):
    return sum((xi*xj) for xi, xj in zip(vec1,vec2))

def calculate_mod(vec):
    return sum(x**2 for x  in vec)**0.5
            
def calculate_dih(point1, point2, point3, point4):
    vec1 = [(xi-xj) for xi, xj in zip(point1,point2)]
    vec2 = [(xi-xj) for xi, xj in zip(point2,point3)]
    vec3 = [(xi-xj) for xi, xj in zip(point3,point4)]
    
    n1 = calculate_norm(calculate_cross_prod(vec1, vec2))
    n2 = calculate_norm(calculate_cross_prod(vec2, vec3))
    
    vec2 = calculate_norm(vec2)
    
    m = calculate_cross_prod(n1, vec2)
    
    x = calculate_dot(n1, n2)
    y = calculate_dot(m, n2)
    return math.atan2(y, x)


def calculate_phi_psi(coordinates):
    phi_psi_pairs = []
    index = min(coordinates.keys())+1
    while True:
        if index+1>max(coordinates.keys()):
            break
        else:
            Ciminus = coordinates[index-1]['C']
            Ni = coordinates[index]['N']
            Cai = coordinates[index]['CA']
            Ci = coordinates[index]['C']
            Niplus = coordinates[index+1]['N']
            
            phi = math.degrees(calculate_dih(Ciminus, Ni, Cai, Ci))
            psi = math.degrees(calculate_dih(Ni, Cai, Ci, Niplus))          
            
            phi_psi_pairs.append((phi, psi))            
            index+=1
    return phi_psi_pairs

def draw_graph(phi_psi,pdb_id):
    x = [d[0] for d in phi_psi]
    y = [d[1] for d in phi_psi]
    
    sns.set_style("whitegrid")
    ax = sns.kdeplot(x, y, kernel="gau", bw = 50, cmap="Blues", n_levels = 10, shade=False, shade_lowest=False, gridsize=150)
    ax2 = sns.scatterplot(x,y,marker='+',color='Black')
    ax.set_frame_on(True)
    plt.xlim(-180, 180)
    plt.ylim(-180, 180)
    plt.xlabel('Phi')
    plt.ylabel('Psi')
    plt.title(pdb_id)
    plt.show()

if __name__ == '__main__':
    pdb_id = input('Please enter your pdb code\n')
    chain = input('Please enter which chain\n')
    data = requests.get('https://files.rcsb.org/download/{}.pdb'.format(pdb_id))
    coordinates = get_coordinates(data.text, chain.upper())
    phi_psi = calculate_phi_psi(coordinates)
    draw_graph(phi_psi, pdb_id)

