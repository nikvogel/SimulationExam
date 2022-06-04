\ Model ProductionMgmtProblem
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  3 x_[1] + 4 x_[2] + 3 x_[3] + 4 x_[4] + 4 x_[5] + 5 x_[6] + 12 y_[1]
   + 15 y_[2] + 30 y_[3] + 23 y_[4] + 19 y_[5] + 45 y_[6] + z_[1] + z_[2]
   + z_[3] + z_[4] + z_[5] + z_[6]
Subject To
 R0: x_[1] + z_[0] - z_[1] = 6
 R1: x_[2] + z_[1] - z_[2] = 7
 R2: x_[3] + z_[2] - z_[3] = 4
 R3: x_[4] + z_[3] - z_[4] = 6
 R4: x_[5] + z_[4] - z_[5] = 3
 R5: x_[6] + z_[5] - z_[6] = 8
 R6: x_[1] - 10 y_[1] <= 0
 R7: x_[2] - 10 y_[2] <= 0
 R8: x_[3] - 10 y_[3] <= 0
 R9: x_[4] - 10 y_[4] <= 0
 R10: x_[5] - 10 y_[5] <= 0
 R11: x_[6] - 10 y_[6] <= 0
 R12: z_[0] = 0
Bounds
Binaries
 y_[1] y_[2] y_[3] y_[4] y_[5] y_[6]
End
