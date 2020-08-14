function incline()

    addpath code

    pp_L = incline_theta_L();
    pp_U = incline_theta_U();

    x_L = 0.2909;  % fminbnd(@(x) -ppval(pp_L, x), 0, 1)
    x_U = 0.3422;  % fminbnd(@(x) +ppval(pp_U, x), 0, 1)

    my_new_figure

        my_fplot(@f_L, '#0069C0')
        my_fplot(@f_U, '#BA000D')

        my_legend({' Lower Leg ', ' Upper Leg '})

        my_ticks([0, 90, 180])

        my_xlabel('Matched Fraction of Gait Cycle')
        my_ylabel('Gyroscope Pitch = $ \theta $ Below $ xy \, $-Plane (deg.)')

        my_title('\textbf{Uphill}')

        my_print incline_theta_LU

    my_new_figure

        my_fplot(@f_K, '#087F23')

        my_ticks([0, 90, 180])

        my_xlabel('Matched Fraction of Gait Cycle')
        my_ylabel('Knee Angle, $ \theta_K $ (deg.)')

        my_title('\textbf{Uphill}')

        my_print incline_theta_K

    my_new_figure

        my_fplot(@(x) deg2rad(d(@f_K, x)) / 1.150263, '#087F23')

        my_ticks([-10, 0, +10])

        my_xlabel('Matched Fraction of Gait Cycle')
        my_ylabel('Knee Anglular Velocity, $ \omega_K $ (rad/s)')

        my_title('\textbf{Uphill}')

        my_print incline_omega_K

    my_new_figure

        my_fplot(@(x) deg2rad(d(@(x) d(@f_K, x), x)) / 1.150263 ^ 2, '#087F23')

        my_ticks([-100, 0, +100])

        my_xlabel('Matched Fraction of Gait Cycle')
        my_ylabel('Knee Angular Acceleration, $ \alpha_K $ (rad/s/s)')

        my_title('\textbf{Uphill}')

        my_print incline_alpha_K

    H = 1.845056;
    m = 1;

    L_T = (0.720 - 0.530) * H;
    L_U = (0.530 - 0.285) * H;

    D = @(x) sqrt(L_T ^ 2 + L_U ^ 2 - 2 * L_T * L_U * cosd(f_U(x) + 90));

    I = @(x) m * D(x) ^ 2;

    my_new_figure

        funx = @(t) arrayfun(@(t) abs(deg2rad(d(@(t) d(@f_K, t), t)) / 1.150263 ^ 2) * I(t), t);
        funy = @(t) arrayfun(@(t) abs(deg2rad(d(@f_K, t)) / 1.150263), t);

      % fplot(funx, funy, [0, 1], 'k', 'LineWidth', 1.5, 'MeshDensity', 3)

      % my_plot([0.000, 18.410, 19.180, 38.910, 40.290, 40.460, 40.460], ...
      %         [3.955,  3.955,  3.947,  3.162,  3.001,  2.725,  0.000], 'k')

      % CORRECTED:

        my_plot([0.000, 16.010, 16.680, 33.830, 35.030, 35.170, 35.170], ...
                [3.955,  3.955,  3.947,  3.162,  3.001,  2.725,  0.000], 'k')

        xticks([0, 50])
        yticks([0,  5])

        yticklabels(pad(string(yticks), 4, 'left'))

        xlim(xticks)
        ylim(yticks)

        my_xlabel('Drive Torque, $ |T| $ (N-m), per 1 kg Backpack Load')
        my_ylabel('Drive Speed, $ |\omega| $ (rad/s)')

        my_title('\textbf{Uphill}')

        my_print incline_omega_vs_T

    function y_L = f_L(x)

            if x < 0;        y_L = f_L(x + 1);

        elseif x < 0.5;      y_L = ppval( pp_L, x + x_L + 1 );
        elseif x < 1 - x_L;  y_L = ppval( pp_L, x + x_L     );
        elseif x < 1;        y_L = ppval( pp_L, x + x_L - 1 );

        else;                y_L = f_L(x - 1);

        end

    end

    function y_U = f_U(x)

            if x < 0;        y_U = f_U(x + 1);

        elseif x < 1 - x_U;  y_U = ppval( pp_U, x + x_U     );
        elseif x < 0.5;      y_U = ppval( pp_U, x + x_U     );
        elseif x < 1;        y_U = ppval( pp_U, x + x_U - 1 );

        else;                y_U = f_U(x - 1);

        end

    end

    function y_K = f_K(x)

        y_K = f_L(x) + f_U(x) - 0.8151;

    end

end
