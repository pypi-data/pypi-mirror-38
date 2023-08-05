# -*- coding: utf-8 -*-

####################################################################################################################################
######五星红旗#######################################################################################################################
####################################################################################################################################
import turtle  
import time  
import os  
#  
def  draw_square(org_x, org_y, x, y):  
    turtle.setpos(org_x, org_y)  # to left and bottom connor  
    turtle.color('red', 'red')  
    turtle.begin_fill()  
    turtle.fd(x)  
    turtle.lt(90)  
    turtle.fd(y)  
    turtle.lt(90)  
    turtle.fd(x)  
    #print(turtle.pos())  
    turtle.lt(90)  
    turtle.fd(y)  
    turtle.end_fill()  
  
def draw_star(center_x, center_y, radius):  
    print(center_x, center_y)  
    turtle.pencolor('black')  
    turtle.setpos(center_x, center_y)  
    pt1 = turtle.pos()  
    turtle.circle(-radius, 360 / 5)  
    pt2 = turtle.pos()  
    turtle.circle(-radius, 360 / 5)  
    pt3 = turtle.pos()  
    turtle.circle(-radius, 360 / 5)  
    pt4 = turtle.pos()  
    turtle.circle(-radius, 360 / 5)  
    pt5 = turtle.pos()  
    turtle.color('yellow', 'yellow')  
    turtle.begin_fill()  
    turtle.goto(pt3)  
    turtle.goto(pt1)  
    turtle.goto(pt4)  
    turtle.goto(pt2)  
    turtle.goto(pt5)  
    turtle.end_fill()  


def flag():
    print(turtle.pos())  
    turtle.pu()  
    draw_square(-320, -260, 660, 440)  
    star_part_x = -320  
    star_part_y = -260 + 440  
    star_part_s = 660 / 30  
    center_x, center_y = star_part_x + star_part_s * 5, star_part_y - star_part_s * 5  
    turtle.setpos(center_x, center_y)  # big star center  
    turtle.lt(90)  
    draw_star(star_part_x + star_part_s * 5, star_part_y - star_part_s * 2, star_part_s * 3)  
      
    # draw 1st small star  
    turtle.goto(star_part_x + star_part_s * 10, star_part_y - star_part_s * 2)    # go to 1st small star center  
    turtle.lt(round(turtle.towards(center_x, center_y)) - turtle.heading())  
    turtle.fd(star_part_s)  
    turtle.rt(90)  
    draw_star(turtle.xcor(), turtle.ycor(), star_part_s)  
      
    # draw 2nd small star  
    turtle.goto(star_part_x + star_part_s * 12, star_part_y - star_part_s * 4)    # go to 1st small star center  
    turtle.lt(round(turtle.towards(center_x, center_y)) - turtle.heading())  
    turtle.fd(star_part_s)  
    turtle.rt(90)  
    draw_star(turtle.xcor(), turtle.ycor(), star_part_s)  
      
    # draw 3rd small star  
    turtle.goto(star_part_x + star_part_s * 12, star_part_y - star_part_s * 7)    # go to 1st small star center  
    turtle.lt(round(turtle.towards(center_x, center_y)) - turtle.heading())  
    turtle.fd(star_part_s)  
    turtle.rt(90)  
    draw_star(turtle.xcor(), turtle.ycor(), star_part_s)  
      
    # draw 4th small star  
    turtle.goto(star_part_x + star_part_s * 10, star_part_y - star_part_s * 9)    # go to 1st small star center  
    turtle.lt(round(turtle.towards(center_x, center_y)) - turtle.heading())  
    turtle.fd(star_part_s)  
    turtle.rt(90)  
    draw_star(turtle.xcor(), turtle.ycor(), star_part_s)  
    turtle.ht()  
    time.sleep(5)  
    #os._exit(1) 


####################################################################################################################################
######9420#######################################################################################################################
####################################################################################################################################

