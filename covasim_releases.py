'''
Plot graph of Covasim releases over time.
'''

import numpy as np
import pylab as pl
import sciris as sc
import datetime as dt


# Command: git tag -l --sort=creatordate --format='%(creatordate:raw)|%(refname:short)'


tagdata = '''
1583907967 -0700 | Mar 10 2020 | v0.1
1584300920 -0700 | Mar 15 2020 | v0.4-oregon
1585522541 -0700 | Mar 29 2020 | v0.19.0
1586239196 -0700 | Apr 6 2020 | v0.23.5
1586493238 -0700 | Apr 9 2020 | v0.25.4
1586516412 -0700 | Apr 10 2020 | v0.26.2
1587028732 -0700 | Apr 16 2020 | v0.27.0
1587192004 -0700 | Apr 17 2020 | v0.27.12
1587288883 -0700 | Apr 19 2020 | v0.28.0
1587356375 -0700 | Apr 19 2020 | v0.28.1
1588113690 -0700 | Apr 28 2020 | v0.29.8
1588196593 -0700 | Apr 29 2020 | v1.0.0-webapp.rc2
1588629630 -0700 | May 4 2020 | v1.0.0-webapp
1588637245 -0700 | May 4 2020 | v0.30.3
1589019659 -0700 | May 9 2020 | v1.0.0
1589053637 -0700 | May 9 2020 | v1.0.1
1589130984 -0700 | May 10 2020 | v1.0.1-webapp
1589177833 -0700 | May 10 2020 | v1.0.2
1589178010 -0700 | May 10 2020 | v1.0.2-webapp
1589246429 -0700 | May 11 2020 | v1.0.3
1589329468 -0700 | May 12 2020 | v1.1.0
1589451050 -0700 | May 14 2020 | v1.1.1
1589843979 -0700 | May 18 2020 | v1.1.2
1589868175 -0700 | May 18 2020 | v1.1.3
1589870790 -0700 | May 18 2020 | v1.1.4
1589875379 -0700 | May 19 2020 | v1.1.5
1589963571 -0700 | May 20 2020 | v1.1.6
1589995787 -0700 | May 20 2020 | v1.1.7
1590046871 -0700 | May 21 2020 | v1.2.0
1590134797 -0700 | May 22 2020 | v1.2.1
1590202430 -0700 | May 22 2020 | v1.2.2
1590277268 -0700 | May 23 2020 | v1.2.3
1590407006 -0700 | May 25 2020 | v1.3.0
1590448413 -0700 | May 25 2020 | v1.3.1
1590458360 -0700 | May 25 2020 | v1.3.2
1590545697 -0700 | May 26 2020 | v1.3.3
1590573781 -0700 | May 27 2020 | v1.3.4
1590706136 -0700 | May 28 2020 | v1.3.5
1590751555 -0700 | May 29 2020 | v1.4.0
1590822434 -0700 | May 30 2020 | v1.4.1
1590906532 -0700 | May 30 2020 | v1.4.2
1590910948 -0700 | May 31 2020 | v1.4.3
1590963072 -0700 | May 31 2020 | v1.4.4
1590988463 -0700 | May 31 2020 | v1.4.5
1591038208 -0700 | Jun 1 2020 | v1.4.6
1591170633 -0700 | Jun 3 2020 | v1.4.7
1593063246 -0700 | Jun 24 2020 | v1.4.8
1593673853 -0700 | Jul 2 2020 | v1.5.0
1597638160 +0800 | Aug 17 2020 | v1.5.1
1597818368 -0700 | Aug 18 2020 | v1.5.2
1599034956 -0700 | Sep 2 2020 | v1.5.3
1599560036 -0700 | Sep 8 2020 | v1.6.0
1600048678 -0700 | Sep 13 2020 | v1.6.1
1600653377 -0700 | Sep 20 2020 | v1.7.0
1600936044 -0700 | Sep 24 2020 | v1.7.1
1601025240 -0700 | Sep 25 2020 | v1.7.2
1602127297 -0700 | Oct 7 2020 | v1.7.3
1602128056 -0700 | Oct 7 2020 | v1.7.4
1603321639 -0700 | Oct 21 2020 | v1.7.5
1603493010 -0700 | Oct 23 2020 | v1.7.6
1607293303 -0800 | Dec 6 2020 | v2.0.0
1607421163 +0100 | Dec 8 2020 | vietnam_lancetgh
1612127429 -0800 | Jan 31 2021 | v2.0.1
1612213004 -0800 | Feb 1 2021 | v2.0.2
1615534944 -0800 | Mar 11 2021 | v2.0.3
1616138977 -0700 | Mar 19 2021 | v2.0.4
1616571208 -0700 | Mar 24 2021 | v2.1.0
1617037720 -0700 | Mar 29 2021 | v2.1.1
1617248709 -0700 | Mar 31 2021 | v2.1.2
1618311626 -0700 | Apr 13 2021 | v3.0.0
1618624954 -0700 | Apr 16 2021 | v3.0.1
1619428416 -0700 | Apr 26 2021 | v3.0.2
1621318433 -0700 | May 17 2021 | v3.0.3
1621496426 -0700 | May 20 2021 | v3.0.4
1622194995 -0700 | May 28 2021 | v3.0.5
1624350554 -0700 | Jun 22 2021 | v3.0.6
1624950086 -0700 | Jun 29 2021 | v3.0.7
1638509793 +0000 | Dec 3 2021 | v3.1.0
1638771995 +0000 | Dec 6 2021 | v3.1.1
1642391616 +0000 | Mon Jan 17 03:53 | v3.1.2
'''

