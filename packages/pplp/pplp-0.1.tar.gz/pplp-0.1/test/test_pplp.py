from pplp import LinearProgram

def test_expr():
    lp = LinearProgram()
    x, y = lp.Var(), lp.Var()
    assert str(x + y) == " 1.00 X1 +  1.00 X2"
    assert str(2 * (x + y)) == " 2.00 X1 +  2.00 X2"
    assert str(2*x + 3*y) == " 2.00 X1 +  3.00 X2"
    assert str(0 <= 2*x) == " 2.00 X1 >=  0.00"
    assert str(3*y <= 7) == " 3.00 X2 <=  7.00"
    e = 0 <= 2*x + 3*y <= 7
    assert str(e) == " 0.00 <=  2.00 X1 +  3.00 X2 <=  7.00"
    e = 2*x + 3*y
    assert str(e <= 7) == " 2.00 X1 +  3.00 X2 <=  7.00"
    assert str(0 <= e) == " 2.00 X1 +  3.00 X2 >=  0.00"
    assert str(x*4 == 8) == " 4.00 X1 ==  8.00"
    assert str(y <= 6) == "X2 <=  6.00"
    assert str(2*x - 3*y) == " 2.00 X1 + -3.00 X2"
    e += 3*lp.Var()
    assert str(e) == " 2.00 X1 +  3.00 X2 +  3.00 X3"

def test_lp1():
    lp = LinearProgram()
    x, y, z = lp.Var(), lp.Var(), lp.Var()
    lp.objective = 10*x - 6*y + 4*z
    lp.add_constraint( 0 <= x <= 10 )
    lp.add_constraint( 0 <= y <= 10 )
    lp.add_constraint( 0 <= z <= 10 )

    maxval = lp.maximize()
    print(maxval)
    print(x.value, y.value, z.value)

    assert maxval == 140
    assert (x.value, y.value, z.value) == (10, 0, 10)

def test_lp2():
    lp = LinearProgram()
    x, y, z = lp.Var(), lp.Var(), lp.Var()
    lp.objective = 10*x - 6*y + 4*z
    lp.add_constraint( x <= 10 )
    lp.add_constraint( 0 <= y  )
    lp.add_constraint( z <= 10 )

    maxval = lp.maximize()
    print(maxval)
    print(x.value, y.value, z.value)

    assert maxval == 140
    assert (x.value, y.value, z.value) == (10, 0, 10)

def test_lp3():
    lp = LinearProgram()
    x, y, z = lp.Var(), lp.Var(), lp.Var()
    lp.objective = 10*x + 6*y + 4*z
    lp.add_constraint( x + y + z <= 100 )
    lp.add_constraint( 10*x + 4*y + 5*z <= 600 )
    lp.add_constraint( 2*x + 2*y + 6*z <= 300 )
    lp.add_constraint( x >= 0 )
    lp.add_constraint( y >= 0 )
    lp.add_constraint( z >= 0 )

    maxval = lp.maximize()
    print(maxval)
    print(x.value, y.value, z.value)

    assert int(maxval) == 733
    assert int(x.value) == 33
    assert int(y.value) == 66
    assert int(z.value) == 0
    
def test_lp4():
    lp = LinearProgram()
    x, y, z = lp.Var(), lp.Var(), lp.Var()
    lp.objective = 10*x - 6*y + 4*z
    lp.add_constraint( 0 <= x <= 10 )
    lp.add_constraint( 0 <= y <= 10 )
    lp.add_constraint( 0 <= z <= 10 )

    minval = lp.minimize()
    print(minval)
    print(x.value, y.value, z.value)

    assert minval == -60
    assert (x.value, y.value, z.value) == (0, 10, 0)

def test_mip1():
    lp = LinearProgram()
    x, y, z = lp.IntVar(), lp.IntVar(), lp.IntVar()
    lp.objective = 10*x - 6*y + 4*z
    lp.add_constraint( 0 <= x <= 10 )
    lp.add_constraint( 0 <= y <= 10 )
    lp.add_constraint( 0 <= z <= 10 )

    minval = lp.minimize()
    print(minval)
    print(x.value, y.value, z.value)

    assert minval == -60
    assert (x.value, y.value, z.value) == (0, 10, 0)
    
def test_mip2():
    lp = LinearProgram()
    x, y, z = lp.IntVar(), lp.IntVar(), lp.IntVar()
    lp.objective = 10*x + 6*y + 4*z
    lp.add_constraint( x + y + z <= 100 )
    lp.add_constraint( 10*x + 4*y + 5*z <= 600 )
    lp.add_constraint( 2*x + 2*y + 6*z <= 300 )
    lp.add_constraint( x >= 0 )
    lp.add_constraint( y >= 0 )
    lp.add_constraint( z >= 0 )

    maxval = lp.maximize()
    print(maxval)
    print(x.value, y.value, z.value)

    assert maxval == 732.0
    assert x.value == 33
    assert y.value == 67
    assert z.value == 0
    

def test_iadd():
    lp = LinearProgram()
    x, y, z = lp.Var(), lp.Var(), lp.Var()
    lp.objective = 10*x - 6*y
    lp.add_constraint( x <= 10 )
    lp.add_constraint( 0 <= y  )
    lp.add_constraint( z <= 10 )
    lp.objective += 4*z

    maxval = lp.maximize()
    print(maxval)
    print(x.value, y.value, z.value)

    assert maxval == 140
    assert (x.value, y.value, z.value) == (10, 0, 10)

def test_isub():
    lp = LinearProgram()
    x, y = lp.Var(), lp.Var()
    lp.objective += 10*x - 6*y
    lp.add_constraint( x <= 10 )
    lp.add_constraint( 0 <= y  )
    lp.objective -= 6*y
    z = lp.Var()
    lp.add_constraint( z <= 10 )
    lp.objective += 4*z

    maxval = lp.maximize()
    print(maxval)
    print(x.value, y.value, z.value)

    assert maxval == 140
    assert (x.value, y.value, z.value) == (10, 0, 10)

def test_mip_zero():
    lp = LinearProgram()
    x, y, z = lp.IntVar(), lp.IntVar(), lp.IntVar()
    lp.objective = 10*x + 6*y + 4*z
    lp.add_constraint( 0 + x + y + z <= 100 )
    lp.add_constraint( 0 + 10*x + 4*y + 5*z <= 600 )
    lp.add_constraint( 2*x + 2*y + 6*z + 0<= 300 )
    lp.add_constraint( x >= 0 )
    lp.add_constraint( y >= 0 )
    lp.add_constraint( z >= 0 )

    maxval = lp.maximize()
    print(maxval)
    print(x.value, y.value, z.value)

    assert maxval == 732.0
    assert x.value == 33
    assert y.value == 67
    assert z.value == 0
