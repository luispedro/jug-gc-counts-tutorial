from matplotlib import pyplot as plt
from matplotlib import style

from jug import value, init
style.use('default')
_,jugspace = init('jugfile3.py', 'jugfile3.jugdata')

data = value(jugspace['final'])
data = data.rename(index=lambda ix: ix.split('/')[1].split('.')[1], )
data = data.sort_values(by='mean')

fig,ax = plt.subplots()
ax.plot(data['25%'], label='Q1')
ax.plot(data['50%'], label='Q2')
ax.plot(data['75%'], label='Q3')
ax.legend(loc='best')

ax.set_ylabel('GC fraction')
ax.set_xlabel('Habitat')

for x in ax.get_xticklabels():
    x.set_rotation(90)
    
fig.tight_layout()
fig.savefig('gc-per-habitat-external.pdf')
