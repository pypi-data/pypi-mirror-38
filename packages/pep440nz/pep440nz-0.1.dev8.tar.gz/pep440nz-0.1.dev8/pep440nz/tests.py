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

def _test_all_parsing(full=True):
    import sys
    if len(sys.argv[1:]):
        for a in sys.argv[1:]:
            vstring = a
            print(a)
            vobj = Version(a)
            print(vobj)
        sys.exit(0)
    def make_vstr(v,e,r,p,P,d,l):
        return ''.join(map(str,[v,e,r,p,P,d,l]))
    if full:
        v_alt = ['','v','V']
        e_alt = {'':0, '0!':0,'42!':42}
        r_alt = {'0':[0],'3.14.0159.265':[3,14,159,265]}
    else:
        v_alt = ['v']
        e_alt = {'':0,'2!':2}
        r_alt = {'3.14':[3,14]}

    p_alt = {'':None}
    p_alt_implicit = set()
    pts_alt = ['','.','-','_']
    pt_alt = {'a':'a','b':'b','rc':'rc','pre':'rc','preview':'rc','c':'rc','alpha':'a','beta':'b'}
    pn_alt = {'':0,'23':23,'-23':23,'_23':23,'.23':23}
    for ts in pts_alt:
        for t in pt_alt:
            for n in pn_alt:
                p_alt[ts+t+n] = (pt_alt[t],pn_alt[n])
                if not n:
                    p_alt_implicit.add(ts+t+n)

    P_alt = {'':None,'-69':69,'-0':0}
    P_alt_implicit_left = {'-69','-0'}
    P_alt_implicit_right= set()
    Pts_alt = ['','.','-','_']
    Pt_alt = ['post','rev','r']
    Pn_alt = {'':0,'69':69,'-69':69,'_69':69,'.69':69}
    for ts in Pts_alt:
        for t in Pt_alt:
            for n in Pn_alt:
                P_alt[ts+t+n] = Pn_alt[n]
                if not n:
                    P_alt_implicit_right.add(ts+t+n)

    d_alt = {'':None}
    d_alt_implicit = set()
    dts_alt = ['','.','-','_']
    dn_alt = {'':0,'13':13}
    for ts in dts_alt:
        for n in dn_alt:
            d_alt[ts+'dev'+n] = dn_alt[n]
            if not n:
                d_alt_implicit.add(ts+'dev'+n)

    l_alt = {'':None,'+ubuntu-1':['ubuntu','1'],'+hello_32-foo.bar':['hello','32','foo','bar']}

    c=0
    for v in v_alt:
        for e in e_alt:
            for r in r_alt:
                for p in p_alt:
                    for P in P_alt:
                        if not (p in p_alt_implicit and P in P_alt_implicit_left):
                            for d in d_alt:
                                if not (P in P_alt_implicit_right and d in d_alt_implicit):
                                    for l in l_alt:
                                        vs = make_vstr(v,e,r,p,P,d,l)
                                        try:
                                            vo = Version(vs)
                                        except Exception as e:
                                            print(vs)
                                            raise e
                                        try:
                                            _equality_assert(vo.epoch.value,e_alt[e])
                                            _equality_assert(vo.release.value,r_alt[r])
                                            _equality_assert(vo.pre.value,p_alt[p])
                                            _equality_assert(vo.post.value,P_alt[P])
                                            _equality_assert(vo.dev.value,d_alt[d])
                                            _equality_assert(vo.local.value,l_alt[l])
                                        except AssertionError as e:
                                            print('>>',vo)
                                            raise e
                                        c+=1
    print('OK {:d}'.format(c))

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
