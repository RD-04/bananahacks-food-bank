import random
import copy
from replit import db
from flask import Flask, render_template, url_for, request, redirect

app = Flask('app')


# [name, quanitity, calories, iron, Magnesium, vitamin C, zinc, calcium, vitamin D]

name, sex, age, weight, height, days = 0, 0, 0, 0, 0, 0
inv = [
    ["apple", 50, 180, 0.1, 5, 4.6, 0.04, 5, 0],
    ["banana", 30, 100, 0.3, 27, 8.7, 0, 5, 0],
    ["orange", 20, 150, 0.1, 10, 53.2, 0.1, 40, 0],
    ["pasta", 100, 355, 1.1, 10, 0, 0.17, 6, 0],
    ["canned beef", 85, 180, 10, 25, 0, 0, 0, 2],
    ["assorted nuts", 28, 168, 5.8, 1.6, 0.2, 0.18, 1.5, 10],
    ["milk", 250, 130, 0, 20, 0, 1.0, 30, 45],
    ["Canned beet", 246, 69, 8, 14, 20, 3.6, 0, 9.1],
    ["cereal", 20, 140, 12.6, 15, 20, 10, 15, 5],
    ["rice", 100, 130, 1.8, 1, 0, 0.91, 1.2, 8],
    ["peanut butter", 28, 161, 7, 19, 0, 0.85, 0, 0],
    ["black beans", 125, 140, 1.8, 60, 0, 0.96, 23, 0]
  ]

#[name, sex (M=True), age, weight, height, calorie, iron, Magnesium, vitamin C, zinc, calcium, vitamin D]

#Cleared

def randMeal(inv, cal):
  cur_cal = 0
  lst = []
  count = 0
  while count < 100:
    cur_item = random.randint(0, (len(inv))-1)
    if inv[cur_item][1] > 0:
      cur_cal += inv[cur_item][2]
      lst.append(cur_item)
      inv[cur_item][1] = (inv[cur_item][1])-1
      if cur_cal >= (cal-(cal*0.05)):
        count += 101
    count += 1
  print(inv)
  return [lst, inv]


def meal_grader(person, lst):
  inv = lst[1]
  lst = lst[0]

  points, cal, iron, mag, vitc, zinc, calc, vitd = 0.0,0,0,0,0,0,0,0
  
  for food in lst:
    cal += inv[food][2]
    iron += inv[food][3]
    mag += inv[food][4]
    vitc += inv[food][5]
    zinc += inv[food][6]
    calc += inv[food][7]
    vitd += inv[food][8]
  
  if person[6]>iron:
    points += 100
  else:
    points += 100*(iron/person[6])

  if person[7]>mag:
    points += 100
  else:
    points += 100*(mag/person[7])

  if person[8]>vitc:
    points += 100
  else:
    points += 100*(vitc/person[8])

  if person[9]>zinc:
    points += 100
  else:
    points += 100*(zinc/person[9])

  if person[10]>calc:
    points += 100
  else:
    points += 100*(calc/person[10])
    
  if person[11]>vitd:
    points += 100
  else:
    points += 100*(vitd/person[11])
  

  return [lst, inv, points]

'''
def meal_gen(inv, person):
  print("First: Inventory Before")
  print(inv)
  print('\n First: Inventory After')
  first = meal_grader(person, randMeal(copy.deepcopy(inv),person[5]))
  print('\n First: Day Plan')
  print(first)
'''



def meal_gen(inv, person):
  print("First: Inventory Before")
  print(inv)
  print('\n First: Inventory After')
  first = meal_grader(person, randMeal(copy.deepcopy(inv),person[5]))
  print('\n First: Day Plan')
  print(first)


  print('\n\n')

  print("Second: Inventory Before")
  print(inv)
  print('\n Second: Inventory After')
  second = meal_grader(person, randMeal(copy.deepcopy(inv),person[5]))
  print('\n Second: Day Plan')
  print(second)


  print('\n\n')

  print("Third: Inventory Before")
  print(inv)
  print('\n Third: Inventory After')
  third = meal_grader(person, randMeal(copy.deepcopy(inv),person[5]))
  print('\n Third: Day Plan')
  print(third)

  
  max_points = max(first[2], second[2], third[2])

  if first[2]==max_points:
    return first

  elif second[2]==max_points:
    return second

  else:
    return third
  


def nutri_needed(people):
  #male
  if people[1]:
    people.append(round(66+(6.3*people[3])+(12.9*people[4])-(6.8*people[2])))
    people.append(8)
    if people[2]<=30:
      people.append(400)
    else:
      people.append(420)
    people.append(90)
    people.append(11)
    if people[2]<=70:
      people.append(1000)
    else:
      people.append(1200)
    if people[2]<=70:
      people.append(0.0015)
    else:
      people.append(0.0020)
    
  #e girls (females)
  else:
    people.append(round(655+(4.3*people[3])+(4.7*people[4])-(4.7*people[2])))
    if people[2]<49:
      people.append(18)
    else:
      people.append(8)
    if people[2]<=30:
      people.append(310)
    else:
      people.append(320)
    people.append(75)
    people.append(8)
    if people[2]<=50:
      people.append(1000)
    if people[2]>=51:
      people.append(1200)
    if people[2]<=70:
      people.append(0.0015)
    else:
      people.append(0.0020)
  return people

def mainfunc(name, sex, height, weight, age, days, invi):
  global inv
  #[name, sex (M=True), age, weight, height]
  person = [name, sex, age, weight, height]

  total_days = days

  #calculates daily calorie intake and adds it to people component list

  person = nutri_needed(person)

  plan = []

  for i in range(total_days):
    cur = meal_gen(invi, person)
    print("\n\n\n\n")
    invi = cur[1]
    plan.append(cur[0])

  print(plan)
  print(invi)

  print(person)

  Give = [0] * (len(invi))

  for i in plan:
    for j in i:
      Give[j] += 1
      
  print(Give)
  print(plan) 

  inv = inv
  db["inv"] = inv
  return Give


'''
Person:
[name, sex (M=True), age, weight, height, calorie, iron, Magnesium, vitamin C, zinc, calcium, vitamin D]

Give: (length is based on number of inventory items)
[howmanyitem1, howmanyitem2, ...]

Inventory:
[]

'''


@app.route('/', methods=['GET', 'POST'])
def main_page():
  global name, sex, height, weight, age, days, inv
  if request.method == "POST":

    print("POSt method iniatlised")
    name = request.form["name"]
    sex = request.form["sex"]
    age = int(request.form["age"])
    weight = int(request.form["weight"])
    height = int(request.form["height"])
    days = int(request.form["days"])
    if sex == "Male" or sex=="male":
      sex=True
    else:
      sex=False
    return redirect(url_for("meal"))
  elif request.method == "GET":
    return render_template("homepage.html", inv=inv)






@app.route('/meal', methods=['GET'])
def meal():
  global name, sex, height, weight, age, days, inv
  meal=mainfunc(name, sex, height, weight, age, days, inv)
  print(meal)
  return render_template("meal.html", meal=meal,length=len(meal), inv=inv)


@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
  global inv
  if request.method == "POST":   
    name = request.form["name"]
    quantity = request.form["quantity"]

    for i in range(len(inv)):
      if name == inv[i][0]:
        inv[i][1]+=int(quantity)
    print("inventory processed")
    return redirect(url_for("main_page"))
  elif request.method == "GET":
    #If the method  is get then it renders the template like usual.
    return render_template("inventory.html")











app.run(host='0.0.0.0', port=8080)
