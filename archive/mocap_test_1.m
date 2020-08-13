im = rot90(imread('20200705_171200.jpg'), -1);

[x, y] = meshgrid(1 : size(im, 2), 1 : size(im, 1));

X = x(all(im == 255, 3));
Y = y(all(im == 255, 3));

hold on
box  on
axis equal off

xticks([])
yticks([])

plot(X, Y, '.', 'MarkerSize', 1, 'Color', '#8EACBB')

plot([min(X), max(X)], [mean(Y), mean(Y)], 'Color', '#34515E')

plot([min(X), max(X(Y > mean(Y)))], [mean(Y(Y > mean(Y))), mean(Y(Y > mean(Y)))], 'Color', '#34515E')

plot([mean(X(Y > mean(Y))), mean(X(Y > mean(Y)))], [mean(Y), max(Y)], 'Color', '#34515E')

x_U = mean(X(Y > mean(Y(Y > mean(Y)))));
y_U = mean(Y(Y > mean(Y(Y > mean(Y)))));

x_K = mean(X(X > mean(X) & Y > mean(Y)));
y_K = mean(Y(X > mean(X) & Y > mean(Y)));

x_L = mean(X(Y < mean(Y)));
y_L = mean(Y(Y < mean(Y)));

plot([x_U, x_K, x_L], [y_U, y_K, y_L], '.-k', 'LineWidth', 1.5, 'MarkerSize', 42, 'MarkerEdgeColor', 'w')

text(x_U, y_U, 'U', 'HorizontalAlignment', 'center', 'FontName', 'Consolas')
text(x_K, y_K, 'K', 'HorizontalAlignment', 'center', 'FontName', 'Consolas')
text(x_L, y_L, 'L', 'HorizontalAlignment', 'center', 'FontName', 'Consolas')

print mocap_test_1_output -dpng -r600
