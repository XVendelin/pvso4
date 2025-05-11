import open3d as o3d
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import Birch


# Load the point cloud
pcd = o3d.io.read_point_cloud("output2.pcd")
print("Original number of points:", len(pcd.points))

# Segment the largest plane
plane_model, inliers = pcd.segment_plane(distance_threshold=0.2,
                                         ransac_n=3,
                                         num_iterations=8000)


# Separate inliers and outliers
outlier_cloud = pcd.select_by_index(inliers)

outlier_cloud, ind = outlier_cloud.remove_statistical_outlier(nb_neighbors=50, std_ratio=1)

# Convert outlier point cloud to numpy array
outlier_points = np.asarray(outlier_cloud.points)

print("Number of points after processing:", len(outlier_points))

# Odstráni riadky s NaN hodnotami
outlier_points = outlier_points[~np.isnan(outlier_points).any(axis=1)]

# Apply K-means to the outliers
k = 2  # počet klastrov
kmeans = KMeans(n_clusters=k, random_state=0).fit(outlier_points)
labels = kmeans.labels_

# Apply birch to the outliers
birch = Birch(n_clusters=k, threshold=0.1, branching_factor=500)
labels1 = birch.fit_predict(outlier_points)


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

clustered_clouds1 = []
for i in range(k):
    indices = np.where(labels1 == i)[0]
    cluster_points = outlier_points[indices]
    cluster_pcd = o3d.geometry.PointCloud()
    cluster_pcd.points = o3d.utility.Vector3dVector(cluster_points)
    cluster_pcd.paint_uniform_color(colors[i % len(colors)])
    clustered_clouds1.append(cluster_pcd)

# Zobraz rovinu + klastre
o3d.visualization.draw_geometries([outlier_cloud],
                                  window_name="Ransack",
                                  point_show_normal=False)
o3d.visualization.draw_geometries(clustered_clouds,
                                  window_name="K-means Clustering",
                                  point_show_normal=False)
o3d.visualization.draw_geometries(clustered_clouds1,
                                  window_name="Birch Clustering",
                                  point_show_normal=False)
