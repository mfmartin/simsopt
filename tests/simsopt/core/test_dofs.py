import unittest
import numpy as np
from collections import Counter

from simsopt.core.optimizable import get_owners, DOF, DOFs, DOFsDataFrame
from simsopt.core.new_functions import Identity, Adder, \
                        TestObject2, Rosenbrock, Affine
from simsopt.core.optimizable import Target

class GetOwnersTests(unittest.TestCase):
    def setUp(self):
        self.obj = object()
        self.i1 = Identity()
        self.i2 = Identity()
        self.i3 = Identity()
        self.comp = lambda list1, list2: Counter(list1) == Counter(list2)

    def tearDown(self) -> None:
        self.obj = None
        self.i1 = None
        self.i2 = None
        self.i3 = None

    def test_no_dependents(self):
        """
        For an object that does not depend on anything, just return the
        original object.
        """
        self.assertEqual(get_owners(self.obj), [self.obj])
        self.assertEqual(get_owners(self.i1), [self.i1])

    def test_depth_1(self):
        """
        Check cases in which the original object depends on 1 or more others.
        """
        self.i1.i2 = self.i2
        self.i1.depends_on = ["i2"]
        self.assertTrue(self.comp(get_owners(self.i1), [self.i1, self.i2]))

        self.i1.depends_on = ["obj", "i2"]
        self.i1.obj = self.obj
        self.assertTrue(self.comp(get_owners(self.i1),
                                  [self.i1, self.obj, self.i2]))
        
    def test_depth_2(self):
        """
        Check cases in which the original object depends on another, which
        depends on another.
        """
        self.i1.depends_on = ["i2"]
        self.i2.depends_on = ["obj"]
        self.i1.i2 = self.i2
        self.i2.obj = self.obj
        self.assertTrue(get_owners(self.i1), [self.i1, self.i2, self.obj])

    def test_circular2(self):
        """
        Verify that a circular dependency among 2 objects is detected.
        """
        self.i1.depends_on = ["i2"]
        self.i2.depends_on = ["i1"]
        self.i1.i2 = self.i2
        self.i2.i1 = self.i1
        with self.assertRaises(RuntimeError):
            get_owners(self.i1)

    def test_circular3(self):
        """
        Verify that a circular dependency among 3 objects is detected.
        """
        self.i1.depends_on = ["i2"]
        self.i2.depends_on = ["i3"]
        self.i3.depends_on = ["i1"]
        self.i1.i2 = self.i2
        self.i2.i3 = self.i3
        self.i3.i1 = self.i1
        with self.assertRaises(RuntimeError):
            get_owners(self.i1)

class DOFTest(unittest.TestCase):
    """
    Unit tests for simsopt.core.DOF class
    """
    def setUp(self):
        rosen = Rosenbrock()
        self.dof1 = DOF(rosen, 'x', 2.0, True, np.NINF, np.inf)
        self.dof2 = DOF(rosen, 'y', 3.0, False, np.NINF, np.inf)

    def tearDown(self) -> None:
        self.dof1 = None
        self.dof2 = None

    #def test_hash(self):
    #    self.assertFalse(True)

    #def test_extended_name(self):
    #    self.assertFalse(True)

    def test_is_fixed(self):
        self.assertFalse(self.dof1.is_fixed())
        self.assertTrue(self.dof2.is_fixed())

    def test_is_free(self):
        self.assertTrue(self.dof1.is_free())
        self.assertFalse(self.dof2.is_free())

    def test_fix(self):
        self.dof1.fix()
        self.assertTrue(self.dof1.is_fixed())

    def test_unfix(self):
        self.dof2.unfix()
        self.assertTrue(self.dof2.is_free())

    def test_min(self):
        self.assertTrue(np.isclose(self.dof1.min, np.NINF))
        self.dof1.min = -10.0
        self.assertAlmostEqual(self.dof1.min, -10.0)

    def test_max(self):
        self.assertTrue(np.isclose(self.dof1.max, np.inf))
        self.dof1.max = 1e2
        self.assertAlmostEqual(self.dof1.max, 100.0)

    #def test_owner(self):
    #    self.assertTrue(False)

    def test_x(self):
        self.assertAlmostEqual(self.dof1.x, 2.0)
        self.dof1.x = 10.0
        self.assertAlmostEqual(self.dof1.x, 10.0)


