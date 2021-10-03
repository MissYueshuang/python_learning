# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 16:26:11 2020

@author: rmileng
"""

#定义一个扑克类，属性是颜色，数字。
class Poker():
    def __init__(self,color,num):
        self.color = color
        self.num = num
    def __str__(self):
        return '{},{}'.format(self.color,self.num)
p1 = Poker('Hearts','A')
p2 = Poker('Spades','k')
p1.__str__()

#定义一个手类，属性是扑克牌得颜色数字
class Hand():
    def __init__(self,poker):
        self.poker = poker

left_hand = Hand(p1)
right_hand = Hand(p2)
    
#定义一个人类，属性是左手，右手。类里定义一些方法，比如交换，展示
class Person():
    
    def __init__(self,left_hand,right_hand):
        self.left_hand = left_hand
        self.right_hand = right_hand
        
    def show_hand(self):
        print(self.right_hand.poker,self.left_hand.poker)

    def swap_hand(self):
        self.right_hand.poker,self.left_hand.poker = self.left_hand.poker, self.right_hand.poker

xiaoming = Person(left_hand,right_hand)
xiaoming.show_hand()