from peewee import *
import test

db = SqliteDatabase('2021-07-31-lichess-evaluations-37MM.db')
dataset = test.EvaluationDataset(db)
for i in range (60,100):
    eval = dataset.__getitem__(i)
    eval2 = dataset.__getitemorg__(i)
    eval3 = dataset.__getitembinpacked__(i)
    print(eval2.fen)
    print(eval3)
#figure out how to translate eval this into something understandable
#add fen to sqlite database and get the binary code that way?
#convert blob feild to text feild? 

print(eval)
#print(eval2.fen)



