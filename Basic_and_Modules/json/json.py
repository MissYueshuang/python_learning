# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 14:03:27 2020

@author: rmileng
"""
import json

with open(r'D:\LYS\python learning\result_files\person.json') as f:
  data = json.load(f)
print(data)

person_dict = {"name": "Bob",
"languages": ["English", "Fench"],
"married": True,
"age": 32
}

with open(r'D:\LYS\python learning\result_files\person.txt', 'w') as json_file:
  json.dump(person_dict, json_file)


## https://blog.csdn.net/luxideyao/article/details/77802389 
# JSONPath 是参照，xpath表达式来解析xml文档的方式，json数据结构通常是匿名的并且不一定需要有根元素。JSONPaht 用一个抽象的名字$来表示最外层对象。

#JOSNPath 表达式可以使用.  符号如下：
#$.store.book[0].title
#或者使用[] 符号
#$['store']['book'][0]['title']


#从输入路径来看。内部或者输出的路径都会转化成-符号。
#
#JSONPath 允许使用通配符 * 表示所以的子元素名和数组索引。还允许使用 '..' 从E4X参照过来的和数组切分语法[start:end:step]是从ECMASCRIPT 4 参照过来的。
#
#表达式在下面的脚本语言中可以使用显示的名称或者索引：
#$.store.book[(@.length-1)].title
#
#
#使用'@'符号表示当前的对象，?(<判断表达式>) 使用逻辑表达式来过滤。
#$.store.book[?(@.price < 10)].title
  
  
  
  
#这里有个表格，说明JSONPath语法元素和对应XPath元素的对比。
#XPath	JSONPath	Description
#/	      $	          表示根元素
#.	      @	          当前元素
#/	      . or []	    子元素
#..	     n/a	        父元素
#//	     ..	         递归下降，JSONPath是从E4X借鉴的。
#*	      *	          通配符，表示所有的元素
#@	      n/a	        属性访问字符
#[]	     []	         子元素操作符
#|	      [,]	    连接操作符在XPath 结果合并其它结点集合。JSONP允许name或者数组索引。
#n/a	[start:end:step]	数组分割操作从ES4借鉴。
#[]	     ?()	        应用过滤表示式
#n/a	      ()	   脚本表达式，使用在脚本引擎下面。
#()	     n/a	        Xpath分组 



#XPath还有很多的语法（本地路径，操作符，和函数）没有列在这里。只要知道xpath和jsonpath脚本之中的不同点就行了。
#[]在xpath表达式总是从前面的路径来操作数组，索引是从1开始。
#使用JOSNPath的[]操作符操作一个对象或者数组，索引是从0开始。


  
{ "store": {
    "book": [ 
      { "category": "reference",
        "author": "Nigel Rees",
        "title": "Sayings of the Century",
        "price": 8.95
      },
      { "category": "fiction",
        "author": "Evelyn Waugh",
        "title": "Sword of Honour",
        "price": 12.99
      },
      { "category": "fiction",
        "author": "Herman Melville",
        "title": "Moby Dick",
        "isbn": "0-553-21311-3",
        "price": 8.99
      },
      { "category": "fiction",
        "author": "J. R. R. Tolkien",
        "title": "The Lord of the Rings",
        "isbn": "0-395-19395-8",
        "price": 22.99
      }
    ],
    "bicycle": {
      "color": "red",
      "price": 19.95
    }
  }
}
    
#XPath	                  JSONPath	           结果
#/store/book/author	$.store.book[*].author	书点所有书的作者
#//author	           $..author	          所有的作者
#/store/*	           $.store.*	      store的所有元素。所有的bookst和bicycle
#/store//price	      $.store..price	  store里面所有东西的price
#//book[3]	          $..book[2]	            第三个书
#//book[last()]	     $..book[(@.length-1)]	  最后一本书
#//book[position()<3]	$..book[:2]        前面的两本书。
#//book[isbn]	   $..book[?(@.isbn)]	 过滤出所有的包含isbn的书。
#//book[price<10]	$..book[?(@.price<10)]	过滤出价格低于10的书。
#//*	                        $..*	           所有元素。    