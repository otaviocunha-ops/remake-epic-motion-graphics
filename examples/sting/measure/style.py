"""Colour samples and cap heights used in SPEC.md section 1. Every value names its frame + box.
Run from pyramids/measure: python3 style.py"""
import numpy as np
from lib import *

def ink_box(F, x0, y0, x1, y1, mode='dark', thr=None):
    """bbox of ink inside a box: dark = lum < thr (default 128), light = lum > thr (default 170)"""
    g = gray(F)[y0:y1, x0:x1]
    m = g < (thr or 128) if mode == 'dark' else g > (thr or 170)
    return bbox(m, x0, y0)

S = {}   # name -> {frame, box, value}
def col(name, F, box, kind='patch'):
    v = patch(F, *box) if kind == 'patch' else ink(F, *box, dark=(kind == 'ink'))
    S[name] = {'frame': F, 'box': list(box), 'hex': v}
def cap(name, F, box, mode='dark', thr=None, ratio=0.705):
    b = ink_box(F, *box, mode=mode, thr=thr)
    if b:
        S[name] = {'frame': F, 'box': list(box), 'ink_bbox': b, 'cap_px': b[3] - b[1], 'font_px_est': round((b[3] - b[1]) / ratio, 1)}

# ---- S1 header / window (f40 settled, f64 hover) ----
for F in (0, 6, 12, 20, 40):
    for y in (0, 180, 360, 540, 700):
        col(f'S1_bg_f{F}_x0-30_y{y}', F, (0, y, 30, min(y + 20, 720)))
col('S1_window_fill_near_header', 40, (440, 400, 500, 430))
col('S1_window_top_band', 40, (300, 278, 330, 288))
col('S1_window_lower_left', 40, (300, 660, 330, 700))
col('S1_window_border_left', 40, (271, 420, 274, 440))
col('S1_logo_disc_fill', 40, (322, 385, 334, 395))
col('S1_logo_disc_rim', 40, (316, 350, 318, 366))
col('S1_logo_glyph', 40, (330, 325, 395, 395), 'ink')
col('S1_Manus_text', 40, (434, 342, 551, 372), 'ink')
col('S1_pill_fill', 40, (590, 370, 600, 378))
col('S1_pill_fill_top', 40, (620, 339, 680, 343))
col('S1_pill_text', 40, (603, 346, 692, 372), 'light')
col('S1_hover_ring', 64, (292, 350, 300, 366))
col('S1_hover_ring_outer', 64, (286, 340, 292, 376))
col('S1_cursor_fill', 40, (521, 255, 527, 262), 'ink')
col('S1_bolt_icon', 40, (345, 470, 375, 520), 'ink')
col('S1_chat_icon', 40, (340, 585, 380, 620), 'ink')
col('S1_site_card_icon', 40, (532, 492, 562, 522))
col('S1_site_card_title', 40, (580, 485, 720, 503), 'ink')
col('S1_site_card_meta', 40, (580, 511, 720, 528), 'ink')
col('S1_site_card_fill', 40, (600, 470, 700, 480))
col('S1_site_screenshot', 40, (520, 600, 700, 700))
cap('S1_Manus_M', 40, (430, 330, 470, 390))
cap('S1_pill_A', 40, (600, 345, 616, 375), 'light', 200)
cap('S1_site_title_C', 40, (578, 480, 596, 506))
cap('S1_site_meta_N', 40, (578, 508, 594, 530), 'dark', 200)
# ---- S2 orbit f86 ----
col('S2_bg', 86, (0, 0, 60, 60))
col('S2_icon_tile', 86, (304, 350, 310, 370))
col('S2_icon_glyph', 86, (320, 315, 400, 405), 'light')
col('S2_halo_disc', 86, (262, 355, 272, 365))
col('S2_halo_inner_ring', 86, (282, 355, 292, 365))
for nm, (cx, cy) in {'yellow': (221, 351), 'blue': (370, 217), 'green': (509, 367), 'magenta': (356, 506)}.items():
    col(f'S2_sq_{nm}_centre', 86, (cx - 4, cy - 4, cx + 4, cy + 4))
    col(f'S2_sq_{nm}_topleft', 86, (cx - 24, cy - 24, cx - 18, cy - 18))
    col(f'S2_sq_{nm}_bottomright', 86, (cx + 18, cy + 18, cx + 24, cy + 24))
