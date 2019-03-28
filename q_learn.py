import numpy as np
grid_shape = (3,3)
goal_state = (2,2)
trap_state = (2,1)
start_state = 0, 0

def is_feasible(i,j,move="left"):
    if move == "left":
        if j-1 >= 0:
            return True
        else:
            return False
    elif move == "right":
        if j+1 <= grid_shape[0]-1:
            return True
        else:
            return False
    elif move == "up":
        if i+1 <= grid_shape[1]-1:
            return True
        else:
            return False
    elif move == "down":
        if i-1 >= 0:
            return True
        else:
            return False
    else:
        print("error")

def get_next_state(i,j,move="left"):
    if (i,j) == goal_state or (i,j) == trap_state:
        return start_state
    if is_feasible(i,j,move):
        if move =="left":
            return i,j-1
        if move == "right":
            return i,j+1
        if move == "up":
            return i+1, j
        if move == "down":
            return i-1,j
    else:
        return i,j

def get_rew(i,j,move):
    i,j = get_next_state(i,j,move)
    if (i,j) == trap_state:
        return -1
    if (i,j) == goal_state:
        return 10
    else:
        return 0

def chose_max_action(i,j,vals):
    if (i,j) == trap_state:
        return -1
    return np.max(vals[i,j])

def print_nicely(vals):
    for i in range(3):
        str_print = ""
        for j in range(3):
            if (i,j) == trap_state:
                str_print +=".X trap.||"
            elif (i,j) == goal_state:
                str_print += "..final.||"
            else:    
                str_print += str(vals[i,j,0])[:3] + " " + str(vals [ i , j ,1])[:3]+" ||"
        print(str_print)
        str_print = ""
        for j in range(3):
            if (i,j) == trap_state:
                str_print +=".X trap.||"
            elif (i,j) == goal_state:
                str_print += "..final.||"
            else:
                str_print += str(vals[i,j,2])[:3] + " " + str(vals [ i , j ,3])[:3]+" ||"
        
        print(str_print)
        print("-------------------------------")
    print("####################################")

if __name__ == "main":
	np.random.seed(np.random.randint(1000))

np.random.seed(np.random.randint(1000))
vals = np.zeros((3,3,4))
gamma = .9
state_seq = [(0,0)]
action_to_ind = {"left":0, "right" : 1, "up":2, "down":3}
action = {1:"left", 2:"right", 3:"up", 4: "down"}
i = 0
j = 0
start_flag = True
episode= 0
for e in range(30):
    if start_flag : 
        i = 0
        j = 0
    eps = np.random.binomial(n=1, p =.5)
    if eps==0:
        print("exploring")
        while True :
            act = np.random.randint(low = 1, high = 5)
            if is_feasible(i,j,action[act]):
                move = action[act]
                break
        
    else :
        print("based on q values")
        max_val = np.max(vals[i,j])
        moves_poss = []
        
        for k in range(vals[i,j].shape[0]):
            if vals[i,j,k] == max_val:
                if is_feasible(i,j,action[k+1]):
                    moves_poss.append(k)

        move = np.random.randint(0,len(moves_poss))
        move = action[moves_poss[move]+1]
    
    flag = True
    print("state is",i,j,"action is",move)
    while flag:
        if is_feasible(i,j,move):
            flag = False
            prev_i = i
            prev_j = j
            if move == "left":
                j -= 1
            elif move == "right":
                j +=1
            elif move == "up":
                i += 1
            else :
                i -= 1
            if get_rew(prev_i,prev_j,move) == -1 or get_rew(prev_i,prev_j,move)==10 :
                start_flag = True
                episode += 1
            else:
                start_flag = False
            vals[prev_i,prev_j,action_to_ind[move]] =  vals[prev_i,prev_j,action_to_ind[move]] + gamma * (get_rew(prev_i,prev_j,move) + chose_max_action(i,j,vals) - vals[prev_i,prev_j,action_to_ind[move]])
            state_seq.append((i,j))

            print_nicely(vals)

            print("episode ",episode)
            vals[2,2,:] = 0

        else :
            print("chose right action")
print(state_seq)

