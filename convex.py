from deq import Deq
from r2point import R2Point


class Figure:
    """ Абстрактная фигура """

    def perimeter(self):
        return 0.0

    def area(self):
        return 0.0

    def n_timer(self):
        return 0


class Void(Figure):
    """ "Hульугольник" """

    def add(self, p):
        return Point(p)


class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p):
        self.p = p

    def add(self, q):
        return self if self.p == q else Segment(self.p, q)

    def n_timer(self):
        if abs(self.p.y) < 1:
            return 1
        else:
            return 0


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q):
        self.p, self.q = p, q

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, self.q, r)
        elif r.is_inside(self.p, self.q):
            return self
        elif self.p.is_inside(r, self.q):
            return Segment(r, self.q)
        else:
            return Segment(self.p, r)

    def n_timer(self):
        if abs(self.p.y) < 1 or abs(self.q.y) < 1 or (
                self.p.y >= 1 and self.q.y <= -1 or
                self.p.y <= -1 and self.q.y >= 1):
            return 'continum'
        else:
            return 0


class Polygon(Figure):
    """ Многоугольник """

    def __init__(self, a, b, c):
        self.points = Deq()
        self.points.push_first(b)
        if b.is_light(a, c):
            self.points.push_first(a)
            self.points.push_last(c)
        else:
            self.points.push_last(a)
            self.points.push_first(c)
        self._perimeter = a.dist(b) + b.dist(c) + c.dist(a)
        self._area = abs(R2Point.area(a, b, c))
        w1 = a.y <= -1
        w2 = b.y <= -1
        w3 = c.y <= -1
        if (abs(a.y) < 1) or (abs(b.y) < 1) or (abs(c.y) < 1):
            self._n_timer = 'continum'
        elif (w1 and w2 and w3) or (not (w1) and not (w2) and not (w3)):
            self._n_timer = 0
        else:
            self._n_timer = 'continum'

    def perimeter(self):
        return self._perimeter

    def area(self):
        return self._area

    def n_timer(self):
        return self._n_timer

    # добавление новой точки
    def add(self, t):

        k = self.points.first().y <= -1
        # поиск освещённого ребра
        for n in range(self.points.size()):
            if t.is_light(self.points.last(), self.points.first()):
                break
            self.points.push_last(self.points.pop_first())

        # хотя бы одно освещённое ребро есть
        if t.is_light(self.points.last(), self.points.first()):

            # учёт удаления ребра, соединяющего конец и начало дека
            self._perimeter -= self.points.first().dist(self.points.last())
            self._area += abs(R2Point.area(t,
                                           self.points.last(),
                                           self.points.first()))

            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()
            while t.is_light(p, self.points.first()):
                self._perimeter -= p.dist(self.points.first())
                self._area += abs(R2Point.area(t, p, self.points.first()))
                p = self.points.pop_first()
            self.points.push_first(p)

            # удаление освещённых рёбер из конца дека
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                self._perimeter -= p.dist(self.points.last())
                self._area += abs(R2Point.area(t, p, self.points.last()))
                p = self.points.pop_last()
            self.points.push_last(p)

            # добавление двух новых рёбер
            self._perimeter += (
                    t.dist(self.points.first()) + t.dist(self.points.last()))
            self.points.push_first(t)

            if self._n_timer != 'continum':
                if ((t.y <= -1) and k) or (not (k) and (t.y >= 1)):
                    self._n_timer = 0
                else:
                    self._n_timer = 'continum'
            else:
                self._n_timer = 'continum'

        return self


if __name__ == "__main__":
    f = Void()
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(1.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 1.0))
    print(type(f), f.__dict__)
