#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sympy as sp

class Simplify():
    def __init__(self, A, x, B, u, z, H):
         self.A=A
         self.x0=x
         self.B=B
         self.u=u
         self.z=z
         self.H=H
         self.dkron=sp.Identity(A.shape[0]).as_explicit()
         self.Q=sp.Matrix(sp.MatrixSymbol('Q', A.shape[0], A.shape[1]))
         self.Q=sp.Matrix([[self.Q[i,j]*self.dkron[i,j] for i in range(A.shape[0])] for j in range(A.shape[1])])
         self.R=sp.Matrix([[sp.Symbol('R')]])
         self.P0=sp.Matrix(sp.MatrixSymbol('P_0', A.shape[0], A.shape[1]))

    def setQ(self, Q):
         self.Q=Q

    def setR(self, R):
         self.R=R

    def getPrior(self):
         self.x1_el = self.A*self.x0+self.B*self.u
         self.x1 = sp.Matrix(sp.MatrixSymbol('x1', self.x1_el.shape[0], self.x1_el.shape[1]))
         self.P1_el = self.A*self.P0*self.A.transpose() + self.Q
         self.P1 = sp.Matrix(sp.MatrixSymbol('P_1', self.P1_el.shape[0], self.P1_el.shape[1]))

    def getPosterior(self):
         self.S = self.H*self.P1*self.H.transpose() + self.R
         self.K_el = self.P1*self.H.transpose()*self.S[0]**-1
         self.K = sp.Matrix(sp.MatrixSymbol('K', self.K_el.shape[0], self.K_el.shape[1]))
         self.y_el = sp.Matrix([[self.z]]) - (self.H*self.x1)
         self.y = sp.Matrix(sp.MatrixSymbol('y', self.y_el.shape[0], self.y_el.shape[1]))
         self.x2 = self.x1 + self.K*self.y
         self.P2 = sp.Identity(self.P1.shape[0]).as_explicit()*self.P1 - self.K*self.H*self.P1

    def compute(self):
         self.getPrior()
         self.getPosterior()

    def printq(self, latex=False):
         print("\n\rx_1:")
         for i in range(len(self.x1_el)):
            if(latex):
                sp.pprint(sp.Eq(sp.Symbol("x_1["+str(i)+"]"),self.x1_el[i]))
            else:
               print("x_1["+str(i)+"]="+str(self.x1_el[i]))
         print('\n\rP_1:')
         for i in range(self.P1_el.shape[0]):
            for j in range(self.P1_el.shape[1]):
                if(latex):
                    sp.pprint(sp.Eq(sp.Symbol("P_1["+str(i)+","+str(j)+"]"),self.P1_el[i,j]))
                else:
                   print("P_1["+str(i)+","+str(j)+"]="+str(self.P1_el[i,j]))
         print('\n\rS:')
         for i in range(self.S.shape[0]):
            for j in range(self.S.shape[1]):
                print("S["+str(i)+","+str(j)+"]="+str(self.S[i,j]))
         print('\n\rK:')
         for i in range(self.K.shape[0]):
            for j in range(self.K.shape[1]):
                print("K["+str(i)+","+str(j)+"]="+str(self.K_el[i,j]))
         print('\n\ry:')
         for i in range(len(self.y_el)):
            print("y["+str(i)+"]="+str(self.y_el[i]))
         print('\n\rx_2:')
         for i in range(len(self.x2)):
            print("x_2["+str(i)+"]="+str(self.x2[i]))
         print('\n\rP_2:')
         for i in range(self.P2.shape[0]):
            for j in range(self.P2.shape[1]):
                print("P_2["+str(i)+","+str(j)+"]="+str(self.P2[i,j]))
