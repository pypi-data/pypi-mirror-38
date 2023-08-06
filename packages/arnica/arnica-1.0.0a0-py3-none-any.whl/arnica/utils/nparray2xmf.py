""" module to create an ensight compatible file
to visualize your  data"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

import h5py
import numpy as np


class NpArray2Xmf(object):
    """ main class for data output in XDMF format """

    def __init__(self, filename):
        """ class startup"""
        extension = os.path.splitext(filename)
        if extension[-1] == ".xmf":
            self.filename = extension[0] + ".h5"
        elif extension[-1] == ".h5":
            self.filename = filename
        else:
            raise RuntimeError("Only extensions .xmf or .h5 are allowed")

        self.geotype = None
        self.mesh = {}
        self.data = {}
        self.shape = None

    def create_grid(self, nparray_x, nparray_y, nparray_z):
        """ create the grid according to numpy arrays x, y ,z
        if arrays are 1D, switch to cloud point
        if arrays are 2D, switch to quad connectivity
        if arrays are 3D, switch to hexaedrons connectivity"""
        self.mesh["x"] = np.ravel(nparray_x)
        self.mesh["y"] = np.ravel(nparray_y)
        self.mesh["z"] = np.ravel(nparray_z)
        self.shape = list(nparray_x.shape)
        dim = len(self.shape)
        if dim == 1:
            self.geotype = "cloud"
        if dim == 2:
            self.geotype = "quads"
        if dim == 3:
            self.geotype = "hexas"

        if self.geotype is None:
            raise RuntimeError("Unexpected shape of nparray :"
                               + " ".join(self.shape))

    def add_field(self, nparray_field, variable_name):
        """ add a field, assuming same shape as nparray of coordiantes """
        self.data[variable_name] = nparray_field

    def _type(self, var):
        """ retrun the xmf type according to nparray"""
        var_shape = list(self.data[var].shape)

        dtype = self.data[var].dtype
        numbertype = None
        if dtype == "float64":
            numbertype = "Float"
        if dtype == "S4":
            numbertype = "Char"
        if numbertype is None:
            raise RuntimeError("Array of type " + dtype
                               + "(" + var + ")"
                               + "not recognized")

        attributetype = None
        if var_shape == self.shape:
            attributetype = "Scalar"
        if var_shape[:-1] == self.shape:
            if var_shape[-1] == 3:
                attributetype = "Vector"
        if attributetype is None:
            raise RuntimeError("Var " + var
                               + " of shape " + str(var_shape)
                               + " not consistent  with grid of shape "
                               + str(self.shape) +
                               "\n (neither scalar nor 3D vector...)")

        shape_str = " ".join(str(dim) for dim in self.data[var].shape)
        return (numbertype,
                attributetype,
                shape_str)

    def xmf_dump(self):
        """ create XDMF descriptor file """

        # give structure template
        xmf_ct = """<?xml version="1.0" ?>
<!DOCTYPE Xdmf SYSTEM "Xdmf.dtd" []>
<Xdmf Version="2.0">
<Domain Name="test_geom">
    <Grid Name="MyMesh" Type="Uniform">
        <Topology Name="ParticleTopo" TopologyType="[TOPOLOGY]" NumberOfElements="[SHAPE]"/>
        <Geometry GeometryType="X_Y_Z">
            <DataItem Format="HDF" NumberType="Float" Precision="8" Dimensions="[SHAPE]">
                [DATASET_X]
            </DataItem>
            <DataItem Format="HDF" NumberType="Float" Precision="8" Dimensions="[SHAPE]">
                [DATASET_Y]
            </DataItem>
            <DataItem Format="HDF" NumberType="Float" Precision="8" Dimensions="[SHAPE]">
                [DATASET_Z]
            </DataItem>
        </Geometry>
        [ATTRIBUTES]
    </Grid>
  </Domain>
