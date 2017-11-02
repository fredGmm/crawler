#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class GetImageFromHtml:

    #  抓取虎扑帖子页面的图片
    def fromHp(self, article_tree=None):
        css_find = {}
        css_find['type_1'] = 'div.floor-show>div.floor_box>table>tr>td>div.quote-content>div>img'
        css_find['type_2'] = 'div.floor-show>div.floor_box>table>tr>td>div.quote-content>p>img'
        css_find['type_3'] = 'div.floor-show>div.floor_box>table>tr>td>div.quote-content>div.pc-detail-left>div.detail-content>p>img'
        css_find['type_4'] = 'div.floor-show>div.floor_box>table>tr>td>div.quote-content>img'

        images = []
        for str in css_find:
            reg = css_find[str]

            image_list = article_tree.cssselect(reg)
            for image_num, image in enumerate(image_list):
                img_path = image.get('src')
                if img_path:
                    # print('num:%s, img_path:%s' % (image_num, img_path))
                    images.append(img_path)
        return images


