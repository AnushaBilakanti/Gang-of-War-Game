'''
Created on October 17, 2016
@author: Anusha Bilakanti
'''

import copy
def minimaxDecision(board_state,n,mode,player,cell_values,first_player,depth_initial):
	
	#generating the possible set of  moves
	move_list=[]
	move=0#keep track if its a stake or raid(0-stake; 1-raid)
	#list_values: have a tuple(board_state,i,j,move)
	dict={}
	moves_track=[]#all the tuples are stored here
	for i in range(n):
		for j in range(n):
			board_state_new=copy.deepcopy(board_state)
			if player=='X' and board_state_new[i][j]!='.':
				continue
			elif player=='O' and board_state_new[i][j]!='.':
				continue
			#stake move
			if player=='X' and board_state_new[i][j]=='.':
				board_state_new[i][j]='X'
				move=0
				move_list.append(board_state_new)
				#print board_state_new
			elif player=='O' and board_state_new[i][j]=='.':
				board_state_new[i][j]='O'
				move=0
				move_list.append(board_state_new)

			
			list_values=(board_state_new,i,j,move)
			moves_track.append(list_values)
				
			conquer=0

			board_state_raid=copy.deepcopy(board_state_new)
			#check if any adjacent positions have same player
			if (i!=n-1 and board_state_raid[i+1][j]==board_state_raid[i][j]) or (i!=0 and board_state_raid[i-1][j]==board_state_raid[i][j]) or (j!=n-1 and board_state_raid[i][j+1]==board_state_raid[i][j]) or (j!=0 and board_state_raid[i][j-1]==board_state_raid[i][j]): 
				conquer=1

			#conquering
			if conquer:
				if i!=0 and board_state_raid[i-1][j]!='.' and board_state_raid[i-1][j]!=board_state_raid[i][j]:
					board_state_raid[i-1][j]=board_state_raid[i][j]
					move=1
					
				if j!=n-1 and  board_state_raid[i][j+1]!='.' and board_state_raid[i][j+1]!=board_state_raid[i][j]:
					board_state_raid[i][j+1]=board_state_raid[i][j]
					move=1
					
				if j!=0 and  board_state_raid[i][j-1]!='.' and board_state_raid[i][j-1]!=board_state_raid[i][j]:
					board_state_raid[i][j-1]=board_state_raid[i][j]
					move=1
					
				if i!=n-1 and  board_state_raid[i+1][j]!='.' and board_state_raid[i+1][j]!=board_state_raid[i][j]:
					board_state_raid[i+1][j]=board_state_raid[i][j]
					move=1
				
			move_list.append(board_state_raid)
			list_values=(board_state_raid,i,j,move)
			moves_track.append(list_values)
	#for each of these moves min_value is called
	value=-9999
	if player=='X':
		player='O'
	else:
		player='X'
	for board_state_item in move_list:
		if mode=="MINIMAX":
			value_ret=minValue(board_state_item,n,mode,player, 1, cell_values,first_player,depth_initial,0,0)
		else:
			value_ret=minValue(board_state_item,n,mode,player, 1, cell_values,first_player,depth_initial,-9999,9999)
		if value_ret>value:
			value=value_ret
			best_move=board_state_item
			for i in moves_track:
				if best_move==i[0]: #got the best move from above and in the tuple searched for that board and found its i,j and move value
					best_result=i
			move_value=best_result[3]
		#used to check if there are two states with same score and stake happens in the second move and raid in first'''
		elif value_ret==value:
			for i in moves_track:
				if board_state_item==i[0]:
					obtained=i
			if move_value==1 and obtained[3]==0:
				value=value_ret
				best_move=board_state_item
				continue
			if move_value==1 and obtained[3]==1:#between two raids
				continue
			if move_value==0 and obtained[3]==0:#between two stakes
				continue
			if move_value==0 and obtained[3]==1: #first stake and then raid
				continue
	for i in moves_track:
		if best_move==i[0]: #got the best move from above and in the tuple searched for that board and found its i,j and move value
			best_result=i

	col=str(chr(best_result[2]+65))
	row=str(best_result[1]+1)
	if best_result[3]==1:
		final_move="Raid"
	else:
		final_move="Stake"
	#print to file
	out_file=open("output.txt","w")
	out_file.write(col+row+" "+final_move)
	for i in best_result[0]:
		out_file.write("\n")
		for j in i:
			out_file.write(str(j))
	out_file.write("\n")
	out_file.close()

