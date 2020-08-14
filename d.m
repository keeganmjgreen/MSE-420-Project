function dy = d(f, x)

    eps = 1e-1;

    dy = (f(x + eps) - f(x)) / eps;
  % dy = (-f(x + 2 * eps) + 4 * f(x + eps) - 3 * f(x)) / (2 * eps);

end
