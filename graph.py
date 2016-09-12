import os
import re
import sys
import urllib
import requests
import networkx as nx
import matplotlib as plt
import itertools
def Download_page():
    for i in range(2,27):
        url = 'http://www.newyorksocialdiary.com/party-pictures?page=%d' %i
        dir = './Pagelist'
        webname = 'Page%d' %i
        urllib.urlretrieve(url, os.path.join(dir, webname))
    return
def Urllist():

    return
def Output(list, filename): 
    f = open(filename, 'w')
    f.write("\n".join(list))
    f.close()
    return

def Out(text, filename):
    f = open(filename, 'w')
    f.write(text)
    f.close()
    return
    
def Url_final():
    url_final = []
    for i in range(2,27):
        pagename = '/Users/HumbleBoy/Documents/Data_Incubator/miniprojects/graph/Pagelist/Page%d' %i
        urlfile = urllib.urlopen(pagename)
        text = urlfile.read()
        urls = re.findall(r'<span class="field-content"><a href="(\S*)"', text)
        domain = 'http://www.newyorksocialdiary.com/'
        for url in urls:
            if '2015' not in url:
                url_comp = domain + url
                url_final.append(url_comp)
    Output(url_final, 'Pre2014URLs')
    return
    
def Download_photopages():
    #Download Photo pages
    urlfile = urllib.urlopen('Pre2014URLs')
    text = urlfile.read()
    url_final = text.split('\n')
    for i in range(2, 1202):
        dir = './Webpage'
        url = url_final[i]
        webname = 'photo%d' %i
        urllib.urlretrieve(url, os.path.join(dir, webname))
    return  
     
def Alltext():
    #extract all text from photo webpages 
    filename = 'AllText'
    f = open(filename, 'w')
    for i in range(2, 1202):
        pagename = '/Users/HumbleBoy/Documents/Data_Incubator/miniprojects/graph/Webpage/photo%d' %i 
        urlfile = urllib.urlopen(pagename)
        #alltext += urlfile.read() + '\n'
        f.write(urlfile.read())
    f.close()
    return     

def Get_names(lines):
    word = lines.split()
    l = len(word)
    list = []
    for i in range(l/2):
        list.extend([(word[i] + ' ' + word[i+1])])
        del word[0]
    return list

def Add_edges(graph, crowd_names):
    allconnections = []
    l = len(crowd_names)
    if l == 1:
        return
    else:
        for i in range(l-1):
            for j in range(1,l):
                allconnections.append((crowd_names[i],crowd_names[j]))       
    graph.add_edges_from(allconnections)
    return

def Last(tuple):
    return tuple[-1]
    
