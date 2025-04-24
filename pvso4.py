import open3d as o3d
import numpy as np
#from sklearn.cluster import KMeans
from sklearn.cluster import Birch


# Load the point cloud
pcd = o3d.io.read_point_cloud("Carola_PointCloud.ply")
print("Original number of points:", len(pcd.points))

# Segment the largest plane
plane_model, inliers = pcd.segment_plane(distance_threshold=0.001,
                                         ransac_n=3,
                                         num_iterations=1000)

# Separate inliers and outliers
inlier_cloud = pcd.select_by_index(inliers)
outlier_cloud = pcd.select_by_index(inliers, invert=True)

# Convert outlier point cloud to numpy array
outlier_points = np.asarray(outlier_cloud.points)

# Odstráni riadky s NaN hodnotami
outlier_points = outlier_points[~np.isnan(outlier_points).any(axis=1)]

# Apply K-means to the outliers
k = 6  # počet klastrov
#kmeans = KMeans(n_clusters=k, random_state=0).fit(outlier_points)
#labels = kmeans.labels_

# Apply birch to the outliers
birch = Birch(n_clusters=k, threshold=0.5, branching_factor=100)
labels = birch.fit_predict(outlier_points)


# Vytvor nové point cloudy pre každý klaster
colors = [
    [1, 0, 0],  # red
    [0, 1, 0],  # green
    [0, 0, 1],  # blue
    [1, 1, 0],  # yellow
    [1, 0, 1],  # magenta
    [0, 1, 1],  # cyan
]

clustered_clouds = []
for i in range(k):
    indices = np.where(labels == i)[0]
    cluster_points = outlier_points[indices]
    cluster_pcd = o3d.geometry.PointCloud()
    cluster_pcd.points = o3d.utility.Vector3dVector(cluster_points)
    cluster_pcd.paint_uniform_color(colors[i % len(colors)])
    clustered_clouds.append(cluster_pcd)

# Zobraz rovinu + klastre
o3d.visualization.draw_geometries([inlier_cloud] + clustered_clouds,
                                  window_name="K-means Clustering",
                                  point_show_normal=False)