def maxValue(board_state,n,mode,player, depth, cell_values,first_player,depth_initial,alpha,beta):
	sum_X=0
	sum_O=0
	move_list=[]
	move_list1=[]
	move_list2=[]
	#computing terminal utility value
	if depth==depth_initial: #checking terminal state
		for i in range(n):
			for j in range(n):
				if board_state[i][j]=='X': #compute game score
					sum_X=sum_X+int(cell_values[i][j])
				elif board_state[i][j]=='O':
					sum_O=sum_O+int(cell_values[i][j])
		if first_player=='X':
			return sum_X - sum_O
		else:
			return sum_O - sum_X

	full=0
	for i in range(n):                  #checking terminal state
		for j in range(n):
			if board_state[i][j]=='.':
				full=1
				break

	if full==0:
		for i in range(n):
			for j in range(n):
				if board_state[i][j]=='X': #compute game score
					sum_X=sum_X+int(cell_values[i][j])
				elif board_state[i][j]=='O':
					sum_O=sum_O+int(cell_values[i][j])
		if first_player=='X':
			return sum_X - sum_O
		else:
			return sum_O - sum_X

	value=-9999
	#move=0    #to keep track of move-default is stake
	#generating child nodes
	for i in range(n):
		for j in range(n):
			
			board_state_new=copy.deepcopy(board_state)
			if player=='X' and board_state_new[i][j]!='.':
				continue
			elif player=='O' and board_state_new[i][j]!='.':
				continue
			#stake move
			if player=='X' and board_state_new[i][j]=='.':
				board_state_new[i][j]='X'
			elif player=='O' and board_state_new[i][j]=='.':
				board_state_new[i][j]='O'
			#raid_conditions
			
			move_list1.append(board_state_new)
			
			conquer=0
			board_state_raid=copy.deepcopy(board_state_new)
			#check if any adjacent positions have same player
			if (i!=n-1 and board_state_raid[i+1][j]==board_state_raid[i][j]) or (i!=0 and board_state_raid[i-1][j]==board_state_raid[i][j]) or (j!=n-1 and board_state_raid[i][j+1]==board_state_raid[i][j]) or (j!=0 and board_state_raid[i][j-1]==board_state_raid[i][j]): 
				conquer=1

			#conquering
			if conquer:
				if i!=0 and board_state_raid[i-1][j]!='.' and board_state_raid[i-1][j]!=board_state_raid[i][j]:
					board_state_raid[i-1][j]=board_state_raid[i][j]
					move=1
					
				if j!=n-1 and  board_state_raid[i][j+1]!='.' and board_state_raid[i][j+1]!=board_state_raid[i][j]:
					board_state_raid[i][j+1]=board_state_raid[i][j]
					move=1
					
				if j!=0 and  board_state_raid[i][j-1]!='.' and board_state_raid[i][j-1]!=board_state_raid[i][j]:
					board_state_raid[i][j-1]=board_state_raid[i][j]
					move=1
					
				if i!=n-1 and  board_state_raid[i+1][j]!='.' and board_state_raid[i+1][j]!=board_state_raid[i][j]:
					board_state_raid[i+1][j]=board_state_raid[i][j]
					move=1
				
			move_list2.append(board_state_raid)

	move_list=move_list1+move_list2
	for board_new in move_list:
		#changing player
		if player=='X':
			player_new='O'
		else:
			player_new='X'
		value=max(value,minValue(board_new, n, mode,player_new, depth+1,cell_values,first_player,depth_initial,alpha,beta))
		if mode=="ALPHABETA":
			if value>=beta:
				return value
			alpha=max(alpha,value)
	return value