def main():
    #Download_page()
    #Url_final()    
    #Download_photopages()
    #Alltext()       
    #extract alltext under each photo
    pagename = 'AllText'
    urlfile = urllib.urlopen(pagename)
    text = urlfile.read()
    nametext = re.findall(r'<td valign="top"><div align="center" class="photocaption"> (.*?)</', text)
    Output(nametext, 'NameText')
    
    #Delete fwords from NameText
    #for line in nametext[0:2]:
        #nameparts = re.findall(r'([A-Z][\S]*)\W', line)
     #   filter1 = re.sub(r'([A-Z].*)\s', line)
        
    #Get individual names,filter out non-name words 
    fwords = ['event', 'co-chairs','co-chair','dr', 'mayor','new','york', 'board', 'member',
    'executive', 'director', 'trustees', 'steering', 'committee', 'city', 'mr', 'mrs', 'miss', 
    'ms','vice', 'president','medical', 'center','benefit','fund','special','surgery',
    'big', 'c&quot', 'trustee', 'girl', 'scout', 'gala', 'chair', 'cooper', 'union', 'honoree',
    'historic', 'valley','editor', 'author','ph.d','museum', 'vice-chair', 'fall', 'house'
    , 'guest'] #need lower-cased
    #fwords = []
    #method from slack
    #reg = '|'.join(fwords)
    #nametext_filtered = []
    #for line in nametext:
    #    nametext_filtered.append(re.sub(reg, '', line))
    name_elements2 = []
    name_elements = []
    #check=0
    for line in nametext: 
        names_line = re.findall(r'([A-Z][a-zA-Z]+\s[A-Z][-\'a-zA-Z]*)', line)
        #check += len(names_line)
        name_elements2.extend([(' '.join(names_line))])
    #print 'found %d names' %(check)
    #print (','.join(names_line
    check=0
    #removecount = 0
    for line in name_elements2:
        nameparts = line.split()
        nameparts_copy = nameparts[:]
        for word in nameparts:
            if word.lower() in fwords:
                nameparts_copy.remove(word)
                #removecount += 1
        name_elements.extend([(' '.join(nameparts_copy))])
    #print 'remove %d times' %removecount
    """#my method
    name_elements = []
    for line in nametext:
        nameparts = re.findall(r'([A-Z]\S*[a-z])\W', line)
        #nameparts = re.findall(r'([A-Z][\S]*)\W', line)
        nameparts_copy = nameparts[:]
        for word in nameparts:
            if word.lower() in fwords:
                nameparts_copy.remove(word)
        name_elements.append(' '.join(nameparts_copy))
    #Output(name_elements,'Name Elements')
    """
    """
    #make namelist 
    namelist = []
    for crowd in name_elements:
        crowd_names = Get_names(crowd)
        for name in crowd_names:
            if name not in namelist:
                namelist.append(name)
    Output(namelist, 'Namelist')
    print len(namelist)
    """
    
    #Add edges to people in the same photo
    graph = nx.MultiGraph()
    for crowd in name_elements:
        crowd_names = Get_names(crowd)
        Add_edges(graph, crowd_names)
    """  
    """ 
    #Q1-degree
    graph = nx.MultiGraph()
    for crowd in name_elements:
        crowd_names = Get_names(crowd)
        Add_edges(graph, crowd_names)
    d = {}
    urlfile = urllib.urlopen('Namelist')
    namelist = urlfile.read().split('\n')
    for name in namelist:
        d[name] = len(graph.edges(name))
    deg100 = sorted(d.items(), key = Last, reverse = True)[:100]
    print 'Degree: \n', deg100
  
    """
    #Best Friends
    print 'start best friends'
    b = {}
    count = 0
    for pair in itertools.combinations(namelist,2):
        count += 1.0
        temp = graph.number_of_edges(pair[0], pair[1])  
        if temp > 8:
            b[pair] = temp
            print 'In progress:', '{:1.2f}'.format(count/(18000000.0)), '% finished'
    bf100 = sorted(b.items(), key = Last, reverse = True)[:100]
    print 'BestFriends:\n', bf100
    """
    
    #Pagerank
    graph = nx.Graph()
    for crowd in name_elements:
        crowd_names = Get_names(crowd)
        Add_edges(graph, crowd_names)
    pr = nx.pagerank(graph)
    pagerank100 = sorted(pr.items(), key = Last, reverse = True)[:100]
    print 'Pagerank:\n', pagerank100
    
    
    
    """
    #networkx package example
    G=nx.Graph()
    G.add_node("a")
    G.add_nodes_from(["b","c"])

    G.add_edge(1,2)
    G.add_edge(1,2)
    edge = ("d", "e")
    G.add_edge(*edge)
    edge = ("a", "b")
    G.add_edge(*edge)
    G.add_edges_from([("a","c"),("c","d"), ("a",1), (1,"d"), ("a",2)])
    print G.number_of_edges('a','a')
    #G.edges('d') gives all edges connected to 'd'
    #G.number_of_edges('a','b')    #gives #of edges between two nodes
    
    for i in range(2,5):
        url = 'http://www.newyorksocialdiary.com/party-pictures?page=%d' %i
        r = requests.get(url)
        #output to a file
        filename = 'Pages%d.txt' %i
        f = open(filename, 'w')
        f.write(r.text)
        f.close()
    """
if __name__ == "__main__":
  main()

#request futures package  
#futures
"""
This is my regex for capturing first names only `(^[A-Z][a-zA-Z]+$)`

[11:21]  
And this is for first name + last name `([A-Z][a-zA-Z]+\s[A-Z][-\'a-zA-Z]*)`

[11:23]  
Both of those are mutually exclusive, i.e. they both return non-overlapping strings
"""