from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import (
    Rectangle,
    Ellipse,
    FancyBboxPatch,
    FancyArrowPatch,
    PathPatch
)

from matplotlib.path import Path as MplPath

W, H = 1834, 755
OUT = Path('.')
BASENAME = 'simplified'

CAPACITY_L = {
    'Reactor 1': 2500,
    'Reactor 2':10000,
    'Reactor 3': 500,
    'Tank 4' : 4000,
    'FD 6' : 1000,
    'Condenser 1' : 17.5,
    'Condenser 2' : 42.7,
    'Condenser 3' : 7.9,
    'Condenser 6' : 7.0,
    'Receiver 6' : 100,
}

MATERIAL = {
    'Reactor 1': 'HC22',
    'Reactor 2': 'HC22',
    'Reactor 3': 'HC22',
    'Tank 4' : 'GL',
    'FD 6' : 'HC22',
    'Condenser 1' : 'HC22',
    'Condenser 2' : 'HC22',
    'Condenser 3' : 'HC22',
    'Condenser 6' : 'HC22',
    'Receiver 6' : 'GL',
}

available = {f.name for f in font_manager.fontManager.ttflist}

for font in [
    # Linux
    "Noto Sans CJK JP",
    "Noto Serif CJK JP",
    "IPAexGothic",
    "IPAexMincho",
    # Windows
    "Yu Gothic",
    "Meiryo",
    "MS Gothic",
    "MS Mincho",
]:
    if font in available:
        plt.rcParams["font.family"] = font
        break
else:
    print(
        'No Japanese font type is found. Please install one such as Noto Sans CJK JP.'
    )

plt.rcParams['svg.fonttype'] = 'none'

fig, ax = plt.subplots(figsize=(W/100, H/100), dpi=150)
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
ax.set_xlim(0, W)
ax.set_ylim(H, 0)
ax.set_aspect('equal')
ax.axis('off')
fig.patch.set_facecolor('white')

BLACK = '#111111'
LW = 0.8

def text(x, y, value, size=9, ha='left', va='top'):
    ax.text(
        x, y, value,
        fontsize=size,
        ha=ha,
        va=va,
        color=BLACK,
        zorder=8
    )

def line(points, dashed=False, zorder=2):
    xs, ys = zip(*points)
    ax.plot(xs, ys,
            color=BLACK,
            lw=LW,
            linestyle=(0, (5,4)) if dashed else'-',
            zorder=zorder)

def pipe(points, both=False):
    line(points)

    ax.add_patch(
        FancyArrowPatch(
            points[-2],
            points[-1] ,
            arrowstyle='->',
            mutation_scale=7,
            lw=LW,
            color=BLACK,
            zorder=3,
        )
    )

    if both:
        ax.add_patch(
            FancyArrowPatch(
                points[1],
                points[0],
                arrowstyle='->',
                mutation_scale=7,
                lw=LW,
                color=BLACK,
                zorder = 3
            )
        )

def equipment_label(name):
    details = []

    capacity = CAPACITY_L.get(name)
    material = MATERIAL.get(name)

    if capacity is not None:
        details.append(f'{capacity:,}L')

    if material:
        details.append(material)

    if details:
        return f'{name}\n({', '.join(details)})'

    return name


def tank(x, y, name):
    w, h = 66, 66

    ax.add_patch(
        FancyBboxPatch(
            (x - w/2, y - h/2),
            w, h,
            boxstyle='round, pad=0, rounding_size=9',
            facecolor='white',
            edgecolor=BLACK,
            lw=LW,
            zorder=5
        )
    )

    text(
        x, y + h/2+8,
        equipment_label(name),
        ha='center',
        size=8
    )

