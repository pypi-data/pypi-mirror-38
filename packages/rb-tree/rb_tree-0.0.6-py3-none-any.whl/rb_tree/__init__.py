class Node:
    def __init__(self, data, color='red'):
        self.color = color
        self.data = data
        self.right = None
        self.left = None
        self.p = None

    def __str__(self):
        return "{}, {}".format(self.data, self.color)


class RBT:
    nil = None

    def __init__(self):
        self.root = RBT.nil

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left is not RBT.nil:
            y.left.p = x
        y.p = x.p
        if x.p == RBT.nil:
            self.root = y
        elif x == x.p.left:
            x.p.left = y
        else:
            x.p.right = y
        y.left = x
        x.p = y

    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right is not RBT.nil:
            y.right.p = x
        y.p = x.p
        if x.p == RBT.nil:
            self.root = y
        elif x == x.p.right:
            x.p.right = y
        else:
            x.p.left = y
        y.right = x
        x.p = y

    def insert(self, data):
        try:
            # user entered an iterable
            for element in data:
                self.__insert(element)
        except TypeError:
            self.__insert(data)

    def __insert(self, data):

        """Note : red is the implicit color of any new node."""
        z = Node(data)

        y = RBT.nil
        x = self.root
        while x is not RBT.nil:
            y = x
            if z.data < x.data:
                x = x.left
            else:
                x = x.right
        z.p = y
        if y is RBT.nil:
            self.root = z
        elif z.data < y.data:
            y.left = z
        else:
            y.right = z
        z.left = RBT.nil
        z.right = RBT.nil
        z.color = 'red'
        self.root.color = 'black'
        self._rb_insert_fixup(z)

    def _rb_insert_fixup(self, z):
        while z.p and z.p.color == 'red':
            if z.p == z.p.p.left:
                y = z.p.p.right
                if y is not None and y.color == 'red':
                    z.p.color = 'black'
                    y.color = 'black'
                    z.p.p.color = 'red'
                    z = z.p.p
                else:
                    if z == z.p.right:
                        z = z.p
                        self._left_rotate(z)
                    z.p.color = 'black'
                    z.p.p.color = 'red'
                    self._right_rotate(z.p.p)
            else:
                y = z.p.p.left
                if y is not None and y.color == 'red':
                    z.p.color = 'black'
                    y.color = 'black'
                    z.p.p.color = 'red'
                    z = z.p.p
                else:
                    if z == z.p.left:
                        z = z.p
                        self._right_rotate(z)
                    z.p.color = 'black'
                    z.p.p.color = 'red'
                    self._left_rotate(z.p.p)
            self.root.color = 'black'

    def _rb_transplant(self, u, v):
        if u.p == RBT.nil:
            self.root = v
        elif u == u.p.left:
            u.p.left = v
        else:
            u.p.right = v
        if v is not RBT.nil:
            v.p = u.p

    def delete(self, z):
        y = z
        y_original_color = y.color
        if z.left == RBT.nil:
            x = z.right
            self._rb_transplant(z, z.right)
        elif z.right == RBT.nil:
            x = z.left
            self._rb_transplant(z, z.left)
        else:
            y = RBT._tree_minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.p == z:
                x.p = y
            else:
                self._rb_transplant(y, y.right)
                y.right = z.right
                y.right.p = y
            self._rb_transplant(z, y)
            y.left = z.left
            y.left.p = y
            y.color = z.color
        if y_original_color == 'black':
            self._rb_delete_fixup(x)

    def _rb_delete_fixup(self, x):
        while x != self.root and x.color == 'black':
            if x == x.p.left:
                w = x.p.wight
                if w.color == 'red':
                    w.color = 'black'
                    x.p.color = 'red'
                    self._left_rotate(x.p)
                    w = x.p.right
                if w.left.color == 'black' and w.right.color == 'black':
                    w.color = 'red'
                    x = x.p
                else:
                    if w.right.color == "black":
                        w.left.color = 'black'
                        w.color = 'red'
                        self._right_rotate(w)
                        w = x.p.right
                    w.color = x.p.color
                    x.p.color = 'black'
                    w.right.color = 'black'
                    self._left_rotate(x.p)
                    x = self.root
            else:
                w = x.p.left
                if w.color == 'red':
                    w.color = 'black'
                    x.p.color = 'red'
                    self._right_rotate(x.p)
                    w = x.p.left
                if w.right.color == 'black' and w.left.color == 'black':
                    w.color = 'red'
                    x = x.p
                else:
                    if w.left.color == "black":
                        w.right.color = 'black'
                        w.color = 'red'
                        self._left_rotate(w)
                        w = x.p.left
                    w.color = x.p.color
                    x.p.color = 'black'
                    w.left.color = 'black'
                    self._right_rotate(x.p)
                    x = self.root
        x.color = 'black'

    @staticmethod
    def _tree_minimum(x):
        while x.left != RBT.nil:
            x = x.left
        return x

    def inorder(self, x):
        if x is not RBT.nil:
            self.inorder(x.left)
            print(x)
            self.inorder(x.right)
