import helper
import database
import dynamic_stability as d_s
import static_stability as s_s
import dynamic_dot_plots as d_dp
import static_dot_plots as s_dp
import os

pause = os.system('pause')

db = database.eat_database('200_database.pickle')

static_groups = [['A', 'A'], ['A', 'B'], ['A', 'C'], ['B', 'D']]
dynamic_groups = [['B', 'A'], ['B', 'B'], ['B', 'C'], ['A', 'D']]


#dynamic_dot_plot_combos
all = dynamic_pulses = [0, 1, 2, 3, 4, 5]
evens = [0, 2, 4]
odds = [1, 3, 5]
pairA = [0, 1]
pairB = [2, 3]
pairC = [4, 5]

"""
call for desired plots hereafter. helper.for_selected_do() iterates through a group
and does the selected action
"""

#helper.for_selected_do(db, dynamic_groups, d_s.make, [dynamic_pulses, 'B'])
#helper.for_selected_do(db, dynamic_groups, d_s.make, [dynamic_pulses, 'A'])


#TODO
#helper.for_selected_do(db, static_groups, s_s.make, ['static'])
#helper.for_selected_do(db, static_groups, s_dp.make, ['static'])



#helper.for_selected_do(db, dynamic_groups, d_dp.make, [all, 'B', 'all pulses'])
#helper.for_selected_do(db, dynamic_groups, d_dp.make, [all, 'A', 'all pulses'])


#helper.for_selected_do(db, dynamic_groups, d_dp.make, [evens, 'B', 'evens'])
#helper.for_selected_do(db, dynamic_groups, d_dp.make, [evens, 'A', 'evens'])

#helper.for_selected_do(db, dynamic_groups, d_dp.make, [odds, 'B', 'odds'])
#helper.for_selected_do(db, dynamic_groups, d_dp.make, [odds, 'A', 'odds'])


#helper.for_selected_do(db, dynamic_groups, d_dp.make, [pairA, 'B', 'pair A'])
#helper.for_selected_do(db, dynamic_groups, d_dp.make, [pairA, 'A', 'pair A'])


#helper.for_selected_do(db, dynamic_groups, d_dp.make, [pairB, 'B', 'pair B'])
#helper.for_selected_do(db, dynamic_groups, d_dp.make, [pairB, 'A', 'pair B'])


#helper.for_selected_do(db, dynamic_groups, d_dp.make, [pairC, 'B', 'pair C'])
#helper.for_selected_do(db, dynamic_groups, d_dp.make, [pairC, 'A', 'pair C'])

#direct call for a single plot
#d_dp.make(db['B']['C']['091'], pairC, 'A', 'pair C')

