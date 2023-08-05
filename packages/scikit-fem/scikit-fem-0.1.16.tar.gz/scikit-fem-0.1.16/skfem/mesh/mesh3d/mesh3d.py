import numpy as np

from ..submesh import Submesh
from ..mesh import Mesh

from typing import Callable, Optional

from numpy import ndarray

class Mesh3D(Mesh):
    """Three dimensional meshes, common methods.

    See the following implementations:

    - :class:`~skfem.mesh.MeshTet`, tetrahedral mesh
    - :class:`~skfem.mesh.MeshHex`, hexahedral mesh

    """

    def nodes_satisfying(self, test: Callable[[float, float, float], bool]) -> ndarray:
        """Return nodes that satisfy some condition.

        Parameters
        ----------
        test
            Evaluates to 1 or True for nodes belonging to the output set.

        """
        return np.nonzero(test(self.p[0, :], self.p[1, :], self.p[2, :]))[0]

    def facets_satisfying(self, test: Callable[[float, float, float], bool]) -> ndarray:
        """Return facets whose midpoints satisfy some condition.
        
        Parameters
        ----------
        test
            Evaluates to 1 or True for facet midpoints of the facets belonging
            to the output set.

        """
        mx = np.sum(self.p[0, self.facets], axis=0)/self.facets.shape[0]
        my = np.sum(self.p[1, self.facets], axis=0)/self.facets.shape[0]
        mz = np.sum(self.p[2, self.facets], axis=0)/self.facets.shape[0]
        return np.nonzero(test(mx, my, mz))[0]

    def edges_satisfying(self, test: Callable[[float, float, float], bool]) -> ndarray:
        """Return edges whose midpoints satisfy some condition.

        Parameters
        ----------
        test
            Evaluates to 1 or True for edge midpoints of the edges belonging to
            the output set.

        """
        mx = 0.5*(self.p[0, self.edges[0, :]] + self.p[0, self.edges[1, :]])
        my = 0.5*(self.p[1, self.edges[0, :]] + self.p[1, self.edges[1, :]])
        mz = 0.5*(self.p[2, self.edges[0, :]] + self.p[2, self.edges[1, :]])
        return np.nonzero(test(mx, my, mz))[0]

    def elements_satisfying(self, test: Callable[[float, float, float], bool]) -> ndarray:
        """Return elements whose midpoints satisfy some condition.

        Parameters
        ----------
        test
            Evaluates to 1 or True for element midpoints of the elements
            belonging to the output set.

        """
        mx = np.sum(self.p[0, self.t], axis=0)/self.t.shape[0]
        my = np.sum(self.p[1, self.t], axis=0)/self.t.shape[0]
        mz = np.sum(self.p[2, self.t], axis=0)/self.t.shape[0]
        return np.nonzero(test(mx, my, mz))[0]

    def submesh(self,
                test: Optional[Callable[[float, float, float], bool]] = None,
                boundaries_only: Optional[bool] = True) -> Submesh:
        """Return Submesh object where all topological entities satisfy some
        condition.
        
        Parameters
        ----------
        test
            Evaluates to 1 or True for the midpoints of the topological
            entities belonging to the output Submesh. If None is given,
            returns a Submesh consisting of all boundary entities.

        """
        if test is None:
            p = self.boundary_nodes()
            facets = self.boundary_facets()
            edges = self.boundary_edges()
            return Submesh(p=p, facets=facets, edges=edges, t=None)
        else:
            p = self.nodes_satisfying(test)
            if len(p) == 0:
                p = None
            facets = self.facets_satisfying(test)
            if len(facets) == 0:
                facets = None
            edges = self.edges_satisfying(test)
            if len(edges) == 0:
                edges = None
            t = None
            if boundaries_only:
                p = np.setdiff1d(p, self.interior_nodes())
                facets = np.setdiff1d(facets, self.interior_facets())
                edges = np.setdiff1d(edges, self.interior_edges())
            else:
                t = self.elements_satisfying(test)
                if len(t) == 0:
                    t = None
            return Submesh(p=p, facets=facets, edges=edges, t=t)

    def boundary_edges(self) -> ndarray:
        """Return an array of boundary edge indices."""
        bnodes = self.boundary_nodes()[:, None]
        return np.nonzero(np.sum(self.edges[0, :] == bnodes, axis=0) *
                          np.sum(self.edges[1, :] == bnodes, axis=0))[0]

    def interior_edges(self) -> ndarray:
        """Return an array of interior edge indices."""
        return np.setdiff1d(np.arange(self.edges.shape[1], dtype=np.int), self.boundary_edges())

    def param(self) -> float:
        """Return (maximum) mesh parameter."""
        return np.max(np.sqrt(np.sum((self.p[:, self.edges[0, :]] -
                                      self.p[:, self.edges[1, :]])**2, axis=0)))

    @staticmethod
    def strip_extra_coordinates(p: ndarray) -> ndarray:
        return p