def love():
    turtle.pensize(10)
    turtle.pencolor("black")
    turtle.penup()
    turtle.goto(-50,180)
    turtle.pendown()
    turtle.goto(50,180)
    turtle.penup()
    turtle.goto(-75,90)
    turtle.pendown()
    turtle.goto(75,90)
    turtle.penup()
    turtle.goto(-100,0)
    turtle.pendown()
    turtle.goto(100,0)
    turtle.penup()
    turtle.goto(-125,-90)
    turtle.pendown()
    turtle.goto(125,-90)
    turtle.penup()
    turtle.goto(-125,-180)
    turtle.pendown()
    turtle.goto(125,-180)
    turtle.penup()
    turtle.goto(-50,180)
    turtle.pendown()
    turtle.goto(-50,90)
    turtle.penup()
    turtle.goto(0,180)
    turtle.pendown()
    turtle.goto(0,90)
    turtle.penup()
    turtle.goto(50,180)
    turtle.pendown()
    turtle.goto(50,90)
    turtle.penup()
    turtle.goto(-75,90)
    turtle.pendown()
    turtle.goto(-75,0)
    turtle.penup()
    turtle.goto(-25,90)
    turtle.pendown()
    turtle.goto(-25,0)
    turtle.penup()
    turtle.goto(25,90)
    turtle.pendown()
    turtle.goto(25,0)
    turtle.penup()
    turtle.goto(75,90)
    turtle.pendown()
    turtle.goto(75,0)
    turtle.penup()
    turtle.goto(-100,0)
    turtle.pendown()
    turtle.goto(-100,-90)
    turtle.penup()
    turtle.goto(-50,0)
    turtle.pendown()
    turtle.goto(-50,-90)
    turtle.penup()
    turtle.goto(0,0)
    turtle.pendown()
    turtle.goto(0,-90)
    turtle.penup()
    turtle.goto(50,0)
    turtle.pendown()
    turtle.goto(50,-90)
    turtle.penup()
    turtle.goto(100,0)
    turtle.pendown()
    turtle.goto(100,-90)
    turtle.penup()
    turtle.goto(-125,-90)
    turtle.pendown()
    turtle.goto(-125,-180)
    turtle.penup()
    turtle.goto(-75,-90)
    turtle.pendown()
    turtle.goto(-75,-180)
    turtle.penup()
    turtle.goto(-25,-90)
    turtle.pendown()
    turtle.goto(-25,-180)
    turtle.penup()
    turtle.goto(25,-90)
    turtle.pendown()
    turtle.goto(25,-180)
    turtle.penup()
    turtle.goto(75,-90)
    turtle.pendown()
    turtle.goto(75,-180)
    turtle.penup()
    turtle.goto(125,-90)
    turtle.pendown()
    turtle.goto(125,-180)
    turtle.penup()
    turtle.goto(-50,150)
    turtle.pendown()
    turtle.goto(-25,150)
    turtle.penup()
    turtle.goto(-25,120)
    turtle.pendown()
    turtle.goto(0,120)
    turtle.penup()
    turtle.goto(25,150)
    turtle.pendown()
    turtle.goto(25,120)
    turtle.penup()
    turtle.goto(-75,30)
    turtle.pendown()
    turtle.goto(-50,30)
    turtle.penup()
    turtle.goto(-50,60)
    turtle.pendown()
    turtle.goto(0,60)
    turtle.penup()
    turtle.goto(0,30)
    turtle.pendown()
    turtle.goto(25,30)
    turtle.penup()
    turtle.goto(50,60)
    turtle.pendown()
    turtle.goto(50,30)
    turtle.penup()
    turtle.goto(-75,-20)
    turtle.pendown()
    turtle.goto(-75,-30)
    turtle.penup()
    turtle.goto(-100,-50)
    turtle.pendown()
    turtle.goto(-75,-50)
    turtle.goto(-75,-70)
    turtle.penup()
    turtle.goto(-25,0)
    turtle.pendown()
    turtle.goto(-25,-55)
    turtle.penup()
    turtle.goto(-50,-80)
    turtle.pendown()
    turtle.goto(-25,-80)
    turtle.penup()
    turtle.goto(-4,0)
    turtle.pendown()
    turtle.goto(-4,-55)
    turtle.penup()
    turtle.goto(-4,-80)
    turtle.pendown()
    turtle.goto(-4,-90)
    turtle.penup()
    turtle.goto(0,-30)
    turtle.pendown()
    turtle.goto(25,-30)
    turtle.penup()
    turtle.goto(25,-60)
    turtle.pendown()
    turtle.goto(50,-60)
    turtle.penup()
    turtle.goto(75,-30)
    turtle.pendown()
    turtle.goto(75,-60)
    turtle.penup()
    turtle.goto(-125,-150)
    turtle.pendown()
    turtle.goto(-100,-150)
    turtle.penup()
    turtle.goto(-100,-120)
    turtle.pendown()
    turtle.goto(-75,-120)
    turtle.penup()
    turtle.goto(-50,-110)
    turtle.pendown()
    turtle.goto(-50,-120)
    turtle.penup()
    turtle.goto(-75,-145)
    turtle.pendown()
    turtle.goto(-50,-145)
    turtle.goto(-50,-165)
    turtle.penup()
    turtle.goto(0,-90)
    turtle.pendown()
    turtle.goto(0,-145)
    turtle.penup()
    turtle.goto(-25,-170)
    turtle.pendown()
    turtle.goto(0,-170)
    turtle.penup()
    turtle.goto(21,-90)
    turtle.pendown()
    turtle.goto(21,-145)
    turtle.penup()
    turtle.goto(21,-170)
    turtle.pendown()
    turtle.goto(21,-180)
    turtle.penup()
    turtle.goto(25,-120)
    turtle.pendown()
    turtle.goto(50,-120)
    turtle.penup()
    turtle.goto(50,-150)
    turtle.pendown()
    turtle.goto(75,-150)
    turtle.penup()
    turtle.goto(100,-120)
    turtle.pendown()
    turtle.goto(100,-150)
    turtle.penup()
    turtle.goto(200,-250)
    turtle.done()



