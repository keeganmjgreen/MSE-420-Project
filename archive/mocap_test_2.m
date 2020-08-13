IM = imread('20200705_171200_1440p.jpg');

BW = bwpropfilt(all(200 <= IM, 3), 'Area', [numel(IM) / 1e4, Inf]);

centroids = cell2mat({regionprops(BW, 'Centroid').Centroid}');

x =               centroids(:, 1);
y = size(BW, 1) - centroids(:, 2);

centroids = table2array(sortrows(table(x, y), 2))

L = centroids(1, :);
K = centroids(2, :);
U = centroids(3, :);

d_LK = sqrt(sum((K - L) .^2));
d_KU = sqrt(sum((U - K) .^2));
d_LU = sqrt(sum((U - L) .^2));

theta_K = acosd((d_LK ^ 2 + d_KU ^ 2 - d_LU ^ 2) / (2 * d_LK * d_KU))