#Min Value
def minValue(board_state,n, mode, player, depth, cell_values,first_player,depth_initial,alpha,beta):
	move_list=[]
	move_list1=[]
	move_list2=[]
	sum_X=sum_O=0
	#computing terminal utility value
	if depth==depth_initial: #checking terminal state
		for i in range(n):
			for j in range(n):  
				if board_state[i][j]=='X': #compute game score
					sum_X=sum_X+int(cell_values[i][j])
				elif board_state[i][j]=='O':
					sum_O=sum_O+int(cell_values[i][j])
		if first_player=='X':
			return sum_X - sum_O
		else:
			return sum_O - sum_X

	full=0
	for i in range(n):                  #checking terminal state
			for j in range(n):
				if board_state[i][j]=='.':
					full=1
					break

	if full==0:
		for i in range(n):
			for j in range(n):
				if board_state[i][j]=='X': #compute game score
					sum_X=sum_X+int(cell_values[i][j])
				elif board_state[i][j]=='O':
					sum_O=sum_O+int(cell_values[i][j])
		if first_player=='X':
			return sum_X - sum_O
		else:
			return sum_O - sum_X

	value=9999
	move=0 #to keep track of move-default is stake
	#generating child nodes
	for i in range(n):
		for j in range(n):
			board_state_new=copy.deepcopy(board_state)
			if player=='X' and board_state_new[i][j]!='.':
				continue
			elif player=='O' and board_state_new[i][j]!='.':
				continue
			#stake move
			if player=='X' and board_state_new[i][j]=='.':
				board_state_new[i][j]='X'
			elif player=='O' and board_state_new[i][j]=='.':
				board_state_new[i][j]='O'

			move_list1.append(board_state_new)
			#raid_conditions
			conquer=0

			board_state_raid=copy.deepcopy(board_state_new)
			#check if any adjacent positions have same player
			if (i!=n-1 and board_state_raid[i+1][j]==board_state_raid[i][j]) or (i!=0 and board_state_raid[i-1][j]==board_state_raid[i][j]) or (j!=n-1 and board_state_raid[i][j+1]==board_state_raid[i][j]) or (j!=0 and board_state_raid[i][j-1]==board_state_raid[i][j]): 
				conquer=1

			#conquering
			if conquer:
				if i!=0 and board_state_raid[i-1][j]!='.' and board_state_raid[i-1][j]!=board_state_raid[i][j]:
					board_state_raid[i-1][j]=board_state_raid[i][j]
					move=1
					
				if j!=n-1 and  board_state_raid[i][j+1]!='.' and board_state_raid[i][j+1]!=board_state_raid[i][j]:
					board_state_raid[i][j+1]=board_state_raid[i][j]
					move=1
					
				if j!=0 and  board_state_raid[i][j-1]!='.' and board_state_raid[i][j-1]!=board_state_raid[i][j]:
					board_state_raid[i][j-1]=board_state_raid[i][j]
					move=1
					
				if i!=n-1 and  board_state_raid[i+1][j]!='.' and board_state_raid[i+1][j]!=board_state_raid[i][j]:
					board_state_raid[i+1][j]=board_state_raid[i][j]
					move=1
				
			move_list2.append(board_state_raid)
	move_list=move_list1+move_list2
	for board_new in move_list:	
		#changing player
		if player=='X':
			player_new='O'
		else:
			player_new='X'
		value=min(value,maxValue(board_new,n,mode,player_new, depth+1, cell_values,first_player,depth_initial,alpha,beta))
		if mode=="ALPHABETA":
			if value<=alpha:
				return value
			beta=min(beta,value)
	return value

obj=open('input.txt','r')
n=int(obj.readline().strip()) #n=width and height
mode=obj.readline().strip()
youplay=obj.readline().strip()
first_player=youplay
depth=int(obj.readline().strip())
depth_initial=depth
cell_values=[[0 for x in range(n)] for y in range(n)] 
for i in range(n):
	read_values=obj.readline().strip().split(" ")
	for j in range(n):
		cell_values[i][j]=read_values[j]
board_state=[[0 for x in range(n)] for y in range(n)] 
for i in range(n):
	read_pos=obj.readline().strip()
	for j in range(n):
		board_state[i][j]=read_pos[j]
minimaxDecision(board_state,n,mode,youplay,cell_values,first_player,depth_initial)