####################################################################################################################################
######皮卡丘#########################################################################################################################
####################################################################################################################################
from turtle import *



def wall():
    penup()
    speed(0)
    seth(180)
    fd(40)
    seth(90)
    fd(255)
    pendown()
    seth(-90)
    pensize(5)
    pencolor("#915442")
    fd(450)
    print(position())
    penup()
    

def nut():
    penup()
    pencolor("#915442")
    fillcolor("chocolate")
    goto(-40.00,-110.00)
    pendown()
    begin_fill()
    seth(20)
    for i in range(1,7):
        fd(9)
        left(7)
    for i in range(1,4):
        fd(10)
        left(13)
    seth(120)
    for i in range(1,7):
        fd(5)
        left(13)
    for i in range(1,7):
        fd(5)
        left(5)
    end_fill()
    penup()
    goto(-40.00,-103.00)
    pendown()
    fillcolor("sandybrown")
    begin_fill()
    seth(24)
    for i in range(1,7):
        fd(9)
        left(7)
    for i in range(1,4):
        fd(9)
        left(13)
    seth(120)
    for i in range(1,5):
        fd(5)
        left(19)
    for i in range(1,7):
        fd(5)
        left(5)
    end_fill()
    penup()
    
def body():
    penup()
    goto(-40.00,-190)
    pendown()
    pencolor("#915442")
    pensize(3)
    fillcolor("#fff699")
    begin_fill()
    seth(0)
    fd(8)
    print(position())
    seth(60)
    for i in range(1,7):
        fd(3)
        right(9)
    for i in range(1,4):
        fd(4)
        right(4)
    penup()
    goto(-30.00,-190.00)
    pendown()
    seth(-30)
    for i in range(1,5):
        fd(3)
        left(12)
    print(position())
    seth(60)
    for i in range(1,4):
        fd(2)
        right(10)
    penup()
    goto(-18.58,-193.43)
    pendown()
    seth(0)
    fd(4)
    for i in range(1,4):
        fd(3)
        left(9)
    print(position())
    for i in range(1,3):
        fd(3)
        left(9)
    penup()
    goto(-5.76,-192.03)
    pendown()
    seth(-40)
    for i in range(1,3):
        fd(1)
        left(20)
    fd(8)
    seth(10)
    for i in range(1,9):
        fd(3)
        left(7)
    seth(70)
    fd(25)
    circle(25,15)
    seth(95)
    fd(35)
    circle(-18,25)
    seth(85)
    fd(30)
    for i in range(1,21):
        fd(5)
        left(7)
    end_fill()
    penup()
    goto(-32.00,-190.00)
    pendown()
    begin_fill()
    seth(60)
    for i in range(1,7):
        fd(3)
        right(9)
    for i in range(1,4):
        fd(4)
        right(4)
    end_fill()
    penup()
    goto(-27.00,-187.50)
    pendown()
    pencolor("#fff699")
    pensize(4.5)
    goto(-5.00,-180.0)
    penup()