# From https://www.who.int/en/activities/tracking-SARS-CoV-2-variants/
vocs = sc.objdict({
    'Pandemic declared'  : '2020-03-11',
    'Alpha + Beta VOCs' : '2020-12-18',
    'Gamma VOC' : '2021-01-11',
    'Delta VOI' : '2021-04-04',
    'Omicron VOC' : '2021-11-26',
})

vals = sc.autolist()
diffs = [0]
stamps = sc.autolist()
for l in tagdata.splitlines():
    if l:
        val = int(l.split()[0])
        vals += val/(24*60*60)
        stamps += dt.datetime.fromtimestamp(val)

vals = np.array(vals)
vals -= vals[0]
diffs = np.diff(vals)

# Line of best fit
m, b = np.polyfit(vals[1:], np.log(diffs), 1)
x = np.arange(vals[0], vals[-1])
xdates = sc.daterange(stamps[0], stamps[-1], asdate=True)
y = np.exp(m*x + b)
r2 = np.corrcoef(vals, np.exp(m*vals + b))[0,1]**2

sc.options(dpi=150)
pl.figure(figsize=(8,8))

ax1 = pl.subplot(2,1,1)
ax1.plot(stamps[1:], diffs, 'o', label='Covasim releases', alpha=0.5)
ax1.plot(xdates, y, '--', c='k')
ax1.set_title('Covasim releases over time\n', fontsize=14)
sc.setylim(ax=ax1)

ax2 = pl.subplot(2,1,2)
ax2.semilogy(stamps[1:], diffs, 'o', alpha=0.5)
ax2.plot(xdates, y, '--', label=f'Line of best fit,\ny ∝ e^{m:0.3f}x\nR² = {r2:0.2f}', c='k')


colors = sc.vectocolor(len(vocs), cmap='brg')
for a,ax in enumerate([ax1, ax2]):
    if a==1: ax.set_xlabel('Date')
    ax.set_ylabel('Days since previous release')
    sc.dateformatter(ax)

    for i,label,date in vocs.enumitems():
        label = label if a==0 else ''
        ax.axvline(sc.date(date), label=label, c=colors[i])

ax1.legend(bbox_to_anchor=(0.08,0.95))
ax2.legend(bbox_to_anchor=(0.6,0.5))
sc.figlayout()

sc.savefig('covasim-releases.png')
pl.show()