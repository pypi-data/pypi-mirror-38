import pytest
from AD import autodif as autodif

def test_f1():
    f1 = "POW(x, POW(x, x))";
    vd = "x:2.0";
    F1 = autodif.AD(f1)
    F1.set_point(vd)
    assert math.fabs(F1.val() - 16) < 1e-7
    assert math.fabs(F1.diff("x") - 107.1104124466013909) < 1e-7

def test_f2():
    f1 = "EXP(3.0*X+X*POW(Y,2))";
    vd ="X:1.0,Y:2.0";
    F1 = autodif.AD(f1)
    F1.set_point(vd)
    assert math.fabs(F1.val() - 1096.6331584284585992) < 1e-7
    assert math.fabs(F1.diff("X") - 7676.432108999210194) < 1e-7
    assert math.fabs(F1.diff("Y") - 4386.532633713834397) < 1e-7

def test_f3():
    f1 = "EXP(3+LOG(POW(X,2)))";
    vd ="X:2.0";
    F1 = autodif.AD(f1)
    F1.set_point(vd)
    assert math.fabs(F1.val() - 80.342147692750670) < 1e-7
    assert math.fabs(F1.diff("X") - 80.342147692750670) < 1e-7

def test_f4():
    f1 = "SIN(2.0/X)-COS(3*X)";
    vd ="X:5.0";
    F1 = autodif.AD(f1)
    F1.set_point(vd)
    assert math.fabs(F1.val() - 1.1491062551674717) < 1e-7
    assert math.fabs(F1.diff("X") - 1.877178640951119) < 1e-7

def test_f5():
    f1 = "SIN(POW(X, 2))*EXP(COS(3.0*Y))";
    vd ="X:2.0,Y:3.0";
    F1 = autodif.AD(f1)
    F1.set_point(vd)
    assert math.fabs(F1.val() - -0.30428721849) < 1e-7
    assert math.fabs(F1.diff("X") - -1.05124071609) < 1e-7
    assert math.fabs(F1.diff("Y") - 0.37620716268) < 1e-7

def test_f6():
    f1 = "POW(2, X)";
    vd = "X:2.0";
    F1 = autodif.AD(f1)
    F1.set_point(vd)
    assert math.fabs(F1.val() - 4) < 1e-7
    assert math.fabs(F1.diff("X") - 2.772588722239781) < 1e-7
