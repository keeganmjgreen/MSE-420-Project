% Uphill ('incline') - Lower Leg ('L')

function pp = incline_theta_L()

addpath code

Orientation.Y = readmatrix('data\incline_theta_L.xlsx', 'Range', 'C:C');

Y = smooth(Orientation.Y - 82.8980 + 90);

[pks, locs] = findpeaks(-Y);

pks_locs = table2array(sortrows(array2table(topkrows([pks, locs], 39, 1)), 2));

pks  = -pks_locs(:, 1);
locs = +pks_locs(:, 2);

my_new_figure()

xData = [];
yData = [];

for i = 1 : length(locs) - 1

    x{i} = (0 : (locs(i + 1) - locs(i)))' / (locs(i + 1) - locs(i));

    y{i} = Y(locs(i) : locs(i + 1));

    plot(x{i}, y{i}, '-', 'Color', '#CFD8DC', 'HandleVisibility', 'off')

    xData = [xData; x{i}];
    yData = [yData; y{i}];

end

pp = csaps([xData; xData + 1], [yData; yData], 1 - 1e-5);

fplot(@(xq) ppval(pp, xq + 1), [0, 0.5], 'k', 'LineWidth', 1.5)
fplot(@(xq) ppval(pp, xq + 0), [0.5, 1], 'k', 'LineWidth', 1.5)

my_legend(' Cubic Smoothing Spline ')

my_ticks([0, 90, 180])

my_xlabel('Arbitrary Fraction of Gait Cycle')
my_ylabel('Gyroscope Pitch = $ \theta $ Below $ xy \, $-Plane (deg.)')

my_title('\textbf{Uphill --- Lower Leg}')

print plots\incline_theta_L -dsvg

clear i my_axes
