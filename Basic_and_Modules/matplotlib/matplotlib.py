# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 15:03:54 2020

matplotlib

@author: rmileng
"""

import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-1, 1, 50)
y1 = 2*x + 1
y2 = x**2
plt.plot(x, y1)
plt.show()

plt.figure()
plt.plot(x,y1)
plt.show()

'''
对照颜色表： https://finthon.com/matplotlib-color-list/
'''

############# a whole fig start from here
plt.figure(num=3,figsize=(8,5))
plt.plot(x,y2)
plt.plot(x,y1,color='red',linewidth=1.0,linestyle='--')

# set limit
plt.xlim((-1,2))
plt.ylim((-2,3))

'''
ticks and label
func table: https://matplotlib.org/api/axis_api.html
'''
plt.xlabel('i am x')
plt.ylabel('i am y')
new_ticks = np.linspace(-1,2,5)
print(new_ticks)
plt.xticks(new_ticks)
plt.yticks([-2,-1.8,-1,1.22,3],['$really\ bad$',r'$bad\ \alpha$',r'$normal$',r'$good$','$really\ good$']) # 加一个转义符就能打出数学形态的alpha

# set the position of axis
# gca = 'get current axis'
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.spines['bottom'].set_position(('data',0)) # axes, outward
ax.spines['left'].set_position(('data',0))
plt.show()


'''
legend
'''

plt.figure(num=3,figsize=(8,5))
# initialize
plt.xlim((-1,2))
plt.ylim((-2,3))
plt.xlabel('i am x')
plt.ylabel('i am y')
new_ticks = np.linspace(-1,2,5)
plt.xticks(new_ticks)
plt.yticks([-2,-1.8,-1,1.22,3],['$really\ bad$',r'$bad\ \alpha$',r'$normal$',r'$good$','$really\ good$']) # 加一个转义符就能打出数学形态的alpha
# add label
l1, = plt.plot(x,y2,label='up')
l2, = plt.plot(x,y1,color='red',linewidth=1.0,linestyle='--',label='down')

'''
annotation
'''

x = np.linspace(-3, 3, 50)
y = 2*x + 1

plt.figure(num=1, figsize=(8, 5),)
plt.plot(x, y,)

ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data', 0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data', 0))

x0 = 1
y0 = 2*x0 + 1
plt.scatter(x0,y0,s=50,color='b')
plt.plot([x0,x0],[y0,0],'k--',lw=2.5)

# method 1
plt.annotate(r'$2x+1=%s$'%y0,xy=(x0,y0),xycoords='data',xytext=(+30,-30),textcoords='offset points',
             fontsize=16,arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=.2')) 
# xy表示注释位置，xycoords表示根据的是数据本身，xytext 表示位置偏移量，textcoords表示根据,

# method 2
plt.text(-3.7,3,r'$This\ is\ the\ some\ text.\ \mu\ \sigma_i\ \alpha_t$',fontdict={'size':16,'color':'red'}) #开始位置x,y + 内容 + 字体

plt.show()

'''
tick visibility
'''

x = np.linspace(-3, 3, 50)
y = 0.1*x

plt.figure()
plt.plot(x, y, linewidth=10, zorder=1)      # zorder值越小就越先绘制, zorder越大，相当于画上去的越晚，也就在上面了
plt.ylim(-2, 2)
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data', 0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data', 0))

list(ax.get_xticklabels()) # 得到所有x轴的刻度标签
for label in ax.get_xticklabels()+ax.get_yticklabels():
    label.set_fontsize(12)
    label.set_bbox(dict(facecolor='white',edgecolor='None',alpha=0.7)) # alpha 代表透明度

plt.show()

'''
scatter
'''
n = 1024
X = np.random.normal(0,1,n)
Y = np.random.normal(0,1,n)
T = np.arctan2(Y,X) # for color value
plt.figure()
#plt.scatter(X,Y,s=75,c=T,alpha=0.5)
plt.scatter(np.arange(5),np.arange(5))
#plt.xlim((-1.5,1.5))
#plt.ylim((-1.5,1.5))
plt.xticks(())
plt.yticks(())
plt.show()

'''
bar
'''
n = 12 # 12个柱状图
plt.figure()
X = np.arange(n)
Y1 = (1 - X / float(n)) * np.random.uniform(0.5, 1.0, n)
Y2 = (1 - X / float(n)) * np.random.uniform(0.5, 1.0, n)

plt.bar(X, +Y1, facecolor='#9999ff', edgecolor='white')
plt.bar(X, -Y2, facecolor='#ff9999', edgecolor='white')

# 加文字
for x, y in zip(X,Y1):
    # ha : horizontal alignment; va: horizontal alignment
    plt.text(x+0.2,y+0.02,'%.2f'% y, ha='center',va='bottom') 

for x, y in zip(X,Y2):
    # ha : horizontal alignment; va: horizontal alignment
    plt.text(x+0.2,-y-0.02,'-%.2f'% y, ha='center',va='top') 
    
plt.show()

'''
contours 等高线图
'''
def f(x,y):
    # the height function
    return (1 - x / 2 + x**5 + y**3) * np.exp(-x**2 -y**2)

n = 256
x = np.linspace(-3, 3, n)
y = np.linspace(-3, 3, n)
X,Y = np.meshgrid(x, y)

# use plt.contourf to filling contours
plt.contourf(X,Y,f(X,Y),8,alpha=0.75,cmap=plt.cm.hot) ## 8代表等高线有多少个圈，分成几部分
# use plt.contour to add contour lines
C = plt.contour(X,Y,f(X,Y),8,colors='black',linewidth=0.5)
# adding label
plt.clabel(C,inline=True,fontsize=10)

plt.xticks(())
plt.yticks(())

plt.show()

'''
image 图片
'''
# image data
a = np.array([0.313660827978, 0.365348418405, 0.423733120134,
              0.365348418405, 0.439599930621, 0.525083754405,
              0.423733120134, 0.525083754405, 0.651536351379]).reshape(3,3)

"""
for the value of "interpolation", check this:
http://matplotlib.org/examples/images_contours_and_fields/interpolation_methods.html