</Xdmf>"""

        # Prepare attribute paragraph
        attributes_ct = ""
        for var in self.data:
            (numbertype,
             attributetype,
             shape_str) = self._type(var)

            attr = """<Attribute Name="[NAME]" AttributeType="[ATTRIBUTETYPE]" Center="Node">
            <DataItem Dimensions="[SHAPE]" NumberType="[NUMBERTYPE]" Precision="8" Format="HDF">
                [DATASET]
            </DataItem>
        </Attribute>
        """
            attr = attr.replace("[NAME]", var)
            attr = attr.replace("[DATASET]",
                                self.filename + ":/variables/" + var)
            attr = attr.replace("[NUMBERTYPE]", numbertype)
            attr = attr.replace("[ATTRIBUTETYPE]", attributetype)
            attr = attr.replace("[SHAPE]", shape_str)

            attributes_ct += attr

        xmf_ct = xmf_ct.replace("[ATTRIBUTES]", attributes_ct)

        # replace values
        if self.geotype == "cloud":
            xmf_ct = xmf_ct.replace("[TOPOLOGY]", "PolyVertex")
        if self.geotype == "quads":
            xmf_ct = xmf_ct.replace("[TOPOLOGY]", "2DSMesh")
        if self.geotype == "hexas":
            xmf_ct = xmf_ct.replace("[TOPOLOGY]", "3DSMesh")

        shape_str = " ".join(str(dim) for dim in self.shape)

        xmf_ct = xmf_ct.replace("[DATASET_X]", self.filename + ":/mesh/x")
        xmf_ct = xmf_ct.replace("[DATASET_Y]", self.filename + ":/mesh/y")
        xmf_ct = xmf_ct.replace("[DATASET_Z]", self.filename + ":/mesh/z")
        xmf_ct = xmf_ct.replace("[SHAPE]", shape_str)

        xmf_file = self.filename.replace(".h5", ".xmf")
        with open(xmf_file, "w") as fout:
            fout.write(xmf_ct)

    def dump(self):
        """ dump the final file """
        fout = h5py.File(self.filename, "w")

        mesh_gp = fout.create_group("mesh")
        for coord in ["x", "y", "z"]:
            mesh_gp.create_dataset(coord, data=self.mesh[coord])

        var_gp = fout.create_group("variables")
        for var in self.data:
            var_gp.create_dataset(var, data=self.data[var])
        fout.close()
        self.xmf_dump()


if __name__ == '__main__':

    DIM_X = 41
    DIM_Y = 21
    DIM_Z = 11

    SIZE_X = 4.
    SIZE_Y = 2.
    SIZE_Z = 1.

    # 1D
    TEST_X = np.linspace(0, SIZE_X, DIM_X)
    TEST_Y = np.linspace(0, SIZE_Y, DIM_X)
    TEST_Z = np.linspace(0, SIZE_Z, DIM_X)
    TEST_U = (np.sin(TEST_X / SIZE_X * 1 * np.pi)
              * np.sin(TEST_Y / SIZE_Y * 1 * np.pi)
              * np.sin(TEST_Z / SIZE_Z * 1 * np.pi))

    TEST_F = NpArray2Xmf("./test1D.h5")
    TEST_F.create_grid(TEST_X, TEST_Y, TEST_Z)
    TEST_F.add_field(TEST_U, "foobar")

    TEST_V = np.stack((TEST_U,
                       TEST_U,
                       TEST_U),
                      axis=1)
    TEST_F.add_field(TEST_V, "foobar_vect")

    TEST_F.dump()

    # 2D
    TEST_X = np.tile(np.linspace(0., SIZE_X, DIM_X), (DIM_Y, 1))
    TEST_Y = np.tile(np.linspace(0., SIZE_Y, DIM_Y), (DIM_X, 1)).transpose()
    TEST_Z = np.ones((DIM_Y, DIM_X))
    TEST_U = (np.sin(TEST_X / SIZE_X * 1 * np.pi)
              * np.sin(TEST_Y / SIZE_Y * 1 * np.pi)
              * np.sin(TEST_Z * 0.5 * np.pi))

    TEST_F = NpArray2Xmf("./test2D.h5")
    TEST_F.create_grid(TEST_X, TEST_Y, TEST_Z)
    TEST_F.add_field(TEST_U, "foobar")
    TEST_F.dump()

    TEST_X = TEST_X[:, :, None].repeat(DIM_Z, 2)
    TEST_Y = TEST_Y[:, :, None].repeat(DIM_Z, 2)
    TEST_Z = np.tile(np.linspace(0., SIZE_Z, DIM_Z), (DIM_X, 1)).transpose()
    TEST_Z = TEST_Z[:, :, None].repeat(DIM_Y, 2).transpose((2, 1, 0))
    TEST_U = (np.sin(TEST_X / SIZE_X * 1 * np.pi)
              * np.sin(TEST_Y / SIZE_Y * 1 * np.pi)
              * np.sin(TEST_Z / SIZE_Z * 1 * np.pi))

    TEST_F = NpArray2Xmf("./test3D.h5")
    TEST_F.create_grid(TEST_X, TEST_Y, TEST_Z)
    TEST_F.add_field(TEST_U, "foobar")
    TEST_F.dump()
