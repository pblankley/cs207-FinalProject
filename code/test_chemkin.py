from chemkin import toy_prog_rate, progress_rate, reaction_rate
import numpy as np

# Testing Suite Toy Progress Rate
def test_toy_prog_rate_int():
    assert(toy_prog_rate([2,2,3],[1,2,3],6)==24.0)
    assert(toy_prog_rate([0.5,2,3],[1,2,3],2.5)==10.0)
    assert(toy_prog_rate([2,2,3],[4,.5,3],2)==8.0)

def test_toy_prog_rate_neg():
    assert(toy_prog_rate([-2,2,3],[2,1,3],8)==2.0)
    assert(toy_prog_rate([0.5,2,3],[4,-2,3],2)==16.0)
    assert(toy_prog_rate([0.5,1,3],[4,-2,3],2)==-8.0)

def test_toy_prog_rate_len():
    try:
        toy_prog_rate([-2,2,3,3],[2,1,3],8)
    except ValueError as err:
        assert(type(err)==ValueError)

    try:
        toy_prog_rate([0.5,2,3,2],[4,-2,3,5],2)
    except ValueError as err:
        assert(type(err)==ValueError)

def test_toy_prog_rate_str():
    try:
        toy_prog_rate([2,2,3],['j1',2,3],6)
    except ValueError as err:
        assert(type(err)==ValueError)
    # Test successful float conversion
    assert(toy_prog_rate([2.,1.,1.], ['1',2.,3.], '5')==10.0)

# Testing Suite Progress Rate
def test_progress_rate_int():
    vp1 = np.array([[0.5,2],[3,0],[0,1]])
    vpp1 = np.array([[0,0],[1,1],[2,1]])
    x1 = np.array([[1],[2],[1]])
    assert(progress_rate(vp1,vpp1,x1,5)==[40.0,5.0])

    vp2 = np.array([[0.5,0.5],[2,1],[0,2]])
    vpp2 = np.array([[0,0],[0,1],[2,1]])
    x2 = np.array([[4],[2],[1]])
    assert(progress_rate(vp2,vpp2,x2,2.5)==[20.0,10.0])

    vp3 = np.array([[1,2],[1,2],[0,1]])
    vpp3 = np.array([[0,0],[0,1],[2,1]])
    x3 = np.array([[0.5],[4],[2]])
    assert(progress_rate(vp3,vpp3,x3,2)==[4.0,16.0])

def test_progress_rate_neg():
    vp1 = np.array([[0.5,-2],[3,0],[0,1]])
    vpp1 = np.array([[0,0],[1,1],[2,1]])
    x1 = np.array([[4],[2],[1]])
    assert(progress_rate(vp1,vpp1,x1,2)==[32.0,0.125])

    vp2 = np.array([[1,2],[2,1],[0,2]])
    vpp2 = np.array([[0,0],[0,1],[2,1]])
    x2 = np.array([[4],[-2],[1]])
    assert(progress_rate(vp2,vpp2,x2,2.5)==[40.0,-80.0])

def test_progress_rate_len():
    try:
        vp1 = np.array([[0.5,-2,7],[3,0,1],[0,1,2]])
        vpp1 = np.array([[0,0],[1,1],[2,1]])
        x1 = np.array([[4],[2],[1]])
        progress_rate(vp1,vpp1,x1,2)
    except ValueError as err:
        assert(type(err)==ValueError)

    try:
        vp2 = np.array([[0.5,-2],[3,0],[0,1]])
        vpp2 = np.array([[0,0],[1,1],[2,1]])
        x2 = np.array([[4,1],[2,2],[1,3]])
        progress_rate(vp2,vpp2,x2,2)
    except ValueError as err:
        assert(type(err)==ValueError)

    try:
        vp3 = np.array([[0.5,-2],[3,0],[0,1]])
        vpp3 = np.array([[0,0],[1,1],[2,1]])
        x3 = np.array([[4],[2],[1],[2]])
        progress_rate(vp3,vpp3,x3,2)
    except ValueError as err:
        assert(type(err)==ValueError)

    try:
        vp4 = np.array([[0.5,-2],[3,0],[0,1],[1,2]])
        vpp4 = np.array([[0,0],[1,1],[2,1],[0,3]])
        x4 = np.array([[4],[2],[1]])
        progress_rate(vp4,vpp4,x4,2)
    except ValueError as err:
        assert(type(err)==ValueError)

def test_progress_rate_str():
    try:
        vp1 = np.array([[0.5,-2],['j3',0],[0,1]])
        vpp1 = np.array([[0,0],[1,1],[2,1]])
        x1 = np.array([[4],[2],[1]])
        progress_rate(vp1,vpp1,x1,2)
    except TypeError as err:
        assert(type(err)==TypeError)

    try:
        vp2 = np.array([[0.5,-2],[3,0],[0,1]])
        vpp2 = np.array([[0,0],[1,1],[2,1]])
        x2 = np.array([[4],[2],[1]])
        progress_rate(vp2,vpp2,x2,'2')
    except ValueError as err:
        assert(type(err)==ValueError)

