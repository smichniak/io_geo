#!/usr/bin/env python3
import numpy as np
import plotly.offline as go_offline
import plotly.graph_objects as go
from math import floor
from .utility_fun import get_dem_data
from .utility_fun import set_title
from matplotlib import use
from ..models import SurfaceImages

use('Agg')  # Fixes crashes on macOS

mycmap = [[0.0, 'rgb(0,196,125)'], [0.005128205128205128, 'rgb(0,198,119)'], [0.010256410256410256, 'rgb(0,201,112)'],
          [0.015384615384615385, 'rgb(0,203,107)'], [0.020512820512820513, 'rgb(1,204,102)'],
          [0.02564102564102564, 'rgb(5,205,103)'], [0.03076923076923077, 'rgb(9,206,104)'],
          [0.035897435897435895, 'rgb(13,207,105)'], [0.041025641025641026, 'rgb(17,207,105)'],
          [0.046153846153846156, 'rgb(21,208,106)'], [0.05128205128205128, 'rgb(25,209,107)'],
          [0.05641025641025641, 'rgb(29,210,108)'], [0.06153846153846154, 'rgb(33,211,109)'],
          [0.06666666666666667, 'rgb(37,211,109)'], [0.07179487179487179, 'rgb(41,212,110)'],
          [0.07692307692307693, 'rgb(45,213,111)'], [0.08205128205128205, 'rgb(49,214,112)'],
          [0.08717948717948718, 'rgb(53,215,113)'], [0.09230769230769231, 'rgb(57,215,113)'],
          [0.09743589743589744, 'rgb(61,216,114)'], [0.10256410256410256, 'rgb(65,217,115)'],
          [0.1076923076923077, 'rgb(69,218,116)'], [0.11282051282051282, 'rgb(73,219,117)'],
          [0.11794871794871795, 'rgb(77,219,117)'], [0.12307692307692308, 'rgb(81,220,118)'],
          [0.1282051282051282, 'rgb(85,221,119)'], [0.13333333333333333, 'rgb(89,222,120)'],
          [0.13846153846153847, 'rgb(93,223,121)'], [0.14358974358974358, 'rgb(97,223,121)'],
          [0.14871794871794872, 'rgb(101,224,122)'], [0.15384615384615385, 'rgb(105,225,123)'],
          [0.15897435897435896, 'rgb(109,226,124)'], [0.1641025641025641, 'rgb(113,227,125)'],
          [0.16923076923076924, 'rgb(117,227,125)'], [0.17435897435897435, 'rgb(121,228,126)'],
          [0.1794871794871795, 'rgb(125,229,127)'], [0.18461538461538463, 'rgb(129,230,128)'],
          [0.18974358974358974, 'rgb(133,231,129)'], [0.19487179487179487, 'rgb(137,231,129)'],
          [0.2, 'rgb(141,232,130)'], [0.20512820512820512, 'rgb(145,233,131)'],
          [0.21025641025641026, 'rgb(149,234,132)'], [0.2153846153846154, 'rgb(153,235,133)'],
          [0.2205128205128205, 'rgb(157,235,133)'], [0.22564102564102564, 'rgb(161,236,134)'],
          [0.23076923076923078, 'rgb(165,237,135)'], [0.2358974358974359, 'rgb(169,238,136)'],
          [0.24102564102564103, 'rgb(173,239,137)'], [0.24615384615384617, 'rgb(177,239,137)'],
          [0.2512820512820513, 'rgb(181,240,138)'], [0.2564102564102564, 'rgb(185,241,139)'],
          [0.26153846153846155, 'rgb(189,242,140)'], [0.26666666666666666, 'rgb(193,243,141)'],
          [0.2717948717948718, 'rgb(197,243,141)'], [0.27692307692307694, 'rgb(201,244,142)'],
          [0.28205128205128205, 'rgb(205,245,143)'], [0.28717948717948716, 'rgb(209,246,144)'],
          [0.2923076923076923, 'rgb(213,247,145)'], [0.29743589743589743, 'rgb(217,247,145)'],
          [0.30256410256410254, 'rgb(221,248,146)'], [0.3076923076923077, 'rgb(225,249,147)'],
          [0.3128205128205128, 'rgb(229,250,148)'], [0.31794871794871793, 'rgb(233,251,149)'],
          [0.3230769230769231, 'rgb(237,251,149)'], [0.3282051282051282, 'rgb(241,252,150)'],
          [0.3333333333333333, 'rgb(245,253,151)'], [0.3384615384615385, 'rgb(249,254,152)'],
          [0.3435897435897436, 'rgb(253,255,153)'], [0.3487179487179487, 'rgb(254,254,152)'],
          [0.35384615384615387, 'rgb(252,251,151)'], [0.358974358974359, 'rgb(250,249,150)'],
          [0.3641025641025641, 'rgb(248,246,149)'], [0.36923076923076925, 'rgb(246,243,148)'],
          [0.37435897435897436, 'rgb(244,241,147)'], [0.37948717948717947, 'rgb(242,238,146)'],
          [0.38461538461538464, 'rgb(240,236,145)'], [0.38974358974358975, 'rgb(238,233,144)'],
          [0.39487179487179486, 'rgb(236,231,143)'], [0.4, 'rgb(234,228,142)'],
          [0.40512820512820513, 'rgb(232,226,141)'], [0.41025641025641024, 'rgb(230,223,139)'],
          [0.4153846153846154, 'rgb(228,220,138)'], [0.4205128205128205, 'rgb(226,218,137)'],
          [0.4256410256410256, 'rgb(224,215,136)'], [0.4307692307692308, 'rgb(222,213,135)'],
          [0.4358974358974359, 'rgb(220,210,134)'], [0.441025641025641, 'rgb(218,208,133)'],
          [0.4461538461538462, 'rgb(216,205,132)'], [0.4512820512820513, 'rgb(214,203,131)'],
          [0.4564102564102564, 'rgb(212,200,130)'], [0.46153846153846156, 'rgb(210,197,129)'],
          [0.4666666666666667, 'rgb(208,195,128)'], [0.4717948717948718, 'rgb(206,192,127)'],
          [0.47692307692307695, 'rgb(204,190,125)'], [0.48205128205128206, 'rgb(202,187,124)'],
          [0.48717948717948717, 'rgb(200,185,123)'], [0.49230769230769234, 'rgb(198,182,122)'],
          [0.49743589743589745, 'rgb(196,179,121)'], [0.5025641025641026, 'rgb(194,177,120)'],
          [0.5076923076923077, 'rgb(192,174,119)'], [0.5128205128205128, 'rgb(190,172,118)'],
          [0.517948717948718, 'rgb(188,169,117)'], [0.5230769230769231, 'rgb(186,167,116)'],
          [0.5282051282051282, 'rgb(184,164,115)'], [0.5333333333333333, 'rgb(182,162,114)'],
          [0.5384615384615384, 'rgb(180,159,112)'], [0.5435897435897435, 'rgb(178,156,111)'],
          [0.5487179487179488, 'rgb(176,154,110)'], [0.5538461538461539, 'rgb(174,151,109)'],
          [0.558974358974359, 'rgb(172,149,108)'], [0.5641025641025641, 'rgb(170,146,107)'],
          [0.5692307692307692, 'rgb(168,144,106)'], [0.5743589743589743, 'rgb(166,141,105)'],
          [0.5794871794871795, 'rgb(164,139,104)'], [0.5846153846153846, 'rgb(162,136,103)'],
          [0.5897435897435898, 'rgb(160,133,102)'], [0.5948717948717949, 'rgb(158,131,101)'],
          [0.6, 'rgb(156,128,100)'], [0.6051282051282051, 'rgb(154,126,98)'], [0.6102564102564103, 'rgb(152,123,97)'],
          [0.6153846153846154, 'rgb(150,121,96)'], [0.6205128205128205, 'rgb(148,118,95)'],
          [0.6256410256410256, 'rgb(146,115,94)'], [0.6307692307692307, 'rgb(144,113,93)'],
          [0.6358974358974359, 'rgb(142,110,92)'], [0.6410256410256411, 'rgb(140,108,91)'],
          [0.6461538461538462, 'rgb(138,105,90)'], [0.6512820512820513, 'rgb(136,103,89)'],
          [0.6564102564102564, 'rgb(134,100,88)'], [0.6615384615384615, 'rgb(132,98,87)'],
          [0.6666666666666666, 'rgb(130,95,86)'], [0.6717948717948717, 'rgb(128,92,84)'],
          [0.676923076923077, 'rgb(129,94,86)'], [0.6820512820512821, 'rgb(131,96,89)'],
          [0.6871794871794872, 'rgb(133,99,92)'], [0.6923076923076923, 'rgb(135,101,94)'],
          [0.6974358974358974, 'rgb(137,104,97)'], [0.7025641025641025, 'rgb(139,107,100)'],
          [0.7076923076923077, 'rgb(141,109,102)'], [0.7128205128205128, 'rgb(143,112,105)'],
          [0.717948717948718, 'rgb(145,114,108)'], [0.7230769230769231, 'rgb(147,117,110)'],
          [0.7282051282051282, 'rgb(149,119,113)'], [0.7333333333333333, 'rgb(151,122,116)'],
          [0.7384615384615385, 'rgb(153,124,118)'], [0.7435897435897436, 'rgb(155,127,121)'],
          [0.7487179487179487, 'rgb(157,130,124)'], [0.7538461538461538, 'rgb(159,132,126)'],
          [0.7589743589743589, 'rgb(161,135,129)'], [0.764102564102564, 'rgb(163,137,132)'],
          [0.7692307692307693, 'rgb(165,140,134)'], [0.7743589743589744, 'rgb(167,142,137)'],
          [0.7794871794871795, 'rgb(169,145,140)'], [0.7846153846153846, 'rgb(171,147,142)'],
          [0.7897435897435897, 'rgb(173,150,145)'], [0.7948717948717948, 'rgb(175,153,148)'],
          [0.8, 'rgb(177,155,150)'], [0.8051282051282052, 'rgb(179,158,153)'],
          [0.8102564102564103, 'rgb(181,160,156)'], [0.8153846153846154, 'rgb(183,163,159)'],
          [0.8205128205128205, 'rgb(185,165,161)'], [0.8256410256410256, 'rgb(187,168,164)'],
          [0.8307692307692308, 'rgb(189,171,167)'], [0.8358974358974359, 'rgb(191,173,169)'],
          [0.841025641025641, 'rgb(193,176,172)'], [0.8461538461538461, 'rgb(195,178,175)'],
          [0.8512820512820513, 'rgb(197,181,177)'], [0.8564102564102564, 'rgb(199,183,180)'],
          [0.8615384615384616, 'rgb(201,186,183)'], [0.8666666666666667, 'rgb(203,188,185)'],
          [0.8717948717948718, 'rgb(205,191,188)'], [0.8769230769230769, 'rgb(207,194,191)'],
          [0.882051282051282, 'rgb(209,196,193)'], [0.8871794871794871, 'rgb(211,199,196)'],
          [0.8923076923076924, 'rgb(213,201,199)'], [0.8974358974358975, 'rgb(215,204,201)'],
          [0.9025641025641026, 'rgb(217,206,204)'], [0.9076923076923077, 'rgb(219,209,207)'],
          [0.9128205128205128, 'rgb(221,211,209)'], [0.9179487179487179, 'rgb(223,214,212)'],
          [0.9230769230769231, 'rgb(225,217,215)'], [0.9282051282051282, 'rgb(227,219,217)'],
          [0.9333333333333333, 'rgb(229,222,220)'], [0.9384615384615385, 'rgb(231,224,223)'],
          [0.9435897435897436, 'rgb(233,227,226)'], [0.9487179487179487, 'rgb(235,229,228)'],
          [0.9538461538461539, 'rgb(237,232,231)'], [0.958974358974359, 'rgb(239,235,234)'],
          [0.9641025641025641, 'rgb(241,237,236)'], [0.9692307692307692, 'rgb(243,240,239)'],
          [0.9743589743589743, 'rgb(245,242,242)'], [0.9794871794871794, 'rgb(247,245,244)'],
          [0.9846153846153847, 'rgb(249,247,247)'], [0.9897435897435898, 'rgb(251,250,250)'],
          [0.9948717948717949, 'rgb(253,252,252)'], [1.0, 'rgb(255,255,255)']]


