clc
clear all
%% *Question 1: Product Mix Problem*
% *Basic Problem*

c = [-4;
     -3;
     -2;
     -2;
     -1];
A = [2 0 0 0 0;
     0 2 2 2 1;
     0.2 1 0 0.5 0;
     1 0 0 0 0;
     0 0 1 0 0;
     1 1 1 0 0;
     0 0 0 1 1];
b = [36000;
     216000;
     18000;
     16000;
     2000;
     34000;
     28000];
lb = [0;
      0;
      0;
      0;
      0];
%%
options = optimoptions('linprog', 'Algorithm', 'dual-simplex', 'Display', 'off');
[x,fval,exitflag,output,lambda] = linprog(c', A, b, [], [], lb, [], [], options)
%%
clc
clear all
%% Question 2: Integer Problem
% Implemetation of Integer Problem

c = [-1;
     -5];
A = [2 -1;
     -1 1;
     1 4];
b = [4;
     1;
     12];
lb = [0;
       0];
options = optimoptions('intlinprog', 'Display', 'off');
intcon = 1:2
[x, fval, exitflag, output] = intlinprog(c', intcon, A, b, [], [], lb, [], options)
% Relaxed Problem

options = optimoptions('linprog', 'Algorithm', 'dual-simplex', 'Display', 'off');
[x,fval,exitflag,output,lambda] = linprog(c', A, b, [], [], lb, [], [], options)
%% 
% The variable x_1 can be rounded to either 1 or 2 (floor or ceil) and x_2 to 
% 2 or 3.
% 
% Combining all the differenct variable values, four pairs can be identified 
% and have to be checked for feasibility:
% 
% x_1 = 1, x_2 = 2  --> feasible, objective value: 11
% 
% x_1 = 1, x_2 = 3 --> infeasible, violating constraints 2 and 3
% 
% x_2 = 2, x_2 = 2 --> feasible, objective value 12 
% 
% x_2 = 2, x_2 = 3 --> infeasible, violating contraint 3
% 
% ...
% Branch & Bound
% 1) Initialization
% Upper Bound: Relaxed Problem, z = 14.6, x_1*= 1.6, x_2*= 2.6
% 
% Lower Bound: Rounding down both variables, z= 11, x_1*= 1, x_2*= 2
% *2) Branching, x_1<=1 (Subproblem A),  x_1 >=2 (Subproblem B),*
% Subproblem A

A = [2 -1;
     -1 1;
     1 4;
     1 0 ];
b = [4;
     1;
     12;
     1];
[x,fval,exitflag,output,lambda] = linprog(c', A, b, [], [], lb, [], [], options)
%% 
% Subproblem B

A = [2 -1;
     -1 1;
     1 4;
     -1 0 ];
b = [4;
     1;
     12;
     -2];
[x,fval,exitflag,output,lambda] = linprog(c', A, b, [], [], lb, [], [], options)
% 3) Branching x_2<= 2 (Subproblem C), Branching x_2>= 3 (Subproblem D)
% Subproblem C

A = [2 -1;
     -1 1;
     1 4;
     -1 0;
     0 1];
b = [4;
     1;
     12;
     -2;
     2];
[x,fval,exitflag,output,lambda] = linprog(c', A, b, [], [], lb, [], [], options)
%% 
% Subproblem D

A = [2 -1;
     -1 1;
     1 4;
     -1 0;
     0 -1];
b = [4;
     1;
     12;
     -2;
     -3];
[x,fval,exitflag,output,lambda] = linprog(c', A, b, [], [], lb, [], [], options)