from matplotlib import pyplot as plt 

labels = ['python', 'java', 'c++', 'ruby', 'javascript']
sizes = [215, 130, 245, 210, 210]
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lightgreen']
explode = (0.1, 0, 0, 0, 0)
plt.pie(sizes, explode=explode, labels=labels, colors=colors,autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')
plt.show()