def test_progress_rate_arr():
    try:
        vp1 = np.array([[0.5,-2],[3,0],[0,1]])
        vpp1 = np.array([[0,0],[1,1],[2,1]])
        x1 = np.array([[4],[2],[1]])
        progress_rate(vp1,vpp1,x1,[2,4,5])
    except ValueError as err:
        assert(type(err)==ValueError)

    try:
        vp2 = np.array([[0.5,-2],[3,0],[0,1]])
        vpp2 = np.array([[0,0],[1,1],[2,1]])
        x2 = np.array([[4],[2],[1]])
        progress_rate(vp2,vpp2,x2,[2])
    except ValueError as err:
        assert(type(err)==ValueError)

    vp3 = np.array([[0.5,2],[3,0],[0,1]])
    vpp3 = np.array([[0,0],[1,1],[2,1]])
    x3 = np.array([[1],[2],[1]])
    assert(progress_rate(vp3,vpp3,x3,[2,5])==[16.0,5.0])

    vp4 = np.array([[0.5,0.5],[2,1],[0,2]])
    vpp4 = np.array([[0,0],[0,1],[2,1]])
    x4 = np.array([[4],[2],[1]])
    assert(progress_rate(vp4,vpp4,x4,[2.5,20])==[20.0,80.0])


# Testing Suite Reaction Rate
def test_reaction_rate_int():
    vp1 = np.array([[0.5,2],[3,0],[0,1]])
    vpp1 = np.array([[0,0],[1,1],[2,1]])
    x1 = np.array([[1],[2],[1]])
    assert(reaction_rate(vp1,vpp1,x1,5)==[-30.0,-75.0,80.0])

    vp2 = np.array([[0.5,0.5],[2,1],[0,2]])
    vpp2 = np.array([[0,0],[0,1],[2,1]])
    x2 = np.array([[4],[2],[1]])
    assert(reaction_rate(vp2,vpp2,x2,2.5)==[-15.0,-40.0,30.0])

    vp3 = np.array([[1,2],[1,2],[0,1]])
    vpp3 = np.array([[0,0],[0,1],[2,1]])
    x3 = np.array([[0.5],[4],[2]])
    assert(reaction_rate(vp3,vpp3,x3,2)==[-36.0,-20.0,8.0])

def test_reaction_rate_neg():
    vp1 = np.array([[0.5,-2],[3,0],[0,1]])
    vpp1 = np.array([[0,0],[1,1],[2,1]])
    x1 = np.array([[4],[2],[1]])
    assert(reaction_rate(vp1,vpp1,x1,2)==[-15.75,-63.875,64.0])

    vp2 = np.array([[1,2],[2,1],[0,2]])
    vpp2 = np.array([[0,0],[0,1],[2,1]])
    x2 = np.array([[4],[-2],[1]])
    assert(reaction_rate(vp2,vpp2,x2,2.5)==[120.0,-80.0,160.0])

def test_reaction_rate_len():
    try:
        vp1 = np.array([[0.5,-2,7],[3,0,1],[0,1,2]])
        vpp1 = np.array([[0,0],[1,1],[2,1]])
        x1 = np.array([[4],[2],[1]])
        reaction_rate(vp1,vpp1,x1,2)
    except ValueError as err:
        assert(type(err)==ValueError)

    try:
        vp2 = np.array([[0.5,-2],[3,0],[0,1]])
        vpp2 = np.array([[0,0],[1,1],[2,1]])
        x2 = np.array([[4,1],[2,2],[1,3]])
        reaction_rate(vp2,vpp2,x2,2)
    except ValueError as err:
        assert(type(err)==ValueError)

    try:
        vp3 = np.array([[0.5,-2],[3,0],[0,1]])
        vpp3 = np.array([[0,0],[1,1],[2,1]])
        x3 = np.array([[4],[2],[1],[2]])
        reaction_rate(vp3,vpp3,x3,2)
    except ValueError as err:
        assert(type(err)==ValueError)

    try:
        vp4 = np.array([[0.5,-2],[3,0],[0,1],[1,2]])
        vpp4 = np.array([[0,0],[1,1],[2,1],[0,3]])
        x4 = np.array([[4],[2],[1]])
        reaction_rate(vp4,vpp4,x4,2)
    except ValueError as err:
        assert(type(err)==ValueError)

def test_reaction_rate_str():
    try:
        vp1 = np.array([[0.5,-2],['j3',0],[0,1]])
        vpp1 = np.array([[0,0],[1,1],[2,1]])
        x1 = np.array([[4],[2],[1]])
        reaction_rate(vp1,vpp1,x1,2)
    except TypeError as err:
        assert(type(err)==TypeError)
