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


t = RBT()
for i in range(6):
    t.insert(i+1)

print(t.root)
print(t.root.right)
print(t.root.left)
print(t.root.right.right)
print(t.root.right.left)
print(t.root.right.right.right)
