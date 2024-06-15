import lvgl as lv


def set_formatting(
    obj: lv.obj, top: int = 0, bottom: int = 0, right: int = 0, left: int = 0
):
    obj.set_style_pad_top(top, lv.PART.MAIN)
    obj.set_style_pad_bottom(bottom, lv.PART.MAIN)
    obj.set_style_pad_right(right, lv.PART.MAIN)
    obj.set_style_pad_left(left, lv.PART.MAIN)


class lv_obj_extended(lv.obj):
    def __init__(self, parent: lv.obj | None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.visible = True
        self.scrollable = False

    @property
    def visible(self):
        return not self.has_flag(lv.obj.FLAG.HIDDEN)

    @visible.setter
    def visible(self, show: bool):
        if not show:
            self.add_flag(lv.obj.FLAG.HIDDEN)
        else:
            self.clear_flag(lv.obj.FLAG.HIDDEN)

    def toggle_visibility(self):
        self.visible = not self.visible

    @property
    def scrollable(self):
        return not self.has_flag(lv.obj.FLAG.SCROLLABLE)

    @scrollable.setter
    def scrollable(self, scroll: bool):
        if not scroll:
            self.clear_flag(lv.obj.FLAG.SCROLLABLE)
        else:
            self.add_flag(lv.obj.FLAG.SCROLLABLE)

    def toggle_scrollability(self):
        self.scrollable = not self.scrollable

    def set_style_pad(
        self, top: int = 0, bottom: int = 0, right: int = 0, left: int = 0
    ):
        set_formatting(self, top, bottom, right, left)


class labelled_btn(lv.btn):
    def __init__(self, parent, name, id=0):
        super().__init__(parent)
        self._name = name
        self.id = id
        self.label = lv.label(self)
        self.label.set_text(self._name)
        self.label.align_to(self, lv.ALIGN.CENTER, 0, 0)
        self.label.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    def set_size(self, width, height):
        super(labelled_btn, self).set_size(width, height)
        self.label.set_width(width)
        self.label.align_to(self, lv.ALIGN.CENTER, 0, 0)

    @property
    def visible(self):
        return not self.has_flag(lv.obj.FLAG.HIDDEN)

    @visible.setter
    def visible(self, show: bool):
        if not show:
            self.add_flag(lv.obj.FLAG.HIDDEN)
        else:
            self.clear_flag(lv.obj.FLAG.HIDDEN)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value
        self.label.set_text(value)
        lv.event_send(self.label, lv.EVENT.REFRESH, None)

    def highlight(self, val):
        if val:
            self.set_style_bg_color(lv.palette_main(lv.PALETTE.RED), lv.PART.MAIN)
        else:
            self.set_style_bg_color(lv.palette_main(lv.PALETTE.BLUE), lv.PART.MAIN)

    def set_style_pad(self, top=0, bottom=0, right=0, left=0):
        set_formatting(self, top, bottom, right, left)