class DOFsDataFrameTests(unittest.TestCase):

    def setUp(self):
        self.identity = Identity(x=1, dof_name='x')
        self.adder = Adder(3, x0=[2, 3, 4], dof_names=["x", "y", "z"])
        self.rosenbrock = Rosenbrock()

    def tearDown(self) -> None:
        self.identity = None
        self.adder = None
        self.rosenbrock = None

    def test_init(self):
        # self.assertRaises(NotImplemented("Test not implemented"))
        pass

    def test_fix(self):
        pass
        # self.assertRaises(NotImplementedError("Test not implemented"))

    def test_unfix(self):
        # self.assertRaises(NotImplementedError("Test not implemented"))
        pass

    def test_fix_all(self):
        # self.assertRaises(NotImplementedError("Test not implemented"))
        pass

    def test_unfix_all(self):
        # self.assertRaises(NotImplementedError("Test not implemented"))
        pass

    def test_any_free(self):
        # self.assertRaises(NotImplementedError("Test not implemented"))
        pass

    def test_any_fixed(self):
        # self.assertRaises(NotImplementedError("Test not implemented"))
        pass

    def test_all_free(self):
        # self.assertRaises(NotImplementedError("Test not implemented"))
        pass

    def test_all_fixed(self):
        # self.assertRaises(NotImplementedError("Test not implemented"))
        pass

    def test_x(self):
        # self.assertRaises(NotImplementedError("Test not implemented"))
        pass

    def test_full_x(self):
        # self.assertRaises(NotImplementedError("Test not implemented"))
        pass

    def test_lower_bounds(self):
        # self.assertRaises(NotImplementedError("Test not implemented"))
        pass

    def test_upper_bounds(self):
        # self.assertRaises(NotImplementedError("Test not implemented"))
        pass

    def test_bounds(self):
        # self.assertRaises(NotImplementedError("Test not implemented"))
        pass

    def test_update_bound(self):
        # self.assertRaises(NotImplementedError("Test not implemented"))
        pass

    def test_no_dependents(self):
        """
        Tests for an object that does not depend on other objects.
        """
        obj = Adder(4)
        obj.set_dofs([101, 102, 103, 104])
        dofs = DOFs.from_functions([obj.J])
        np.testing.assert_allclose(dofs.x, [101, 102, 103, 104])
        self.assertEqual(dofs.all_owners, [obj])
        self.assertEqual(dofs.dof_owners, [obj, obj, obj, obj])
        np.testing.assert_allclose(dofs.indices, [0, 1, 2, 3])
        dummy = dofs.f()  # f must be evaluated before we know nvals_per_func
        self.assertEqual(list(dofs.nvals_per_func), [1])
        self.assertEqual(dofs.nvals, 1)

        obj.dof_fixed = [True, False, True, False]
        dofs = DOFs.from_functions([obj.J])
        np.testing.assert_allclose(dofs.x, [102, 104])
        self.assertEqual(dofs.all_owners, [obj])
        self.assertEqual(dofs.dof_owners, [obj, obj])
        np.testing.assert_allclose(dofs.indices, [1, 3])

        obj.dof_fixed[0] = False
        dofs = DOFs.from_functions([obj.J])
        np.testing.assert_allclose(dofs.x, [101, 102, 104])
        self.assertEqual(dofs.all_owners, [obj])
        self.assertEqual(dofs.dof_owners, [obj, obj, obj])
        np.testing.assert_allclose(dofs.indices, [0, 1, 3])

    def test_no_fixed(self):
        """
        Test behavior when there is no 'fixed' attribute.
        """
        obj = Adder(4)
        del obj.dof_fixed
        self.assertFalse(hasattr(obj, 'fixed'))
        obj.set_dofs([101, 102, 103, 104])
        dofs = DOFs.from_functions([obj.J])
        np.testing.assert_allclose(dofs.x, [101, 102, 103, 104])
        self.assertEqual(dofs.all_owners, [obj])
        self.assertEqual(dofs.dof_owners, [obj, obj, obj, obj])
        np.testing.assert_allclose(dofs.indices, [0, 1, 2, 3])

    def test_with_dependents(self):
        """
        Test the case in which the original object depends on another object.
        """
        o1 = Adder(3)
        o2 = Adder(4)
        o1.set_dofs([10, 11, 12])
        o2.set_dofs([101, 102, 103, 104])
        o1.depends_on = ["o2"]
        o1.o2 = o2
        dofs = DOFs.from_functions([o1.J])
        np.testing.assert_allclose(dofs.x, [10, 11, 12, 101, 102, 103, 104])
        self.assertEqual(dofs.all_owners, [o1, o2])
        self.assertEqual(dofs.dof_owners, [o1, o1, o1, o2, o2, o2, o2])
        np.testing.assert_allclose(dofs.indices, [0, 1, 2, 0, 1, 2, 3])
        f = dofs.f()  # f must be evaluated before we know nvals_per_func
        self.assertEqual(list(dofs.nvals_per_func), [1])
        self.assertEqual(dofs.nvals, 1)

        o1.dof_fixed = [True, False, True]
        o2.dof_fixed = [False, False, True, True]
        del o1.depends_on
        o2.depends_on = ["o1"]
        o2.o1 = o1
        dofs = DOFs.from_functions([o2.J])
        np.testing.assert_allclose(dofs.x, [101, 102, 11])
        self.assertEqual(dofs.all_owners, [o2, o1])
        self.assertEqual(dofs.dof_owners, [o2, o2, o1])
        np.testing.assert_allclose(dofs.indices, [0, 1, 1])

    def test_vector_valued(self):
        """
        For a function that returns a vector rather than a scalar, make
        sure DOFs.f(), DOFs.jac(), and DOFs.fd_jac() behave correctly.
        """
        for nparams in range(1, 5):
            for nvals in range(1, 5):
                o = Affine(nparams=nparams, nvals=nvals)
                o.set_dofs((np.random.rand(nparams) - 0.5) * 4)
                dofs = DOFs.from_functions([o])
                np.testing.assert_allclose(dofs.f(), np.matmul(o.A, o.x) + o.B, \
                                           rtol=1e-13, atol=1e-13)
                np.testing.assert_allclose(dofs.jac(), o.A, rtol=1e-13,
                                           atol=1e-13)
                np.testing.assert_allclose(dofs.fd_jac(centered=True), \
                                           o.A, rtol=1e-7, atol=1e-7)

    def test_multiple_vector_valued(self):
        """
        For a function that returns a vector rather than a scalar, make
        sure DOFs.f(), DOFs.jac(), and DOFs.fd_jac() behave correctly.
        """
        for nparams1 in range(1, 5):
            for nvals1 in range(1, 5):
                nparams2 = np.random.randint(1, 6)
                nparams3 = np.random.randint(1, 6)
                nvals2 = np.random.randint(1, 6)
                nvals3 = np.random.randint(1, 6)
                o1 = Affine(nparams=nparams1, nvals=nvals1)
                o2 = Affine(nparams=nparams2, nvals=nvals2)
                o3 = Affine(nparams=nparams3, nvals=nvals3)
                dofs = DOFs.from_functions([o1, o2, o3])
                dofs.x = (np.random.rand(
                    nparams1 + nparams2 + nparams3) - 0.5) * 4
                f1 = np.matmul(o1.A, o1.x) + o1.B
                f2 = np.matmul(o2.A, o2.x) + o2.B
                f3 = np.matmul(o3.A, o3.x) + o3.B
                np.testing.assert_allclose(dofs.f(),
                                           np.concatenate((f1, f2, f3)), \
                                           rtol=1e-13, atol=1e-13)
                true_jac = np.zeros(
                    (nvals1 + nvals2 + nvals3, nparams1 + nparams2 + nparams3))
                true_jac[0:nvals1, 0:nparams1] = o1.A
                true_jac[nvals1:nvals1 + nvals2,
                nparams1:nparams1 + nparams2] = o2.A
                true_jac[nvals1 + nvals2:nvals1 + nvals2 + nvals3, \
                nparams1 + nparams2:nparams1 + nparams2 + nparams3] = o3.A
                np.testing.assert_allclose(dofs.jac(), true_jac, rtol=1e-13,
                                           atol=1e-13)
                np.testing.assert_allclose(dofs.fd_jac(centered=True), \
                                           true_jac, rtol=1e-7, atol=1e-7)

    def test_mixed_vector_valued(self):
        """
        For a mixture of functions that return a scalar vs return a
        vector, make sure DOFs.f(), DOFs.jac(), and DOFs.fd_jac()
        behave correctly.
        """
        for nparams1 in range(1, 5):
            for nvals1 in range(1, 5):
                nparams2 = np.random.randint(1, 6)
                nparams3 = np.random.randint(1, 6)
                nvals2 = np.random.randint(1, 6)
                nvals3 = np.random.randint(1, 6)
                o1 = Affine(nparams=nparams1, nvals=nvals1)
                o2 = Affine(nparams=nparams2, nvals=nvals2)
                o3 = Affine(nparams=nparams3, nvals=nvals3)
                a1 = Adder(n=2)
                a2 = Adder(n=3)
                dofs = DOFs.from_functions([o1, o2, a1, o3, a2])
                dofs.x = (np.random.rand(
                    nparams1 + nparams2 + nparams3 + 5) - 0.5) * 4
                f1 = np.matmul(o1.A, o1.x) + o1.B
                f2 = np.matmul(o2.A, o2.x) + o2.B
                f3 = np.array([a1.f])
                f4 = np.matmul(o3.A, o3.x) + o3.B
                f5 = np.array([a2.f])
                np.testing.assert_allclose(dofs.f(),
                                           np.concatenate((f1, f2, f3, f4, f5)), \
                                           rtol=1e-13, atol=1e-13)
                true_jac = np.zeros((nvals1 + nvals2 + nvals3 + 2,
                                     nparams1 + nparams2 + nparams3 + 5))
                true_jac[0:nvals1, 0:nparams1] = o1.A
                true_jac[nvals1:nvals1 + nvals2,
                nparams1:nparams1 + nparams2] = o2.A
                true_jac[nvals1 + nvals2:nvals1 + nvals2 + 1, \
                nparams1 + nparams2:nparams1 + nparams2 + 2] = np.ones(2)
                true_jac[nvals1 + nvals2 + 1:nvals1 + nvals2 + 1 + nvals3, \
                nparams1 + nparams2 + 2:nparams1 + nparams2 + 2 + nparams3] = o3.A
                true_jac[
                nvals1 + nvals2 + 1 + nvals3:nvals1 + nvals2 + nvals3 + 2, \
                nparams1 + nparams2 + nparams3 + 2:nparams1 + nparams2 + nparams3 + 5] = np.ones(
                    3)
                np.testing.assert_allclose(dofs.jac(), true_jac, rtol=1e-13,
                                           atol=1e-13)
                np.testing.assert_allclose(dofs.fd_jac(centered=True), \
                                           true_jac, rtol=1e-7, atol=1e-7)

    def test_Jacobian(self):
        for n in range(1, 20):
            v1 = np.random.rand() * 4 - 2
            v2 = np.random.rand() * 4 - 2
            o = TestObject2(v1, v2)
            o.adder.set_dofs(np.random.rand(2) * 4 - 2)
            o.t.set_dofs([np.random.rand() * 4 - 2])
            o.t.adder1.set_dofs(np.random.rand(3) * 4 - 2)
            o.t.adder2.set_dofs(np.random.rand(2) * 4 - 2)
            r = Rosenbrock(b=3.0)
            r.set_dofs(np.random.rand(2) * 3 - 1.5)
            a = Affine(nparams=3, nvals=3)

            # Randomly fix some of the degrees of freedom
            o.dof_fixed = np.random.rand(2) > 0.5
            o.adder.dof_fixed = np.random.rand(2) > 0.5
            o.t.adder1.dof_fixed = np.random.rand(3) > 0.5
            o.t.adder2.dof_fixed = np.random.rand(2) > 0.5
            r.dof_fixed = np.random.rand(2) > 0.5
            a.dof_fixed = np.random.rand(3) > 0.5

            rtol = 1e-6
            atol = 1e-6

            for j in range(4):
                # Try different sets of the objects:
                if j == 0:
                    dofs = DOFs.from_functions([o.J, r.terms, o.t.J])
                    nvals = 4
                    nvals_per_func = [1, 2, 1]
                elif j == 1:
                    dofs = DOFs.from_functions([r.term2, r.terms])
                    nvals = 3
                    nvals_per_func = [1, 2]
                elif j == 2:
                    dofs = DOFs.from_functions(
                        [r.term2, Target(o.t, 'f'), r.term1, Target(o, 'f')])
                    nvals = 4
                    nvals_per_func = [1, 1, 1, 1]
                elif j == 3:
                    dofs = DOFs.from_functions([a, o])
                    nvals = 4
                    nvals_per_func = [3, 1]

                jac = dofs.jac()
                fd_jac = dofs.fd_jac()
                fd_jac_centered = dofs.fd_jac(centered=True)
                # print('j=', j, '  Diff in Jacobians:', jac - fd_jac)
                # print('jac: ', jac)
                # print('fd_jac: ', fd_jac)
                # print('fd_jac_centered: ', fd_jac_centered)
                # print('shapes: jac=', jac.shape, '  fd_jac=', fd_jac.shape, '  fd_jac_centered=', fd_jac_centered.shape)
                np.testing.assert_allclose(jac, fd_jac, rtol=rtol, atol=atol)
                np.testing.assert_allclose(fd_jac, fd_jac_centered, rtol=rtol,
                                           atol=atol)
                self.assertEqual(dofs.nvals, nvals)
                self.assertEqual(list(dofs.nvals_per_func), nvals_per_func)