def marginal():
    goto(-40,100)
    pencolor("#915442")
    fillcolor("#fff699")
    begin_fill()
    pendown()
    seth(15)
    fd(13)
    pencolor("#bda537")#这是耳朵边缘色
    seth(-100)
    pensize(3)
    fd(10)
    goto(-27.44,103.36)
    seth(70)
    pencolor("#915442")
    for i in range(4):
        fd(15)
        rt(5)
    for i in range(3):
        fd(17)
        rt(8)
    seth(-45)
    fd(3)
    seth(-100)
    fd(15)
    for i in range(8):
        rt(1)
        fd(1)
    seth(-108)
    fd(20)
    for i in range(3):
        fd(19)
        rt(9)
    pencolor("#915442")
    fd(8)
    penup()
    goto(3.46,96.21)
    pendown()
    pensize(4)
    seth(-10)
    fd(15)
    pensize(3)
    circle(-40,30)
    pensize(4)
    fd(10)
    pensize(3)
    circle(30,20)
    for i in range(5):
        fd(1.5)
        lt(2)
    pensize(2)
    seth(0)
    fd(5)
    pensize(3)
    seth(-160)
    circle(-80,10)
    pensize(2)
    fd(4)
    penup()
    lt(180)
    fd(4)
    pendown()
    seth(-30)
    pensize(3)
    fd(20)
    circle(-1,140)
    fd(8)
    seth(-30)
    pencolor("#d06521")
    circle(-20,45)
    penup()
    pencolor("#915442")
    goto(61.53,54.30)
    pendown()
    seth(10)
    pensize(4)
    fd(50)#从这开始耳朵要涂棕色
    print(position())
    for i in range(5):
        fd(10)
        rt(3)
    seth(-10)
    pensize(3)
    for i in range(9):
        fd(1.5)
        rt(20)
    lt(55)
    circle(-90,30)#涂到这里为止
    circle(-120,25)
    seth(110)
    pensize(1)
    fd(3)
    pensize(4)
    seth(-80)
    fd(25)
    for i in range(10):
        fd(2)
        rt(2)
    for i in range(5):
        fd(3)
        rt(3)
    fd(40)#到达了脸红色涂色的右侧边缘
    circle(-20,60)
    circle(-10,40)
    lt(25)
    fd(64.91)
    end_fill()
    
    penup()
        

def eyes():
    goto(-38,10)
    seth(45)
    pendown()
    begin_fill()
    pencolor("#6b2a18")
    fillcolor("#6b2a18")
    circle(50,30)
    circle(7,170)
    end_fill()
    goto(-34,39)
    pencolor("#fffcea")
    dot(5)
    penup()
    goto(-50,100)
    
    penup()
    pencolor("#743212")
    goto(45,-35)
    pendown()
    seth(50)
    begin_fill()
    fillcolor("#6b2a18")
    circle(50,30)
    circle(6,170)
    rt(25)
    circle(50,25)
    circle(7,30)
    circle(6,35)
    circle(7,45)
    goto(45,-35)
    end_fill()
    penup()
    goto(45,-9)
    pendown()
    pencolor("#fffcea")
    dot(5)
    penup()
    hideturtle()
        
def printleft():
    penup()
    goto(-27.44,103.36)
    fillcolor("#8b3c15")
    seth(70)
    pencolor("#915442")
    for i in range(3):
        fd(15)
        rt(5)
    begin_fill()
    for i in range(1):
        fd(15)
        rt(5)
    for i in range(3):
        fd(17)
        rt(8)
    seth(-45)
    fd(3)
    seth(-100)
    fd(15)
    for i in range(8):
        rt(1)
        fd(1)
    seth(-108)
    fd(20)
    for i in range(1):
        fd(19)
        rt(9)
    seth(95)
    circle(60,20)
    circle(10,70)
    end_fill()
    penup()

def rightprint():
    goto(61.53,54.30)
    pendown()
    seth(10)
    pensize(4)
    fd(50)
    fillcolor("#8b3c15")
    begin_fill()
    for i in range(5):
        fd(10)
        rt(3)
    seth(-10)
    for i in range(9):
        fd(1.5)
        rt(20)
    lt(55)
    circle(-90,30)
    circle(-120,7)
    seth(60)
    circle(40,30)
    circle(15,40)
    penup()
    end_fill()

