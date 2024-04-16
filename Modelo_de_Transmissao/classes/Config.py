import numpy as np
import cv2

class Config:
    
    def dBm2Lin(dBm):
        Lin = pow(10,-3) * pow(10,(dBm/10))
        return Lin
    
    #Pb = dBm2Lin(30);
    Pb = 10**(30/10)
    #Pu = dBm2Lin(10);
    Pu = 10**(10/10)
    sigma = -94;
    FUL = 5000;
    FDL = 50000;
    NW = 30;
    b = 2;
    M = 15;
    m = 0.7;
    phi = 30;
    Y = 10;
    gamma = 0.5;
    w = 0.98;
    sigSquareGA_i = 0.151;
    dzero = 5;
    #fc = 28
    fc = 28 * 10**9;
    c = 3 * 10**8;
    wlLoS = 2;
    wlNLoS = 2.4;
    miSigmaLoS = 5.3;
    miSigmaNLoS = 5.27;
    GA = 11;
    gammaDelay = 8;
    gammaQuality = 0.8;
    sigmaSquare_i = 0.193;
    A = 50;
    T = 5;
    lambda_ = 0.005;
    L = 3;
    v = 2;
    sigmaSquareB = 0.05;

    #####################################
    us = 20; # numero de usuários
    bs = 5; # numero de base stations
    obj = 1; # numero de objetos
    ti = 100; # quantidade de estampas de tempo
    V = 10; # limite de usuários bor BS no Downlink
    
    prefix_in = ''
    #prefix_in = 'instances/' + str(us) + '/'
    
    prefix_out = ''
    #prefix_out = 'outputs/OP/' + str(us) + '_'
    
    users_file = prefix_in + 'users.json'
    bs_file = prefix_in + 'base_stations.json'
    decisions_file = prefix_in + 'BIP_for_all_combinations.json'
    results_file_opt = prefix_out + 'optimal_results.json'
    results_file_meta = prefix_out + 'meta_results.json'
    #####################################
    #p_2 = dBm2Lin(-105)
    p_2 = 10**(-105/10)

    VR_Frame = cv2.imread("3DShootGame-Frame.jpg")
    num_pixels = VR_Frame.shape[0]*VR_Frame.shape[1]*VR_Frame.shape[2]
    
    # convert to RGB
    VR_Frame = cv2.cvtColor(VR_Frame, cv2.COLOR_BGR2RGB)
    
    BaseResolution = len(VR_Frame) * len(VR_Frame[0])
    
    BaseResolutionBitsPerPixel = 24;
    
    
    LightSpeed = 299792458