for the value of "origin"= ['upper', 'lower'], check this:
http://matplotlib.org/examples/pylab_examples/image_origin.html
"""
plt.imshow(a, interpolation='nearest', cmap='bone', origin='lower') # origin = 'lower'/'upper'
plt.colorbar(shrink=.92)

plt.xticks(())
plt.yticks(())
plt.show()

'''
3D plot
'''
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = Axes3D(fig)
# X, Y value
X = np.arange(-4, 4, 0.25)
Y = np.arange(-4, 4, 0.25)
X, Y = np.meshgrid(X, Y) # 把x和ymesh到底面
R = np.sqrt(X ** 2 + Y ** 2)
# height value
Z = np.sin(R)

ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.get_cmap('rainbow'), edgecolor='black') # stride代表网格线的跨度
"""
============= ================================================
        Argument      Description
        ============= ================================================
        *X*, *Y*, *Z* Data values as 2D arrays
        *rstride*     Array row stride (step size), defaults to 10
        *cstride*     Array column stride (step size), defaults to 10
        *color*       Color of the surface patches
        *cmap*        A colormap for the surface patches.
        *facecolors*  Face colors for the individual patches
        *norm*        An instance of Normalize to map values to colors
        *vmin*        Minimum value to map
        *vmax*        Maximum value to map
        *shade*       Whether to shade the facecolors
        ============= ================================================
"""

# I think this is different from plt12_contours
ax.contourf(X, Y, Z, zdir='z', offset=-2, cmap=plt.get_cmap('rainbow'))
"""
==========  ================================================
        Argument    Description
        ==========  ================================================
        *X*, *Y*,   Data values as numpy.arrays
        *Z*
        *zdir*      The direction to use: x, y or z (default)
        *offset*    If specified plot a projection of the filled contour
                    on this position in plane normal to zdir
        ==========  ================================================
"""

ax.set_zlim(-2, 2)

plt.show()