def hand():
    penup()
    goto(16,-80)
    pencolor("#915442")
    pensize(3)
    fillcolor("#fff699")
    pendown()
    begin_fill()
    seth(100)
    fd(10)
    circle(10,30)
    fd(15)
    circle(10,40)
    fd(10)
    seth(300)
    fd(5)
    seth(170)
    fd(7)
    seth(280)
    fd(7)
    seth(170)
    fd(5)
    seth(250)
    fd(7)
    for i in range(1,6):
        fd(0.5)
        left(10)
    seth(-70)
    fd(15)
    circle(30,10)
    for i in range(1,5):
        fd(7)
        left(4)
    end_fill()
    pendown()

def nose():
    penup()
    goto(2,-15)
    pendown()
    pencolor("#915442")
    dot(4)
    penup()

def pikachu():
        
    wall()
    body()
    marginal()
    nut()
    printleft()
    rightprint()
    hand()
    nose()
    eyes()

    done()

####################################################################################################################################
######玫瑰花#########################################################################################################################
####################################################################################################################################

def rose():
    tracer(50)
    #global pen and speed
    pencolor("black")
    fillcolor("red")
    speed(50)
    s=0.08
    #init poistion
    penup()
    goto(0,600*s)
    pendown()

    begin_fill()
    circle(200*s,30)
    for i in range(60):
        lt(1)
        circle(50*s,1)
    circle(200*s,30)
    for i in range(4):
        lt(1)
        circle(100*s,1)
    circle(200*s,50)
    for i in range(50):
        lt(1)
        circle(50*s,1)
    circle(350*s,65)
    for i in range(40):
        lt(1)
        circle(70*s,1)
    circle(150*s,50)
    for i in range(20):
        rt(1)
        circle(50*s,1)
    circle(400*s,60)
    for i in range(18):
        lt(1)
        circle(50*s,1)

    fd(250*s)
    rt(150)
    circle(-500*s,12)
    lt(140)
    circle(550*s,110)
    lt(27)
    circle(650*s,100)
    lt(130)
    circle(-300*s,20)
    rt(123)
    circle(220*s,57)
    end_fill()

    lt(120)
    fd(280*s)
    lt(115)
    circle(300*s,33)
    lt(180)
    circle(-300*s,33)
    for i in range(70):
        rt(1)
        circle(225*s,1)
    circle(350*s,104)
    lt(90)
    circle(200*s,105)
    circle(-500*s,63)

    penup()
    goto(170*s,-330*s)
    pendown()
    lt(160)
    for i in range(20):
        lt(1)
        circle(2500*s,1)
    for i in range(220):
        rt(1)
        circle(250*s,1)
        
    fillcolor('green')
    penup()
    goto(670*s,-480*s)
    pendown()
    rt(140)
    begin_fill()
    circle(300*s,120)
    lt(60)
    circle(300*s,120)
    end_fill()
    penup()
    goto(180*s,-850*s)
    pendown()
    rt(85)
    circle(600*s,40)

    penup()
    goto(-150*s,-1300*s)
    pendown()

    begin_fill()
    rt(120)
    circle(300*s,115)
    lt(75)
    circle(300*s,100)
    end_fill()
    penup()
    goto(430*s,-1370*s)
    pendown()
    rt(30)
    circle(-600*s,35)
    done()

    update()


####################################################################################################################################
######屋子##########################################################################################################################
####################################################################################################################################

from math import *

