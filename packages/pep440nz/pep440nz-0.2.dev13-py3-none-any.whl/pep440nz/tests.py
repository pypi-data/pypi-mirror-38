def _equality_assert(a,b):
    try:
        assert(a == b)
    except AssertionError as e:
        print(type(a),a,b,type(b),a==b)
        raise e
def _lt_assert(a,b):
    try:
        assert(a < b)
    except AssertionError as e:
        print(type(a),a,b,type(b))
        raise e

def _test_copy():
    o_str = '1337!3.14rc22.post42.dev69+ubuntu.1'
    o_epoch = 1337
    o_release = ['3','14']
    o_pre = ('rc',22)
    o_post = 42
    o_dev = 69
    o_local = ['ubuntu','1']
    v1 = Version(epoch=o_epoch,release=o_release,pre=o_pre,post=o_post,dev=o_dev,local=o_local)
    _equality_assert(str(v1),o_str)
    v2 = v1.copy()
    _equality_assert(str(v2),o_str)
    v2.post.value = 21
    v2.local.value.append('foo')
    n_str = '1337!3.14rc22.post21.dev69+ubuntu.1'
    _equality_assert(str(v2),n_str)
    _equality_assert(str(v1),o_str)

def _test_operations():
    vstr = '1337!3.14rc22.post42.dev69+ubuntu.1'
    o_epoch = 1337
    o_release = ['3','14']
    o_pre = ('rc',22)
    o_post = 42
    o_dev = 69
    o_local = ['ubuntu','1']
    v = Version(epoch=o_epoch,release=o_release,pre=o_pre,post=o_post,dev=o_dev,local=o_local)
    _equality_assert(str(v),vstr)

    # Epoch
    eid = id(v.epoch)
    v.epoch += 5
    Vstr = '1342!3.14rc22.post42.dev69+ubuntu.1'
    _equality_assert(eid,id(v.epoch))
    _equality_assert(str(v),Vstr)
    v.epoch -= Epoch(5)
    _equality_assert(eid,id(v.epoch))
    _equality_assert(str(v),vstr)
    V = Version(epoch=v.epoch,release=v.release,pre=v.pre,post=v.post,dev=v.dev,local=v.local)
    V.epoch = V.epoch + 5
    _equality_assert(str(V),Vstr)
    _equality_assert(str(v),vstr)

    # Release
    rid = id(v.release)
    v.release += 1
    Vstr = '1337!4.14rc22.post42.dev69+ubuntu.1'
    _equality_assert(rid,id(v.release))
    _equality_assert(str(v),Vstr)
    v.release -= 1
    _equality_assert(rid,id(v.release))
    _equality_assert(str(v),vstr)
    ok=0
    try:
        v.release -= 4
    except ValueError:
        ok=1
    if not ok:
        raise AssertionError(v.release)
    _equality_assert(str(v),vstr)
    _equality_assert(v.release[0],int(o_release[0]))
    v.release[1] = 18
    Vstr = '1337!3.18rc22.post42.dev69+ubuntu.1'
    _equality_assert(str(v),Vstr)
    v.release.append('159')
    v.release[1] = 14
    Vstr = '1337!3.14.159rc22.post42.dev69+ubuntu.1'
    _equality_assert(str(v),Vstr)
    _equality_assert(v.release.pop(),159)
    _equality_assert(str(v),vstr)

    # Pre-Release
    v.pre += 2
    Vstr = '1337!3.14rc24.post42.dev69+ubuntu.1'
    _equality_assert(str(v),Vstr)
    v.pre -= ('pre',1)
    Vstr = '1337!3.14rc23.post42.dev69+ubuntu.1'
    _equality_assert(str(v),Vstr)
    v.pre -= 1
    _equality_assert(str(v),vstr)
    ok=0
    try:
        v.pre += ('a',1)
    except ValueError:
        ok=1
    if not ok:
        raise AssertionError(v.pre)
    _equality_assert(str(v),vstr)
    v.pre = None
    Vstr = '1337!3.14.post42.dev69+ubuntu.1'
    _equality_assert(str(v),Vstr)
    ok=0
    try:
        v.pre += 3
    except TypeError:
        ok=1
    if not ok:
        raise AssertionError(v.pre)
    v.pre+=('c',22)
    _equality_assert(str(v),vstr)

    # Post-Release
    v.post -= 21
    Vstr = '1337!3.14rc22.post21.dev69+ubuntu.1'
    _equality_assert(str(v),Vstr)
    v.post += 21
    _equality_assert(str(v),vstr)
    ok=0
    try:
        v.post -= 45
    except ValueError:
        ok=1
    if not ok:
        raise AssertionError(v.post)
    _equality_assert(str(v),vstr)
    v.post = None
    v.post += 42
    _equality_assert(str(v),vstr)

    # Dev Release
    Vstr = '1337!3.14rc22.post42.dev69+ubuntu.1'

def _test_comparison():
    vstr = '3.14rc22.post42.dev69+ubuntu.1'
    for wstr in ['1!0',
            '4.0',
            '3.15',
            '3.14',
            '3.14c23',
            '3.14post1',
            '3.14c22r42dev70',
            '3.14c22r42dev69+ubuntu.2']:
        _lt_assert(Version(vstr),Version(wstr))

__all__ = ['Version','Epoch','Release','PreRelease','PostRelease','DevRelease','LocalRelease']

if __name__=='__main__':
    _test_all_parsing(full=False)
    _test_copy()
    _test_operations()
    _test_comparison()