# ---- S3 laptop f150 ----
col('S3_page_above', 150, (300, 100, 400, 200))
col('S3_bezel', 150, (300, 292, 400, 300))
col('S3_bezel_top_edge_grey', 150, (300, 283, 400, 286))
col('S3_menubar', 150, (20, 325, 120, 350))
col('S3_wall_top_left', 150, (10, 380, 40, 400))
col('S3_wall_mid', 150, (330, 600, 370, 620))
col('S3_wall_bottom_right', 150, (650, 690, 700, 715))
col('S3_wall_streak', 150, (60, 560, 90, 575))
col('S3_box_fill_top', 150, (300, 395, 330, 405))
col('S3_box_fill_bottom', 150, (300, 510, 330, 520))
col('S3_box_border_top', 150, (300, 380, 330, 383))
col('S3_box_text', 150, (169, 415, 425, 437), 'light')
col('S3_send_btn', 150, (568, 484, 572, 488))
col('S3_box_icons', 150, (165, 478, 325, 502), 'light')
col('S3_menubar_text', 150, (515, 328, 630, 350), 'light')
col('S3_dot_blue', 150, (403, 333, 413, 343)); col('S3_dot_green', 150, (436, 333, 446, 343)); col('S3_dot_magenta', 150, (468, 333, 478, 343))
col('S3_menubar_icon_tile', 150, (357, 324, 362, 329))
cap('S3_prompt_T', 150, (166, 405, 182, 445), 'light', 170)
cap('S3_menubar_M', 150, (513, 325, 535, 355), 'light', 170)
# ---- S4 answer f180 ----
col('S4_page', 180, (600, 380, 720, 420))
col('S4_body_grey', 180, (80, 190, 400, 215), 'ink')
col('S4_heading_grey', 180, (80, 112, 480, 140), 'ink')
col('S4_bold_black', 180, (230, 345, 470, 372), 'ink')
col('S4_tint_f159', 159, (0, 0, 40, 40)); col('S4_tint_f162', 162, (0, 0, 40, 40))
cap('S4_heading_T', 180, (80, 105, 96, 145), 'dark', 225)
cap('S4_body_T', 180, (80, 185, 98, 225), 'dark', 215)
cap('S4_bold_P', 180, (229, 340, 247, 380), 'dark', 128)
cap('S4_body_B', 180, (80, 420, 96, 452), 'dark', 215)
# ---- S5 card f205 ----
col('S5_card_white', 205, (300, 600, 420, 630))
col('S5_caption', 205, (262, 643, 458, 666), 'ink')
col('S5_subcaption', 205, (320, 682, 400, 697), 'ink')
col('S5_handle_bar', 205, (340, 250, 380, 255))
col('S5_photo_sky_tl', 205, (160, 245, 200, 285))
col('S5_photo_sand', 205, (300, 560, 420, 580))
cap('S5_caption_P', 205, (258, 638, 276, 672), 'dark', 128)
cap('S5_subcaption_C', 205, (318, 680, 332, 700), 'dark', 200)
# ---- S6 cards f230 ----
col('S6_page', 230, (20, 20, 80, 80))
col('S6_explore_pill', 230, (210, 130, 220, 150))
col('S6_explore_text', 230, (222, 133, 268, 148), 'light')
col('S6_dots_btn', 230, (488, 132, 494, 138))
col('S6_Khufu_overlay', 230, (200, 262, 520, 340), 'light')
col('S6_Khafre_overlay_mid', 230, (260, 530, 420, 580))
cap('S6_Khufu_K_vs_sky', 230, (192, 240, 214, 300), 'light', 200)
cap('S6_explore_E', 230, (220, 130, 232, 152), 'light', 230)
# ---- S7 / S8 ----
col('S7_page', 270, (0, 0, 60, 60)); col('S7_disc', 270, (310, 350, 320, 370)); col('S7_glyph', 270, (330, 325, 390, 395), 'ink')
col('S8_bg_corner', 320, (0, 0, 40, 40)); col('S8_bg_centre_above', 320, (340, 240, 380, 260)); col('S8_bg_below', 320, (340, 470, 380, 490))
col('S8_bg_bottom', 320, (340, 690, 380, 720)); col('S8_word', 320, (175, 330, 545, 390), 'light')
cap('S8_d_ascender', 320, (170, 320, 200, 400), 'light', 200, ratio=0.74)

if __name__ == '__main__':
    for k, v in S.items(): print(k, v)
    save_part('style', S)