def house():
    speed(0)
    pensize(3)
    up();goto(-400,-200);down()
    fd(30);up();fd(20);down()
    fd(50);up();fd(20);down()
    fd(750);up();fd(10);down()
    fd(20);up();fd(10);down()
    fd(20);up();goto(-200,-200);down()
    fillcolor('#EDEDED');begin_fill()
    left(90);fd(90);x1,y1=pos()
    left(-90);fd(610)#房子长度
    x2,y2=pos()
    left(-90);fd(90);end_fill()
    up();goto(0,-200)#第一级台阶左下角坐标
    down()
    fillcolor('#CDB38B');begin_fill()
    setheading(90);fd(30);left(-90);fd(270)
    left(-90);fd(30);end_fill()
    up();goto(5,-170)#第二级台阶左下角坐标
    down()
    begin_fill();setheading(90);fd(30)
    left(-90);fd(260);left(-90);fd(30);end_fill()
    up();goto(10,-140)#第三级台阶左下角的坐标
    down()
    begin_fill();setheading(90);fd(30);left(-90);fd(250)
    left(-90);fd(30);end_fill()
    up()
    goto(10,-110)#坐标
    down()
    fillcolor('#F7F7F7');begin_fill();setheading(90)
    fd(180);left(-90);fd(250);left(-90);fd(180);end_fill()
    up();goto(10,70);down()
    fillcolor('#EEDFCC');begin_fill();setheading(90)
    fd(10);left(-90);fd(250);left(-90);fd(10);end_fill()
    up();goto(x2,y2);down();fillcolor('#F7F7F7');begin_fill()
    setheading(90);fd(190);x3,y3=pos();left(30)
    fd(150);left(120);fd(150);setheading(-90);fd(190);end_fill()
    up();goto(x3,y3);down()
    fillcolor('#B3B3B3');begin_fill();setheading(0)
    fd(10);left(120);fd(170);left(120);fd(170)
    setheading(0);fd(10);left(60);fd(150);left(-120);fd(150)
    end_fill()
    up();goto(x1,y1);down()
    fillcolor('#F7F7F7');begin_fill()
    setheading(90);fd(190);left(-30);fd(210);left(-120);fd(210);left(-30)
    fd(190)
    end_fill()
    up();goto(x1,y1+190);down()
    fillcolor('#B3B3B3');begin_fill()
    setheading(180);fd(10);left(-120);fd(230);left(-120);fd(230)
    x4,y4=pos()
    left(-120);fd(10);left(-60);fd(210);left(120);fd(210)
    end_fill()
    up();goto(x4,y4);down()
    fillcolor('#EE5C42');begin_fill()
    setheading(120);fd(130)
    x5,y5=pos()
    setheading(0);fd(360);left(-120);fd(130);setheading(180);fd(230)
    end_fill()
    up();goto(x5+300,y5);down()
    begin_fill()
    setheading(90);fd(50);left(-90);fd(30);left(-90);fd(50)
    end_fill()
    up();goto(110,-110);down()
    fillcolor('#CDC5BF');begin_fill()
    setheading(90);fd(120);left(-90);fd(60);left(-90);fd(120)
    end_fill()
    up();goto(130,-105);down()
    setheading(90);fd(70)
    up();fd(10);down();fd(20)
    up();goto(150,-110);down();fd(40)
    up();fd(30);down();fd(40)
    up();goto(160,-50);down()
    dot(5,'black')
    up();goto(x2-20,y2+20);down();setheading(90)
    fillcolor('#FF6A6A');begin_fill()
    fd(100);circle(55,180);fd(100);left(90);fd(110)
    end_fill()
    up();goto(x2-30,y2+30);down();setheading(90)
    fillcolor('#FFC125');begin_fill()
    fd(90);circle(45,180);fd(90);left(90);fd(90)
    end_fill()
    up();goto(x2-55,y2+30);down();setheading(90);fd(130)
    up();goto(x2-90,y2+30);down();setheading(90);fd(130)
    up();goto(x2-30,y2+70);down();setheading(180);fd(90)
    up();goto(x2-30,y2+100);down();setheading(180);fd(90)
    up();goto(x1+180-20,y2+20);down();setheading(90)
    fillcolor('#FF6A6A');begin_fill()
    fd(100);circle(55,180);fd(100);left(90);fd(110)
    end_fill()
    up();goto(x1+180-30,y2+30);down();setheading(90)
    fillcolor('#FFC125');begin_fill()
    fd(90);circle(45,180);fd(90);left(90);fd(90)
    end_fill()
    up();goto(x1+180-55,y2+30);down();setheading(90);fd(130)
    up();goto(x1+180-90,y2+30);down();setheading(90);fd(130)
    up();goto(x1+180-30,y2+70);down();setheading(180);fd(90)
    up();goto(x1+180-30,y2+100);down();setheading(180);fd(90)


    # up();goto(x2-75,y2+260);down();begin_fill();circle(30);end_fill()
    # up();goto(x2-75,y2+200);down();setheading(90);fd(60)
    # up();goto(x2-105,y2+230);down();setheading(0);fd(60)
    # up();goto(x1+180-75,y2+200);down();begin_fill();circle(40);end_fill()
    # up();goto(x1+180-75,y2+200);down();setheading(90);fd(80)
    # up();goto(x1+180-115,y2+240);down();setheading(0);fd(80)
    # up();goto(-300,300);down();pencolor('#5CACEE');fd(40);up();fd(10);down();fd(80)
    # up();goto(-300,320);down();fd(40);left(90);circle(20,180);setheading(0)
    # up();goto(-240,320);down();fd(80);left(90);circle(40,180);setheading(0)
    # up();goto(100,340);down();fd(50);up();fd(10);down();fd(30);up();fd(20);down()
    # fd(70)
    # up();goto(100,360);down();fd(40);left(90);circle(20,180);setheading(0)
    # up();goto(160,360);down();fd(80);left(90);circle(40,180);setheading(0)
    # up();goto(250,360);down();fd(40);left(90);circle(20,180);setheading(0)


    # tracer(False)
    # pencolor('#FF3030')
    # def koch(n,k):
    #     if n==0:
    #         forward(k)
    #     else:
    #         for angle in (60,-120,60,0):
    #             koch(n-1,k/3)
    #             left(angle)
    # delay(0)
    # i=0
    # while i<=7:
    #     x=400+50*cos(i);y=350+50*sin(i)#圆的位置可以改变
    #     up()
    #     goto(x,y)
    #     down()
    #     koch(3,10)
    #     right(120)
    #     koch(3,10)
    #     right(120)
    #     koch(3,10)
    #     i+=0.1
    # up()
    # goto(400,350)#太阳中心的坐标
    # down()
    # dot(100,'yellow')
    hideturtle()
    mainloop()