def reactor(x, y, name, filter_dryer=False):
    w = 78
    top = y - 32
    bottom = y + 39

    if filter_dryer:
        ax.add_patch(
            Rectangle(
                (x - w/2, top),
                w, 60,
                facecolor = 'white',
                edgecolor=BLACK,
                lw=LW,
                zorder=5
            )
        )

        for cy in [top, bottom-10]:
            ax.add_patch(
                Ellipse(
                    (x, cy),
                    w, 15,
                    facecolor='white',
                    edgecolor=BLACK,
                    lw=LW,
                    zorder=6
                )
            )

        line(
            [(x - w/2, y+18), (x + w/2, y + 18)],
            zorder=7
        )

    else:
        verts = [
            (x - w/2, top),
            (x + w/2, top),
            (x + w/2, y + 8),
            (x + w/2, bottom),
            (x, bottom),
            (x - w/2, bottom),
            (x - w/2, y + 8),
            (x - w/2, top),
            (x - w/2, top)
        ]

        codes = [
            MplPath.MOVETO,
            MplPath.LINETO,
            MplPath.LINETO,
            MplPath.CURVE3,
            MplPath.CURVE3,
            MplPath.CURVE3,
            MplPath.CURVE3,
            MplPath.LINETO,
            MplPath.CLOSEPOLY
        ]

        ax.add_patch(
            PathPatch(
                MplPath(verts, codes),
                facecolor='white',
                edgecolor=BLACK,
                lw=LW,
                zorder=5
            )
        )

    line([(x, y-62), (x,y+18)], zorder=7)

    ax.add_patch(
        FancyBboxPatch(
            (x-11, y-86),
            61, 23,
            boxstyle='round, pad=0, rounding_size=3',
            facecolor='white',
            edgecolor=BLACK,
            lw=LW,
            zorder=7
        )
    )

    line(
        [
            (x - 17, y),
            (x + 17, y + 24),
            (x + 17, y),
            (x - 17, y + 24),
            (x - 17, y),
        ],
        zorder=7
    )

    text(
        x-100, y +49,
        equipment_label(name),
        size=8
    )

def condenser(x, y, name):
    ax.add_patch(
        FancyBboxPatch(
            (x-9, y-20),
            18, 40,
            boxstyle='round, pad=0, rounding_size=4',
            facecolor='white',
            edgecolor=BLACK,
            lw=LW,
            zorder = 5
        )
    )

    line(
        [
            (x - 5, y - 12),
            (x + 5, y - 5),
            (x - 5, y + 3),
            (x + 5, y + 11)
        ],
        zorder=7
    )

    text(
        x + 16, y - 18,
        equipment_label(name),
        size=7
    )

def receiver(x, y, name):
    ax.add_patch(
        FancyBboxPatch(
            (x - 19, y - 23),
            38, 46,
            boxstyle = 'round, pad=0, rounding_size=5',
            facecolor = 'white',
            edgecolor=BLACK,
            lw=LW,
            zorder=5,
        )
    )

    text(
        x+26, y-16,
        equipment_label(name),
        size=7
    )


text(35, 16, 'Sample Schematics', size=12)
text(
    1795, 20,
    'Volume: Nominal / Arrow: Flow direction',
    size=7.5,
    ha='right'
)

for y, upper, lower in [
    (177, '4F', '3F'),
    (399, '3F', '2F'),
    (600, '2F', '1F')
]:
    line([(38, y), (1795, y)], dashed=True)
    text(43, y - 19, upper, size = 9)
    text(43, y + 5,lower, size = 9)



#釜1, 2, 3からろ過乾燥機
for x in [420, 840, 1260]:
    line([(x, 291), (x, 377)])

line([(420, 377), (1260, 377)])
pipe([(1208, 377),
      (1208, 423),
      (1238, 423),
      (1238, 440)])

#釜1 タンク4
pipe([(401, 291),
      (401, 387),
      (630, 387),
      (630, 437)],
      both=True)

#釜2 タンク4
pipe([(821, 291),
      (821, 391),
      (670, 391),
      (670, 437)],
      both=True)

#釜3 タンク4
pipe([(683, 452),
      (1128, 452),
      (1128, 207),
      (1238, 207),
      (1238, 220)])

#FD タンク7
pipe([(1260, 511), (1260, 615)])


#コンデンサー
for x, cx in [(420, 530),
              (840, 950, 1260, 1370)]:
    #釜→コンデンサー
    pipe([(x+25, 220),
          (x+25, 212),
          (cx, 212),
          (cx, 218)]
        )




