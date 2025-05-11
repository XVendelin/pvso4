import open3d as o3d
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from collections import Counter


def filter_small_clusters(labels, min_points=300):
    # Count how many points belong to each cluster
    cluster_counts = Counter(labels)

    # Remove noise (-1) from the count
    if -1 in cluster_counts:
        del cluster_counts[-1]  # Noise points should not be counted as clusters

    # Identify clusters with enough points (greater than or equal to min_points)
    valid_cluster_labels = [label for label, count in cluster_counts.items() if count >= min_points]

    # Reassign labels of small clusters to noise (-1)
    updated_labels = np.array([
        label if label in valid_cluster_labels else -1  # Keep valid clusters, assign -1 to small ones
        for label in labels
    ])

    return updated_labels



# Load the point cloud
pcd = o3d.io.read_point_cloud("notredame plus spire.ply")
print("Original number of points:", len(pcd.points))

pcd_down = pcd.voxel_down_sample(voxel_size=0.13)  # Adjust voxel_size as needed
print("Downsampled number of points:", len(pcd_down.points))

# Assign downsampled cloud to outlier_cloud
outlier_cloud = pcd_down

# Convert outlier point cloud to numpy array
outlier_points = np.asarray(outlier_cloud.points)
print("Number of points after processing:", len(outlier_points))

# Odstráni riadky s NaN hodnotami
outlier_points = outlier_points[~np.isnan(outlier_points).any(axis=1)]

# Apply K-means to the outliers
k = 3  # počet klastrov
kmeans = KMeans(n_clusters=k, random_state=0).fit(outlier_points)
labels = kmeans.labels_
print("kmeans done\n")
# Apply DBSCAN to the outliers
db = DBSCAN(eps=0.8, min_samples=235)  # Adjust eps/min_samples as needed
labels1 = db.fit_predict(outlier_points)
labels1 = filter_small_clusters(labels1, min_points=6000)

print("DBSCAN done\n")

# Analyze DBSCAN results
n_clusters = len(set(labels1)) - (1 if -1 in labels1 else 0)
n_noise = list(labels1).count(-1)
total_points = len(labels1)
noise_ratio = 100.0 * n_noise / total_points

print(f"DBSCAN found {n_clusters} clusters")
print(f"Noise points: {n_noise} ({noise_ratio:.2f}% of total)")



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

# Add clusters (labels >= 0)
for i in range(n_clusters):
    indices = np.where(labels1 == i)[0]
    cluster_points = outlier_points[indices]
    if len(cluster_points) == 0:
        print(colors[i % len(colors)]);
        continue
    cluster_pcd = o3d.geometry.PointCloud()
    cluster_pcd.points = o3d.utility.Vector3dVector(cluster_points)
    cluster_pcd.paint_uniform_color(colors[i % len(colors)])
    clustered_clouds1.append(cluster_pcd)

# Add noise points (label == -1)
noise_indices = np.where(labels1 == -1)[0]
if len(noise_indices) > 0:
    noise_points = outlier_points[noise_indices]
    noise_pcd = o3d.geometry.PointCloud()
    noise_pcd.points = o3d.utility.Vector3dVector(noise_points)
    noise_pcd.paint_uniform_color([0.5, 0.5, 0.5])  # gray
    clustered_clouds1.append(noise_pcd)


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