class NewDOFsTests(unittest.TestCase):

    def setUp(self):
        self.identity = Identity(x=1, dof_name='x')
        self.adder = Adder(3, x0=[2, 3, 4], dof_names=["x", "y", "z"])
        self.rosenbrock = Rosenbrock()

    def tearDown(self) -> None:
        self.identity = None
        self.adder = None
        self.rosenbrock = None

    def test_init(self):
        #self.assertRaises(NotImplemented("Test not implemented"))
        pass

    def test_getitem(self):
        # Use optimizable._dofs to isolate the testing to only dofs
        dof = DOF(self.identity, 'x', 1)
        self.assertTrue(self.identity._dofs[0] == dof)
        self.assertTrue(self.identity._dofs['x'] == dof)

        dof = DOF(self.adder, 'z', 4.0)
        self.assertTrue(self.adder._dofs[2] == dof)
        self.assertTrue(self.adder._dofs['z'] == dof)
        dof = DOF(self.adder, 'y', 3.0)
        self.assertTrue(self.adder._dofs['y'] == dof)
        dof = DOF(self.adder, 'x', 2.0)
        self.assertTrue(self.adder._dofs[0] == dof)

    def test_setitem(self):
        dof = DOF(self.identity, 'x', 1)
        self.adder._dofs[2] = dof
        self.assertTrue(self.adder._dofs.owners[2] == self.identity)
        self.assertTrue(self.adder._dofs.names[2] == 'x')
        self.assertTrue(self.adder._dofs.full_x[2] == 1)

    def test_delitem(self):
        del self.adder._dofs[2]
        print(self.adder._dofs['z'])
        with self.assertRaises(IndexError):
            self.adder._dofs['z']
        with self.assertRaises(IndexError):
                self.adder._dofs[2]
        del self.adder._dofs['x']
        with self.assertRaises(IndexError):
            self.adder._dofs[1]
        with self.assertRaises(IndexError):
            self.adder._dofs['x']

    def test_len(self):
        self.assertTrue(len(self.adder._dofs) == 3)
        self.assertTrue(len(self.identity._dofs) == 1)

    def test_contains(self):
        self.assertTrue('x' in self.adder._dofs)
        self.assertTrue(3 in self.adder._dofs)
        dof = DOF(self.adder, 'z', 4)
        self.assertTrue(dof in self.adder._dofs)

    def test_iter(self):
        for dof in self.adder._dofs:
            self.assertTrue(isinstance(dof, DOF))
        dof_iter = iter(self.adder._dofs)
        dof = next(dof_iter)
        self.assertTrue(dof.x == 2 and dof.name == 'x' and
                        dof.owner == self.adder)
        dof = next(dof_iter)
        self.assertTrue(dof.x == 3 and dof.name == 'y' and
                        dof.owner == self.adder)
        dof = next(dof_iter)
        self.assertTrue(dof.x == 4 and dof.name == 'z' and
                        dof.owner == self.adder)

    def test_reversed(self):
        for dof in reversed(self.adder._dofs):
            self.assertTrue(isinstance(dof, DOF))
        dof_iter = reversed(self.adder._dofs)
        dof = next(dof_iter)
        self.assertTrue(dof.x == 4 and dof.name == 'z' and
                        dof.owner == self.adder)
        dof = next(dof_iter)
        self.assertTrue(dof.x == 3 and dof.name == 'y' and
                        dof.owner == self.adder)
        dof = next(dof_iter)
        self.assertTrue(dof.x == 2 and dof.name == 'x' and
                    dof.owner == self.adder)

    def test_add(self):
        dofs1 = self.adder._dofs
        dofs2 = self.identity._dofs
        dofs3 = self.rosenbrock._dofs
        dofs = dofs1 + dofs2 + dofs3
        dof_iter = iter(dofs)
        dof = next(dof_iter)
        self.assertTrue(dof.x == 2 and dof.name == 'x' and
                        dof.owner == self.adder)
        dof = next(dof_iter)
        self.assertTrue(dof.x == 3 and dof.name == 'y' and
                        dof.owner == self.adder)
        dof = next(dof_iter)
        self.assertTrue(dof.x == 4 and dof.name == 'z' and
                        dof.owner == self.adder)
        dof = next(dof_iter)
        self.assertTrue(dof.x == 1 and dof.name == 'x' and
                        dof.owner == self.identity)
        dof = next(dof_iter)
        self.assertTrue(dof.x == 0 and dof.name == 'x' and
                        dof.owner == self.rosenbrock)
        dof = next(dof_iter)
        self.assertTrue(dof.x == 0 and dof.name == 'y' and
                        dof.owner == self.rosenbrock)

    def test_reverse(self):
        #self.assertRaises(NotImplementedError("Test not implemented"))
        pass

    def test_extend(self):
        #self.assertRaises(NotImplementedError("Test not implemented"))
        pass

    def test_pop(self):
        #self.assertRaises(NotImplementedError("Test not implemented"))
        pass

    def test_remove(self):
        #self.assertRaises(NotImplementedError("Test not implemented"))
        pass

    def test_fix(self):
        pass
        #self.assertRaises(NotImplementedError("Test not implemented"))

    def test_unfix(self):
        #self.assertRaises(NotImplementedError("Test not implemented"))
        pass

    def test_fix_all(self):
        #self.assertRaises(NotImplementedError("Test not implemented"))
        pass

    def test_unfix_all(self):
        #self.assertRaises(NotImplementedError("Test not implemented"))
        pass

    def test_any_free(self):
        #self.assertRaises(NotImplementedError("Test not implemented"))
        pass

    def test_any_fixed(self):
        #self.assertRaises(NotImplementedError("Test not implemented"))
        pass

    def test_all_free(self):
        #self.assertRaises(NotImplementedError("Test not implemented"))
        pass

    def test_all_fixed(self):
        #self.assertRaises(NotImplementedError("Test not implemented"))
        pass
    
    def test_x(self):
        #self.assertRaises(NotImplementedError("Test not implemented"))
        pass
    
    def test_full_x(self):
        #self.assertRaises(NotImplementedError("Test not implemented"))
        pass

    def test_lower_bounds(self):
        #self.assertRaises(NotImplementedError("Test not implemented"))
        pass

    def test_upper_bounds(self):
        #self.assertRaises(NotImplementedError("Test not implemented"))
        pass

    def test_bounds(self):
        #self.assertRaises(NotImplementedError("Test not implemented"))
        pass

    def test_update_bound(self):
        #self.assertRaises(NotImplementedError("Test not implemented"))
        pass


    def test_no_dependents(self):
        """
        Tests for an object that does not depend on other objects.
        """
        obj = Adder(4)
        obj.set_dofs([101, 102, 103, 104])
        dofs = DOFs.from_functions([obj.J])
        np.testing.assert_allclose(dofs.x, [101, 102, 103, 104])
        self.assertEqual(dofs.all_owners, [obj])
        self.assertEqual(dofs.dof_owners, [obj, obj, obj, obj])
        np.testing.assert_allclose(dofs.indices, [0, 1, 2, 3])
        dummy = dofs.f()  # f must be evaluated before we know nvals_per_func
        self.assertEqual(list(dofs.nvals_per_func), [1])
        self.assertEqual(dofs.nvals, 1)

        obj.dof_fixed = [True, False, True, False]
        dofs = DOFs.from_functions([obj.J])
        np.testing.assert_allclose(dofs.x, [102, 104])
        self.assertEqual(dofs.all_owners, [obj])
        self.assertEqual(dofs.dof_owners, [obj, obj])
        np.testing.assert_allclose(dofs.indices, [1, 3])

        obj.dof_fixed[0] = False
        dofs = DOFs.from_functions([obj.J])
        np.testing.assert_allclose(dofs.x, [101, 102, 104])
        self.assertEqual(dofs.all_owners, [obj])
        self.assertEqual(dofs.dof_owners, [obj, obj, obj])
        np.testing.assert_allclose(dofs.indices, [0, 1, 3])

    def test_no_fixed(self):
        """
        Test behavior when there is no 'fixed' attribute.
        """
        obj = Adder(4)
        del obj.dof_fixed
        self.assertFalse(hasattr(obj, 'fixed'))
        obj.set_dofs([101, 102, 103, 104])
        dofs = DOFs.from_functions([obj.J])
        np.testing.assert_allclose(dofs.x, [101, 102, 103, 104])
        self.assertEqual(dofs.all_owners, [obj])
        self.assertEqual(dofs.dof_owners, [obj, obj, obj, obj])
        np.testing.assert_allclose(dofs.indices, [0, 1, 2, 3])

    def test_with_dependents(self):
        """
        Test the case in which the original object depends on another object.
        """
        o1 = Adder(3)
        o2 = Adder(4)
        o1.set_dofs([10, 11, 12])
        o2.set_dofs([101, 102, 103, 104])
        o1.depends_on = ["o2"]
        o1.o2 = o2
        dofs = DOFs.from_functions([o1.J])
        np.testing.assert_allclose(dofs.x, [10, 11, 12, 101, 102, 103, 104])
        self.assertEqual(dofs.all_owners, [o1, o2])
        self.assertEqual(dofs.dof_owners, [o1, o1, o1, o2, o2, o2, o2])
        np.testing.assert_allclose(dofs.indices, [0, 1, 2, 0, 1, 2, 3])
        f = dofs.f()  # f must be evaluated before we know nvals_per_func
        self.assertEqual(list(dofs.nvals_per_func), [1])
        self.assertEqual(dofs.nvals, 1)

        o1.dof_fixed = [True, False, True]
        o2.dof_fixed = [False, False, True, True]
        del o1.depends_on
        o2.depends_on = ["o1"]
        o2.o1 = o1
        dofs = DOFs.from_functions([o2.J])
        np.testing.assert_allclose(dofs.x, [101, 102, 11])
        self.assertEqual(dofs.all_owners, [o2, o1])
        self.assertEqual(dofs.dof_owners, [o2, o2, o1])
        np.testing.assert_allclose(dofs.indices, [0, 1, 1])

    def test_vector_valued(self):
        """
        For a function that returns a vector rather than a scalar, make
        sure DOFs.f(), DOFs.jac(), and DOFs.fd_jac() behave correctly.
        """
        for nparams in range(1, 5):
            for nvals in range(1, 5):
                o = Affine(nparams=nparams, nvals=nvals)
                o.set_dofs((np.random.rand(nparams) - 0.5) * 4)
                dofs = DOFs.from_functions([o])
                np.testing.assert_allclose(dofs.f(), np.matmul(o.A, o.x) + o.B, \
                                           rtol=1e-13, atol=1e-13)
                np.testing.assert_allclose(dofs.jac(), o.A, rtol=1e-13,
                                           atol=1e-13)
                np.testing.assert_allclose(dofs.fd_jac(centered=True), \
                                           o.A, rtol=1e-7, atol=1e-7)

    def test_multiple_vector_valued(self):
        """
        For a function that returns a vector rather than a scalar, make
        sure DOFs.f(), DOFs.jac(), and DOFs.fd_jac() behave correctly.
        """
        for nparams1 in range(1, 5):
            for nvals1 in range(1, 5):
                nparams2 = np.random.randint(1, 6)
                nparams3 = np.random.randint(1, 6)
                nvals2 = np.random.randint(1, 6)
                nvals3 = np.random.randint(1, 6)
                o1 = Affine(nparams=nparams1, nvals=nvals1)
                o2 = Affine(nparams=nparams2, nvals=nvals2)
                o3 = Affine(nparams=nparams3, nvals=nvals3)
                dofs = DOFs.from_functions([o1, o2, o3])
                dofs.x = (np.random.rand(
                    nparams1 + nparams2 + nparams3) - 0.5) * 4
                f1 = np.matmul(o1.A, o1.x) + o1.B
                f2 = np.matmul(o2.A, o2.x) + o2.B
                f3 = np.matmul(o3.A, o3.x) + o3.B
                np.testing.assert_allclose(dofs.f(),
                                           np.concatenate((f1, f2, f3)), \
                                           rtol=1e-13, atol=1e-13)
                true_jac = np.zeros(
                    (nvals1 + nvals2 + nvals3, nparams1 + nparams2 + nparams3))
                true_jac[0:nvals1, 0:nparams1] = o1.A
                true_jac[nvals1:nvals1 + nvals2,
                nparams1:nparams1 + nparams2] = o2.A
                true_jac[nvals1 + nvals2:nvals1 + nvals2 + nvals3, \
                nparams1 + nparams2:nparams1 + nparams2 + nparams3] = o3.A
                np.testing.assert_allclose(dofs.jac(), true_jac, rtol=1e-13,
                                           atol=1e-13)
                np.testing.assert_allclose(dofs.fd_jac(centered=True), \
                                           true_jac, rtol=1e-7, atol=1e-7)

    def test_mixed_vector_valued(self):
        """
        For a mixture of functions that return a scalar vs return a
        vector, make sure DOFs.f(), DOFs.jac(), and DOFs.fd_jac()
        behave correctly.
        """
        for nparams1 in range(1, 5):
            for nvals1 in range(1, 5):
                nparams2 = np.random.randint(1, 6)
                nparams3 = np.random.randint(1, 6)
                nvals2 = np.random.randint(1, 6)
                nvals3 = np.random.randint(1, 6)
                o1 = Affine(nparams=nparams1, nvals=nvals1)
                o2 = Affine(nparams=nparams2, nvals=nvals2)
                o3 = Affine(nparams=nparams3, nvals=nvals3)
                a1 = Adder(n=2)
                a2 = Adder(n=3)
                dofs = DOFs.from_functions([o1, o2, a1, o3, a2])
                dofs.x = (np.random.rand(
                    nparams1 + nparams2 + nparams3 + 5) - 0.5) * 4
                f1 = np.matmul(o1.A, o1.x) + o1.B
                f2 = np.matmul(o2.A, o2.x) + o2.B
                f3 = np.array([a1.f])
                f4 = np.matmul(o3.A, o3.x) + o3.B
                f5 = np.array([a2.f])
                np.testing.assert_allclose(dofs.f(),
                                           np.concatenate((f1, f2, f3, f4, f5)), \
                                           rtol=1e-13, atol=1e-13)
                true_jac = np.zeros((nvals1 + nvals2 + nvals3 + 2,
                                     nparams1 + nparams2 + nparams3 + 5))
                true_jac[0:nvals1, 0:nparams1] = o1.A
                true_jac[nvals1:nvals1 + nvals2,
                nparams1:nparams1 + nparams2] = o2.A
                true_jac[nvals1 + nvals2:nvals1 + nvals2 + 1, \
                nparams1 + nparams2:nparams1 + nparams2 + 2] = np.ones(2)
                true_jac[nvals1 + nvals2 + 1:nvals1 + nvals2 + 1 + nvals3, \
                nparams1 + nparams2 + 2:nparams1 + nparams2 + 2 + nparams3] = o3.A
                true_jac[
                nvals1 + nvals2 + 1 + nvals3:nvals1 + nvals2 + nvals3 + 2, \
                nparams1 + nparams2 + nparams3 + 2:nparams1 + nparams2 + nparams3 + 5] = np.ones(
                    3)
                np.testing.assert_allclose(dofs.jac(), true_jac, rtol=1e-13,
                                           atol=1e-13)
                np.testing.assert_allclose(dofs.fd_jac(centered=True), \
                                           true_jac, rtol=1e-7, atol=1e-7)

    def test_Jacobian(self):
        for n in range(1, 20):
            v1 = np.random.rand() * 4 - 2
            v2 = np.random.rand() * 4 - 2
            o = TestObject2(v1, v2)
            o.adder.set_dofs(np.random.rand(2) * 4 - 2)
            o.t.set_dofs([np.random.rand() * 4 - 2])
            o.t.adder1.set_dofs(np.random.rand(3) * 4 - 2)
            o.t.adder2.set_dofs(np.random.rand(2) * 4 - 2)
            r = Rosenbrock(b=3.0)
            r.set_dofs(np.random.rand(2) * 3 - 1.5)
            a = Affine(nparams=3, nvals=3)

            # Randomly fix some of the degrees of freedom
            o.dof_fixed = np.random.rand(2) > 0.5
            o.adder.dof_fixed = np.random.rand(2) > 0.5
            o.t.adder1.dof_fixed = np.random.rand(3) > 0.5
            o.t.adder2.dof_fixed = np.random.rand(2) > 0.5
            r.dof_fixed = np.random.rand(2) > 0.5
            a.dof_fixed = np.random.rand(3) > 0.5

            rtol = 1e-6
            atol = 1e-6

            for j in range(4):
                # Try different sets of the objects:
                if j == 0:
                    dofs = DOFs.from_functions([o.J, r.terms, o.t.J])
                    nvals = 4
                    nvals_per_func = [1, 2, 1]
                elif j == 1:
                    dofs = DOFs.from_functions([r.term2, r.terms])
                    nvals = 3
                    nvals_per_func = [1, 2]
                elif j == 2:
                    dofs = DOFs.from_functions(
                        [r.term2, Target(o.t, 'f'), r.term1, Target(o, 'f')])
                    nvals = 4
                    nvals_per_func = [1, 1, 1, 1]
                elif j == 3:
                    dofs = DOFs.from_functions([a, o])
                    nvals = 4
                    nvals_per_func = [3, 1]

                jac = dofs.jac()
                fd_jac = dofs.fd_jac()
                fd_jac_centered = dofs.fd_jac(centered=True)
                # print('j=', j, '  Diff in Jacobians:', jac - fd_jac)
                # print('jac: ', jac)
                # print('fd_jac: ', fd_jac)
                # print('fd_jac_centered: ', fd_jac_centered)
                # print('shapes: jac=', jac.shape, '  fd_jac=', fd_jac.shape, '  fd_jac_centered=', fd_jac_centered.shape)
                np.testing.assert_allclose(jac, fd_jac, rtol=rtol, atol=atol)
                np.testing.assert_allclose(fd_jac, fd_jac_centered, rtol=rtol,
                                           atol=atol)
                self.assertEqual(dofs.nvals, nvals)
                self.assertEqual(list(dofs.nvals_per_func), nvals_per_func)


class DOFsTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self) -> None:
        pass

    def test_no_dependents(self):
        """
        Tests for an object that does not depend on other objects.
        """
        obj = Adder(4)
        obj.set_dofs([101, 102, 103, 104])
        dofs = DOFs.from_functions([obj.J])
        np.testing.assert_allclose(dofs.x, [101, 102, 103, 104])
        self.assertEqual(dofs.all_owners, [obj])
        self.assertEqual(dofs.dof_owners, [obj, obj, obj, obj])
        np.testing.assert_allclose(dofs.indices, [0, 1, 2, 3])
        dummy = dofs.f() # f must be evaluated before we know nvals_per_func
        self.assertEqual(list(dofs.nvals_per_func), [1])
        self.assertEqual(dofs.nvals, 1)

        obj.dof_fixed = [True, False, True, False]
        dofs = DOFs.from_functions([obj.J])
        np.testing.assert_allclose(dofs.x, [102, 104])
        self.assertEqual(dofs.all_owners, [obj])
        self.assertEqual(dofs.dof_owners, [obj, obj])
        np.testing.assert_allclose(dofs.indices, [1, 3])

        obj.dof_fixed[0] = False
        dofs = DOFs.from_functions([obj.J])
        np.testing.assert_allclose(dofs.x, [101, 102, 104])
        self.assertEqual(dofs.all_owners, [obj])
        self.assertEqual(dofs.dof_owners, [obj, obj, obj])
        np.testing.assert_allclose(dofs.indices, [0, 1, 3])

    def test_no_fixed(self):
        """
        Test behavior when there is no 'fixed' attribute.
        """
        obj = Adder(4)
        del obj.dof_fixed
        self.assertFalse(hasattr(obj, 'fixed'))
        obj.set_dofs([101, 102, 103, 104])
        dofs = DOFs.from_functions([obj.J])
        np.testing.assert_allclose(dofs.x, [101, 102, 103, 104])
        self.assertEqual(dofs.all_owners, [obj])
        self.assertEqual(dofs.dof_owners, [obj, obj, obj, obj])
        np.testing.assert_allclose(dofs.indices, [0, 1, 2, 3])


    def test_with_dependents(self):
        """
        Test the case in which the original object depends on another object.
        """
        o1 = Adder(3)
        o2 = Adder(4)
        o1.set_dofs([10, 11, 12])
        o2.set_dofs([101, 102, 103, 104])
        o1.depends_on = ["o2"]
        o1.o2 = o2
        dofs = DOFs.from_functions([o1.J])
        np.testing.assert_allclose(dofs.x, [10, 11, 12, 101, 102, 103, 104])
        self.assertEqual(dofs.all_owners, [o1, o2])
        self.assertEqual(dofs.dof_owners, [o1, o1, o1, o2, o2, o2, o2])
        np.testing.assert_allclose(dofs.indices, [0, 1, 2, 0, 1, 2, 3])
        f = dofs.f() # f must be evaluated before we know nvals_per_func
        self.assertEqual(list(dofs.nvals_per_func), [1])
        self.assertEqual(dofs.nvals, 1)

        o1.dof_fixed = [True, False, True]
        o2.dof_fixed = [False, False, True, True]
        del o1.depends_on
        o2.depends_on = ["o1"]
        o2.o1 = o1
        dofs = DOFs.from_functions([o2.J])
        np.testing.assert_allclose(dofs.x, [101, 102, 11])
        self.assertEqual(dofs.all_owners, [o2, o1])
        self.assertEqual(dofs.dof_owners, [o2, o2, o1])
        np.testing.assert_allclose(dofs.indices, [0, 1, 1])

    def test_vector_valued(self):
        """
        For a function that returns a vector rather than a scalar, make
        sure DOFs.f(), DOFs.jac(), and DOFs.fd_jac() behave correctly.
        """
        for nparams in range(1, 5):
            for nvals in range(1, 5):
                o = Affine(nparams=nparams, nvals=nvals)
                o.set_dofs((np.random.rand(nparams) - 0.5) * 4)
                dofs = DOFs.from_functions([o])
                np.testing.assert_allclose(dofs.f(), np.matmul(o.A, o.x) + o.B, \
                                           rtol=1e-13, atol=1e-13)
                np.testing.assert_allclose(dofs.jac(), o.A, rtol=1e-13, atol=1e-13)
                np.testing.assert_allclose(dofs.fd_jac(centered=True), \
                                           o.A, rtol=1e-7, atol=1e-7)
        
    def test_multiple_vector_valued(self):
        """
        For a function that returns a vector rather than a scalar, make
        sure DOFs.f(), DOFs.jac(), and DOFs.fd_jac() behave correctly.
        """
        for nparams1 in range(1, 5):
            for nvals1 in range(1, 5):
                nparams2 = np.random.randint(1, 6)
                nparams3 = np.random.randint(1, 6)
                nvals2 = np.random.randint(1, 6)
                nvals3 = np.random.randint(1, 6)
                o1 = Affine(nparams=nparams1, nvals=nvals1)
                o2 = Affine(nparams=nparams2, nvals=nvals2)
                o3 = Affine(nparams=nparams3, nvals=nvals3)
                dofs = DOFs.from_functions([o1, o2, o3])
                dofs.x = (np.random.rand(nparams1 + nparams2 + nparams3) - 0.5) * 4
                f1 = np.matmul(o1.A, o1.x) + o1.B
                f2 = np.matmul(o2.A, o2.x) + o2.B
                f3 = np.matmul(o3.A, o3.x) + o3.B
                np.testing.assert_allclose(dofs.f(), np.concatenate((f1, f2, f3)), \
                                           rtol=1e-13, atol=1e-13)
                true_jac = np.zeros((nvals1 + nvals2 + nvals3, nparams1 + nparams2 + nparams3))
                true_jac[0:nvals1, 0:nparams1] = o1.A
                true_jac[nvals1:nvals1 + nvals2, nparams1:nparams1 + nparams2] = o2.A
                true_jac[nvals1 + nvals2:nvals1 + nvals2 + nvals3, \
                         nparams1 + nparams2:nparams1 + nparams2 + nparams3] = o3.A
                np.testing.assert_allclose(dofs.jac(), true_jac, rtol=1e-13, atol=1e-13)
                np.testing.assert_allclose(dofs.fd_jac(centered=True), \
                                           true_jac, rtol=1e-7, atol=1e-7)
        
    def test_mixed_vector_valued(self):
        """
        For a mixture of functions that return a scalar vs return a
        vector, make sure DOFs.f(), DOFs.jac(), and DOFs.fd_jac()
        behave correctly.
        """
        for nparams1 in range(1, 5):
            for nvals1 in range(1, 5):
                nparams2 = np.random.randint(1, 6)
                nparams3 = np.random.randint(1, 6)
                nvals2 = np.random.randint(1, 6)
                nvals3 = np.random.randint(1, 6)
                o1 = Affine(nparams=nparams1, nvals=nvals1)
                o2 = Affine(nparams=nparams2, nvals=nvals2)
                o3 = Affine(nparams=nparams3, nvals=nvals3)
                a1 = Adder(n=2)
                a2 = Adder(n=3)
                dofs = DOFs.from_functions([o1, o2, a1, o3, a2])
                dofs.x = (np.random.rand(nparams1 + nparams2 + nparams3 + 5) - 0.5) * 4
                f1 = np.matmul(o1.A, o1.x) + o1.B
                f2 = np.matmul(o2.A, o2.x) + o2.B
                f3 = np.array([a1.f])
                f4 = np.matmul(o3.A, o3.x) + o3.B
                f5 = np.array([a2.f])
                np.testing.assert_allclose(dofs.f(), np.concatenate((f1, f2, f3, f4, f5)), \
                                           rtol=1e-13, atol=1e-13)
                true_jac = np.zeros((nvals1 + nvals2 + nvals3 + 2, nparams1 + nparams2 + nparams3 + 5))
                true_jac[0:nvals1, 0:nparams1] = o1.A
                true_jac[nvals1:nvals1 + nvals2, nparams1:nparams1 + nparams2] = o2.A
                true_jac[nvals1 + nvals2:nvals1 + nvals2 + 1, \
                         nparams1 + nparams2:nparams1 + nparams2 + 2] = np.ones(2)
                true_jac[nvals1 + nvals2 + 1:nvals1 + nvals2 + 1 + nvals3, \
                         nparams1 + nparams2 + 2:nparams1 + nparams2 + 2 + nparams3] = o3.A
                true_jac[nvals1 + nvals2 + 1 + nvals3:nvals1 + nvals2 + nvals3 + 2, \
                         nparams1 + nparams2 + nparams3 + 2:nparams1 + nparams2 + nparams3 + 5] = np.ones(3)
                np.testing.assert_allclose(dofs.jac(), true_jac, rtol=1e-13, atol=1e-13)
                np.testing.assert_allclose(dofs.fd_jac(centered=True), \
                                           true_jac, rtol=1e-7, atol=1e-7)
        
    def test_Jacobian(self):
        for n in range(1, 20):
            v1 = np.random.rand() * 4 - 2
            v2 = np.random.rand() * 4 - 2
            o = TestObject2(v1, v2)
            o.adder.set_dofs(np.random.rand(2) * 4 - 2)
            o.t.set_dofs([np.random.rand() * 4 - 2])
            o.t.adder1.set_dofs(np.random.rand(3) * 4 - 2)
            o.t.adder2.set_dofs(np.random.rand(2) * 4 - 2)
            r = Rosenbrock(b=3.0)
            r.set_dofs(np.random.rand(2) * 3 - 1.5)
            a = Affine(nparams=3, nvals=3)

            # Randomly fix some of the degrees of freedom
            o.dof_fixed = np.random.rand(2) > 0.5
            o.adder.dof_fixed = np.random.rand(2) > 0.5
            o.t.adder1.dof_fixed = np.random.rand(3) > 0.5
            o.t.adder2.dof_fixed = np.random.rand(2) > 0.5
            r.dof_fixed = np.random.rand(2) > 0.5
            a.dof_fixed = np.random.rand(3) > 0.5
            
            rtol = 1e-6
            atol = 1e-6

            for j in range(4):
                # Try different sets of the objects:
                if j==0:
                    dofs = DOFs.from_functions([o.J, r.terms, o.t.J])
                    nvals = 4
                    nvals_per_func = [1, 2, 1]
                elif j==1:
                    dofs = DOFs.from_functions([r.term2, r.terms])
                    nvals = 3
                    nvals_per_func = [1, 2]
                elif j==2:
                    dofs = DOFs.from_functions(
                        [r.term2, Target(o.t, 'f'), r.term1, Target(o, 'f')])
                    nvals = 4
                    nvals_per_func = [1, 1, 1, 1]
                elif j==3:
                    dofs = DOFs.from_functions([a, o])
                    nvals = 4
                    nvals_per_func = [3, 1]

                jac = dofs.jac()
                fd_jac = dofs.fd_jac()
                fd_jac_centered = dofs.fd_jac(centered=True)
                #print('j=', j, '  Diff in Jacobians:', jac - fd_jac)
                #print('jac: ', jac)
                #print('fd_jac: ', fd_jac)
                #print('fd_jac_centered: ', fd_jac_centered)
                #print('shapes: jac=', jac.shape, '  fd_jac=', fd_jac.shape, '  fd_jac_centered=', fd_jac_centered.shape)
                np.testing.assert_allclose(jac, fd_jac, rtol=rtol, atol=atol)
                np.testing.assert_allclose(fd_jac, fd_jac_centered, rtol=rtol, atol=atol)
                self.assertEqual(dofs.nvals, nvals)
                self.assertEqual(list(dofs.nvals_per_func), nvals_per_func)
                

if __name__ == "__main__":
    unittest.main()
