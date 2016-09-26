#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  playersdata.py
#  
#  Copyright 2016 Alvaro Fernández Galiana <alvarofernandezgaliana@dhcp-18-189-5-170.dyn.mit.edu>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

description = ""
author = "Alvaro Fernandez"

#-------------------------------------------------

import numpy as np
import pickle 

#-------------------------------------------------

def averageDistance(dist05, dist510, dist1015, dist1520, dist20):
	return (dist05*0+dist510*5+dist1015*10+dist1520*15+dist20*20)/(dist05+dist510+dist1015+dist1520+dist20)

if __name__ == '__main__':
	
	
	#file_names = ['test.txt','test.txt']
	file_names = ['Hackathon_nba_2014-15_sv_box_scores.txt','Hackathon_nba_2015-16_sv_box_scores.txt']
	c = []
	for filename in file_names:
	
		file_obj = open(filename, 'r') 
		fields = []

		a = []
		for _ in file_obj.readline().strip().split():
			a.append( _.strip('"') )
		fields.append( a )

		for line in file_obj: 
			a = [] 
			
			for _ in line.strip().split('"'): 
				if ((_ == '\t') or (_ == '')):
					pass
				else :
					a.append( _.strip('"') )
				
			fields.append( a )
			

		#print (len(fields[0]) == len(fields[1]))

		#headersAll = np.array(fields[0])

		fieldsArray = np.array(fields)

		truth = (fieldsArray[0,:]!="DATE_EST")*(fieldsArray[0,:]!="LOCATION")*(fieldsArray[0,:]!="OUTCOME")
		headersAll = fieldsArray[0, np.array(truth)]
		dataAll = fieldsArray[1:, np.array(truth)].astype('float')

		print np.shape(dataAll)



		#print headersAll
		#print dataAll

		#print (len(fields[0]))
		#print (len(fields[1]))

		#------------------------------------


		


			

		#print fields[1]

		# -----------------------------------

		headers = np.array("GAME_ID PERSON_ID AVG_SPEED_KPH AVG_SPEED_OFF_KPH AVG_SPEED_DEF_KPH TCH_RATIO AVG_SEC_PER_TCH AVG_DRIB_PER_TCH AVG_FG_DIST SHOT_DIST_0_5_FGR SHOT_DIST_5_10_FGR SHOT_DIST_10_15_FGR SHOT_DIST_15_20_FGR SHOT_DIST_20_PLUS_FGR CATCH_SHOOT_DIST_0_10_FGRATIO CATCH_SHOOT_DIST_10_15_FGR CATCH_SHOOT_DIST_15_20_FGR CATCH_SHOOT_DIST_20_PLUS_FGR CATCH_SHOOT_FG3R DRIB_0_0_FGR DRIB_1_2_FGR DRIB_3_4_FGR DRIB_5_PLUS_FGR DRIB_0_0_FG3R DRIB_1_2_FG3R DRIB_3_4_FG3R DRIB_5_PLUS_FG3R POSS_SEC_0_2_FGR POSS_SEC_2_4_FGR POSS_SEC_4_PLUS_FGR POSS_SEC_0_2_FG3R POSS_SEC_2_4_FG3R POSS_SEC_4_PLUS_FG3R DEF_DIST_0_2_FGR DEF_DIST_2_4_FGR DEF_DIST_4_PLUS_FGR DEF_DIST_0_2_FG3R DEF_DIST_2_4_FG3R DEF_DIST_4_PLUS_FG3R SHOT_CLK_0_6_FGR SHOT_CLK_6_12_FGR SHOT_CLK_12_18_FGR SHOT_CLK_18_24_FGR SHOT_CLK_0_6_FG3R SHOT_CLK_6_12_FG3R SHOT_CLK_12_18_FG3R SHOT_CLK_18_24_FG3R CONT_RIM_DEF_1_1_FGR CONT_RIM_DEF_2_5_FGR SHOT_10FT_DEF_DIST_0_2_FGR SHOT_10FT_DEF_DIST_2_4_FGR SHOT_10FT_DEF_DIST_4_PLUS_FGR SHOT_10FT_DEF_DIST_0_2_FG3R SHOT_10FT_DEF_DIST_2_4_FG3R SHOT_10FT_DEF_DIST_4_PLUS_FG3R SHOT_10FT_DRIB_0_0_FGR SHOT_10FT_DRIB_1_2_FGR SHOT_10FT_DRIB_3_4_FGR SHOT_10FT_DRIB_5_PLUS_FGR SHOT_10FT_DRIB_0_0_FG3R SHOT_10FT_DRIB_1_2_FG3R SHOT_10FT_DRIB_3_4_FG3R SHOT_10FT_DRIB_5_PLUS_FG3R DEF_RIM_FGR PASSES_RATIO OREB_AVG_DIST OREB_CONTEST_PCT OREB_CHANCE_PCT OREB_CHANCE_PCT_ADJ DREB_AVG_DIST DREB_CONTEST_PCT DREB_CHANCE_PCT DREB_CHANCE_PCT_ADJ REB_AVG_DIST REB_CONTEST_PCT REB_CHANCE_PCT REB_CHANCE_PCT_ADJ AST_TO_PASS_PCT AST_TO_PASS_PCT_ADJ DRIVE_FTR DRIVE_FGR DRIVE_AST_PCT DRIVE_TOV_PCT ELBOW_TOUCHES_RATIO POST_TOUCHES_RATIO PAINT_TOUCHES_RATIO ELBOW_THOUCH_PTS_RATIO POST_THOUCH_PTS_RATIO PAINT_THOUCH_PTS_RATIO ELBOW_TOUCH_FTR ELBOW_TOUCH_FGR ELBOW_TOUCH_AST_PCT ELBOW_TOUCH_TOV_PCT POST_TOUCH_FTR POST_TOUCH_FGR POST_TOUCH_AST_PCT POST_TOUCH_TOV_PCT PAINT_TOUCH_FTR PAINT_TOUCH_FGR PAINT_TOUCH_AST_PCT PAINT_TOUCH_TOV_PCT".split())

		Ncol = len(headers)
		Nrow = len(fields)-1

		b = np.ones((Nrow, Ncol))


		for col_ind in xrange(Ncol):
			
			label = headers[col_ind]
			if label.endswith("R"):
				
				prefix = label[:-1]
				labelA = prefix+"A"
				labelM = prefix+"M"
				truthA = headersAll==labelA
				truthM = headersAll==labelM
				
				if np.any(truthA) and np.any(truthM):

					a = dataAll[:, truthA]
					m = dataAll[:, truthM]
					a[a==0.0] = 1.0
					r = m/a
					b[:, headers==label] = r
				
				else:
					print labelA
					print "Label ends with R but not in previous"
					break
						
			else:
			
				if np.any(headersAll==label):
					b[:, headers==label] = dataAll[:, headersAll==label]
				else:
					if label == "TCH_RATIO":
						t = dataAll[:, headersAll=="NUM_TOUCHES"]
						p =  dataAll[:, headersAll=="NUM_HALF_CT_TOUCHES"]
						t[t==0.0] = 1.0
						r = p/t
						b[:, headers==label] = r
						
					elif label == "AVG_FG_DIST":
						b[:, headers==label] = dataAll[:, headersAll=="SHOT_DIST_0_5_FGA"]*0+dataAll[:, headersAll=="SHOT_DIST_5_10_FGA"]*5+dataAll[:, headersAll=="SHOT_DIST_10_15_FGA"]*10+dataAll[:, headersAll=="SHOT_DIST_15_20_FGA"]*15+dataAll[:, headersAll=="SHOT_DIST_20_PLUS_FGA"]*20 
					
					# Calculation of the ratio of field goals from a catch and shoot made from 0-10 ft, by considering the the total amount of catch shoot inside the 3pt line is the substaction of the zero dribble FG to the zero dribble 3pt. Therefore, the amount of catch and shoot made in short distance is the total number made inside the 3pt line minus the ones at 10+ft
					elif label == "CATCH_SHOOT_DIST_0_10_FGRATIO":
						t = dataAll[:, headersAll=="DRIB_0_0_FGA"]-dataAll[:, headersAll=="CATCH_SHOOT_DIST_10_15_FGA"]-dataAll[:, headersAll=="CATCH_SHOOT_DIST_15_20_FGA"]-dataAll[:, headersAll=="CATCH_SHOOT_DIST_20_PLUS_FGA"]-dataAll[:, headersAll=="DRIB_0_0_FG3A"]
						p =  dataAll[:, headersAll=="DRIB_0_0_FGM"]-dataAll[:, headersAll=="CATCH_SHOOT_DIST_10_15_FGM"]-dataAll[:, headersAll=="CATCH_SHOOT_DIST_15_20_FGM"]-dataAll[:, headersAll=="CATCH_SHOOT_DIST_20_PLUS_FGM"]-dataAll[:, headersAll=="DRIB_0_0_FG3M"]
						t[t==0.0] = 1.0
						r = p/t
						b[:, headers==label] = r
						
					elif label == "PASSES_RATIO":
						t = dataAll[:, headersAll=="PASSES_MADE"]
						p =  dataAll[:, headersAll=="PASSES_RECEIVED"]
						t[t==0.0] = 1.0
						r = p/t
						b[:, headers==label] = r
					
					elif label == "ELBOW_TOUCHES_RATIO":
						t = dataAll[:, headersAll=="NUM_TOUCHES"]
						p =  dataAll[:, headersAll=="ELBOW_TOUCHES"]
						t[t==0.0] = 1.0
						r = p/t
						b[:, headers==label] = r
					
					elif label == "POST_TOUCHES_RATIO":
						t = dataAll[:, headersAll=="NUM_TOUCHES"]
						p =  dataAll[:, headersAll=="POST_TOUCHES"]
						t[t==0.0] = 1.0
						r = p/t
						b[:, headers==label] = r
					
					elif label == "PAINT_TOUCHES_RATIO":
						t = dataAll[:, headersAll=="NUM_TOUCHES"]
						p =  dataAll[:, headersAll=="PAINT_TOUCHES"]
						t[t==0.0] = 1.0
						r = p/t
						b[:, headers==label] = r
					
					elif label == "ELBOW_THOUCH_PTS_RATIO":
						t = dataAll[:, headersAll=="ELBOW_TOUCH_PTS"]+dataAll[:, headersAll=="POST_TOUCH_PTS"]+dataAll[:, headersAll=="PAINT_TOUCH_PTS"]
						p =  dataAll[:, headersAll=="ELBOW_TOUCH_PTS"]
						t[t==0.0] = 1.0
						r = p/t
						b[:, headers==label] = r 
					
					elif label == "POST_THOUCH_PTS_RATIO":
						t = dataAll[:, headersAll=="ELBOW_TOUCH_PTS"]+dataAll[:, headersAll=="POST_TOUCH_PTS"]+dataAll[:, headersAll=="PAINT_TOUCH_PTS"]
						p =  dataAll[:, headersAll=="POST_TOUCH_PTS"]
						t[t==0.0] = 1.0
						r = p/t
						b[:, headers==label] = r 
					
					elif label == "PAINT_THOUCH_PTS_RATIO":
						t = dataAll[:, headersAll=="ELBOW_TOUCH_PTS"]+dataAll[:, headersAll=="POST_TOUCH_PTS"]+dataAll[:, headersAll=="PAINT_TOUCH_PTS"]
						p =  dataAll[:, headersAll=="PAINT_TOUCH_PTS"]
						t[t==0.0] = 1.0
						r = p/t
						b[:, headers==label] = r 
					
					else:
						print label
		c+=[b]
	dic={}
	dic['headers'] = headers
	dic['data'] = np.append(c[0],c[1]).reshape((-1,len(headers)))
	pickle.dump(dic,open('Playes_Games_Data.pkl', 'wt'))
	print dic['headers'].shape
	print dic['data'].shape
	#print dic['data']
	
	
	