####################################################################################################################################
######轻松熊#########################################################################################################################
####################################################################################################################################

def bear():
    tracer(10)
    ht()
    fillcolor('#B8860B')
    pensize(10)
    pencolor('#5E2612')
    #body
    penup()
    goto(-70,-85)
    seth(135)
    pendown()
    begin_fill()
    circle(18,180)
    circle(200,17)
    seth(-90)
    circle(400,13)
    circle(18,180)
    seth(-104)
    circle(18,180)
    circle(400,13)
    seth(28)
    circle(200,17)
    circle(18,180)
    end_fill()
    #body white
    penup()
    goto(0,-185)
    fillcolor("white")
    pencolor("white")
    seth(0)
    pendown()
    begin_fill()
    circle(20,22.5)
    circle(30,135)
    circle(20,45)
    circle(30,135)
    circle(20,22.5)
    end_fill()
    #face
    fillcolor('#B8860B')
    pencolor('#5E2612')
    seth(-22.5)
    penup()
    goto(0,0)
    fd(120)
    pendown()
    seth(60)
    begin_fill()
    circle(75,45)
    circle(125,135)
    circle(75,45)
    circle(125,135)
    end_fill()
    pensize(17)
    penup()
    goto(45,0)
    pendown()
    circle(5,360)
    penup()
    goto(-45,0)
    pendown()
    circle(5,360)
    #face white
    penup()
    seth(-22.5)
    fd(75)
    seth(60)
    pendown()
    fillcolor("white")
    begin_fill()
    pencolor("white")
    circle(15,45)
    circle(30,135)
    circle(15,45)
    circle(30,135)
    end_fill()
    #face2
    fillcolor('#B8860B')
    pencolor('#5E2612')
    penup()
    goto(0,-15)
    pendown()
    pensize(10)
    seth(0)
    circle(5,360)
    seth(-45)
    fd(20)
    penup()
    goto(0,-15)
    seth(-135)
    pendown()
    fd(20)
    penup()
    goto(65,100)
    circle(35,170)
    pendown()
    begin_fill() 
    circle(35,205)
    end_fill() 
    penup()
    goto(-65,100)
    seth(-45)
    circle(-35,175)
    pendown()
    begin_fill() 
    circle(-35,195)
    end_fill()
    #heart
    penup()
    goto(150,150)
    seth(45)
    pencolor("red")
    fillcolor("red")
    pendown()
    begin_fill()
    fd(19)
    circle(25,45)
    circle(11.25,180)
    seth(90)
    circle(11.25,180)
    circle(25,45)
    fd(19)
    end_fill()
    update()
    hideturtle()
    mainloop()


if __name__ == '__main__':
    # flag()
    # love()
    # pikachu()
    # rose()
    # house()
    bear()

