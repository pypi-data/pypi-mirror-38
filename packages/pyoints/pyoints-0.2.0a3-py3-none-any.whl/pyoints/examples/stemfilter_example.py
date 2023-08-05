# BEGIN OF LICENSE NOTE
# This file is part of Pyoints.
# Copyright (c) 2018, Sebastian Lamprecht, Trier University,
# lamprecht@uni-trier.de
#
# Pyoints is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyoints is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pyoints. If not, see <https://www.gnu.org/licenses/>.
# END OF LICENSE NOTE
"""In this example, we try to detect stems in a forest using a point cloud
of terrestrial laser scans. A couple of .las-files will be generated, which
should be inspected with software like CloudCompare.


Let's begin with loading the required modules.

>>> import os
>>> import numpy as np

>>> from pyoints.interpolate import KnnInterpolator
>>> from pyoints import (
...     storage,
...     grid,
...     transformation,
...     filters,
...     clustering,
...     classification,
...     vector,
...     GeoRecords,
...     interpolate,
... )


First, we define an input and an output path.

>>> inpath = os.path.join(
...                 os.path.dirname(os.path.abspath(__file__)), 'data')
>>> outpath = os.path.join(
...                 os.path.dirname(os.path.abspath(__file__)), 'output')


Thereafter, we load an input LAS point cloud.

>>> infile = os.path.join(inpath, 'forest.las')
>>> lasReader = storage.LasReader(infile)
>>> las = lasReader.load()
>>> print(len(las))
482981


The basic idea of the algorithm is to first derive a digital elevation model to calculate
the height above ground. We simply rasterize the point cloud by deriving the
lowest z-coordinate of each cell.

>>> T = transformation.matrix(t=las.t.origin[:2], s=[0.8, 0.8])
>>> def aggregate_function(ids):
...     return las.coords[ids, 2].min() if len(ids) > 0 else np.nan
>>> dtype = [('z', float)]
>>> dem_grid = grid.voxelize(las, T, agg_func=aggregate_function, dtype=dtype)
>>> print(dem_grid.shape)
(9, 9)


We save the DEM as a .tif-image.

>>> outfile = os.path.join(outpath, 'stemfilter_dem.tif')
>>> storage.writeRaster(dem_grid, outfile, field='z')


We create a surface interpolator.

>>> dem = KnnInterpolator(dem_grid.records().coords, dem_grid.records().z)


For the stem detection, we will focus on points with height above ground 
greater 0.5 m.

>>> height = las.coords[:, 2] - dem(las.coords)
>>> s_ids = np.where(height > 0.5)[0]
>>> print(len(s_ids))
251409


We filter the point cloud using a small filter radius. Only a subset of points
with a point distance of at least 10 cm is kept.

>>> f_ids = list(filters.ball(las.indexKD(), 0.1, order=s_ids))
>>> las = las[f_ids]
>>> print(len(las))
11181

>>> outfile = os.path.join(outpath, 'stemfilter_ball_10.las')
>>> storage.writeLas(las, outfile)


We only keep points with a lot of neighbors to reduce noise.

>>> count = las.indexKD().ball_count(0.3)
>>> mask = count > 10
>>> las = las[mask]
>>> print(len(las))
8154

>>> outfile = os.path.join(outpath, 'stemfilter_denoised.las')
>>> storage.writeLas(las, outfile)


Now, we will filter with a radius of 1 m. This results in a point cloud
with point distances of at least 1 m. Here, points associated with stems are
arranged in straight lines.

>>> f_ids = list(filters.ball(las.indexKD(), 1.0))
>>> las = las[f_ids]
>>> print(len(las))
189

>>> outfile = os.path.join(outpath, 'stemfilter_ball_100.las')
>>> storage.writeLas(las, outfile)

For dense point clouds, the filtering technique results in point distances
between 1 m and 2 m. Thus, we can assume that linear arranged points should
have 2 to 3 neighboring points within a radius of 1.5 m.

>>> count = las.indexKD().ball_count(1.5)
>>> mask = np.all((count >= 2, count <= 3), axis=0)
>>> las = las[mask]
>>> print(len(las))
84

>>> outfile = os.path.join(outpath, 'stemfilter_linear.las')
>>> storage.writeLas(las, outfile)


Now, the stems are clearly visible in the point cloud. Thus, we can detect the
stems by clustering the points.

>>> cluster_indices = clustering.dbscan(las.indexKD(), 2, epsilon=1.5)

>>> print(len(cluster_indices))
84
>>> print(np.unique(cluster_indices))
[-1  0  1  2  3  4  5]


In the next step, we remove small clusters and unassigned points.

>>> cluster_dict = classification.classes_to_dict(cluster_indices, min_size=5)
>>> cluster_indices = classification.dict_to_classes(cluster_dict, len(las))

>>> print(sorted(cluster_dict.keys()))
[0, 1, 3, 5]


We add an additional field to the point cloud to store the tree number.

>>> las = las.add_fields([('tree_id', int)], data=[cluster_indices])

>>> outfile = os.path.join(outpath, 'stemfilter_stems.las')
>>> storage.writeLas(las, outfile)


Now, we can fit a vector to each stem. You should take a close look at the
characteristics of the `Vector` object.

>>> stems = {}
>>> for tree_id in cluster_dict:
...     coords = las[cluster_dict[tree_id]].coords
...     stem = vector.Vector.from_coords(coords)
...     stems[tree_id] = stem


Finally, we determinate the tree root coordinates using the previously derived
digital elevation model.

>>> roots = []
>>> for tree_id in stems:
...     stem = stems[tree_id]
...     coord = vector.vector_surface_intersection(stem, dem)
...     roots.append((tree_id, coord))

>>> dtype = [('tree_id', int), ('coords', float, 3)]
>>> roots = np.array(roots, dtype=dtype).view(np.recarray)
>>> roots = GeoRecords(las.proj, roots)

>>> outfile = os.path.join(outpath, 'stemfilter_roots.las')
>>> storage.writeLas(roots, outfile)

"""
