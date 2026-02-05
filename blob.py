import numpy as np


def blob_sphere(n_points, center, radius, noise=0.1):
    phi = np.random.uniform(0, 2 * np.pi, n_points)
    theta = np.random.uniform(0, np.pi, n_points)
    r = radius + np.random.normal(0, noise, n_points)

    x = center[0] + r * np.sin(theta) * np.cos(phi)
    y = center[1] + r * np.sin(theta) * np.sin(phi)
    z = center[2] + r * np.cos(theta)

    return np.column_stack([x, y, z])


def blob_cubic(n_points, center, shape, noise=0.1):
    x = np.random.uniform(-shape / 2, shape / 2, n_points) + center[0] + np.random.normal(0, noise, n_points)
    y = np.random.uniform(-shape / 2, shape / 2, n_points) + center[1] + np.random.normal(0, noise, n_points)
    z = np.random.uniform(-shape / 2, shape / 2, n_points) + center[2] + np.random.normal(0, noise, n_points)

    return np.column_stack([x, y, z])


def blob_spiral(n_points, center, radius_max, height, turns):
    t = np.linspace(0, turns * 2 * np.pi, n_points)
    r = np.linspace(0, radius_max, n_points)
    x = center[0] + r * np.cos(t)
    y = center[1] + r * np.sin(t)
    z = center[2] + np.linspace(0, height, n_points)

    return np.column_stack([x, y, z])


def blob_ring(n_points, center, radius_max, radius_min, axis='z'):
    phi = np.random.uniform(0, 2 * np.pi, n_points)
    theta = np.random.uniform(0, 2 * np.pi, n_points)
    r = radius_min

    if axis == 'z':
        x = center[0] + (radius_max + r * np.cos(theta)) * np.cos(phi)
        y = center[1] + (radius_max + r * np.cos(theta)) * np.sin(phi)
        z = center[2] + r * np.sin(theta)
    elif axis == 'x':
        x = center[0] + r * np.sin(theta)
        y = center[1] + (radius_max + r * np.cos(theta)) * np.cos(phi)
        z = center[2] + (radius_max + r * np.cos(theta)) * np.sin(phi)
    else:
        x = center[0] + (radius_max + r * np.cos(theta)) * np.cos(phi)
        y = center[1] + r * np.sin(theta)
        z = center[2] + (radius_max + r * np.cos(theta)) * np.sin(phi)

    return np.column_stack([x, y, z])


def blob_gaussiana(n_points, center, covariance):
    return np.random.multivariate_normal(center, covariance, n_points)


def blob_cylindrical(n_points, center, radio, height):
    theta = np.random.uniform(0, 2 * np.pi, n_points)
    r = np.random.uniform(0, radio, n_points)
    h = np.random.uniform(-height / 2, height / 2, n_points)

    x = center[0] + r * np.cos(theta)
    y = center[1] + r * np.sin(theta)
    z = center[2] + h

    return np.column_stack([x, y, z])


def blob_concentric(n_points, center, radios):
    points = []

    for n, c, radio in zip(n_points, center, radios):
        t = np.random.uniform(0, 2 * np.pi, n)
        x = c[0] + radio * np.cos(t)
        y = c[1] + radio * np.sin(t)
        z = c[2] + np.random.normal(0, 0.1, n)

        points.append(np.column_stack([x, y, z]))

    return np.vstack(points)
