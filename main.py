import pygame
import math
import numpy as np
import json

'''
Constants
'''
WIDTH = 800
HEIGHT = 600
FPS = 60
series = []


'''
Distance between two points
'''
def dist(p1, p2):
    return math.ceil((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)



'''
Calculates the discrete fourier transform of a given series
'''
def dft(series , N = len(series)):
    
    dft = []
    for k in range(N):
        sum = 0
        for n in range(len(series)):
           sum += series[n] * np.exp(-1j * 2 * np.pi * k * n / N)
        dft.append({
            'real': sum.real,
            'imag': sum.imag,
            'radi': np.abs(sum),
            'phase': np.angle(sum),
            'k': k,
        })
    return dft

'''
Main class
'''
class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = False
        self.N = len(series)
        self.n = 0
        self.series_cen = []
        self.drawn = []
        self.no_vec = 50
        '''
        Shifting the points to the center of the screen
        '''
        max_width , max_height = max(np.real(series)), np.max(np.imag(series))
        for point in series:
            self.series_cen.append(-(max_width // 2) - 1j*(max_height // 2) + point)


        self.dft = dft(self.series_cen , N = self.N)
        self.dft = sorted(self.dft , key=lambda x: x['radi'] , reverse=True)
        self.update()


    def home_screen(self):
        '''
        Draw a simple home screen with text showing the intructions to speed up and down
        '''
        while not self.running:
            self.screen.fill((255, 255, 255))
            font = pygame.font.SysFont('Arial', 30)
            text = font.render("Press 'd' and 'a' to increase and decrese no of vectors", True, (0, 0, 0))
            text2 = font.render("Press ENTER TO START", True, (0, 0, 0))

            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            self.screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2 - text2.get_height() // 2 + 50))
            pygame.display.flip()
            self.events()
            


    def run(self):
        while self.running:
            self.events()
            self.draw()
            pygame.display.flip()
            if self.no_vec < 500:
                self.clock.tick(FPS)
        

    def draw(self):
        self.screen.fill((255, 255, 255))
        N = self.N
        prev_center = (0, 0)
        '''
        Finding the circles which make up the wave
        '''
        sum = 0
        for i in range(self.no_vec):
            rad = self.dft[i]["radi"]
            phase = self.dft[i]["phase"]
            k = self.dft[i]["k"]
            theta = ((2*np.pi*k*self.n)/N) + phase

            sum +=  rad*np.cos(theta)  + 1j*rad* np.sin(theta)
            
            center = (int(np.real(sum / N)), int(np.imag(sum / N)))
            pygame.draw.line(self.screen, (0, 0, 0), (prev_center[0]  + WIDTH//2 , prev_center[1] + HEIGHT//2 ), (center[0] + WIDTH//2, center[1] + HEIGHT//2))
            pygame.draw.circle(self.screen, (0, 0, 0), (center[0] + WIDTH//2, center[1] + HEIGHT//2), rad / N , width = 2)
            prev_center = center

        
        self.drawn.append(prev_center[0] + 1j*prev_center[1])
        if len(self.drawn) > 0.9*N:
            self.drawn.pop(0)
        font = pygame.font.SysFont('Arial', 30)
        text = font.render("No of Vectors : " + str(self.no_vec), True, (0, 0, 0))
        self.screen.blit(text, (WIDTH - text.get_width(), HEIGHT - text.get_height() ))
        self.n += 1
        self.n %= N   

        '''
        Draw the created figure
        '''
        for i in range( 0 , len(self.drawn) - 1):
            pygame.draw.line(self.screen, (0, 0, 0), [self.drawn[i].real + WIDTH//2, self.drawn[i].imag + HEIGHT//2] , [self.drawn[i+1].real + WIDTH//2, self.drawn[i+1].imag + HEIGHT//2], 3)


    def update(self):
        sum = 0
        N = self.N
        for i in range(N):
            rad = self.dft[i]["radi"]
            phase = self.dft[i]["phase"]
            k = self.dft[i]["k"]
            theta = ((2*np.pi*k*self.n)/N) + phase
            sum +=  rad*np.cos(theta)  + 1j*rad* np.sin(theta)
        

        if len(self.drawn) > 0.9*N:
            self.drawn.pop(0)
        self.drawn.append(sum /N)
        self.n += 1
        self.n %= N    

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.no_vec += 50
                    if self.no_vec > self.N:
                        self.no_vec = self.N
                if event.key == pygame.K_a:
                    self.no_vec -= 50
                    if self.no_vec < 0:
                        self.no_vec = 50
                if event.key == pygame.K_RETURN:
                    self.running = True
                    self.run()
    


'''
main function
'''

def main():

    global series
    global FPS
    vector = input("Enter the vector_file_name.json: ")
    points = json.load(open(vector + ".json"))["points"]
    print(points)
    for i in range(0,len(points) , 2):
        series.append(points[i]+ 1j*points[i+1])
    if len(series) > 300:
        FPS = 100
    else:
        FPS = 30
    # series = np.array(series) * 2
    main = Main()
    main.home_screen()



'''
calling main function
'''
if __name__ == '__main__':
    main()