def gen_3d_surface(longitude1, latitude1, longitude2, latitude2):
    data_array, surface_filename, surface_database_url = get_dem_data(longitude1, latitude1, longitude2, latitude2)

    surface_filename += '.html'
    surface_database_url += '.html'
    max_points = 800000
    points = len(data_array) * len(data_array[0])
    div = round(points / max_points)
    if div > 0:
        data_array = data_array[::div]
    title = set_title('Surface of [', longitude1, latitude1, longitude2, latitude2)
    zrange = (0, max(int(data_array.max()), 2000))
    lighting_effects = dict(ambient=0.4, diffuse=0.5, roughness=0.9, fresnel=0.2)

    fig = go.Figure()
    fig.add_trace(go.Surface(z=data_array, colorscale=mycmap, cmin=0,
                             cmax=max(int(data_array.max()), 2000), lighting=lighting_effects))
    fig.update_layout(scene=dict(aspectratio=dict(x=2, y=2, z=0.75),
                                 xaxis=go.layout.scene.XAxis(title='', showticklabels=False),
                                 yaxis=go.layout.scene.YAxis(title='', showticklabels=False),
                                 zaxis=go.layout.scene.ZAxis(title='height [m]', range=zrange)),
                      title=title, autosize=True)
    fig.show()
    go_offline.plot(fig, filename=surface_filename, validate=True, auto_open=False)
    saved_file = SurfaceImages.objects.create(image=surface_database_url)

    return saved_file.id
