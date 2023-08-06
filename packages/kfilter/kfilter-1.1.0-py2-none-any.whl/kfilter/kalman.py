#!/usr/bin/python
# -*- coding: UTF-8 -*-

import numpy as np

class Kalman:
     def __init__(self, A, x, B, H, Q, R, P):
          self.A = A
          self.B = B
          self.H = H
          self.Q = Q
          self.R = R
          self.x = [None, None, None]
          self.P = [None, None, None]
          self.x[0] = x
          self.P[0] = P

     def prior(self, u):  # Estimativa a priori
          self.x[1] = self.A * self.x[0] + self.B * u  # Predição do estado
          self.P[1] = self.A * self.P[0] * self.A.transpose() + self.Q  # Predição da covariância

     def posterior(self, z):  # Estimativa a posteriori
          self.S = self.H * self.P[1] * self.H.transpose() + self.R  # Resíduo da covariância
          self.K = self.P[1] * self.H.transpose() * self.S.I  # Ganho ótimo de Kalman
          y = z - self.H * self.x[1]  # Resíduo da medição
          self.x[2] = self.x[1] + self.K * y  # Estado atualizado
          self.P[2] = (np.identity(len(self.P[1])) - self.K * self.H) * self.P[1]  # Covariância atualizada
          self.x[0] = self.x[2]
          self.P[0] = self.P[2]

     def compute(self, u, z):
          self.prior(u)
          self.posterior(z)
          return self.x[2]

     def setA(self, A):
         self.A = A

     def setB(self, B):
         self.B = B

     def setQ(self, Q):
         self.Q = Q

     def setR(self, R):
         self.R = R





