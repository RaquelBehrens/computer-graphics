import numpy as np

def projection(points, object, normalized_window):
    x_center = normalized_window.wc[0]
    y_center = normalized_window.wc[1]
    z_center = normalized_window.wc[2]

    vrp = normalized_window.vrp
    translation_matrix = [[1, 0, 0, 0],
                          [0, 1, 0, 0],
                          [0, 0, 1, 0],
                          [-(float(vrp[0])), -(float(vrp[1])), -(float(vrp[2])), 1]]

    #print('translation_matrix: ', translation_matrix)
    
    vpn = normalized_window.define_vpn(translation_matrix)
    #print('vnp: ', vpn)
    tan_x = vpn[1] / vpn[2]
    tan_y = vpn[0] / vpn[2]
    vpn_angle_x = np.arctan(tan_x)
    vpn_angle_y = np.arctan(tan_y)

    #print('angles: ', vpn_angle_x, vpn_angle_y)

    rot_x = object.calculate_matrix_operation('x', vpn_angle_x)
    rot_y = object.calculate_matrix_operation('y', vpn_angle_y)

    transform_matrix = np.matmul(translation_matrix, rot_x)
    transform_matrix = np.matmul(transform_matrix, rot_y)

    #print('final matrix: ', transform_matrix)
    new_points = []
    for point in points:
        new_point = []
        points_matrix = [point[0], point[1], point[2], 1]

        result_points = np.matmul(points_matrix, transform_matrix)

        new_point.append(result_points[0])
        new_point.append(result_points[1])
        new_point.append(result_points[2])
        new_points.append(new_point)
    
    return new_points
