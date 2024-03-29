import collections

EllipticCurve = collections.namedtuple('EllipticCurve', ['name', 'p', 'a', 'b', 'g', 'n', 'h'])

curve = EllipticCurve(
    name='secp256k1',
    p=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f,
    a=0,
    b=7,
    g=(
        0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
        0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
    ),
    n=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141,
    h=1
)


def is_on_curve(point):
    """
    Returns True if the given point lies on the elliptic curve
    """
    if point is None:
        return True
    x, y = point
    return (y*y - x*x*x - curve.a*x - curve.b) % curve.p == 0


def inverse_mod(k, p):
    """
    Returns the inverse of k modulo p
    This function returns the only integer x such that (x * k) % p == 1
    k must be non-zero and p must be a prime
    """
    if k == 0:
        raise ZeroDivisionError('division by zero')
    
    if k < 0:
        return p - inverse_mod(-k, p)

    # Extended Euclidean algorithm
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = p, k

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    gcd, x, y = old_r, old_s, old_t

    assert gcd == 1
    assert (k * x) % p == 1

    return x % p


def point_add(point1, point2):
    """
    Returns the result of point1 + point2 according to the group law
    """
    assert is_on_curve(point1)
    assert is_on_curve(point2)

    # point1 is 'point on inifinity'
    if point1 is None:
        # 0 + point2 = point2
        return point2
    
    # point2 is 'point on infinity'
    if point2 is None:
        # 0 + point1 = point1
        return point1
    
    x1, y1 = point1
    x2, y2 = point2

    if x1 == x2 and y1 != y2:
        # point1 + (-point1) = 0
        return None

    if x1 == x2:
        # This is the case point1 == point2
        m = (3*x1*x1 + curve.a) * inverse_mod(2 * y1, curve.p)
    else:
        m = (y1 - y2) * inverse_mod(x1 - x2, curve.p)
    
    x3 = m * m - x1 - x2
    y3 = y1 + m * (x3 - x1)

    result = (x3 % curve.p, -y3 % curve.p)
    assert is_on_curve(result)
    return result


def scalar_mult(k, point):
    """
    Returns k * point computed using double and point_add algorithm
    """
    assert is_on_curve(point)

    if k % curve.n == 0 or point is None:
        return None

    result = None
    addend = point

    while k:
        if k & 1:
            result = point_add(result, addend)
        
        # Double
        addend = point_add(addend, addend)
        k >>= 1

    assert is_on_curve(result)
    return result


